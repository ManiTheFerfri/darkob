# Roadmap

This is a working document, not a wish list. Every item has evidence, an
effort estimate, and a reason it belongs here.

## Where darkob stands

Measured on 2026-11-05 via the GitHub and PyPI APIs:

| Project | Stars | PyPI downloads / month |
| --- | --- | --- |
| `discord.py` | — | 4,854,830 |
| `telethon` | — | 3,009,805 |
| `aiogram` | — | 2,756,261 |
| `pyrogram` | — | 261,325 |
| **`maxrubika`** (upstream) | 24 | **1,083** |
| `shayanheidari01/rubika` | 130 | — |
| `Bahman-Ahmadi/rubika` | 81 | — |
| `mivmi/rubika` | 66 | — |
| `Mahdy-Ahmadi/rubka` | 53 | — |
| `AliGanji1/Pyrubi` | 40 | — |
| `ErfanBahramali/Rubika-PHP` | 12 | — |

Three facts fall out of this table.

1. **The ecosystem is tiny and fragmented.** No Rubika library has more
   than ~130 stars. There is no clear default, no de-facto standard, and
   no project with a serious CI or test suite.
2. **The ceiling is far above where we are.** `pyrogram` — a *single
   platform*, unofficial — does 261k downloads/month. Rubika is a smaller
   market, but not a 240× smaller market. The gap is product quality, not
   demand.
3. **Whoever wins will win on developer experience.** Every rival has
   roughly the same API knowledge. Nobody has better docs, types, tests,
   or AI support. That is the opening.

The ecosystem is also noisy: a large share of "Rubika" repositories are
account-filtering and scraping tools. darkob should be visibly the
*legitimate engineering* option, not another one of those.

## Strategy

Three bets, in priority order.

**Bet 1 — AI-first developer experience.** Most new darkob bots will be
generated, not typed. The library that a model can use *correctly without
asking questions* wins. This is already partly shipped (`llms.txt`,
`api.json`, generated reference); the roadmap extends it to tooling.

**Bet 2 — Stability as the brand.** The inherited codebase hid failures.
Every competitor still does. Being the library that tells you what went
wrong is a durable differentiator, and it compounds with Bet 1: models
debug well when errors are typed and specific.

**Bet 3 — Become the ecosystem's foundation.** One excellent library plus
a plugin surface beats five mediocre ones. We should absorb the useful
ideas from `rubika`, `rubka` and `Pyrubi` rather than competing feature by
feature.

---

## H0 — Now (0–4 weeks)

Everything here is small and unblocks something else.

| Item | Why | Effort | Risk |
| --- | --- | --- | --- |
| **MCP server for darkob** | Lets an AI client query the real API surface as a tool instead of from memory. The single highest-leverage AI feature available to us. | M | Low |
| **Agent skill / rules file** | A versioned `SKILL.md` + editor rules so assistants pick the right idioms without a long prompt. | S | Low |
| **`mypy` in CI** | Types are the best anti-hallucination tool. Start with `--ignore-missing-imports` on the public surface only. | M | Medium |
| **Middleware on routers** | Currently bot-level only; the obvious gap next to `Router`. | S | Low |
| **Pagination helpers** | `async for msg in bot.iter_messages(...)` instead of hand-managed cursors. | M | Low |
| **Redis storage backend** | `Storage` is an interface with one durable backend; multi-process bots need Redis. | S | Low |
| **CLI: `darkob new`, `darkob run`** | Removes the "what do I create first" step for a human *and* a model. | M | Low |
| **Stale-doc guard** (done) | CI already fails if generated docs drift. | — | — |

**Exit criteria:** an assistant with only `llms.txt` + the MCP server can
write a router-based, FSM-backed bot that runs first try.

## H1 — Next (1–3 months)

Depth on developer experience.

| Item | Why | Effort | Risk |
| --- | --- | --- | --- |
| **Typed public API** | Full annotations + `py.typed`, so editors autocomplete instead of guessing. | L | Medium |
| **Type stubs for `types/`** | Event models are the least discoverable part; stubs make `event.` completions real. | L | Medium |
| **Testing toolkit** (`darkob.testing`) | `FakeEvent`, `FakeBot`, recorded fixtures — mirrors what made `aiohttp` and `fastapi` easy to test. | M | Low |
| **Template gallery** | 5–8 runnable starters (echo, admin, FSM form, channels, scheduler). Models copy patterns; give them good ones. | M | Low |
| **i18n / message catalogue** | Persian + English strings for common flows. The userbase is bilingual. | M | Medium |
| **Benchmark suite** | Throughput for dispatch, retries, uploads. Needed to defend "faster" claims. | M | Low |
| **Structured logging + request IDs** | Correlate a bot log line with a server request. | S | Low |
| **Error catalogue page** | Every exception, its cause, and its fix — one page models can quote. | S | Low |
| **Contract tests against the live Bot API** | Opt-in CI job with a real token to catch upstream protocol drift. | M | Medium (needs a token + rate limits) |

## H2 — Later (3–6 months)

Platform depth and operational maturity.

| Item | Why | Effort | Risk |
| --- | --- | --- | --- |
| **Full Bot API coverage audit** | Enumerate every documented endpoint and prove each has a method. Publish the matrix. | M | Low |
| **Shad parity verification** | `Shad` mirrors `Messenger` by construction; prove it with tests, not assumption. | M | Low |
| **Resumable uploads/downloads** | Large media over flaky Iranian networks is the top real-world complaint pattern. | L | Medium |
| **Webhook server hardening** | Signature verification, replay protection, backpressure. | M | Medium |
| **Rate-limit governor** | Token bucket per chat + global, honouring `TOO_REQUESTS`. | M | Medium |
| **Multi-account manager** | Run N sessions in one process with shared transport limits. | L | Medium |
| **Metrics/tracing** | Prometheus + OpenTelemetry hooks so operators can see failures. | M | Low |
| **Session migration tool** | Import a `maxrubika` session by re-deriving the old key, so forks are not a cliff. | M | Medium |
| **Offline update queue** | Buffer outgoing messages while the network is down, flush on recovery. | L | Medium |

## H3 — Beyond (6–12 months)

Ecosystem plays.

| Item | Why | Effort | Risk |
| --- | --- | --- | --- |
| **Plugin registry + discovery** | A curated list beats a README section. | M | Low |
| **Generated SDKs** (JS/TS, Go) from `api.json` | The spec already exists; codegen is cheap and expands the ecosystem. | XL | Medium |
| **Official bot directory** | Showcase real bots; the main discovery channel today is Telegram channels. | M | Low |
| **Hosted docs search with AI answers** | Answer "how do I X" from the corpus, with citations back to pages. | M | Medium |
| **Rubika app-version tracker** | Detect protocol/app-version changes and open a PR automatically. | L | Medium — legal/fragile |

## Moonshot

- **Natural-language bot builder.** "Make me a support bot with a 3-step
  form" → generated, tested, runnable project. Only credible if H0–H1
  land, because it depends on an MCP server, templates, and typed models.
- **Hosted runtime.** Deploy a darkob bot without a server. High value,
  high operational and jurisdictional risk.
- **Bidirectional bridge** (Rubika ↔ Telegram/Shad). Only if legally and
  ethically defensible.

---

## What NOT to build

Listing these matters as much as the backlog.

- **Session generators that scrape credentials.** Some rivals ship these.
  They are the ecosystem's main trust problem and invite abuse.
- **Bulk DM / mass-invite / spam tooling.** Same reason. darkob should
  have no "message everyone" primitive.
- **Account-filtering / "hack" utilities.** A large slice of the
  ecosystem's repositories are these; associating with them would sink the
  project's credibility.
- **A Telegram API clone for its own sake.** Copy the *ergonomics*
  (routers, FSM, middleware) — not the surface area we do not need.
- **A GUI.** Out of scope; the value is a clean library and docs.
- **Premature async rewrite of the Bot API internals.** Current design is
  sound; churn here buys nothing measurable.

## Success metrics

Measure these monthly, not by vibes.

| Metric | Today | 3 months | 12 months |
| --- | --- | --- | --- |
| PyPI downloads / month | new | 3,000 | 25,000 |
| GitHub stars | 0 | 100 | 750 |
| Tests | 225 | 400 | 700 |
| Public API type coverage | ~0% | 60% | 95% |
| Median issue first response | — | < 48 h | < 24 h |
| Stale-doc CI failures | 0 | 0 | 0 |
| Bots created from templates | 0 | 25 | 400 |

## Risks

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Upstream diverges (maxrubika keeps shipping) | Merge pain | Keep `upstream` remote; cherry-pick fixes; track diffs weekly |
| Rubika changes the private API | Messenger breaks | Version the protocol; ship a compatibility matrix; fast release cadence |
| Iranian network/proxy instability | CI and user pain | Bounded retries (done); pooled sessions (done); document proxy config |
| PyPI access restrictions | Release risk | Trusted publishing (done); mirrored release notes; sdist fallback |
| Ecosystem association with scraping tools | Trust | Explicit "what we do not build" stance; no credential tooling |
| AI writes plausible-but-wrong code | Adoption | MCP server + `api.json` validation + prompt pack |

## Sequencing rule

Ship in this order, and do not skip:

1. Make it **correct** (tests, types, lint).
2. Make it **legible** (docs, generated reference, AI assets).
3. Make it **fast** (dispatch, transport, retries).
4. Make it **big** (features, ecosystem).

Steps 1–3 are done or in progress. Step 4 is where the growth lives — but
only after the first three are true.
