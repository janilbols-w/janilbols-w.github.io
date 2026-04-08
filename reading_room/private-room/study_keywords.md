---
title: Study Keyword Analytics (Private)
permalink: /reading_room/private-room/study_keywords/
---

Keyword extraction and frequency statistics from file names under `/Volumes/home/study`.

## Method

- Scope A: all files (broad scan)
- Scope B: document-like files (`pdf`, `ppt`, `pptx`, `md`, `txt`, `doc`, `docx`, `drawio`, `xmind`, `ipynb`)
- Tokenization: lowercase, split by non-alphanumeric chars
- Filtering: remove numbers-only tokens and common stopwords/extensions

## High-Level Stats

| Metric | Value |
|---|---:|
| Unique keywords (all files) | 1230 |
| Unique keywords (document-like files) | 845 |
| Drawio files | 8 |
| PPT/PPTX/KEY files | 46 |
| XMind files | 14 |
| DOC/DOCX files | 6 |
| PDF files | 497 |


## Notes

- All-file results are influenced by large image asset sets.
- Document-like scope is more representative for study content themes.
