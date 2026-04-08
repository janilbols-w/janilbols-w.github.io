---
title: Global Navigator
---

<section class="hero-card nav-hero">
  <p class="page-kicker">Site Jump Hub</p>
  <h2>全局跳转导航</h2>
  <p>输入关键词快速筛选页面，或直接从分区入口跳转到目标内容。</p>

  <label class="nav-search-label" for="nav-search">搜索页面</label>
  <input id="nav-search" class="nav-search" type="search" placeholder="例如: deepseek / inference / kubernetes / survey" autocomplete="off">
</section>

<section class="section-card nav-section" data-nav-group="core">
  <h3>Core Entry</h3>
  <div class="nav-link-grid">
    <a class="nav-link-card" data-nav-title="home" href="{{ '/' | relative_url }}">Home</a>
    <a class="nav-link-card" data-nav-title="garage" href="{{ '/garage/' | relative_url }}">Garage</a>
    <a class="nav-link-card" data-nav-title="reading room" href="{{ '/reading_room/' | relative_url }}">Reading Room</a>
    <a class="nav-link-card" data-nav-title="llm zone" href="{{ '/reading_room/artificial_intelligence/llm_large_language_models/' | relative_url }}">LLM Zone</a>
  </div>
</section>

<section class="section-card nav-section" data-nav-group="garage">
  <h3>Garage</h3>
  <div class="nav-link-grid">
    <a class="nav-link-card" data-nav-title="kubernetes" href="{{ '/garage/kubernetes/' | relative_url }}">Kubernetes</a>
    <a class="nav-link-card" data-nav-title="latex usage" href="{{ '/garage/latex-usage/' | relative_url }}">LaTeX Usage</a>
  </div>
</section>

<section class="section-card nav-section" data-nav-group="llm-projects">
  <h3>LLM Projects</h3>
  <div class="nav-link-grid">
    <a class="nav-link-card" data-nav-title="llm projects" href="{{ '/reading_room/artificial_intelligence/llm_large_language_models/llm_projects/' | relative_url }}">LLM Projects</a>
    <a class="nav-link-card" data-nav-title="inference frameworks" href="{{ '/reading_room/artificial_intelligence/llm_large_language_models/llm_projects/inference-frameworks/' | relative_url }}">Inference Frameworks</a>
    <a class="nav-link-card" data-nav-title="deepseek v3 architecture" href="{{ '/reading_room/artificial_intelligence/llm_large_language_models/llm_projects/inference-frameworks/Deepseek-v3/' | relative_url }}">DeepSeek V3 Arch</a>
    <a class="nav-link-card" data-nav-title="vllm" href="{{ '/reading_room/artificial_intelligence/llm_large_language_models/llm_projects/inference-frameworks/vllm/' | relative_url }}">vLLM</a>
    <a class="nav-link-card" data-nav-title="continuous batching" href="{{ '/reading_room/artificial_intelligence/llm_large_language_models/llm_projects/inference-frameworks/vllm/continuous-batching/' | relative_url }}">Continuous Batching</a>
  </div>
</section>

<section class="section-card nav-section" data-nav-group="llm-readings">
  <h3>LLM Readings</h3>
  <div class="nav-link-grid">
    <a class="nav-link-card" data-nav-title="llm readings" href="{{ '/reading_room/artificial_intelligence/llm_large_language_models/llm_readings/' | relative_url }}">LLM Readings</a>
    <a class="nav-link-card" data-nav-title="inference" href="{{ '/reading_room/artificial_intelligence/llm_large_language_models/llm_readings/inference/' | relative_url }}">Inference</a>
    <a class="nav-link-card" data-nav-title="model" href="{{ '/reading_room/artificial_intelligence/llm_large_language_models/llm_readings/model/' | relative_url }}">Model</a>
    <a class="nav-link-card" data-nav-title="deepseek papers" href="{{ '/reading_room/artificial_intelligence/llm_large_language_models/llm_readings/model/deepseek-paper/' | relative_url }}">DeepSeek Paper</a>
    <a class="nav-link-card" data-nav-title="survey" href="{{ '/reading_room/artificial_intelligence/llm_large_language_models/llm_readings/survey/' | relative_url }}">Survey</a>
    <a class="nav-link-card" data-nav-title="ai agent" href="{{ '/reading_room/artificial_intelligence/llm_large_language_models/llm_readings/survey/ai_agent/' | relative_url }}">AI Agent</a>
    <a class="nav-link-card" data-nav-title="train" href="{{ '/reading_room/artificial_intelligence/llm_large_language_models/llm_readings/train/' | relative_url }}">Train</a>
    <a class="nav-link-card" data-nav-title="test time scaling" href="{{ '/reading_room/artificial_intelligence/llm_large_language_models/llm_readings/train/test-time scaling/' | relative_url }}">Test-Time Scaling</a>
  </div>
</section>

<p class="nav-empty" data-nav-empty hidden>没有匹配结果，请尝试其他关键词。</p>

<script>
  (() => {
    const searchInput = document.getElementById('nav-search');
    const navSections = Array.from(document.querySelectorAll('.nav-section'));
    const navLinks = Array.from(document.querySelectorAll('.nav-link-card'));
    const emptyState = document.querySelector('[data-nav-empty]');

    if (!searchInput || navSections.length === 0 || navLinks.length === 0) {
      return;
    }

    const applyFilter = () => {
      const keyword = searchInput.value.trim().toLowerCase();
      let visibleCount = 0;

      navLinks.forEach((link) => {
        const haystack = `${link.textContent || ''} ${link.getAttribute('data-nav-title') || ''}`.toLowerCase();
        const matched = !keyword || haystack.includes(keyword);
        link.hidden = !matched;
        if (matched) visibleCount += 1;
      });

      navSections.forEach((section) => {
        const hasVisibleLink = Array.from(section.querySelectorAll('.nav-link-card')).some((link) => !link.hidden);
        section.hidden = !hasVisibleLink;
      });

      if (emptyState) {
        emptyState.hidden = visibleCount > 0;
      }
    };

    searchInput.addEventListener('input', applyFilter);
  })();
</script>