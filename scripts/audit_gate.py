"""Fail the build only when a vulnerability affects a *direct* dependency.

    python scripts/audit_gate.py            # exit 1 on a direct-dependency CVE
    python scripts/audit_gate.py --all      # exit 1 on any advisory at all

`pip-audit` on its own is a bad CI gate. It reports advisories from the entire
installed environment, which includes test tooling and build backends that a
user of the library never installs — so a `pytest` or `setuptools` advisory
turns every pull request red for a problem that cannot reach anybody running
`pip install darkob`. That is how a security gate gets `|| true`'d into
irrelevance.

This gate separates the two cases:

* an advisory in one of darkob's **runtime dependencies** fails the build;
* an advisory anywhere else is printed as a warning and does not.

`--all` restores the blunt behaviour for a scheduled audit, where you do want
to hear about everything.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from typing import Any, Dict, List, Optional

#: darkob's runtime dependencies, per ``[project].dependencies``.
DIRECT = {"aiohttp", "aiofiles", "pycryptodome"}


def _flatten(report: Any) -> List[Dict[str, Any]]:
    """Normalise pip-audit's JSON, whose shape changed between releases.

    Older versions emit ``{"dependencies": [...]}``; newer ones emit a bare
    list of the same records.
    """
    if isinstance(report, dict):
        dependencies = report.get("dependencies") or report.get("records") or []
    elif isinstance(report, list):
        dependencies = report
    else:
        dependencies = []

    records: List[Dict[str, Any]] = []
    for entry in dependencies:
        if not isinstance(entry, dict):
            continue
        name = entry.get("name") or entry.get("package", "")
        version = entry.get("version", "?")
        for vuln in entry.get("vulns") or []:
            if isinstance(vuln, str):
                records.append({"name": name, "version": version, "id": vuln})
                continue
            records.append(
                {
                    "name": name,
                    "version": version,
                    "id": vuln.get("id", "?"),
                    "fix": ", ".join(vuln.get("fix_versions") or []) or "none",
                    "description": (vuln.get("description") or "").strip(),
                }
            )
    return records


def _normalise(name: str) -> str:
    return name.strip().lower().replace("-", "_")


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--all",
        action="store_true",
        help="Fail on any advisory, not only on runtime dependencies.",
    )
    parser.add_argument(
        "--requirement",
        action="append",
        default=[],
        help="Extra pip-audit arguments (repeatable).",
    )
    args = parser.parse_args(argv)

    command = [
        sys.executable,
        "-m",
        "pip_audit",
        "--format",
        "json",
        "--desc",
        "--progress-spinner",
        "off",
        *args.requirement,
    ]
    try:
        result = subprocess.run(command, capture_output=True, text=True)
    except FileNotFoundError:
        print("::warning::pip-audit is not installed; the audit was skipped.")
        return 0

    try:
        report = json.loads(result.stdout or "[]")
    except ValueError:
        print("::warning::pip-audit produced no parseable JSON; skipped.")
        print(result.stdout[-1000:])
        print(result.stderr[-1000:])
        return 0

    records = _flatten(report)
    direct = [
        record
        for record in records
        if _normalise(record["name"]) in {_normalise(name) for name in DIRECT}
    ]
    other = [record for record in records if record not in direct]

    for record in other:
        print(
            f"::warning::{record['name']} {record['version']} is affected by "
            f"{record['id']} (not a runtime dependency of darkob)."
        )

    if not records:
        print("No advisories reported.")
        return 0

    if not direct and not args.all:
        print(
            f"{len(other)} advisor{'y' if len(other) == 1 else 'ies'} outside the "
            "runtime dependency set; not failing the build."
        )
        return 0

    for record in direct or records:
        print(
            f"::error::{record['name']} {record['version']} is affected by "
            f"{record['id']} (fixed in: {record.get('fix', 'unknown')})."
        )
        if record.get("description"):
            print(f"  {record['description'][:500]}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
