"""Generate machine-readable and AI-friendly documentation assets.

Everything produced here is derived from the installed package, so the
reference cannot drift from the code. Run from the repository root:

    python scripts/generate_docs_assets.py

Outputs:
    docs/api/bot.md          human + LLM readable Bot reference
    docs/api/messenger.md    Messenger reference
    docs/api/shad.md         Shad reference
    docs/api.json            machine-readable method index
    docs/llms-full.txt       complete corpus in one file for LLMs

Signatures are rendered from source AST rather than introspection so that
output does not depend on the interpreter version. CI still compares the
committed output byte-for-byte; if you regenerate with a different Python
major/minor, review the diff before committing.
"""

from __future__ import annotations

import ast
import inspect
import json
import sys
import textwrap
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

DOCS = ROOT / "docs"
API_DIR = DOCS / "api"

CLASSES = [
    ("Bot", "bot", "The official Rubika Bot API. Token based, plain HTTP JSON."),
    (
        "Messenger",
        "messenger",
        "A real user account (userbot): channels, groups, voice chats, settings.",
    ),
    (
        "Shad",
        "shad",
        "The Shad education platform. Same Messenger protocol, Shad hosts.",
    ),
]

GROUP_ORDER = [
    "messages",
    "chats",
    "groups",
    "channels",
    "users",
    "settings",
    "extras",
    "bots",
    "base",
    "core",
]


def signature_of(func: Any) -> str:
    """Render a signature from source AST, not introspection.

    ``inspect.signature`` renders annotations differently across Python
    versions (PEP 604 unions, stringified annotations), which made the
    generated docs drift depending on which interpreter ran the script.
    Parsing the source text gives byte-identical output everywhere.
    """
    try:
        source = textwrap.dedent(inspect.getsource(func))
        module = ast.parse(source)
        node = module.body[0]
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            return f"{func.__name__}({ast.unparse(node.args)})"
    except (OSError, TypeError, SyntaxError, IndentationError, IndexError):
        pass

    try:
        return f"{func.__name__}{inspect.signature(func)}"
    except (TypeError, ValueError):
        return f"{func.__name__}(...)"


def clean_doc(func: Any) -> str:
    doc = inspect.getdoc(func) or ""
    return textwrap.dedent(doc).strip()


def module_group(func: Any) -> str:
    module = getattr(func, "__module__", "") or ""
    parts = module.split(".")
    if len(parts) >= 3 and parts[0] == "darkob":
        # darkob.client.messages.send_message -> messages
        for candidate in parts:
            if candidate in GROUP_ORDER:
                return candidate
        return parts[-2] if len(parts) >= 2 else "other"
    return "core"


def collect(cls: type) -> List[Dict[str, Any]]:
    """Public callables defined across the class MRO, de-duplicated."""
    seen = {}
    for base in reversed(cls.__mro__):
        for name, member in vars(base).items():
            if name.startswith("_"):
                continue
            func = member
            if isinstance(func, (staticmethod, classmethod)):
                func = func.__func__
            if not callable(func) or not hasattr(func, "__doc__"):
                continue
            seen[name] = func

    entries = []
    for name, func in sorted(seen.items()):
        entries.append(
            {
                "name": name,
                "signature": signature_of(func),
                "doc": clean_doc(func),
                "group": module_group(func),
                "module": getattr(func, "__module__", ""),
            }
        )
    return entries


def render_class_markdown(
    class_name: str, summary: str, entries: List[Dict[str, Any]], is_mirror: bool = False
) -> str:
    lines = [
        f"# {class_name} API reference",
        "",
        summary,
        "",
        "> Generated from the installed package by "
        "`scripts/generate_docs_assets.py`. Every signature below is real; "
        "do not hand-edit this file.",
        "",
    ]

    if is_mirror:
        lines += [
            "!!! note \"Shad mirrors Messenger\"",
            "    `Shad` exposes the same methods as `Messenger`, against Shad "
            "hosts. Use the Messenger reference for signatures and behaviour.",
            "",
        ]

    lines += [
        f"**{len(entries)} public methods.**",
        "",
        "## Method index",
        "",
    ]

    groups: Dict[str, List[Dict[str, Any]]] = {}
    for entry in entries:
        groups.setdefault(entry["group"], []).append(entry)

    ordered = [g for g in GROUP_ORDER if g in groups] + [
        g for g in sorted(groups) if g not in GROUP_ORDER
    ]

    for group in ordered:
        items = groups[group]
        names = ", ".join(f"[`{e['name']}`](#{e['name'].lower().replace('_', '-')})" for e in items)
        lines.append(f"- **{group}** ({len(items)}): {names}")

    lines.append("")

    for group in ordered:
        lines += [f"## {group}", ""]
        for entry in groups[group]:
            lines += [
                f"### {entry['name']}",
                "",
                "```python",
                entry["signature"],
                "```",
                "",
            ]
            if entry["doc"]:
                lines += [entry["doc"], ""]
            else:
                lines += ["_No docstring available._", ""]

    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    import darkob

    API_DIR.mkdir(parents=True, exist_ok=True)

    index: Dict[str, Any] = {
        "package": "darkob",
        "version": getattr(darkob, "__version__", "unknown"),
        "generated_from": "installed package source",
        "classes": {},
    }

    for attr, slug, summary in CLASSES:
        cls = getattr(darkob, attr)
        entries = collect(cls)

        is_mirror = attr == "Shad"
        (API_DIR / f"{slug}.md").write_text(
            render_class_markdown(attr, summary, entries, is_mirror=is_mirror),
            encoding="utf-8",
        )

        index["classes"][attr] = {
            "summary": summary,
            "method_count": len(entries),
            "methods": [
                {
                    "name": e["name"],
                    "signature": e["signature"],
                    "group": e["group"],
                    "module": e["module"],
                    "doc": e["doc"],
                }
                for e in entries
            ],
        }
        print(f"{attr}: {len(entries)} methods")

    (DOCS / "api.json").write_text(
        json.dumps(index, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # ---- llms-full.txt: one self-contained corpus for an LLM --------
    # Not a dump of every page: a curated order that teaches the model
    # the model of the library, then gives it every real signature.
    CURATED = [
        "get-started/installation.md",
        "get-started/quickstart.md",
        "guides/handlers.md",
        "guides/filters.md",
        "guides/routers.md",
        "guides/fsm.md",
        "guides/keyboards.md",
        "guides/composing-messages.md",
        "guides/errors.md",
        "guides/sync-and-async.md",
        "guides/testing.md",
        "ai/index.md",
    ]

    chunks = [
        "# darkob — complete reference",
        "",
        f"darkob {index['version']} — async Python for the Rubika and Shad "
        "messaging platforms.",
        "",
        "Read this file top to bottom before writing code. It contains the "
        "full public API (every real signature), the filter catalogue, the "
        "patterns, and the mistakes to avoid. No other page is required.",
        "",
        "Hard rules:",
        "- Handlers are `async def name(bot, event)`.",
        "- `event`, never `message`; `event.chat_id`, never `event.chat.id`.",
        "- Filters come from `darkob.bot.filters` and are INSTANTIATED: "
        "`IsGroup()`, not `IsGroup`.",
        "- There is no Dispatcher, no message_handler, no aiogram/Pyrogram "
        "types.",
        "- If a method is not in the API section below, it does not exist.",
        "",
    ]

    for relative in CURATED:
        path = DOCS / relative
        if not path.exists():
            continue
        body = path.read_text(encoding="utf-8").strip()
        body = body.split("\n", 1)[1] if body.startswith("# ") else body
        chunks += ["", "---", f"# SOURCE: {relative}", "", body, ""]

    chunks += ["", "---", "# COMPLETE API: every public signature", ""]
    for attr, _slug, _summary in CLASSES:
        entries = index["classes"][attr]["methods"]
        chunks += [f"## {attr} ({len(entries)} methods)", ""]
        for entry in entries:
            chunks.append(f"### `{entry['signature']}`")
            chunks.append("")
            doc = entry["doc"].strip()
            if doc:
                chunks.append(doc)
            else:
                chunks.append("_No docstring._")
            chunks.append("")
        chunks.append("")

    chunks += ["", "---", "# PUBLIC API: classes and helpers", ""]
    chunks.append(
        "Every name exported from the package root, so no part of the "
        "library is missing from this file."
    )
    chunks.append("")
    seen_exports = set()
    for export in getattr(darkob, "__all__", []):
        target = getattr(darkob, export, None)
        if target is None or id(target) in seen_exports:
            continue
        seen_exports.add(id(target))
        # Own docstring only: getdoc() walks the MRO and would describe a
        # class with an unrelated base class's documentation.
        summary = (getattr(target, "__doc__", None) or "").split("\n")[0].strip()
        line = f"- `darkob.{export}`"
        if summary:
            line += f" — {summary}"
        chunks.append(line)
    chunks.append("")

    (DOCS / "llms-full.txt").write_text("\n".join(chunks), encoding="utf-8")
    size = (DOCS / "llms-full.txt").stat().st_size
    print(f"llms-full.txt: {size // 1024} KB")
    print(f"api.json: {(DOCS / 'api.json').stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
