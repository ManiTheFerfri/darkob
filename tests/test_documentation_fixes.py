"""Offline regressions for documentation generation, claims, and accessibility."""

from __future__ import annotations

import ast
import re
from pathlib import Path

import darkob
import pytest

from scripts import conformance
from scripts.generate_docs_assets import collect, render_class_markdown


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
VALID_TOKEN = "ABCDE" + "0" * 59
EXPECTED_DECORATORS = {
    "middleware",
    "on_bot_joined",
    "on_bot_permissions_changed",
    "on_bot_removed",
    "on_callback",
    "on_command",
    "on_delete_message",
    "on_edit_message",
    "on_error",
    "on_event_data",
    "on_message",
    "on_new_message",
    "on_shutdown",
    "on_start",
    "on_started_bot",
    "on_stopped_bot",
    "on_update",
}


@pytest.mark.parametrize("slug", ["bot", "messenger", "shad", "rubino", "rubiai", "rubikatv"])
def test_api_method_index_anchors_match_heading_ids(slug):
    """Underscores in IDs must not become unrelated hyphenated links."""
    text = (DOCS / "api" / f"{slug}.md").read_text(encoding="utf-8")
    index = text.split("## Method index", 1)[1].split("\n## ", 1)[0]
    anchors = set(re.findall(r"\]\(#([^)]+)\)", index))
    headings = {name.lower() for name in re.findall(r"^### ([^\n]+)$", text, re.M)}
    assert anchors == headings


def test_api_markdown_links_bind_to_exact_underscore_ids():
    markdown = render_class_markdown("Bot", "Bot API", collect(darkob.Bot))
    assert "[`get_me`](#get_me)" in markdown
    assert "[`on_new_message`](#on_new_message)" in markdown
    assert "#get-me" not in markdown


def test_collect_includes_real_instance_injected_bot_decorators():
    entries = collect(darkob.Bot)
    by_name = {entry["name"]: entry for entry in entries}
    assert len(entries) == 68
    assert EXPECTED_DECORATORS == EXPECTED_DECORATORS.intersection(by_name)
    assert by_name["on_command"]["module"] == "darkob.bot.command"
    assert by_name["on_command"]["signature"].startswith("on_command(self")
    assert "prefixes" in by_name["on_command"]["signature"]
    assert by_name["on_new_message"]["doc"] == "Handle brand-new messages."


def test_code_examples_do_not_call_nonexistent_bot_get_chats():
    for relative in ("ai/recipes.md", "guides/sync-and-async.md"):
        text = (DOCS / relative).read_text(encoding="utf-8")
        for match in re.finditer(r"```python[^\n]*\n(.*?)```", text, re.S):
            for node in ast.walk(ast.parse(match.group(1))):
                if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
                    if node.value.id == "bot" and node.attr.startswith("get_"):
                        assert hasattr(darkob.Bot, node.attr), f"{relative}: bot.{node.attr}"


@pytest.mark.asyncio
async def test_conformance_requires_ok_status():
    conformance.results.clear()
    await conformance.check("missingStatus", lambda: _value({"data": {}}))
    await conformance.check("notOk", lambda: _value({"status": "INVALID_INPUT"}))
    assert [result[1] for result in conformance.results] == [
        conformance.FAIL,
        conformance.FAIL,
    ]


@pytest.mark.asyncio
async def test_file_probe_calls_get_file_not_get_chat_info():
    class FileBot:
        async def get_chat_info(self, chat):
            return {"status": "OK", "data": {"kind": "chat"}}

        async def get_file(self, file_id):
            return {"status": "OK", "data": {"download_url": f"offline:{file_id}"}}

    result = await conformance._probe_file(FileBot(), "file-42")
    assert result["data"]["download_url"] == "offline:file-42"


def test_file_discovery_requires_a_real_file_id():
    updates = {
        "data": {
            "updates": [
                {"message": {"message_id": "7", "file_inline": {"file_id": "file-42"}}}
            ]
        }
    }
    discover = getattr(conformance, "first_file_id", None)
    assert discover is not None
    assert discover(updates) == "file-42"
    assert discover({"data": {"updates": [{"message": {"message_id": "7"}}]}}) is None


async def _value(value):
    return value


@pytest.mark.asyncio
async def test_conformance_never_destroys_commands_or_proves_membership(monkeypatch):
    class FakeBot:
        def __init__(self, *args, **kwargs):
            self.command_calls = []
            self.other_calls = []

        async def get_me(self, refresh=False):
            return {"status": "OK", "data": {"user": {"user_guid": "b0fake"}}}

        async def get_updates(self, limit=1):
            return {"status": "OK", "data": {"updates": []}}

        async def send_message(self, chat, text):
            return {"status": "OK", "data": {"message_id": "1"}}

        async def request_send_file(self, file_type):
            return {"status": "OK", "data": {}}

        async def set_commands(self, commands):
            self.command_calls.append(commands)
            return {"status": "OK"}

        def __getattr__(self, name):
            async def call(*args, **kwargs):
                self.other_calls.append(name)
                return {"status": "OK"}

            return call

    fake = FakeBot()
    monkeypatch.setattr(darkob, "Bot", lambda *args, **kwargs: fake)
    conformance.results.clear()

    status = await conformance.main(
        ["--writes", "--token", VALID_TOKEN, "--chat", "g0" + "0" * 30]
    )

    assert status == 0
    assert fake.command_calls == []
    assert "ban_member" not in fake.other_calls
    assert "unban_member" not in fake.other_calls


def test_relative_documentation_links_resolve():
    missing = []
    for path in DOCS.rglob("*.md"):
        text = re.sub(r"```.*?```", "", path.read_text(encoding="utf-8"), flags=re.S)
        text = re.sub(r"`[^`\n]*`", "", text)
        for target in re.findall(r"(?<!!)\[[^\]]*\]\(([^)]+)\)", text):
            target = target.split()[0].strip("<>")
            if target.startswith(("https://", "http://", "mailto:", "#")):
                continue
            relative = target.split("#", 1)[0].split("?", 1)[0]
            if relative and not (path.parent / relative).resolve().exists():
                missing.append(f"{path.relative_to(ROOT)}: {target}")
    assert missing == []


def _contrast(first: str, second: str) -> float:
    def luminance(color: str) -> float:
        channels = [int(color[index : index + 2], 16) / 255 for index in (0, 2, 4)]
        channels = [
            value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4
            for value in channels
        ]
        return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2]

    high, low = sorted((luminance(first), luminance(second)), reverse=True)
    return (high + 0.05) / (low + 0.05)


def test_light_link_accent_has_normal_text_contrast_on_white():
    css = (DOCS / "stylesheets" / "extra.css").read_text(encoding="utf-8")
    root = re.search(r":root\s*\{(.*?)\}", css, re.S).group(1)
    accent = re.search(r"--md-accent-fg-color:\s*#([0-9a-fA-F]{6})", root).group(1)
    assert _contrast(accent, "ffffff") >= 4.5


def test_dark_homepage_subtitle_has_normal_text_contrast():
    css = (DOCS / "stylesheets" / "extra.css").read_text(encoding="utf-8")
    background = re.search(r"--md-default-bg-color:\s*#([0-9a-fA-F]{6})", css).group(1)
    rule = re.search(
        r'\[data-md-color-scheme="slate"\]\s+'
        r"\.md-typeset h1 \+ p > strong\s*\{[^}]*color:\s*#([0-9a-fA-F]{6})",
        css,
        re.S,
    )
    assert rule is not None
    assert _contrast(rule.group(1), background) >= 4.5


def test_persian_content_has_native_language_and_direction():
    text = (DOCS / "fa" / "quickstart.md").read_text(encoding="utf-8")
    opening = text.index("<div")
    heading = text.index("# راهنمای")
    assert opening < heading
    assert re.search(r'<div dir="rtl" lang="fa" markdown="1">', text)


def test_keyboard_chaining_example_is_valid_python():
    text = (DOCS / "guides" / "keyboards.md").read_text(encoding="utf-8")
    blocks = re.findall(r"```python[^\n]*\n(.*?)```", text, re.S)
    for block in blocks:
        ast.parse(block)
