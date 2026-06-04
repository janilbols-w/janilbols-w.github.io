---
title: Home
body_class: home-page
hide_page_heading: true
---

<section class="home-hero">
  <p class="home-kicker">Janilbols Notes</p>
  <h1>工程笔记、项目复盘和长期学习档案</h1>
  <p class="home-hero-copy">记录面向实战的技术知识：从 Kubernetes 运维到 LLM 推理系统，再到持续维护的项目索引。这里不是博客流水账，而是一份可检索、可复用、可长期迭代的个人知识库。</p>
  <div class="home-chip-row" aria-label="Homepage highlights">
    <span class="home-chip">AI Infra</span>
    <span class="home-chip">Kubernetes</span>
    <span class="home-chip">LLM Serving</span>
    <span class="home-chip">Project Tracking</span>
    <span class="home-chip">Knowledge Base</span>
  </div>
  <div class="home-hero-actions">
    <a class="home-btn home-btn-primary" href="{{ '/navigator/' | relative_url }}">进入全站导航</a>
    <a class="home-btn home-btn-ghost" href="{{ '/projects/' | relative_url }}">查看项目动态</a>
  </div>
</section>

<section class="home-feature-grid" aria-label="Home sections">
  <article class="home-feature-card">
    <p class="home-card-kicker">01</p>
    <h2><a href="{{ '/garage/' | relative_url }}">Garage</a></h2>
    <p>日常高频使用的实战资料：命令速查、调试路径、部署清单和问题定位笔记。</p>
    <ul>
      <li><a href="{{ '/garage/kubernetes/' | relative_url }}">Kubernetes</a></li>
      <li><a href="{{ '/garage/latex-usage/' | relative_url }}">LaTeX usage</a></li>
      <li><a href="{{ '/garage/llm-selfhost/' | relative_url }}">LLM Selfhost</a></li>
    </ul>
  </article>

  <article class="home-feature-card">
    <p class="home-card-kicker">02</p>
    <h2><a href="{{ '/reading_room/' | relative_url }}">Reading Room</a></h2>
    <p>面向中长期积累的深度学习记录，聚焦推理框架、模型工程、论文与产业趋势。</p>
    <ul>
      <li><a href="{{ '/reading_room/artificial_intelligence/llm_large_language_models/' | relative_url }}">LLM Zone</a></li>
      <li><a href="{{ '/reading_room/artificial_intelligence/llm_large_language_models/llm_projects/' | relative_url }}">LLM Projects</a></li>
      <li><a href="{{ '/reading_room/artificial_intelligence/llm_large_language_models/llm_readings/' | relative_url }}">LLM Readings</a></li>
    </ul>
  </article>

  <article class="home-feature-card">
    <p class="home-card-kicker">03</p>
    <h2><a href="{{ '/projects/' | relative_url }}">Projects</a></h2>
    <p>自动追踪 <code>github.com/janilbols-w</code> 公开仓库更新，聚合最近推送和活动轨迹。</p>
    <ul>
      <li><a href="{{ '/projects/' | relative_url }}">GitHub Projects Tracker</a></li>
      <li>最近 Push 时间与活跃事件摘要</li>
      <li>定时刷新，保持近实时可见</li>
    </ul>
  </article>
</section>

<section class="home-links-block">
  <h2>Quick Entry</h2>
  <div class="home-links-grid">
    <a href="{{ '/navigator/' | relative_url }}">Global Navigator</a>
    <a href="{{ '/projects/' | relative_url }}">Projects Tracker</a>
    <a href="{{ '/garage/kubernetes/overview/' | relative_url }}">Kubernetes 概念概览</a>
    <a href="{{ '/garage/kubernetes/quickstart/' | relative_url }}">Kubernetes 终端交互常用命令</a>
    <a href="{{ '/garage/latex-usage/' | relative_url }}">LaTeX Usage</a>
    <a href="{{ '/reading_room/artificial_intelligence/llm_large_language_models/' | relative_url }}">LLM Zone</a>
    <a href="{{ '/reading_room/artificial_intelligence/llm_large_language_models/llm_projects/' | relative_url }}">LLM Projects</a>
    <a href="{{ '/reading_room/artificial_intelligence/llm_large_language_models/llm_readings/' | relative_url }}">LLM Readings</a>
  </div>
</section>
