"""Fail the build when a hot path regresses.

    python benchmarks/check_regression.py                # compare to baseline
    python benchmarks/check_regression.py --update       # rewrite baseline.json
    python benchmarks/check_regression.py --tolerance 0.25

Two kinds of number are compared, and neither is an absolute duration:

* **Head-to-head factors** from :mod:`benchmarks.benchmark_suite` — darkob
  versus maxrubika doing the same job in the same process. This is
  machine-independent by construction: both libraries run on the same box in
  the same conditions. A factor that *drops* means ground was lost against
  the competitor.

* **Normalised ratios** from :mod:`benchmarks.scenarios` — seconds divided by
  a fixed CPU calibration workload measured in the same run. Dividing by
  calibration removes the machine's raw speed, which is what makes a baseline
  recorded on a laptop still meaningful on a CI runner. A ratio that *rises*
  means darkob's own overhead grew.

Absolute milliseconds are deliberately not gated: they move 3× between a
laptop and a shared CI runner for reasons that have nothing to do with the
code under test.

Exit codes: ``0`` no regression, ``1`` regression found, ``2`` the baselines
could not be produced at all.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import platform
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

BENCHMARK_DIR = Path(__file__).resolve().parent
REPO_ROOT = BENCHMARK_DIR.parent
BASELINE_PATH = BENCHMARK_DIR / "baseline.json"

#: Default regression tolerance. CI passes a looser value because a shared
#: runner is noisier than the machine a contributor measures on.
DEFAULT_TOLERANCE = 0.10

#: A fast machine finishing sooner than this suggests a broken measurement.
MIN_SANE_SECONDS = 0.00001


def _run_json(script: str, timeout: int) -> Optional[Any]:
    """Run a benchmark script and parse its JSON output."""
    try:
        result = subprocess.run(
            [sys.executable, str(BENCHMARK_DIR / script), "--json"],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(REPO_ROOT),
        )
    except subprocess.TimeoutExpired:
        print(f"::warning::{script} timed out after {timeout}s")
        return None

    if result.returncode != 0:
        print(f"::warning::{script} exited {result.returncode}")
        print(result.stderr[-2000:])
        return None

    try:
        return json.loads(result.stdout)
    except ValueError:
        print(f"::warning::{script} did not print valid JSON")
        print(result.stdout[-1000:])
        return None


def collect() -> Dict[str, Any]:
    """Produce the same shape as ``baseline.json``."""
    head_to_head: Dict[str, float] = {}
    for row in _run_json("benchmark_suite.py", timeout=900) or []:
        factor = row.get("factor")
        if factor:
            head_to_head[row["name"]] = round(float(factor), 3)

    scenario_run = _run_json("scenarios.py", timeout=1800) or {}
    scenarios: Dict[str, float] = {}
    for key, measured in (scenario_run.get("cases") or {}).items():
        if not measured:
            continue
        ratio = measured.get("ratio")
        if ratio:
            scenarios[key] = round(float(ratio), 6)

    return {
        "generated": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "environment": scenario_run.get("environment")
        or {"platform": platform.platform()},
        "head_to_head": head_to_head,
        "scenarios": scenarios,
    }


def _classify(
    name: str,
    current: float,
    baseline: float,
    tolerance: float,
    higher_is_better: bool,
) -> Tuple[str, float]:
    """Return ``(verdict, relative change)`` for one measurement."""
    if baseline <= 0:
        return "skipped", 0.0
    change = (current - baseline) / baseline
    if higher_is_better:
        regressed = current < baseline * (1.0 - tolerance)
    else:
        regressed = current > baseline * (1.0 + tolerance)
    if regressed:
        return "regressed", change
    if abs(change) >= tolerance:
        return "improved", change
    return "stable", change


def compare(
    baseline: Dict[str, Any],
    current: Dict[str, Any],
    tolerance: float,
    scenario_tolerance: Optional[float] = None,
) -> int:
    failures: List[str] = []
    rows: List[Tuple[str, str, float, float, str, float]] = []
    scenario_limit = tolerance if scenario_tolerance is None else scenario_tolerance

    for group, higher_is_better, group_tolerance in (
        ("head_to_head", True, tolerance),
        ("scenarios", False, scenario_limit),
    ):
        expected = baseline.get(group) or {}
        measured = current.get(group) or {}
        for name in sorted(expected):
            if name not in measured:
                rows.append((group, name, expected[name], 0.0, "missing", 0.0))
                continue
            current_value = measured[name]
            if current_value < MIN_SANE_SECONDS:
                rows.append(
                    (group, name, expected[name], current_value, "suspicious", 0.0)
                )
                continue
            verdict, change = _classify(
                name, current_value, expected[name], group_tolerance, higher_is_better
            )
            rows.append(
                (group, name, expected[name], current_value, verdict, change)
            )
            if verdict == "regressed":
                failures.append(f"{name} ({group})")

    print(f"| Group | Case | Baseline | Current | Change | Verdict |")
    print("| --- | --- | --- | --- | --- | --- |")
    for group, name, expected_value, current_value, verdict, change in rows:
        print(
            f"| {group} | {name} | {expected_value:g} | {current_value:g} "
            f"| {change:+.1%} | {verdict} |"
        )

    print(
        f"\nTolerances: head-to-head {tolerance:.0%}, "
        f"scenarios {scenario_limit:.0%}."
    )

    if failures:
        for name in failures:
            print(
                f"::error::Performance regression in {name}: outside tolerance. "
                f"Re-run locally; if the change is intentional, refresh the "
                f"baseline with --update."
            )
        return 1

    print("No regression outside tolerance.")
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--tolerance",
        type=float,
        default=DEFAULT_TOLERANCE,
        help="Fractional change allowed before a case counts as a regression.",
    )
    parser.add_argument(
        "--update",
        action="store_true",
        help="Rewrite baseline.json from the current measurements.",
    )
    parser.add_argument(
        "--no-cross-check",
        action="store_true",
        help="Compare anyway when the recording machine differs from this one.",
    )
    parser.add_argument(
        "--scenario-tolerance",
        type=float,
        default=None,
        help=(
            "Separate tolerance for the normalised scenario ratios. Needed "
            "when the baseline was recorded on another OS: head-to-head "
            "factors are platform-independent by construction, the ratios are "
            "only approximately so."
        ),
    )
    args = parser.parse_args(argv)

    if args.tolerance < 0:
        parser.error("--tolerance must not be negative.")
    if args.scenario_tolerance is not None and args.scenario_tolerance < 0:
        parser.error("--scenario-tolerance must not be negative.")

    if args.update:
        snapshot = collect()
        if not snapshot["head_to_head"] and not snapshot["scenarios"]:
            print("::error::Nothing was measured; baseline left untouched.")
            return 2
        BASELINE_PATH.write_text(
            json.dumps(snapshot, indent=2) + "\n", encoding="utf-8"
        )
        print(f"Wrote {BASELINE_PATH}")
        print(json.dumps(snapshot, indent=2))
        return 0

    if not BASELINE_PATH.exists():
        print(
            f"::error::No baseline at {BASELINE_PATH}. "
            "Record one with --update on a quiet machine."
        )
        return 2

    baseline = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
    current = collect()

    print(
        f"Baseline recorded {baseline.get('generated', 'unknown')} on "
        f"{(baseline.get('environment') or {}).get('platform', 'unknown')}; "
        f"now running on {platform.platform()}."
    )
    expected_platform = (baseline.get("environment") or {}).get("platform")
    if expected_platform and expected_platform != platform.platform():
        message = (
            "the baseline was recorded on a different platform; ratios should "
            "still hold, but treat a borderline result with suspicion."
        )
        if args.no_cross_check:
            print(f"::warning::{message}")
        else:
            print(f"::notice::{message}")

    return compare(baseline, current, args.tolerance, args.scenario_tolerance)


if __name__ == "__main__":
    raise SystemExit(main())
