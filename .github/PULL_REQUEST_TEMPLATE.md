<!--
  Thanks for contributing to darkob. Keep this pull request small and focused:
  one logical change. Fill in every section that applies and delete the ones
  that do not. CI must be green before this can be merged.
-->

## Description

<!--
  What does this change do, and why? Link the issue if there is one.
  If the "why" is not obvious, explain it here rather than in the commit body —
  reviewers read this first.
-->

## Type of change

<!-- Tick the one that fits. If more than one fits, reconsider splitting the PR. -->

- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds capability)
- [ ] Performance improvement
- [ ] Refactor (no behaviour change)
- [ ] Documentation update
- [ ] Test or CI/tooling change
- [ ] Breaking change (see the section below)

## Checklist

- [ ] Tests added or updated — a bug fix includes a regression test that fails before the fix.
- [ ] `python -m pytest` passes locally.
- [ ] `ruff check .` is clean.
- [ ] `mypy darkob/router.py darkob/retry.py darkob/builders.py darkob/keyboards.py darkob/formatting.py darkob/testing.py` reports no new errors in the strict modules.
- [ ] Documentation updated in `docs/` if user-facing behaviour changed.
- [ ] `python scripts/generate_docs_assets.py` re-run and its output committed, if any public API changed.
- [ ] No public API was removed or renamed (`maxrubika` compatibility preserved).
- [ ] Benchmark numbers included below, if this is a performance change.

## Benchmark results

<!--
  Required for changes that touch the dispatch hot path: routing, filter
  matching, serialisation, session reuse. Paste the before/after table from
  `python benchmarks/benchmark_suite.py`. Delete this section if it does not apply.
-->

## Breaking change?

<!--
  darkob is a strict superset of maxrubika's public API. A breaking change needs
  a deprecation cycle: keep the old name working, emit a DeprecationWarning, and
  remove it no sooner than the next minor release.
-->

- [ ] No — nothing in the public API changed.
- [ ] Yes — described below, with the deprecation plan and the release it targets.

<!-- If yes, explain what breaks, who is affected, and how they migrate. -->

## Related issues

<!-- Use "Closes #123" so the issue closes automatically when this merges. -->

Closes #
