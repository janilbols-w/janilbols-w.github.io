# Janilbols's HOME PAGE

Personal page for recording study notes.
Join me to make it better if you like!

- [LLM ZONE](reading_room/artificial_intelligence/llm_large_language_models)

## Local preview

This repository is now set up as a Jekyll site for GitHub Pages.

```bash
bundle install
bundle exec jekyll serve
```

Open `http://127.0.0.1:4000` after the local server starts.

If your network cannot access `rubygems.org`, switch bundler to a mirror before `bundle install`:

```bash
bundle config mirror.https://rubygems.org https://mirrors.tuna.tsinghua.edu.cn/rubygems/
```

## Auto index template (write markdown only)

You can keep writing `.md` files only. This repo includes an auto-index template:

- Script: `scripts/generate_indexes.py`
- Workflow: `.github/workflows/auto-index.yml`
- Default scan roots: `garage`, `reading_room`

How it works:

- If a directory has markdown notes and no `index.md`, it will create one.
- If `index.md` contains AUTO-GENERATED markers, only that block is refreshed.
- Manual `index.md` without markers is kept as-is by default.

Run locally:

```bash
python scripts/generate_indexes.py --roots garage reading_room
```

Preview changes only:

```bash
python scripts/generate_indexes.py --roots garage reading_room --dry-run
```

Force overwrite manual index files (use carefully):

```bash
python scripts/generate_indexes.py --roots garage reading_room --force
```

## Deployment

This project includes GitHub Actions workflow for Pages deployment:

- Workflow file: `.github/workflows/pages.yml`
- Trigger: push to `master` or `main`
- Build: `actions/jekyll-build-pages`
- Deploy: `actions/deploy-pages`

After you push to GitHub, check the **Actions** tab and wait for **Build and Deploy Pages** to complete.

Auto index workflow:

- Workflow file: `.github/workflows/auto-index.yml`
- Trigger: markdown changes (`**/*.md`, except `**/index.md`)
- Action: generate missing/managed `index.md` pages and auto-commit changes
