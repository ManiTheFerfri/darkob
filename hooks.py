"""MkDocs build hooks.

Serves the raw Markdown source of every page alongside its rendered HTML,
so an AI assistant can fetch a clean, navigation-free version of any page
by appending ``.md`` to the URL.
"""

from __future__ import annotations

import shutil
from pathlib import Path


def on_post_build(config, **kwargs) -> None:
    docs_dir = Path(config["docs_dir"])
    site_dir = Path(config["site_dir"])

    copied = 0
    for source in docs_dir.rglob("*.md"):
        relative = source.relative_to(docs_dir)
        destination = site_dir / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        copied += 1

    print(f"[hooks] exposed {copied} raw Markdown pages")
