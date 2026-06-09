---
title: Qwen3.5-397B-A17B Interactive Recipe
hide_sidebar: true
---

<style>
@import url("https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=JetBrains+Mono:wght@400;600&display=swap");

.rx-shell {
  --rx-bg-0: #0b1116;
  --rx-bg-1: #122033;
  --rx-bg-2: #183b45;
  --rx-card: rgba(11, 18, 24, 0.82);
  --rx-line: rgba(159, 220, 255, 0.18);
  --rx-ink: #e8f4ff;
  --rx-muted: #9cb7c9;
  --rx-accent: #35d2ff;
  --rx-accent-2: #79f8bf;
  --rx-warn: #ffcb6b;
  font-family: "Space Grotesk", "Noto Sans SC", sans-serif;
  color: var(--rx-ink);
  min-height: 100vh;
  margin: -24px -16px;
  padding: 28px 20px 36px;
  background:
    radial-gradient(circle at 8% -6%, #27677f 0%, transparent 38%),
    radial-gradient(circle at 90% 0%, #143e57 0%, transparent 40%),
    linear-gradient(140deg, var(--rx-bg-0), var(--rx-bg-1) 45%, var(--rx-bg-2));
}

.rx-wrap {
  width: min(1180px, 100%);
  margin: 0 auto;
  display: grid;
  gap: 18px;
}

.rx-hero {
  border: 1px solid var(--rx-line);
  border-radius: 16px;
  padding: 18px;
  background: linear-gradient(170deg, rgba(9, 23, 36, 0.9), rgba(10, 18, 30, 0.8));
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.28);
}

.rx-topline {
  display: inline-flex;
  align-items: center;
  border: 1px solid rgba(53, 210, 255, 0.35);
  border-radius: 999px;
  padding: 4px 10px;
  color: var(--rx-accent);
  font-size: 12px;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

.rx-hero h1 {
  margin: 10px 0 8px;
  font-size: clamp(24px, 3vw, 40px);
  line-height: 1.12;
}

.rx-sub {
  margin: 0;
  color: var(--rx-muted);
  max-width: 86ch;
}

.rx-grid {
  display: grid;
  grid-template-columns: 1.2fr 0.8fr;
  gap: 16px;
}

.rx-card {
  border: 1px solid var(--rx-line);
  border-radius: 14px;
  background: var(--rx-card);
  backdrop-filter: blur(8px);
  padding: 14px;
}

.rx-card h2,
.rx-card h3 {
  margin: 0 0 10px;
  font-size: 16px;
}

.rx-strategies {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 10px;
}

.rx-strategy {
  border: 1px solid var(--rx-line);
  background: rgba(19, 31, 44, 0.72);
  border-radius: 10px;
  padding: 10px;
  cursor: pointer;
  transition: transform 140ms ease, border-color 140ms ease, background 140ms ease;
}

.rx-strategy:hover {
  transform: translateY(-1px);
  border-color: rgba(121, 248, 191, 0.55);
}

.rx-strategy[aria-pressed="true"] {
  border-color: var(--rx-accent-2);
  background: rgba(17, 53, 58, 0.75);
}

.rx-strategy b {
  display: block;
  font-size: 14px;
}

.rx-strategy span {
  color: var(--rx-muted);
  font-size: 12px;
}

.rx-form {
  display: grid;
  gap: 10px;
}

.rx-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.rx-field label {
  display: block;
  font-size: 12px;
  color: var(--rx-muted);
  margin-bottom: 6px;
}

.rx-input,
.rx-select {
  width: 100%;
  border: 1px solid rgba(149, 190, 221, 0.25);
  background: rgba(6, 13, 20, 0.8);
  color: var(--rx-ink);
  border-radius: 8px;
  padding: 8px 10px;
  font: inherit;
  font-size: 14px;
}

.rx-switches {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
  gap: 8px;
}

.rx-switch {
  border: 1px solid var(--rx-line);
  border-radius: 10px;
  padding: 8px 10px;
  display: flex;
  gap: 8px;
  align-items: flex-start;
  background: rgba(6, 14, 20, 0.6);
}

.rx-switch input[type="checkbox"] {
  margin-top: 3px;
}

.rx-switch b {
  font-size: 13px;
}

.rx-switch span {
  display: block;
  color: var(--rx-muted);
  font-size: 11px;
  margin-top: 2px;
}

.rx-note {
  margin: 2px 0 0;
  color: var(--rx-warn);
  font-size: 12px;
}

.rx-code {
  background: #060d14;
  border: 1px solid rgba(129, 184, 220, 0.22);
  border-radius: 10px;
  padding: 12px;
  font-family: "JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size: 12px;
  line-height: 1.5;
  white-space: pre-wrap;
  word-break: break-word;
}

.rx-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.rx-btn {
  border: 1px solid rgba(117, 220, 255, 0.4);
  border-radius: 8px;
  background: rgba(15, 43, 61, 0.7);
  color: var(--rx-ink);
  padding: 8px 12px;
  cursor: pointer;
  font: inherit;
  font-size: 13px;
}

.rx-btn:hover {
  border-color: var(--rx-accent-2);
}

.rx-kpis {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.rx-kpi {
  border: 1px solid var(--rx-line);
  border-radius: 10px;
  padding: 10px;
  background: rgba(5, 13, 20, 0.6);
}

.rx-kpi small {
  color: var(--rx-muted);
}

.rx-kpi b {
  display: block;
  font-size: 18px;
  margin-top: 4px;
}

.rx-foot {
  color: var(--rx-muted);
  font-size: 12px;
}

@media (max-width: 980px) {
  .rx-grid {
    grid-template-columns: 1fr;
  }

  .rx-row {
    grid-template-columns: 1fr;
  }

  .rx-kpis {
    grid-template-columns: 1fr;
  }
}
</style>

<section class="rx-shell">
  <div class="rx-wrap">
    <div class="rx-hero">
      <span class="rx-topline">Interactive vLLM Recipe</span>
      <h1>Qwen3.5-397B-A17B 可交互部署页</h1>
      <p class="rx-sub">仿照 recipes.vllm.ai 的配置体验，增强为可视化策略切换、参数联动和命令实时生成。支持 URL 参数 <code>?strategy=multi_node_tp_pp</code> 直达策略。</p>
    </div>

    <div class="rx-grid">
      <div class="rx-card">
        <h2>1) Strategy 选择</h2>
        <div id="strategy-group" class="rx-strategies" role="group" aria-label="strategy selector"></div>

        <h3 style="margin-top:14px;">2) 参数面板</h3>
        <div class="rx-form">
          <div class="rx-row">
            <div class="rx-field">
              <label for="model-id">模型 ID</label>
              <input id="model-id" class="rx-input" value="Qwen/Qwen3.5-397B-A17B" />
            </div>
            <div class="rx-field">
              <label for="dtype">精度 / 权重路径</label>
              <select id="dtype" class="rx-select">
                <option value="bf16">bf16 (default)</option>
                <option value="fp8">fp8</option>
              </select>
            </div>
          </div>

          <div class="rx-row">
            <div class="rx-field">
              <label for="tp">--tensor-parallel-size</label>
              <input id="tp" type="number" min="1" class="rx-input" value="8" />
            </div>
            <div class="rx-field">
              <label for="pp">--pipeline-parallel-size</label>
              <input id="pp" type="number" min="1" class="rx-input" value="2" />
            </div>
          </div>

          <div class="rx-row">
            <div class="rx-field">
              <label for="dp">--data-parallel-size</label>
              <input id="dp" type="number" min="1" class="rx-input" value="4" />
            </div>
            <div class="rx-field">
              <label for="max-len">--max-model-len</label>
              <input id="max-len" type="number" min="1024" class="rx-input" value="262144" />
            </div>
          </div>

          <div class="rx-row">
            <div class="rx-field">
              <label for="kv-dtype">--kv-cache-dtype</label>
              <select id="kv-dtype" class="rx-select">
                <option value="auto">auto</option>
                <option value="fp8">fp8</option>
                <option value="bf16">bf16</option>
              </select>
            </div>
            <div class="rx-field">
              <label for="gpu-mem">--gpu-memory-utilization</label>
              <input id="gpu-mem" class="rx-input" value="0.90" />
            </div>
          </div>

          <h3 style="margin-top:8px;">3) Feature 开关</h3>
          <div class="rx-switches">
            <label class="rx-switch"><input id="tool-calling" type="checkbox" checked /><span><b>tool_calling</b><span>--enable-auto-tool-choice + --tool-call-parser</span></span></label>
            <label class="rx-switch"><input id="reasoning" type="checkbox" checked /><span><b>reasoning</b><span>--reasoning-parser qwen3</span></span></label>
            <label class="rx-switch"><input id="spec" type="checkbox" /><span><b>spec_decoding</b><span>--speculative-config JSON</span></span></label>
            <label class="rx-switch"><input id="prefix" type="checkbox" checked /><span><b>prefix_caching</b><span>--enable-prefix-caching / --no-enable-prefix-caching</span></span></label>
            <label class="rx-switch"><input id="text-only" type="checkbox" /><span><b>text_only</b><span>--language-model-only (与 encoder_parallel 互斥)</span></span></label>
            <label class="rx-switch"><input id="encoder-parallel" type="checkbox" /><span><b>encoder_parallel</b><span>--mm-encoder-tp-mode data (与 text_only 互斥)</span></span></label>
          </div>
          <p id="feature-note" class="rx-note"></p>
        </div>
      </div>

      <div class="rx-card">
        <h2>生成命令</h2>
        <div id="cmd" class="rx-code"></div>
        <div class="rx-actions" style="margin-top:10px;">
          <button id="copy-btn" class="rx-btn" type="button">复制命令</button>
          <button id="share-btn" class="rx-btn" type="button">复制当前链接</button>
        </div>

        <h3 style="margin-top:14px;">部署速览</h3>
        <div class="rx-kpis">
          <div class="rx-kpi"><small>策略</small><b id="kpi-strategy">-</b></div>
          <div class="rx-kpi"><small>并行度</small><b id="kpi-parallel">-</b></div>
          <div class="rx-kpi"><small>推荐场景</small><b id="kpi-scene">-</b></div>
          <div class="rx-kpi"><small>风险提示</small><b id="kpi-risk">-</b></div>
        </div>
        <p class="rx-foot">说明: 该页面用于生成“可执行命令骨架”，具体 parser 名称、镜像和跨节点启动器可按你的集群脚本替换。</p>
      </div>
    </div>
  </div>
</section>

<script>
(() => {
  const strategies = {
    single_node_tp: {
      label: "Single Node TP",
      desc: "最稳妥起步，单机横向切张量",
      scene: "小规模验证",
      risk: "吞吐扩展受限"
    },
    multi_node_tp: {
      label: "Multi Node TP",
      desc: "跨机张量并行",
      scene: "长上下文 + 高吞吐",
      risk: "跨机通信成本"
    },
    multi_node_tep: {
      label: "Multi Node TEP",
      desc: "TP/DP 与 Expert Parallel 组合",
      scene: "MoE 大模型生产",
      risk: "拓扑与负载均衡复杂"
    },
    multi_node_tp_pp: {
      label: "Multi Node TP+PP",
      desc: "跨机张量 + Pipeline 并行",
      scene: "超大模型切分部署",
      risk: "流水线气泡与调参成本"
    }
  };

  const dom = {
    strategyGroup: document.getElementById("strategy-group"),
    modelId: document.getElementById("model-id"),
    dtype: document.getElementById("dtype"),
    tp: document.getElementById("tp"),
    pp: document.getElementById("pp"),
    dp: document.getElementById("dp"),
    maxLen: document.getElementById("max-len"),
    kvDtype: document.getElementById("kv-dtype"),
    gpuMem: document.getElementById("gpu-mem"),
    toolCalling: document.getElementById("tool-calling"),
    reasoning: document.getElementById("reasoning"),
    spec: document.getElementById("spec"),
    prefix: document.getElementById("prefix"),
    textOnly: document.getElementById("text-only"),
    encoderParallel: document.getElementById("encoder-parallel"),
    featureNote: document.getElementById("feature-note"),
    cmd: document.getElementById("cmd"),
    copyBtn: document.getElementById("copy-btn"),
    shareBtn: document.getElementById("share-btn"),
    kpiStrategy: document.getElementById("kpi-strategy"),
    kpiParallel: document.getElementById("kpi-parallel"),
    kpiScene: document.getElementById("kpi-scene"),
    kpiRisk: document.getElementById("kpi-risk")
  };

  const query = new URLSearchParams(window.location.search);
  let state = {
    strategy: query.get("strategy") || "multi_node_tp_pp"
  };

  if (!strategies[state.strategy]) {
    state.strategy = "multi_node_tp_pp";
  }

  function renderStrategies() {
    dom.strategyGroup.innerHTML = "";
    Object.entries(strategies).forEach(([key, item]) => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "rx-strategy";
      btn.setAttribute("aria-pressed", String(key === state.strategy));
      btn.innerHTML = `<b>${item.label}</b><span>${item.desc}</span>`;
      btn.addEventListener("click", () => {
        state.strategy = key;
        update();
      });
      dom.strategyGroup.appendChild(btn);
    });
  }

  function strategyArgs() {
    const tp = Number(dom.tp.value || 1);
    const pp = Number(dom.pp.value || 1);
    const dp = Number(dom.dp.value || 1);
    const args = [];

    if (state.strategy === "single_node_tp") {
      args.push(`--tensor-parallel-size ${tp}`);
    }

    if (state.strategy === "multi_node_tp") {
      args.push(`--tensor-parallel-size ${tp}`);
      args.push("--distributed-executor-backend ray");
    }

    if (state.strategy === "multi_node_tep") {
      args.push(`--data-parallel-size ${dp}`);
      args.push("--enable-expert-parallel");
      args.push("--distributed-executor-backend ray");
    }

    if (state.strategy === "multi_node_tp_pp") {
      args.push(`--tensor-parallel-size ${tp}`);
      args.push(`--pipeline-parallel-size ${pp}`);
      args.push("--distributed-executor-backend ray");
    }

    return args;
  }

  function featureArgs() {
    const args = [];
    let note = "";

    if (dom.textOnly.checked && dom.encoderParallel.checked) {
      dom.encoderParallel.checked = false;
      note = "text_only 与 encoder_parallel 互斥，已自动关闭 encoder_parallel。";
    }

    if (dom.toolCalling.checked) {
      args.push("--enable-auto-tool-choice");
      args.push("--tool-call-parser qwen3_json");
    }

    if (dom.reasoning.checked) {
      args.push("--reasoning-parser qwen3");
    }

    if (dom.spec.checked) {
      args.push("--speculative-config '{\"method\":\"mtp\",\"num_speculative_tokens\":1}'");
    }

    if (dom.prefix.checked) {
      args.push("--enable-prefix-caching");
    } else {
      args.push("--no-enable-prefix-caching");
    }

    if (dom.textOnly.checked) {
      args.push("--language-model-only");
    }

    if (dom.encoderParallel.checked) {
      args.push("--mm-encoder-tp-mode data");
    }

    dom.featureNote.textContent = note;
    return args;
  }

  function commandText() {
    const model = dom.modelId.value.trim() || "Qwen/Qwen3.5-397B-A17B";
    const lines = [
      `vllm serve ${model}`,
      ...strategyArgs(),
      `--max-model-len ${dom.maxLen.value || 262144}`,
      `--gpu-memory-utilization ${dom.gpuMem.value || 0.90}`
    ];

    if (dom.kvDtype.value !== "auto") {
      lines.push(`--kv-cache-dtype ${dom.kvDtype.value}`);
    }

    if (dom.dtype.value === "fp8") {
      lines.push("--dtype float16");
      lines.push("# 若使用 FP8 权重模型，请将 model-id 切换为对应 FP8 checkpoint");
    } else {
      lines.push("--dtype bfloat16");
    }

    lines.push(...featureArgs());

    return lines.map((line, i) => (i === 0 ? line + " \\\n" : "  " + line + (i === lines.length - 1 ? "" : " \\\n"))).join("");
  }

  function updateKpi() {
    const cfg = strategies[state.strategy];
    dom.kpiStrategy.textContent = cfg.label;
    dom.kpiScene.textContent = cfg.scene;
    dom.kpiRisk.textContent = cfg.risk;
    if (state.strategy === "multi_node_tp_pp") {
      dom.kpiParallel.textContent = `TP ${dom.tp.value} x PP ${dom.pp.value}`;
    } else if (state.strategy === "multi_node_tep") {
      dom.kpiParallel.textContent = `DP ${dom.dp.value} + EP`;
    } else {
      dom.kpiParallel.textContent = `TP ${dom.tp.value}`;
    }
  }

  function updateQuery() {
    const url = new URL(window.location.href);
    url.searchParams.set("strategy", state.strategy);
    window.history.replaceState({}, "", url.toString());
  }

  function update() {
    renderStrategies();
    dom.cmd.textContent = commandText();
    updateKpi();
    updateQuery();
  }

  [
    dom.modelId,
    dom.dtype,
    dom.tp,
    dom.pp,
    dom.dp,
    dom.maxLen,
    dom.kvDtype,
    dom.gpuMem,
    dom.toolCalling,
    dom.reasoning,
    dom.spec,
    dom.prefix,
    dom.textOnly,
    dom.encoderParallel
  ].forEach((el) => el.addEventListener("input", update));

  dom.copyBtn.addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(dom.cmd.textContent);
      dom.copyBtn.textContent = "已复制";
      setTimeout(() => {
        dom.copyBtn.textContent = "复制命令";
      }, 1300);
    } catch {
      dom.copyBtn.textContent = "复制失败";
      setTimeout(() => {
        dom.copyBtn.textContent = "复制命令";
      }, 1300);
    }
  });

  dom.shareBtn.addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(window.location.href);
      dom.shareBtn.textContent = "链接已复制";
      setTimeout(() => {
        dom.shareBtn.textContent = "复制当前链接";
      }, 1300);
    } catch {
      dom.shareBtn.textContent = "复制失败";
      setTimeout(() => {
        dom.shareBtn.textContent = "复制当前链接";
      }, 1300);
    }
  });

  update();
})();
</script>
