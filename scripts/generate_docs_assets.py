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
"""

from __future__ import annotations

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

    # ---- llms-full.txt: the whole corpus in one file --------------------
    guides = sorted(DOCS.rglob("*.md"))
    chunks = [
        "# darkob — complete documentation",
        "",
        "This file concatenates the entire darkob documentation for LLM "
        "ingestion. Source: https://github.com/ManiTheFerfri/darkob",
        "",
        f"Version: {index['version']}",
        "",
    ]
    for path in guides:
        if path.name in {"llms-full.txt"}:
            continue
        relative = path.relative_to(DOCS).as_posix()
        chunks += [
            "",
            "---",
            f"# SOURCE: {relative}",
            "",
            path.read_text(encoding="utf-8").strip(),
            "",
        ]

    (DOCS / "llms-full.txt").write_text("\n".join(chunks), encoding="utf-8")
    size = (DOCS / "llms-full.txt").stat().st_size
    print(f"llms-full.txt: {size // 1024} KB")
    print(f"api.json: {(DOCS / 'api.json').stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
