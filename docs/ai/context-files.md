# Context files

darkob publishes three machine-readable artifacts. All are generated or
verified by CI, so they match the released version.

## `llms.txt`

The [llms.txt convention](https://llmstxt.org/) is a small Markdown file
at the site root that tells a model what the project is and where the
detail lives.

```text
https://manitheferfri.github.io/Darkob/llms.txt
```

Use it when the model needs an overview and the ability to ask for more.

## `llms-full.txt`

The entire documentation — every guide, every page, both API surfaces —
concatenated into one Markdown file with `SOURCE:` markers.

```text
https://manitheferfri.github.io/Darkob/llms-full.txt
```

Use it when you want the model to answer anything without follow-up
retrieval. It is large; prefer `api/bot.md` alone if you only touch bots.

Cost control:

- Bot-only work: `api/bot.md` (~40 methods) instead of the full file.
- Full app: `llms-full.txt` once at the start of a long session, then
  keep the conversation going rather than re-pasting.

## `api.json`

Structured, generated, and exact:

```json
{
  "package": "darkob",
  "version": "0.2.1",
  "classes": {
    "Bot": {
      "summary": "…",
      "method_count": 42,
      "methods": [
        {
          "name": "send_message",
          "signature": "send_message(self, chat_id, text, metadata=None, …)",
          "group": "messages",
          "module": "darkob.bot.send_message",
          "doc": "Send a text message …"
        }
      ]
    }
  }
}
```

Use it for tooling: validate that a model-proposed method exists, generate
stubs, or drive an agent that must not hallucinate.

```python
import json, urllib.request

api = json.load(urllib.request.urlopen(
    "https://manitheferfri.github.io/Darkob/api.json"
))

bot_methods = {m["name"]: m for m in api["classes"]["Bot"]["methods"]}
print(len(bot_methods), "real Bot methods")
print(bot_methods["send_message"]["signature"])
```

## Raw Markdown for every page

Any page is also served as raw Markdown:

| Page | Raw |
| --- | --- |
| `/guides/routers/` | `/guides/routers.md` |
| `/api/bot/` | `/api/bot.md` |
| `/ai/prompt-pack/` | `/ai/prompt-pack.md` |

This is the cheapest way to give a model one topic without navigation,
headers or footer noise.

## Suggested integration

=== "Claude / ChatGPT"

    Attach `llms-full.txt` for full-context work, or paste the single
    relevant `.md` page for a focused task.

=== "Cursor / Copilot / Windsurf"

    Add a project rule (see the [prompt pack](prompt-pack.md)) and keep
    `api.json` in the repo so the model can grep real signatures.

=== "Custom agents / RAG"

    Index `llms-full.txt` split on `SOURCE:` markers — each chunk is one
    coherent page. Store `api.json` separately as a structured lookup
    tool rather than as prose to embed.

## Freshness

`docs/api/*.md`, `docs/api.json` and `docs/llms-full.txt` are generated
by `scripts/generate_docs_assets.py` from the installed package. CI fails
if they are stale, so the published context can never describe methods
that do not exist.
