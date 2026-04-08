#!/usr/bin/env python3
"""Generate Jekyll page source dates from git commit metadata.

The output is written to _data/page_dates.json and keyed by repository-relative
page paths such as "reading_room/index.md".
"""

from __future__ import annotations

import json
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path


EXCLUDED_PARTS = {".git", ".github", "_site", "assets", "vendor", "node_modules"}
ROOTS = ("garage", "reading_room", "cv", "navigator.md", "index.md")
PROGRESS_EVERY = 10
COMMIT_MARKER = "__COMMIT__"


def log(message: str) -> None:
    now = datetime.now().strftime("%H:%M:%S")
    print(f"[page-dates {now}] {message}", flush=True)


def run_git(args: list[str], repo_root: Path) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def collect_git_dates(repo_root: Path, target_paths: set[str]) -> tuple[dict[str, str], dict[str, str]]:
    """Collect created/updated dates for many files with a single git log call.

    - updated: the first (newest) commit date touching the file.
    - created: the last (oldest) commit date touching the file.
    """
    if not target_paths:
        return {}, {}

    scope_args = list(ROOTS)
    output = run_git(
        [
            "log",
            "--date=short",
            "--name-only",
            f"--pretty=format:{COMMIT_MARKER}%ad",
            "--",
            *scope_args,
        ],
        repo_root,
    )

    if not output:
        return {}, {}

    created: dict[str, str] = {}
    updated: dict[str, str] = {}
    current_date = ""

    for raw_line in output.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        if line.startswith(COMMIT_MARKER):
            current_date = line[len(COMMIT_MARKER):].strip()
            continue

        if not current_date:
            continue

        if line not in target_paths:
            continue

        if line not in updated:
            updated[line] = current_date
        created[line] = current_date

    return created, updated


def discover_markdown_pages(repo_root: Path) -> list[Path]:
    paths: list[Path] = []
    for root in ROOTS:
        target = repo_root / root
        if not target.exists():
            continue
        if target.is_file() and target.suffix.lower() == ".md":
            if target.name.lower() == "index.md":
                continue
            paths.append(target)
            continue
        if target.is_dir():
            for path in sorted(target.rglob("*.md")):
                if any(part.startswith(".") for part in path.parts):
                    continue
                if any(part in EXCLUDED_PARTS for part in path.parts):
                    continue
                if path.name.lower() == "index.md":
                    continue
                paths.append(path)
    return paths


def filesystem_date(path: Path, attr: str) -> str:
    stat = path.stat()
    timestamp = getattr(stat, attr, None)
    if timestamp is None:
        timestamp = stat.st_mtime
    return datetime.fromtimestamp(timestamp, tz=timezone.utc).date().isoformat()


def build_mapping(repo_root: Path) -> dict[str, dict[str, str]]:
    payload: dict[str, dict[str, str]] = {}
    pages = discover_markdown_pages(repo_root)
    total = len(pages)
    rel_paths = [path.relative_to(repo_root).as_posix() for path in pages]

    log(f"Discovered {total} markdown pages. Start collecting git dates...")
    git_started = time.perf_counter()
    created_map, updated_map = collect_git_dates(repo_root, set(rel_paths))
    git_elapsed = time.perf_counter() - git_started
    log(
        "Collected git history for "
        f"{len(created_map)} tracked files in {git_elapsed:.2f}s using one batched git log call"
    )

    for idx, path in enumerate(pages, start=1):
        rel_path = path.relative_to(repo_root).as_posix()
        created = created_map.get(rel_path, "")
        updated = updated_map.get(rel_path, "")

        # Fallback for untracked/new files.
        if not created:
            created = filesystem_date(path, "st_birthtime")
        if not updated:
            updated = filesystem_date(path, "st_mtime")

        payload[rel_path] = {
            "created": created,
            "updated": updated,
        }

        if idx == 1 or idx % PROGRESS_EVERY == 0 or idx == total:
            log(f"Progress {idx}/{total}: {rel_path}")

    return payload


def main() -> int:
    started = time.perf_counter()
    repo_root = Path(__file__).resolve().parents[1]
    output_path = repo_root / "_data" / "page_dates.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    log("Generator started")
    payload = build_mapping(repo_root)
    output_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    elapsed = time.perf_counter() - started
    log(f"Wrote {len(payload)} page source dates to {output_path.relative_to(repo_root)} in {elapsed:.2f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())