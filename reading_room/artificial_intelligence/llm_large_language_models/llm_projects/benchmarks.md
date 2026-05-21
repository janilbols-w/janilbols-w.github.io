---
title: LLM Benchmark 项目整理（GuideLLM / genai-bench 扩展）
---

# LLM Benchmark 项目整理

> 目标：围绕推理与服务性能，整理类似 GuideLLM / genai-bench 的 benchmark 项目。
>
> 最后更新：2026-05-21

---

## 1. 核心推荐（同类优先）

| 项目 | 定位 | 适用场景 | 链接 |
|---|---|---|---|
| GuideLLM | 面向线上推理部署的评估与压测框架 | vLLM/SGLang/TGI 等服务端延迟与吞吐评估 | https://github.com/vllm-project/guidellm |
| genai-bench | SGLang 生态的 GenAI 基准测试 | SGLang 相关性能对比与回归 | https://github.com/sgl-project/genai-bench |
| aiperf | 面向 LLM serving 的压测与性能分析工具 | 服务端吞吐/延迟评估，适合接入到持续性能回归 | https://github.com/ai-dynamo/aiperf |
| inference-perf | Kubernetes 社区的 GenAI 推理性能基准工具 | K8s 集群上模型服务性能基准 | https://github.com/kubernetes-sigs/inference-perf |
| InferenceX | 持续化跨硬件推理基准（含多卡平台） | 机型/卡型横向对比（H100/B200/MI 系） | https://github.com/SemiAnalysisAI/InferenceX |

---

## 2. 按用途分类

### 2.1 推理服务性能压测（Latency/Throughput）

| 项目 | 重点指标 | 备注 | 链接 |
|---|---|---|---|
| GuideLLM | TTFT、ITL、TPS、并发稳定性 | 最贴近生产服务压测 | https://github.com/vllm-project/guidellm |
| genai-bench | 吞吐、延迟、场景化负载 | SGLang 生态优先 | https://github.com/sgl-project/genai-bench |
| aiperf | 延迟、吞吐、并发稳定性 | 可用于服务基准与回归压测（goodput 需按 SLO 二次计算） | https://github.com/ai-dynamo/aiperf |
| llm-inference-bench | decode 吞吐/并发对比 | 支持 vLLM 与 SGLang | https://github.com/local-inference-lab/llm-inference-bench |
| LLM-Inference-Bench-Mac | Apple Silicon 推理对比 | 本地多 runtime 横评 | https://github.com/saciducak/LLM-Inference-Bench-Mac |
| whichllm | 本地硬件下模型/运行时排序 | 偏本地选型辅助 | https://github.com/Andyyyy64/whichllm |

### 2.2 集群与生产系统基准

| 项目 | 重点能力 | 备注 | 链接 |
|---|---|---|---|
| inference-perf | K8s 环境基准测试 | 社区工具，偏平台能力 | https://github.com/kubernetes-sigs/inference-perf |
| vllm ci-infra | vLLM CI 与性能基建 | 偏内部基准基础设施 | https://github.com/vllm-project/ci-infra |
| deplodock | 配置/硬件组合基准与部署 | 适合多 GPU 配置探索 | https://github.com/cloudrift-ai/deplodock |
| inference-pipeline-benchmark | 多框架流水线基准 | 包含 vLLM/SGLang/TensorRT-LLM | https://github.com/syseeker/inference-pipeline-benchmark |

### 2.3 能力与场景评测（非纯吞吐）

| 项目 | 评测重点 | 备注 | 链接 |
|---|---|---|---|
| tool-eval-bench | 工具调用/多轮编排质量 | 可用于服务栈功能回归 | https://github.com/SeraphimSerapis/tool-eval-bench |
| agentic-swarm-bench | Agent swarm 推理负载 | 压测复杂 agent 模式 | https://github.com/SwarmOne/agentic-swarm-bench |

---

## 3. 推荐基准方法（实践）

1. 基线对齐：固定模型、上下文长度、并发模式、采样参数。
2. 首先测服务指标：TTFT、ITL、tokens/s、P95/P99。
3. 再测系统指标：GPU 利用率、显存占用、队列等待、错误率。
4. 最后测场景指标：多轮对话、工具调用、长上下文与批处理混部。

建议最小矩阵：
- 引擎：vLLM / SGLang
- 负载：短请求 / 长请求 / 混合
- 并发：1, 8, 32, 128
- 指标：TTFT, ITL, tokens/s, P99, 成本/百万 token

---

## 4. 与 MaaS 文档联动

- 选型全景：`maas/maas_projects.md`
- 开源生态：`opensource.md`
- 本文件用于专门维护 benchmark 工具与方法，不和选型清单混写。

---

## 5. 备注

- 本页优先保留“推理/服务性能”相关基准项目。
- 对 stars 很低但方向正确的项目，仅作为探索候选，不作为主推荐。
