"""Report how much of the public API has a runnable docstring example.

    python scripts/docstring_coverage.py            # summary + worst modules
    python scripts/docstring_coverage.py --verbose  # list every missing method
    python scripts/docstring_coverage.py --json

"Runnable" means the docstring contains a ``>>>`` doctest block, which
``tests/test_docstrings.py`` executes on every run. A prose example in a
fenced block is useful documentation but it is not verified, so it does not
count here.

This is a measuring tool, not a gate. The gate is the ratchet in
``tests/test_docstrings.py``: the number of executable examples may not go
down. Raising it is the actual work.
"""

from __future__ import annotations

import argparse
import inspect
import json
import pkgutil
import sys
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def iter_modules() -> Iterator[str]:
    """Every importable module in the package."""
    import darkob

    for info in pkgutil.walk_packages(darkob.__path__, prefix="darkob."):
        yield info.name


def public_members(module: Any) -> Iterator[Tuple[str, Any]]:
    """Public callables defined by *module* itself."""
    for name, member in vars(module).items():
        if name.startswith("_"):
            continue
        if getattr(member, "__module__", None) != module.__name__:
            continue
        if inspect.isclass(member):
            yield name, member
            for attribute, value in vars(member).items():
                if attribute.startswith("_") and attribute != "__init__":
                    continue
                if callable(value) or isinstance(value, property):
                    try:
                        if isinstance(value, property):
                            value = value.fget
                        if inspect.isfunction(value):
                            yield f"{name}.{attribute}", value
                    except (AttributeError, TypeError):
                        continue
        elif callable(member):
            yield name, member


def has_doctest(obj: Any) -> bool:
    doc = getattr(obj, "__doc__", "") or ""
    return ">>>" in doc


def survey() -> Dict[str, Any]:
    import importlib

    per_module: Dict[str, Dict[str, int]] = {}
    missing: List[str] = []

    for module_name in iter_modules():
        try:
            module = importlib.import_module(module_name)
        except Exception:
            continue

        documented = total = 0
        for label, obj in public_members(module):
            total += 1
            if has_doctest(obj):
                documented += 1
            else:
                missing.append(f"{module_name}.{label}")
        if total:
            per_module[module_name] = {"documented": documented, "total": total}

    documented_total = sum(item["documented"] for item in per_module.values())
    total_total = sum(item["total"] for item in per_module.values())

    return {
        "documented": documented_total,
        "total": total_total,
        "percent": round(100.0 * documented_total / total_total, 1)
        if total_total
        else 0.0,
        "modules": per_module,
        "missing": sorted(missing),
    }


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument(
        "--top", type=int, default=15, help="How many modules to list."
    )
    args = parser.parse_args(argv)

    report = survey()

    if args.json:
        print(json.dumps(report, indent=2))
        return 0

    print(
        f"{report['documented']} of {report['total']} public members have a "
        f"runnable example ({report['percent']}%)."
    )

    ranked = sorted(
        report["modules"].items(),
        key=lambda item: (item[1]["total"] - item[1]["documented"]),
        reverse=True,
    )
    print(f"\nMost missing, worst first (top {args.top}):")
    for name, counts in ranked[: args.top]:
        gap = counts["total"] - counts["documented"]
        if gap:
            print(
                f"  {name:<58} {counts['documented']:>4}/{counts['total']:<4} "
                f"missing {gap}"
            )

    if args.verbose:
        print("\nMissing:")
        for item in report["missing"]:
            print(f"  {item}")
    else:
        print(
            f"\nRun with --verbose to list all {len(report['missing'])} "
            "undocumented members."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
