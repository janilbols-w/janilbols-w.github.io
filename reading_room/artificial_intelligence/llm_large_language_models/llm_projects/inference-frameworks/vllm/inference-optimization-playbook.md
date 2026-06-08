---
title: vLLM Inference Optimization Playbook
---

# vLLM 推理优化参数配置清单

目标：把 vLLM 参数调优分为三层，避免把“系统通用优化”和“模型本身限制”混在一起。

- 第一层：通用优化（大多数模型都适用）
- 第二层：模型限制优化（由模型结构、精度、上下文长度决定）
- 第三层：三方服务插件优化（LMCache、Higress 等）

---

## 1. 通用优化（General）

### 1.1 并发与吞吐

| 参数 | 作用 | 建议起点 | 观察指标 | 常见副作用 |
| --- | --- | --- | --- | --- |
| `max-num-seqs` | 单步调度可并发序列数上限 | 64~512（按显存） | QPS、TTFT、P95 latency | 过高会导致排队抖动、显存吃紧 |
| `max-num-batched-tokens` | 每步批处理 token 上限 | 8k~64k | tokens/s、P95/P99 | 过大可能让短请求尾延迟变差 |
| `scheduling-policy`（如 FCFS/priority） | 请求调度策略 | FCFS 起步，SLA 场景切 priority | 长尾延迟、饥饿比例 | 优先级不当会让低优先级饥饿 |
| `num-scheduler-steps`（若版本支持） | 每轮调度深度 | 1 起步，小步递增 | 调度开销占比 | 过高带来 CPU 调度负担 |

### 1.2 显存与 KV Cache

| 参数 | 作用 | 建议起点 | 观察指标 | 常见副作用 |
| --- | --- | --- | --- | --- |
| `gpu-memory-utilization` | vLLM 可使用的显存占比 | 0.88~0.94 | OOM 次数、吞吐 | 太高易碎片化或瞬时 OOM |
| `kv-cache-dtype` | KV 缓存精度（如 fp8） | 默认起步，再试 fp8 | 首 token 延迟、精度回归 | 低精度可能带来质量下降 |
| `swap-space` | CPU 侧交换缓冲 | 8~32 GiB | OOM 恢复率、尾延迟 | 太大可能触发频繁 PCIe 交换 |
| `cpu-offload-gb` | 权重/缓存 CPU offload 容量 | 0 起步，必要时 8~40 | 可承载上下文长度 | 吞吐下降、延迟上升 |

### 1.3 前缀复用与重复上下文

| 参数 | 作用 | 建议起点 | 观察指标 | 常见副作用 |
| --- | --- | --- | --- | --- |
| `enable-prefix-caching` | 启用前缀缓存 | 直接开启（多轮对话强烈建议） | TTFT、缓存命中率 | 缓存管理不当会占用显存 |
| `max-model-len` | 服务侧允许最大上下文 | 按业务真实上限设置，不要盲开超长 | 可用并发、OOM | 设太大显著降低并发 |

### 1.4 并行策略

| 参数 | 作用 | 建议起点 | 观察指标 | 常见副作用 |
| --- | --- | --- | --- | --- |
| `tensor-parallel-size` | 张量并行度 | 单机多卡常用 2/4/8 | tokens/s、GPU 利用率 | 通信开销提升 |
| `pipeline-parallel-size` | 流水并行度 | 超大模型再启用 | 显存可装载性、吞吐 | 小 batch 下气泡开销明显 |
| `distributed-executor-backend` | 分布式后端（mp/ray） | 单机 mp，多机 ray | 稳定性、调度延迟 | 多机网络放大尾延迟 |

### 1.5 启动模板（通用基线）

```bash
vllm serve <model> \
  --gpu-memory-utilization 0.9 \
  --max-num-seqs 128 \
  --max-num-batched-tokens 16384 \
  --enable-prefix-caching \
  --max-model-len 8192
```

---

## 2. 模型限制优化（Model-Constrained）

核心原则：先满足“模型可运行 + 质量不回归”，再追求极致吞吐。

### 2.1 Dense 大模型（7B/14B/32B/70B）

| 约束 | 建议参数策略 |
| --- | --- |
| 显存紧张 | 优先量化（AWQ/GPTQ/FP8 视模型支持），其次提高 TP，不要先把 `max-model-len` 拉满 |
| 通信瓶颈 | TP 过大时先回退 1 档，观察 tokens/s 是否反升 |
| 长上下文需求 | 用真实业务分位设置 `max-model-len`（如 P99 对话长度），避免“一刀切 32k/128k” |

### 2.2 MoE 模型（Mixtral/DeepSeek-MoE 类）

| 约束 | 建议参数策略 |
| --- | --- |
| All-to-All 通信重 | 优先保证 NVLink/IB 拓扑，TP 和 EP（若版本支持）平衡，不要盲目堆并行度 |
| 路由不均衡 | 先看专家负载分布，再调 batch 上限，避免个别专家过热导致长尾 |
| 显存碎片 | `gpu-memory-utilization` 保守一点（如 0.86~0.9），稳定性优先 |

### 2.3 长上下文模型

| 约束 | 建议参数策略 |
| --- | --- |
| KV 占用线性增长 | 降低 `max-num-seqs`，搭配 prefix caching；必要时启用 KV 低精度 |
| TTFT 过高 | 开启 chunked prefill（若版本支持）并限制超长请求占比 |
| 多租户争抢 | 按租户做上下文配额，不要给所有请求同一 `max-model-len` |

### 2.4 多模态模型（VLM）

| 约束 | 建议参数策略 |
| --- | --- |
| 视觉编码耗时高 | 文本与图像请求分池部署；多模态实例降低 `max-num-seqs` |
| 显存占用不稳定 | 为图像输入大小设上限，避免突发 OOM |
| 吞吐目标不同 | 单独看 image-heavy 与 text-heavy 两类流量的 SLA |

### 2.5 推测解码（Speculative Decoding）

| 约束 | 建议参数策略 |
| --- | --- |
| 草稿模型质量不足 | 提升草稿模型质量或减少 speculative token 数 |
| 验证拒绝率高 | 监控 acceptance rate，低于阈值时自动降级关闭 |
| 短请求占比高 | 短请求可能收益有限，按流量类型灰度启用 |

---

## 2.6 参考 recipes.vllm.ai 的模型分类优化手段

recipes.vllm.ai 的组织方式更接近“模型家族 + 部署策略 + 硬件画像”。从公开 recipe 看，不同模型最常见的优化手段大致如下。

| 模型类型 | 官方示例 | 常见优化手段 | 适用判断 |
| --- | --- | --- | --- |
| Dense 文本模型 | `Qwen/Qwen3-32B` | 单机 `tensor-parallel-size` 起步；按 GPU 数量做单机或多机 TP；先保证最简单稳定路径，再扩并行 | 7B~32B 一类模型，优先追求低复杂度和稳定上线 |
| 超大 MoE 模型 | `Qwen/Qwen3-235B-A22B-Instruct-2507` | 大 TP 起步；官方额外提供 TEP、DEP、TP+PP、PD cluster 等替代策略；优先按拓扑选并行方案 | 总参数超大、活跃参数较小、通信成为主瓶颈 |
| 长上下文 / Hybrid / Mamba / MoE | `nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-BF16` | `kv-cache-dtype fp8`、`max-model-len 262144`、较保守 `max-num-seqs`、`enable-flashinfer-autotune`、`async-scheduling`、MTP speculative decoding、专用 `mamba-backend` | 128K+ 上下文、混合注意力、Mamba 或长推理链模型 |
| 多模态统一模型 | `google/gemma-4-12B-it` | 单卡或小 TP 起步；使用特定镜像或 nightly；按模态启用额外依赖；图文音频能力优先保证兼容性而不是极致并发 | 文本 + 图像 + 音频统一服务的模型 |
| Embedding / Pooling 模型 | `jinaai/jina-embeddings-v5-text-small` | `--runner pooling`；通常 TP 很小；重点是任务变体选择（retrieval / matching / classification / clustering），不是 decode 吞吐优化 | 只做向量编码，不做生成 |
| Reranker 模型 | `jinaai/jina-reranker-m0` | 更保守的 `gpu-memory-utilization` 和 `max-num-seqs`；优先稳定 batch 打分延迟；通常单卡或小 TP | 文档重排、cross-encoder 打分场景 |

### Dense 文本模型

从 recipes 看，Dense 文本模型的默认思路非常克制：

- 先用最简单的单机 TP 跑通。
- 只有当模型放不下或吞吐不够时，才切多机 TP。
- 工具调用、reasoning parser 这些更多是能力开关，不属于性能优化主旋钮。

这类模型最值得优先调的是：

- `tensor-parallel-size`
- `max-num-seqs`
- `max-num-batched-tokens`
- `gpu-memory-utilization`

### 超大 MoE 模型

recipes 对 MoE 的信号很明确：优化重点不是“把 batch 调更大”，而是“先选对并行策略”。

官方常见策略包括：

- TP：默认和最通用的起点
- TEP：Tensor + Expert Parallel，适合专家路由明显的 MoE
- DEP：Data + Expert Parallel，适合更大规模吞吐扩展
- TP + PP：当单纯 TP 无法兼顾装载与效率时使用
- PD cluster：Prefill / Decode 解耦，适合长上下文和高并发混合场景

因此这类模型的首要优化项通常是：

- 并行切分方式
- 节点间互联质量（NVLink / IB）
- 每卡负载是否均衡
- 长请求与短请求是否需要分池

### 长上下文 / Hybrid / Mamba 类模型

Nemotron 这类 recipe 给出的信息很典型，说明长上下文模型会把优化重点放在 KV 和调度层：

- 用 `kv-cache-dtype fp8` 降低 KV 开销
- 用较小 `max-num-seqs` 控制长上下文并发风险
- 提高 `max-model-len` 时同步控制 `max-num-batched-tokens`
- 开启 `async-scheduling` 降低等待开销
- 开启 `enable-flashinfer-autotune` 提升 kernel 路径表现
- 对 Mamba 结构单独指定 `mamba-backend` 和 `mamba-ssm-cache-dtype`
- 对 reasoning 模型叠加 MTP speculative decoding 降低延迟

结论是：长上下文模型的主要优化点不在“盲目扩 batch”，而在 KV 压缩、异步调度、结构专用后端和 prefill/decode 拆分。

### 多模态统一模型

Gemma 4 这类 recipe 显示，多模态模型首先关注的是兼容性和模态支持完整性：

- 特定 Docker 镜像或 nightly 版本
- 模态额外依赖按需安装，例如 audio extras
- 通常先从单卡或小 TP 启动
- 优先验证聊天模板、工具调用模板、reasoning parser 是否匹配模型协议

所以多模态模型的优化顺序通常是：

1. 先确认运行时、镜像、模板、依赖完全匹配。
2. 再压测图文混合负载。
3. 最后才扩大并发和 batch。

### Embedding 与 Reranker 模型

recipes 对这两类模型的优化思路与生成模型明显不同。

Embedding：

- 重点不是 decode，而是 pooling 路径，因此常见 `--runner pooling`
- 更关注任务变体是否正确，如 retrieval、text matching、classification、clustering
- 一般不需要复杂 speculative decoding、prefix caching、tool parser 一类配置

Reranker：

- 更保守地设置 `gpu-memory-utilization`
- 更保守地设置 `max-num-seqs`
- 优先稳定单批次评分延迟，而不是追求超高 tokens/s

可以把这两类模型理解为“非生成式推理”，优化重心更偏批评分吞吐、显存稳定性和任务头正确性。

### 一句话归类

- Dense：先用最简单 TP 跑通，再调 batch 和显存。
- MoE：先选对并行策略，再谈 batch。
- 长上下文 / Hybrid：先控 KV 和调度，再追求并发。
- 多模态：先保兼容与模态链路正确，再做性能优化。
- Embedding / Reranker：先选对 runner 和任务变体，再做保守批量优化。

---

## 3. 三方服务插件优化（Ecosystem）

## 3.1 LMCache（KV 外部化/跨实例复用）

适用场景：
- 多副本部署，重复系统提示词/长前缀很多
- 希望跨实例共享前缀收益，降低冷启动 TTFT

重点配置维度：

| 维度 | 配置建议 | 观测指标 |
| --- | --- | --- |
| 缓存后端 | 先本地磁盘/内存层，再远端分布式缓存 | 命中率、回源比例 |
| 容量与淘汰 | 按热点前缀大小设置容量，启用 LRU/TTL | 缓存抖动、OOM |
| 一致性策略 | 对高时效场景缩短 TTL，避免陈旧上下文 | 错答率、回滚率 |
| 网络链路 | LMCache 与 vLLM 尽量同可用区、低 RTT | TTFT、P99 |

落地建议：
- 先做只读旁路（cache hit 加速，不命中不阻塞）。
- 命中率稳定后再扩大容量和实例范围。
- 设定降级开关，缓存后端异常时自动回退到纯 vLLM。

## 3.2 Higress（网关层流量治理 + AI 插件）

适用场景：
- 多模型路由（成本优先、质量优先、租户隔离）
- API 网关统一鉴权、限流、观测

重点配置维度：

| 维度 | 配置建议 | 观测指标 |
| --- | --- | --- |
| 超时与重试 | 重试次数低配（1~2），避免放大后端雪崩 | 网关 P99、5xx |
| 限流与并发保护 | 按 tenant / API key 做令牌桶与并发上限 | 拒绝率、后端稳定性 |
| 熔断降级 | 针对慢模型设置熔断和兜底模型路由 | 可用性、降级命中率 |
| 缓存策略 | 对可缓存响应启用短 TTL，避免陈旧结果 | 命中率、正确率 |
| 可观测性 | 打通 tracing（请求 ID 贯穿 Higress -> vLLM） | 问题定位时长 |

落地建议：
- 先在 Higress 做路由与限流，不要一开始叠太多插件。
- 对 vLLM 设置合理超时，网关超时要略大于后端超时，避免误判。
- 对高优先级租户单独路由到保底算力池。

---

## 4. 推荐调优流程（实践版）

1. 建立基线：仅开通用参数（prefix cache + 内存占比 + 基础并发）。
2. 压测三组流量：短请求、长请求、混合请求。
3. 逐个旋钮调参：每次只改 1~2 个参数，记录 TTFT、TPOT、P95、P99、tokens/s。
4. 引入模型限制策略：按 Dense/MoE/长上下文分组做差异化配置。
5. 最后接入插件：先 LMCache，再 Higress 治理；每一步都要有降级开关。

---

## 5. 最小指标看板（建议）

- 延迟：TTFT、TPOT、P50/P95/P99
- 吞吐：req/s、tokens/s（prefill/decode 分开）
- 资源：GPU util、显存水位、CPU util、网络 RTT
- 缓存：prefix hit rate、LMCache hit rate、eviction rate
- 稳定性：OOM 次数、5xx 比例、重试率、降级触发率

用一句话总结：
- 通用优化负责“把引擎跑顺”；
- 模型限制优化负责“按模型特性避免踩雷”；
- 三方插件优化负责“把规模化场景的稳定性和成本打磨出来”。
