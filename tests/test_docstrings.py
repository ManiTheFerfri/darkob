"""Execute every doctest example in the package, and ratchet their number.

A fenced ``python`` block in a docstring is documentation; a ``>>>`` block is a
test. This module makes the second kind true: every executable example found
anywhere in ``darkob`` is run on every CI run, so an example cannot silently
rot the way prose does.

The second test is a ratchet. The project has far more public methods than
verified examples (see ``python scripts/docstring_coverage.py``), and turning
that around is incremental work rather than a single change. What is
enforceable today is the direction of travel: the number of executable
examples may not decrease. When you document something new with a ``>>>``
block, raise ``docstring_baseline.json`` to match.
"""

from __future__ import annotations

import doctest
import importlib
import json
import pkgutil
from pathlib import Path
from typing import Any, List

import pytest

import darkob

BASELINE_PATH = Path(__file__).with_name("docstring_baseline.json")

#: Examples run with these flags. ELLIPSIS lets an example abbreviate output
#: that legitimately varies (memory addresses, timings); NORMALIZE_WHITESPACE
#: keeps trailing whitespace from failing a build.
OPTION_FLAGS = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE


def _modules() -> List[Any]:
    """Every importable module in the package."""
    loaded = []
    for info in pkgutil.walk_packages(darkob.__path__, prefix="darkob."):
        try:
            loaded.append(importlib.import_module(info.name))
        except Exception:  # pragma: no cover - broken optional submodule
            continue
    return loaded


def _examples() -> List[doctest.DocTest]:
    """Every doctest block in the package that actually contains examples."""
    finder = doctest.DocTestFinder()
    found: List[doctest.DocTest] = []
    for module in _modules():
        for test in finder.find(module):
            if test.examples:
                found.append(test)
    return found


EXAMPLES = _examples()


def test_the_package_has_executable_examples():
    """Guard against the finder silently matching nothing."""
    assert EXAMPLES, (
        "No doctest examples were found anywhere in darkob. If this fails "
        "after a refactor, the finder is broken, not the docs."
    )


def test_every_docstring_example_still_runs():
    """An example that does not run is worse than no example at all."""
    runner = doctest.DocTestRunner(optionflags=OPTION_FLAGS, verbose=False)
    failures: List[str] = []

    for test in EXAMPLES:
        result = runner.run(test, clear_globs=True)
        if result.failed:
            failures.append(
                f"  {test.name}: {result.failed} of {result.attempted} failed"
            )

    assert not failures, (
        "Docstring examples no longer run:\n"
        + "\n".join(failures)
        + "\n\nFix the examples, or delete the one that cannot work."
    )


def executable_example_count() -> int:
    """Examples that actually run.

    ``# doctest: +SKIP`` marks an example that is meant to be read rather than
    executed — typically because it needs a live session. Those stay in the
    documentation but must not inflate the ratchet.
    """
    return sum(
        1
        for test in EXAMPLES
        for example in test.examples
        if not example.options.get(doctest.SKIP)
    )


def test_example_count_has_not_regressed():
    """The ratchet: examples may be added, never removed."""
    baseline = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
    total = executable_example_count()

    assert total >= baseline["examples"], (
        f"The number of runnable docstring examples fell from "
        f"{baseline['examples']} to {total}. Documentation regressions are "
        f"still regressions. If an example genuinely had to go, lower the "
        f"baseline in {BASELINE_PATH.name} and say why in the commit message."
    )


@pytest.mark.parametrize("test", EXAMPLES, ids=lambda t: t.name)
def test_examples_are_namespaced_to_this_project(test: doctest.DocTest):
    """Every example must belong to a darkob module."""
    assert test.name.startswith("darkob"), test.name
