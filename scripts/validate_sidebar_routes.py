#!/usr/bin/env python3
"""Validate sidebar/page route uniqueness before commit.

Checks for URL collisions across markdown/html pages under configured roots,
using the same URL resolution rule as sidebar generation:
1) front matter permalink if present
2) otherwise pretty URL from file path without extension

A collision means two different files resolve to the same URL.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

EXCLUDED_DIRS = {".git", ".github", "_site", "assets", "vendor", "node_modules", "temp"}


def is_page(p: Path) -> bool:
    return p.is_file() and p.suffix.lower() in {".md", ".html"}


def should_skip_path(p: Path) -> bool:
    for part in p.parts:
        if part in EXCLUDED_DIRS or part.startswith("."):
            return True
    return False


def front_matter_permalink(page: Path) -> str | None:
    try:
        text = page.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None

    if not text.startswith("---\n"):
        return None

    end = text.find("\n---", 4)
    if end == -1:
        return None

    head = text[4:end]
    m = re.search(r"(?mi)^permalink:\s*(.+?)\s*$", head)
    if not m:
        return None

    value = m.group(1).strip().strip('"\'')
    if not value:
        return None
    if not value.startswith("/"):
        value = "/" + value
    return value


def page_url(page: Path, repo_root: Path) -> str:
    fm = front_matter_permalink(page)
    if fm:
        return fm
    rel = page.relative_to(repo_root)
    return f"/{rel.with_suffix('').as_posix()}"


def iter_pages(root: Path) -> list[Path]:
    pages: list[Path] = []
    for p in root.rglob("*"):
        if not is_page(p):
            continue
        if should_skip_path(p.relative_to(root)):
            continue
        name = p.name.lower()
        if name in {"index.md", "index.html", "readme.md", "readme.html"}:
            continue
        pages.append(p)
    return pages


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate page route uniqueness")
    parser.add_argument("--roots", nargs="+", default=["garage", "reading_room", "projects"])
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]

    all_pages: list[Path] = []
    for root_name in args.roots:
        root = repo_root / root_name
        if root.exists():
            all_pages.extend(iter_pages(root))

    by_url: dict[str, list[Path]] = {}
    for p in all_pages:
        u = page_url(p, repo_root)
        by_url.setdefault(u, []).append(p)

    collisions = {u: ps for u, ps in by_url.items() if len(ps) > 1}
    if not collisions:
        print("[route-check] OK: no page URL collisions detected.")
        return 0

    print("[route-check] ERROR: page URL collisions detected:")
    for url, paths in sorted(collisions.items()):
        print(f"  - {url}")
        for p in sorted(paths):
            print(f"      * {p.relative_to(repo_root).as_posix()}")

    print("[route-check] Fix by renaming files or setting unique permalink values.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
