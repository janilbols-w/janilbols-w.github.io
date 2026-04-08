#!/usr/bin/env python3
"""Generate projects/index.md from janilbols-w public GitHub activity."""

from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib import error, request


OWNER = "janilbols-w"
MAX_REPOS = 80
MAX_EVENTS = 100


def log(message: str) -> None:
    now = datetime.now().strftime("%H:%M:%S")
    print(f"[projects {now}] {message}", flush=True)


def api_get_json(url: str, token: str | None = None) -> Any:
    req = request.Request(url)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "janilbols-w-project-tracker")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def safe_iso_to_ymd(iso_time: str | None) -> str:
    if not iso_time:
        return "-"
    return iso_time[:10]


def summarize_event(event: dict[str, Any]) -> str:
    etype = event.get("type", "Event")
    payload = event.get("payload", {}) if isinstance(event.get("payload"), dict) else {}
    if etype == "PushEvent":
        commits = payload.get("size", 0)
        ref = payload.get("ref", "")
        branch = ref.split("/")[-1] if ref else "-"
        return f"Push ({commits} commits) to {branch}"
    if etype == "PullRequestEvent":
        action = payload.get("action", "updated")
        return f"PR {action}"
    if etype == "IssuesEvent":
        action = payload.get("action", "updated")
        return f"Issue {action}"
    if etype == "ReleaseEvent":
        action = payload.get("action", "published")
        return f"Release {action}"
    if etype == "CreateEvent":
        ref_type = payload.get("ref_type", "resource")
        return f"Create {ref_type}"
    return etype.replace("Event", "")


def build_projects_page(repos: list[dict[str, Any]], repo_events: dict[str, dict[str, str]]) -> str:
    lines: list[str] = [
        "---",
        "title: GitHub Projects Tracker",
        "permalink: /projects/",
        "---",
        "",
        f"Auto-tracked updates for [github.com/{OWNER}](https://github.com/{OWNER}).",
        "",
        "## Snapshot",
        "",
        f"- Total repositories tracked: {len(repos)}",
        "- Source: GitHub public API (repositories + public events)",
        "- Refresh: scheduled by GitHub Actions",
        "",
        "## Repositories (Sorted by Recent Push)",
        "",
        "| Repository | Description | Language | Stars | Forks | Last Push | Last Activity |",
        "|---|---|---|---:|---:|---|---|",
    ]

    for repo in repos:
        name = repo.get("name", "-")
        full_name = repo.get("full_name", name)
        html_url = repo.get("html_url", "")
        desc = (repo.get("description") or "-").replace("|", "\\|").replace("\n", " ").strip()
        if len(desc) > 100:
            desc = desc[:97] + "..."
        lang = repo.get("language") or "-"
        stars = repo.get("stargazers_count", 0)
        forks = repo.get("forks_count", 0)
        pushed = safe_iso_to_ymd(repo.get("pushed_at"))

        event_info = repo_events.get(full_name, {})
        event_date = event_info.get("date", "-")
        event_text = event_info.get("text", "-")
        activity = f"{event_date}: {event_text}" if event_date != "-" else "-"
        activity = activity.replace("|", "\\|")

        lines.append(
            f"| [{name}]({html_url}) | {desc} | {lang} | {stars} | {forks} | {pushed} | {activity} |"
        )

    lines.extend(
        [
            "",
            "## Notes",
            "",
            "- This page is generated automatically; avoid manual edits.",
            "- The page updates only when repository/event data changes, reducing noisy commits.",
            "- For private repositories, GitHub API may not expose details without token-based auth.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    output_path = repo_root / "projects" / "index.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    token = os.getenv("GITHUB_TOKEN")
    repos_url = f"https://api.github.com/users/{OWNER}/repos?per_page={MAX_REPOS}&sort=pushed&direction=desc"
    events_url = f"https://api.github.com/users/{OWNER}/events/public?per_page={MAX_EVENTS}"

    try:
        log("Fetching repositories...")
        repos = api_get_json(repos_url, token=token)
        if not isinstance(repos, list):
            raise RuntimeError("Unexpected repos response")

        log("Fetching public events...")
        events = api_get_json(events_url, token=token)
        if not isinstance(events, list):
            events = []
    except error.HTTPError as exc:
        log(f"GitHub API HTTP error: {exc.code}")
        raise
    except error.URLError as exc:
        log(f"GitHub API network error: {exc}")
        raise

    repo_events: dict[str, dict[str, str]] = {}
    for event in events:
        repo = event.get("repo", {}) if isinstance(event, dict) else {}
        full_name = repo.get("name")
        if not full_name or full_name in repo_events:
            continue
        repo_events[full_name] = {
            "date": safe_iso_to_ymd(event.get("created_at")),
            "text": summarize_event(event),
        }

    content = build_projects_page(repos, repo_events)
    output_path.write_text(content, encoding="utf-8")
    log(f"Wrote projects tracker page to {output_path.relative_to(repo_root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
