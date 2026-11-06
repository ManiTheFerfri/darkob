# Performance

darkob is measured against [maxrubika](https://github.com/MEH2RAB/maxrubika)
on five hot paths, with each case running in a fresh process so neither
library inherits the other's warm state. Both libraries run on the same
machine, in the same run.

| Benchmark | darkob | maxrubika | Result |
| --- | --- | --- | --- |
| Read `event.text` ×20,000 | 13.5 ms | 20.9 ms | **1.5× faster** |
| Nested key lookup ×20,000 | 3.0 ms | 16.8 ms | **5.7× faster** |
| Filter evaluation ×5,000 | 5.1 ms | 10.5 ms | **1.4× faster** |
| Route 5,000 updates, 50 handlers | 160 ms | 344 ms | **2.2× faster** |
| Route 5,000 updates, 500 handlers | 1.50 s | 3.33 s | **2.2× faster** |

Measured on an i5-12400F, Windows 11, CPython 3.14.7, against maxrubika
1.17.0. Your absolute times will differ; the *ratio* between the columns is
what should hold.

Under realistic load, routing 1,000 updates against 100 registered handlers
runs at about **17,500 updates/s**, and a 4 MiB download resumed from 50%
costs **1.9 ms** of library overhead.

## Where the difference comes from

**Lookups are indexed.** A payload builds a key index the first time anything
looks into it, so `event.text` — which searches `text` and then `caption` —
does not walk the structure on every read.

**Dispatch is an index, not a scan.** Handlers are grouped by the update name
they handle, once. Routing cost then scales with the handlers that match, not
with the handlers that exist.

**The per-update bookkeeping is nearly free.** `capitalize()` is memoised, and
a pending `ask()` costs one integer check per update rather than an `Event`
construction.

## What these numbers do not show

- **No network.** Nothing here measures latency against the Rubika API. In a
  running bot, network time dominates every row; these figures describe CPU
  work per update.
- **The dispatch rows time the client dispatch path**, the one both libraries
  expose identically, which is what keeps the comparison fair. `darkob.Bot`
  routes through its own handler registry — a linear scan, not an index — so
  its per-update cost differs and is not what those rows measure.
- **The micro-benchmarks isolate one code path each.** The 5.7× nested lookup
  is a real measurement on a payload shape those properties actually walk, but
  the end-to-end gain in a bot is smaller. The dispatch rows are the ones you
  will notice, because routing runs on every single update.
- **A benchmark bug is worse than no benchmark.** The dispatch cases used to
  register their handlers as `{handler: Handler() for _ in range(count)}` — a
  dict keyed by the function, so 500 identical entries collapsed into one key.
  Both "50 handlers" and "500 handlers" were measuring a single handler. With
  distinct handlers the gap widened from 1.5× to 2.2×, because an index only
  helps once there is something to index. Numbers published before 0.18.0
  should be discarded.

## Reproducing it

```bash
git clone https://github.com/ManiTheFerfri/darkob
cd darkob
python -m venv .venv
.venv/Scripts/activate          # .venv/bin/activate on Linux/macOS
pip install -e .
pip install "maxrubika==1.17.0"
python benchmarks/benchmark_suite.py     # head-to-head table
python benchmarks/scenarios.py           # absolute throughput
```

If `maxrubika` is not installed the competitor column reads `n/a`; the suite
will not fabricate a comparison.

## The regression gate

CI runs `python benchmarks/check_regression.py` on every push. It compares two
*derived* quantities and never an absolute duration:

- **Head-to-head factors** (darkob ÷ maxrubika). Machine-independent by
  construction, because both libraries run on the same runner.
- **Calibration-normalised ratios.** Every scenario run also measures a fixed,
  allocation-free integer loop, and reports `case_seconds ÷ calibration`. This
  removes the host's raw CPU speed, which is what makes a baseline recorded in
  one place meaningful in another.

A head-to-head factor that *drops* past tolerance is a regression; a scenario
ratio that *rises* past tolerance is a regression. CI's tolerance is wider
than the one a contributor gets locally, because a shared runner is noisier
than a quiet machine.

See the [benchmarks README](https://github.com/ManiTheFerfri/darkob/blob/main/benchmarks/README.md)
for the full methodology, the recording hardware and how to add a case.

## See also

- [Architecture](explanation/architecture.md) — the request pipeline these
  numbers measure.
- [Rate limiting](how-to/rate-limit-safely.md) — staying under the API's
  ceiling without wasting throughput.
