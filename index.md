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
    <h2><a href="{{ '/projects/' | relative_url }}">Projects</a></h2>
    <p>Auto-tracked updates for repositories under <code>github.com/janilbols-w</code>, including recent push activity and event summary.</p>
    <ul>
      <li><a href="{{ '/projects/' | relative_url }}">GitHub Projects Tracker</a></li>
      <li>Last push date and latest public activity per repository</li>
      <li>Scheduled refresh every 6 hours</li>
    </ul>
  </section>

  <section class="section-card">
    <h2><a href="{{ '/garage/' | relative_url }}">Garage</a></h2>
    <p>Hands-on notes, operational guides, and quick references for topics that are directly used in daily work.</p>
    <ul>
      <li><a href="{{ '/garage/kubernetes/' | relative_url }}">Kubernetes</a></li>
      <li><a href="{{ '/garage/latex-usage/' | relative_url }}">LaTeX usage</a></li>
      <li>Interview notes</li>
    </ul>
  </section>

  <section class="section-card">
    <h2><a href="{{ '/reading_room/' | relative_url }}">Reading Room</a></h2>
    <p>Longer study notes focused on large language models, inference systems, papers, and implementation details.</p>
    <ul>
      <li><a href="{{ '/reading_room/artificial_intelligence/' | relative_url }}">Artificial Intelligence</a></li>
      <li><a href="{{ '/reading_room/artificial_intelligence/llm_large_language_models/' | relative_url }}">LLM Zone</a></li>
      <li><a href="{{ '/reading_room/artificial_intelligence/llm_large_language_models/llm_projects/' | relative_url }}">LLM Projects</a></li>
      <li><a href="{{ '/reading_room/artificial_intelligence/llm_large_language_models/llm_readings/' | relative_url }}">LLM Readings</a></li>
    </ul>
  </section>
</div>

## Quick Entry

- [Global Navigator]({{ '/navigator/' | relative_url }})
- [Projects Tracker]({{ '/projects/' | relative_url }})
- [Kubernetes 概念概览]({{ '/garage/kubernetes/overview/' | relative_url }})
- [Kubernetes 终端交互常用命令]({{ '/garage/kubernetes/quickstart/' | relative_url }})
- [LaTeX Usage]({{ '/garage/latex-usage/' | relative_url }})
- [LLM Zone]({{ '/reading_room/artificial_intelligence/llm_large_language_models/' | relative_url }})
- [LLM Projects]({{ '/reading_room/artificial_intelligence/llm_large_language_models/llm_projects/' | relative_url }})
- [LLM Readings]({{ '/reading_room/artificial_intelligence/llm_large_language_models/llm_readings/' | relative_url }})
