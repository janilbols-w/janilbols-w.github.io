#!/usr/bin/env python3
"""
Auto-generate directory index.md pages for markdown notes.

Behavior:
- Create index.md when missing for directories that contain markdown files or note subdirectories.
- Update only files that include AUTO-GENERATED markers.
- Keep manual index.md files unchanged unless --force is provided.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


START_MARKER = "<!-- AUTO-GENERATED:START -->"
END_MARKER = "<!-- AUTO-GENERATED:END -->"
EXCLUDED_DIRS = {".git", ".github", "_site", "assets", "vendor", "node_modules"}


@dataclass
class DirEntry:
    abs_path: Path
    rel_posix: str


def title_from_name(name: str) -> str:
    return name.replace("_", " ").replace("-", " ").strip().title() or "Index"


def is_markdown_file(path: Path) -> bool:
    return path.is_file() and path.suffix.lower() == ".md"


def path_to_url(rel_path: Path, is_dir: bool) -> str:
    if is_dir:
        return f"/{rel_path.as_posix().strip('/')}/"
    # Jekyll pretty permalink style: file.md -> /file/
    no_suffix = rel_path.with_suffix("")
    return f"/{no_suffix.as_posix().strip('/')}/"


def has_note_content(dir_path: Path) -> bool:
    for child in dir_path.iterdir():
        if child.name.startswith("."):
            continue
        if child.is_dir() and child.name not in EXCLUDED_DIRS:
            # A child directory is considered note content if it has markdown files recursively.
            if any(is_markdown_file(p) for p in child.rglob("*.md")):
                return True
        if is_markdown_file(child) and child.name.lower() != "index.md":
            return True
    return False


def collect_child_dirs(base_dir: Path, root_dir: Path) -> list[DirEntry]:
    result: list[DirEntry] = []
    for child in sorted(base_dir.iterdir(), key=lambda p: p.name.lower()):
        if child.name.startswith(".") or not child.is_dir() or child.name in EXCLUDED_DIRS:
            continue
        if has_note_content(child):
            rel = child.relative_to(root_dir)
            result.append(DirEntry(abs_path=child, rel_posix=rel.as_posix()))
    return result


def collect_markdown_files(base_dir: Path, root_dir: Path) -> list[DirEntry]:
    result: list[DirEntry] = []
    for child in sorted(base_dir.iterdir(), key=lambda p: p.name.lower()):
        if child.name.startswith("."):
            continue
        if not is_markdown_file(child):
            continue
        if child.name.lower() == "index.md":
            continue
        rel = child.relative_to(root_dir)
        result.append(DirEntry(abs_path=child, rel_posix=rel.as_posix()))
    return result


def render_auto_block(current_dir: Path, root_dir: Path) -> str:
    child_dirs = collect_child_dirs(current_dir, root_dir)
    md_files = collect_markdown_files(current_dir, root_dir)

    lines: list[str] = [START_MARKER, ""]

    if child_dirs:
        lines.append("## Sections")
        lines.append("")
        for entry in child_dirs:
            name = title_from_name(entry.abs_path.name)
            url = path_to_url(Path(entry.rel_posix), is_dir=True)
            lines.append(f"- [{name}]({{{{ '{url}' | relative_url }}}})")
        lines.append("")

    if md_files:
        lines.append("## Pages")
        lines.append("")
        for entry in md_files:
            name = title_from_name(entry.abs_path.stem)
            url = path_to_url(Path(entry.rel_posix), is_dir=False)
            lines.append(f"- [{name}]({{{{ '{url}' | relative_url }}}})")
        lines.append("")

    if not child_dirs and not md_files:
        lines.append("No markdown notes found in this directory yet.")
        lines.append("")

    lines.append(END_MARKER)
    lines.append("")
    return "\n".join(lines)


def create_new_index(current_dir: Path, root_dir: Path) -> str:
    rel = current_dir.relative_to(root_dir)
    title = title_from_name(current_dir.name) if rel.as_posix() != "." else "Home"
    preface = (
        "This page is generated automatically. "
        "Keep writing markdown files, then run the generator workflow."
    )
    return (
        f"---\n"
        f"title: {title}\n"
        f"---\n\n"
        f"{preface}\n\n"
        f"{render_auto_block(current_dir, root_dir)}"
    )


def update_existing_index(existing: str, auto_block: str) -> str:
    start = existing.find(START_MARKER)
    end = existing.find(END_MARKER)
    if start == -1 or end == -1 or end < start:
        return existing
    end += len(END_MARKER)
    return f"{existing[:start]}{auto_block}{existing[end:]}"


def iter_target_dirs(roots: Iterable[Path]) -> Iterable[Path]:
    for root in roots:
        if not root.exists() or not root.is_dir():
            continue
        yield root
        for path in sorted(root.rglob("*")):
            if not path.is_dir():
                continue
            if any(part.startswith(".") for part in path.parts):
                continue
            if any(part in EXCLUDED_DIRS for part in path.parts):
                continue
            yield path


def process_dir(current_dir: Path, root_dir: Path, force: bool, dry_run: bool) -> tuple[bool, str]:
    index_path = current_dir / "index.md"

    # Only create/update index for directories that have useful note content.
    if not has_note_content(current_dir):
        return False, f"skip: {index_path.relative_to(root_dir)} (no note content)"

    if not index_path.exists():
        content = create_new_index(current_dir, root_dir)
        if not dry_run:
            index_path.write_text(content, encoding="utf-8")
        return True, f"create: {index_path.relative_to(root_dir)}"

    existing = index_path.read_text(encoding="utf-8")
    auto_block = render_auto_block(current_dir, root_dir)

    if START_MARKER in existing and END_MARKER in existing:
        updated = update_existing_index(existing, auto_block)
        if updated != existing:
            if not dry_run:
                index_path.write_text(updated, encoding="utf-8")
            return True, f"update: {index_path.relative_to(root_dir)}"
        return False, f"keep: {index_path.relative_to(root_dir)} (already up to date)"

    if force:
        updated = create_new_index(current_dir, root_dir)
        if not dry_run:
            index_path.write_text(updated, encoding="utf-8")
        return True, f"overwrite: {index_path.relative_to(root_dir)}"

    return False, f"skip: {index_path.relative_to(root_dir)} (manual file without markers)"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate index.md pages for markdown directories.")
    parser.add_argument(
        "--roots",
        nargs="+",
        default=["garage", "reading_room"],
        help="Root directories to scan.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Show planned changes only.")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite manual index.md files that do not contain markers.",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    roots = [repo_root / r for r in args.roots]

    changed = 0
    for target_dir in iter_target_dirs(roots):
        did_change, message = process_dir(target_dir, repo_root, args.force, args.dry_run)
        print(message)
        if did_change:
            changed += 1

    mode = "dry-run" if args.dry_run else "write"
    print(f"done: mode={mode}, changed={changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
