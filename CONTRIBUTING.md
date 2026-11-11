# Contributing to darkob

Thanks for taking the time to contribute.

darkob is an async Python library for the [Rubika](https://rubika.ir) and
[Shad](https://shad.ir) platforms — bots and userbots on `asyncio`, with a public
API covered by offline tests and opt-in live checks. It is a hard fork of
[maxrubika](https://github.com/MEH2RAB/maxrubika) by MEHRAB Farahmand, and it is a
**library only**: there is no CLI and no `darkob` command to run.

Every contribution counts. A corrected docstring, a test that pins a bug, a
benchmark that proves a regression, or a careful bug report is worth as much as a
new feature — often more, because it makes the next person's work easier.

## Table of contents

- [Ways to contribute](#ways-to-contribute)
- [Development environment](#development-environment)
- [Running the tests](#running-the-tests)
- [Linting and type checking](#linting-and-type-checking)
- [Benchmarks](#benchmarks)
- [Regenerating docs](#regenerating-docs)
- [Project layout](#project-layout)
- [Coding guidelines](#coding-guidelines)
- [Commit and PR conventions](#commit-and-pr-conventions)
- [Adding a new feature](#adding-a-new-feature)
- [Reporting bugs](#reporting-bugs)
- [Requesting features](#requesting-features)
- [Good first issues](#good-first-issues)
- [Review process](#review-process)
- [AI-assisted contributions](#ai-assisted-contributions)

## Ways to contribute

- **Report a bug** with a minimal reproduction — see [Reporting bugs](#reporting-bugs).
- **Improve the docs** in `docs/`: unclear guides, missing examples, broken links.
- **Write a regression test** for a bug you hit: the most useful bug report there is.
- **Add a benchmark** in `benchmarks/` when a change touches the hot path.
- **Implement a feature**, or port behaviour from `maxrubika` that darkob lacks.
- **Review a PR or triage an issue**: a second opinion on a typed module or a
  crypto-adjacent change is genuinely valuable.

## Development environment

Clone the repository and install it in editable mode with the `dev` extra:

```
git clone https://github.com/ManiTheFerfri/darkob
cd darkob
python -m pip install -e ".[dev]"
```

The `dev` extra installs `pytest>=8`, `pytest-asyncio>=0.24`, `pytest-cov>=5` and
`ruff>=0.6`.

darkob 0.20.0+ supports **Python 3.10 through 3.14** and requires
`aiohttp>=3.14.4,<4`. CI runs the suite on all supported versions plus a Windows
job on 3.12. Darkob 0.19.1 is the last Python 3.9 line and does not include the
new dependency security floor.

**You do not need a Rubika account to work on darkob.** The suite runs fully
offline: `tests/conftest.py` provides a `FakeSession` that replays queued HTTP
responses and records calls, so nothing opens a socket or talks to the real API,
and `darkob.testing` provides `FakeBot`, `FakeEvent` and `make_message`.

## Running the tests

```
python -m pytest
```

pytest runs with `asyncio_mode = "auto"`, so an `async def test_...` needs no
decorator. The suite has over 800 offline test cases and finishes in seconds. For
coverage:

```
python -m pytest --cov=darkob --cov-report=term-missing
```

CI enforces a coverage floor of 30% on the 3.12 job. That is a floor, not a
target: new code should be tested and coverage should trend up.

## Linting and type checking

Lint with ruff (configured in `pyproject.toml`: line length 100):

```
ruff check .
```

Type checking is deliberately split. The modules written for typing support are
in **strict** mode and must stay clean. Install its runner first:

```
python -m pip install mypy
mypy darkob/router.py darkob/retry.py darkob/builders.py darkob/keyboards.py darkob/formatting.py darkob/testing.py
```

Newer typed modules are also checked with `pyright`; see the `pyright` job in
`.github/workflows/ci.yml` for the exact file list. The inherited parts of the
codebase are **not yet fully typed**, so a package-wide `mypy darkob` failure is
expected and is not a blocker. The requirement is not to add *new* errors in the
strict modules, and not to hide a real one behind `# type: ignore`.

## Benchmarks

Performance is a core selling point, so a change that regresses the dispatch hot
path matters even when every test passes.

```
python benchmarks/benchmark_suite.py
```

This compares darkob against `maxrubika` and prints a table; `scripts/benchmark.py`
runs the micro-benchmarks. CI runs both in a blocking job. If your change
could affect routing, filter matching, serialisation or session reuse, run the
suite before and after and put the numbers in your pull request.

## Regenerating docs

Docs live in `docs/` and are built with
[mkdocs-material](https://squidfunk.github.io/mkdocs-material/). The generated API
reference (`docs/api/`, `docs/api.json`, `docs/llms-full.txt`) comes from the docs
generator:

```
python -m pip install mkdocs-material pymdown-extensions pygments
python scripts/generate_docs_assets.py
mkdocs build
```

CI regenerates the assets and **fails if the output differs from what is
committed**. If you change a public API — a signature, an `__all__` entry, a
docstring that becomes a reference entry — re-run the generator and commit its
output in the same pull request. The published site is
<https://manitheferfri.github.io/darkob/>.

## Project layout

```
darkob/       the library itself
  bot/          Bot client, handler registry and dispatch
  client/       session/HTTP plumbing and the Rubika/Shad clients
  compat/       the maxrubika import shim
  types/        wire-format models and enums; utils/ the small typed helpers
  strict-mypy: router.py, retry.py, builders.py, keyboards.py, formatting.py,
  testing.py; shad.py is the Shad platform client
tests/        offline test suite and its fakes
benchmarks/   comparison suite against maxrubika; scripts/ has the docs generator
              and conformance checks; docs/ is the mkdocs-material site
```

## Coding guidelines

- **Never remove or rename public API.** darkob must stay a strict superset of
  `maxrubika`'s public surface. If a change is unavoidable it needs a deprecation
  cycle: keep the old name working, emit a `DeprecationWarning`, and remove it no
  sooner than the next minor release (`tests/test_api_parity.py` guards this).
- **SemVer** `MAJOR.MINOR.PATCH`. While the project is pre-1.0 (`0.x`), bug fixes
  and additions bump **MINOR**; breaking changes are called out in the release notes.
- **Every bug fix needs a regression test** that fails before the fix and passes
  after it. If you cannot write one, explain why in the pull request.
- **New public functions need a docstring with a runnable example** — something a
  reader can paste into a script and have work.
- **Style:** `ruff`, line length 100, 4-space indent, `async def` for I/O paths.
- **No blocking calls inside coroutines**: no `time.sleep`, no synchronous file I/O,
  no CPU-bound work without `asyncio.to_thread` — blocking the loop stalls everyone.
- Keep `__all__` in sync with what you export, and keep annotations honest.

## Commit and PR conventions

Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/)
(`feat:`, `fix:`, `docs:`, `perf:`, `test:`, `refactor:`, `chore:`, `ci:`), in the
imperative mood, with a subject under about 72 characters.

Pull requests should be **small and focused**: one logical change, one PR. A PR that
fixes a bug and reformats a file is two PRs; say so early if a change is large.

**CI must be green.** The `CI` workflow covers the test matrix, the Windows job,
`lint`, `typing`, `pyright`, `package` and `docs`. The `benchmark` and `security`
jobs are also blocking and must pass. Individual extra reports within those jobs
may be non-blocking; consult the workflow before dismissing a failure.

## Adding a new feature

- [ ] The feature is described in the PR body, with a usage example.
- [ ] No existing public API was removed, renamed, or changed in meaning.
- [ ] I/O paths are `async def` and await properly.
- [ ] New public functions have a docstring with a runnable example.
- [ ] Tests cover the happy path, the obvious failure modes, and the offline
      behaviour via `FakeSession` / `FakeBot`.
- [ ] `python -m pytest` passes and `ruff check .` is clean.
- [ ] `mypy` is clean on the strict modules and `pyright` on the typed ones.
- [ ] Docs updated in `docs/guides/` or `docs/get-started/`.
- [ ] `python scripts/generate_docs_assets.py` re-run and committed if a public
      signature or export changed.
- [ ] Benchmark numbers included if the change could affect the hot path.

## Reporting bugs

Open an issue with the **Bug report** template: it asks for what happened, what you
expected, a minimal reproduction, the traceback, your versions and OS, the client
(`Bot`, `Messenger` or `Shad`) and whether it happens live or in a unit test.

Two things decide whether a bug gets fixed in a day or stalls: a **minimal
reproduction** — strip it down until removing anything else makes the bug disappear —
and **redacted secrets**, since no report should contain a bot token or a `Messenger`
session string. Search existing issues first, and never report a security problem in
public: follow [SECURITY.md](SECURITY.md).

## Requesting features

Open an issue with the **Feature request** template. Describe the problem before the
API you want — that is what makes a proposal reviewable. Sketch the call site, and say
whether the feature exists in `maxrubika` and whether darkob should match or improve it.

## Good first issues

Issues labelled [`good first issue`](https://github.com/ManiTheFerfri/darkob/labels/good%20first%20issue)
are scoped so someone new to the codebase can finish one without deep context: a missing
test, a docstring example, a small bug in one module, a docs correction. They touch one
or two files, and `help wanted` marks larger work that is open to outside contributors.

Comment on the issue if you are unsure where to start and a maintainer will explain
what is needed. Please do not claim an issue and then vanish — a short note that you are
still working on it is all we ask.

## Review process

- A pull request needs **one maintainer approval** before merge; the maintainer is Mani
  Keikhosravi.
- Expect a **first response within about a week**. This is a volunteer project; if a
  week passes without a reply, a friendly ping on the PR is welcome.
- Review comments are about the code. Push back if a reviewer is wrong — with
  reasoning, a test, or a benchmark.
- Keep the PR mergeable while it is open: rebase on `main` on conflict, and re-run
  the tests after resolving.

## AI-assisted contributions

AI-assisted contributions are welcome — using good tools is not a problem. The rules:

- **You are responsible for understanding the code you submit** and able to explain
  every line in review; "the model wrote it" does not explain why a lock is needed.
- **You are responsible for testing it.** Run `python -m pytest` and `ruff check .`
  yourself — AI-generated code is prone to plausible-looking APIs that do not exist here.
- **No invented benchmarks, test results, or unverified claims.** If you did not run
  `benchmarks/benchmark_suite.py`, do not quote numbers from it. Fabricated evidence
  gets a PR closed.
- **Disclose it and keep it small.** One line in the PR description ("drafted with an
  AI assistant, reviewed and tested by me") is enough; unrequested 20k-line rewrites
  get closed.

Thank you for contributing.
