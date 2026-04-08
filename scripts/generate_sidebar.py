#!/usr/bin/env python3
"""Auto-generate the sidebar navigator tree HTML in _layouts/default.html.

Scans garage/ and reading_room/ directories, builds nested <details>/<summary>
HTML, and writes it between <!-- SIDEBAR-TREE:START --> / <!-- SIDEBAR-TREE:END -->
markers in the layout file.
"""

from __future__ import annotations

import argparse
from pathlib import Path


START = "<!-- SIDEBAR-TREE:START -->"
END = "<!-- SIDEBAR-TREE:END -->"

EXCLUDED_DIRS = {".git", ".github", "_site", "assets", "vendor", "node_modules", "temp"}
IMAGE_DIRS = {"image", "images"}

TOKEN_MAP = {
    "ai": "AI",
    "llm": "LLM",
    "latex": "LaTeX",
    "readme": "README",
    "api": "API",
    "gpu": "GPU",
    "kvcache": "KVCache",
    "vllm": "vLLM",
    "deepseek": "DeepSeek",
}


def title_from_name(name: str) -> str:
    normalized = name.replace("_", " ").replace("-", " ").strip()
    words = [TOKEN_MAP.get(t.lower(), t.title()) for t in normalized.split()]
    return " ".join(words) or "Index"


def is_md(p: Path) -> bool:
    return p.is_file() and p.suffix.lower() == ".md"


def is_drawio(p: Path) -> bool:
    return p.is_file() and p.suffix.lower() == ".drawio"


def has_note_content(d: Path) -> bool:
    """True if the directory contains note content (md/drawio) recursively."""
    for child in d.iterdir():
        if child.name.startswith("."):
            continue
        if child.is_dir() and child.name not in EXCLUDED_DIRS and child.name not in IMAGE_DIRS:
            if any(is_md(p) or is_drawio(p) for p in child.rglob("*")):
                return True
        if is_md(child) and child.name.lower() != "index.md":
            return True
        if is_drawio(child):
            return True
    return False


def interesting_child_dirs(d: Path) -> list[Path]:
    result = []
    for child in sorted(d.iterdir(), key=lambda p: p.name.lower()):
        if not child.is_dir():
            continue
        if child.name.startswith(".") or child.name in EXCLUDED_DIRS or child.name in IMAGE_DIRS:
            continue
        if has_note_content(child):
            result.append(child)
    return result


def child_md_files(d: Path) -> list[Path]:
    """Non-index, non-README markdown files directly in d."""
    result = []
    for child in sorted(d.iterdir(), key=lambda p: p.name.lower()):
        if is_md(child) and child.name.lower() not in ("index.md", "readme.md"):
            result.append(child)
    return result


def liq(url: str) -> str:
    """Wrap a URL in Jekyll's relative_url Liquid filter."""
    return "{{ '" + url + "' | relative_url }}"


def render_node(d: Path, repo_root: Path, depth: int) -> list[str]:
    """Render one directory as sidebar HTML lines."""
    pad = " " * (10 + depth * 4)    # <details> indent
    inner = " " * (10 + depth * 4 + 2)  # <summary>/<div> indent
    cont = " " * (10 + depth * 4 + 4)   # children indent

    rel = d.relative_to(repo_root)
    url = f"/{rel.as_posix()}/"
    title = title_from_name(d.name)

    dirs = interesting_child_dirs(d)
    files = child_md_files(d)

    # Leaf directory: no children to show, just a link
    if not dirs and not files:
        return [f'{pad}<a href="{liq(url)}">{title}</a>']

    css = "tree-group" if depth == 0 else "tree-group tree-group-sub"
    lines: list[str] = []
    lines.append(f'{pad}<details class="{css}">')
    lines.append(f'{inner}<summary>{title}</summary>')
    lines.append(f'{inner}<div class="tree-children">')
    lines.append(f'{cont}<a href="{liq(url)}">Overview</a>')

    for sub in dirs:
        lines.append("")
        lines.extend(render_node(sub, repo_root, depth + 1))

    for md in files:
        md_rel = md.relative_to(repo_root)
        md_url = f"/{md_rel.with_suffix('').as_posix()}"
        lines.append(f'{cont}<a href="{liq(md_url)}">{title_from_name(md.stem)}</a>')

    lines.append(f'{inner}</div>')
    lines.append(f'{pad}</details>')
    return lines


def generate_tree_html(roots: list[Path], repo_root: Path) -> str:
    """Build the full replacement block including markers."""
    BASE = " " * 10
    lines: list[str] = [START]
    for root in roots:
        if not root.exists():
            continue
        lines.append("")
        lines.extend(render_node(root, repo_root, depth=0))
    lines.append("")
    lines.append(BASE + END)
    return "\n".join(lines)


def update_layout(layout_path: Path, new_html: str, dry_run: bool) -> bool:
    content = layout_path.read_text(encoding="utf-8")
    start_idx = content.find(START)
    end_idx = content.find(END)

    if start_idx == -1 or end_idx == -1:
        print(f"[sidebar] Markers not found in {layout_path.name}. "
              "Add <!-- SIDEBAR-TREE:START --> and <!-- SIDEBAR-TREE:END --> to the file first.")
        return False

    end_idx += len(END)
    updated = content[:start_idx] + new_html + content[end_idx:]

    if updated == content:
        print(f"[sidebar] {layout_path.name}: already up to date.")
        return False

    if not dry_run:
        layout_path.write_text(updated, encoding="utf-8")

    verb = "Would update" if dry_run else "Updated"
    print(f"[sidebar] {verb} {layout_path.name}")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate sidebar tree HTML in _layouts/default.html"
    )
    parser.add_argument("--roots", nargs="+", default=["garage", "reading_room"])
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    roots = [repo_root / r for r in args.roots]
    layout_path = repo_root / "_layouts" / "default.html"

    html = generate_tree_html(roots, repo_root)
    update_layout(layout_path, html, args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
