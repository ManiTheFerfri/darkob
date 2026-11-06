# Benchmarks

Two suites live here. Both run **offline**, both report their own environment,
and neither trusts a number it did not measure on the machine it is running on.

```bash
python benchmarks/benchmark_suite.py     # darkob vs maxrubika, same job, same box
python benchmarks/scenarios.py           # darkob alone, under realistic load
python benchmarks/check_regression.py    # fail if a hot path regressed
```

`benchmark_suite.py` and `scenarios.py` both accept `--json`, which is what
`check_regression.py` consumes.

---

## `benchmark_suite.py` — head-to-head

Five hot paths implemented by both libraries, measured by calling each
library's own public objects:

| Case | What runs |
| --- | --- |
| `event_text` | 20,000 reads of `event.text` |
| `lookup` | 20,000 `Data.find_keys("text")` lookups on a nested payload |
| `filter` | 5,000 evaluations of a `Text` filter |
| `dispatch_50` | 5,000 updates routed with 50 handlers registered |
| `dispatch_500` | 5,000 updates routed with 500 handlers registered |

Each case runs in a **fresh subprocess per library**, so neither benefits from
warm caches or an import the other already paid for. The reported figure is
the fastest of three runs, which suppresses OS scheduling noise. A competitor
that is not installed is reported as `n/a` rather than silently skipped.

### A bug this suite had, and what it cost

Until the 0.18 cycle, `dispatch_50` and `dispatch_500` registered their
handlers with

```python
client.handlers = {handler: MessageUpdates() for _ in range(count)}
```

`handlers` is a dict keyed by the handler *function*, so one shared `handler`
object collapsed all 500 entries into a single key. The suite was measuring
**one** handler at every "N handlers" size — which is why the two rows used to
report suspiciously similar times (5.3 ms and 5.4 ms). Each handler is now a
distinct closure, and the measured cost scales with the handler count as it
should. The corrected numbers also made darkob look better, not worse, because
the dispatch index only pays off once there is something to index.

If you add a case, key the handler registry with distinct functions. That is
the single easiest way to write a benchmark that measures nothing.

---

## `scenarios.py` — realistic load

| Scenario | What it measures |
| --- | --- |
| `dispatch_1000x100` | 1,000 updates × 100 registered handlers |
| `sendqueue_100` | 100 messages through `SendQueue` on the success path |
| `resume_download_4mb` | finishing a 4 MiB download interrupted at 50% |
| `filters_2000x5` | 5 text filters × 2,000 events |
| `json_5000` | decoding 5,000 realistic update payloads |

The transport is an in-memory fake that implements HTTP `Range`, so no socket
is opened. That is the point: the network is the same for every library, so
what is worth measuring is darkob's own work — range negotiation, append mode,
the chunked copy loop, queue bookkeeping, filtering, decoding.

`resume_download_4mb` asserts the byte count after resuming, so a scenario can
fail rather than quietly report a fast wrong answer.

---

## Why the numbers are ratios

Absolute milliseconds do not survive a change of machine. The same commit
measures about 3× slower on a shared two-core CI runner than on a desktop, for
reasons that have nothing to do with the code.

So `scenarios.py` also measures a fixed calibration workload — an
allocation-free integer loop — in every run, and reports

```
ratio = case_seconds / calibration_seconds
```

Dividing by calibration removes raw CPU speed. A baseline recorded on a laptop
therefore stays meaningful on a runner, which is what makes
`check_regression.py` usable in CI.

Head-to-head factors need no such correction: both libraries run on the same
box, in the same process conditions, so `theirs / ours` is already
machine-independent.

`check_regression.py` compares **only** these two derived quantities. It never
gates on an absolute duration.

---

## Regression gate

```bash
python benchmarks/check_regression.py                  # 10% tolerance
python benchmarks/check_regression.py --tolerance 0.25 # what CI uses
python benchmarks/check_regression.py --update         # rewrite baseline.json
```

The gate is asymmetric on purpose:

* a head-to-head **factor** that drops past tolerance is a regression — we
  lost ground to maxrubika;
* a scenario **ratio** that rises past tolerance is a regression — our own
  overhead grew.

CI runs the gate at 25% tolerance and a contributor runs it at 10%, because a
shared runner is noisier than a quiet machine. That asymmetry is a deliberate
trade: a threshold tight enough to catch a 10% regression on a shared runner
would also fail on unrelated noise, and a gate that cries wolf gets deleted.

If a change is *intentionally* slower — a correctness fix on a hot path, say —
refresh the baseline in the same commit with `--update` and explain why in the
commit message. Never refresh the baseline to make a red build go green; that
turns the gate into a rubber stamp.

---

## Reproducing the published numbers

The table in the project README was recorded on:

| | |
| --- | --- |
| CPU | 12th Gen Intel Core i5-12400F (6 cores / 12 threads) |
| RAM | 15.8 GB |
| OS | Windows 11 Pro, build 26300 |
| Python | CPython 3.14.7 |
| darkob | 0.18.0 |
| maxrubika | 1.17.0 |

To reproduce:

```bash
python -m venv .venv
.venv/Scripts/activate          # .venv/bin/activate on Linux/macOS
pip install -e .
pip install "maxrubika==1.17.0"
python benchmarks/benchmark_suite.py
```

If `maxrubika` is not installed the competitor column reads `n/a` — the suite
will not fabricate a comparison. Expect your absolute times to differ. The
*ratio* between the two columns is what should hold, because both libraries
are measured on your machine, in the same run.

### What these numbers do not show

* No network is involved, so nothing here measures latency against the Rubika
  API. In a real bot, network time dominates every row in the table.
* The micro-benchmarks (`event_text`, `lookup`, `filter`) isolate one code
  path each. The 5.6× on nested lookup is real but applies to a payload shape
  those properties actually walk; the end-to-end gain in a running bot is
  smaller.
* The two dispatch rows are the ones that show up in practice, because
  routing runs on every single update.

Anyone quoting these numbers should quote the caveat with them.

---

## Adding a case

1. Add a `measure_*` function to `benchmark_suite.py` (head-to-head) or a
   `scenario_*` function to `scenarios.py` (absolute), and register it in the
   `MEASUREMENTS` / `SCENARIOS` list.
2. Make sure the workload is deterministic and offline.
3. Run `python benchmarks/check_regression.py --update` on a quiet machine and
   commit `baseline.json` with the new case.
4. If the case exercises something maxrubika also does, add the matching
   function to the head-to-head suite instead — a comparison is worth more
   than an absolute number.
