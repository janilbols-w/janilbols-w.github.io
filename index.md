---
title: Home
---

<section class="hero-card">
  <p class="page-kicker">Personal Knowledge Base</p>
  <h1>Notes, quickstarts, and reading records</h1>
  <p>This site is built with Jekyll for GitHub Pages and organizes engineering notes into two streams: practical hands-on material in Garage, and longer-form study records in Reading Room.</p>
</section>

<div class="section-grid">
  <section class="section-card">
    <h2><a href="{{ '/garage/' | relative_url }}">Garage</a></h2>
    <p>Hands-on notes, operational guides, and quick references for topics that are directly used in daily work.</p>
    <ul>
      <li><a href="{{ '/garage/kubernetes/' | relative_url }}">Kubernetes</a></li>
      <li><a href="{{ '/garage/latex-usage/quickstart_latex_on_win/' | relative_url }}">LaTeX usage</a></li>
      <li>Interview notes</li>
    </ul>
  </section>

  <section class="section-card">
    <h2><a href="{{ '/reading_room/' | relative_url }}">Reading Room</a></h2>
    <p>Longer study notes focused on large language models, inference systems, papers, and implementation details.</p>
    <ul>
      <li><a href="{{ '/reading_room/artificial_intelligence/llm_large_language_models/' | relative_url }}">LLM Zone</a></li>
      <li>Papers, surveys, and project notes</li>
    </ul>
  </section>
</div>

## Quick Entry

- [Kubernetes 概念概览]({{ '/garage/kubernetes/overview/' | relative_url }})
- [Kubernetes 终端交互常用命令]({{ '/garage/kubernetes/quickstart/' | relative_url }})
- [LLM Zone]({{ '/reading_room/artificial_intelligence/llm_large_language_models/' | relative_url }})
