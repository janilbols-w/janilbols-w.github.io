# HCache 论文摘要

- 论文标题: Fast State Restoration in LLM Serving with HCache
- 会议: EuroSys 2025
- DOI: 10.1145/3689031.3696072
- 关键词: LLM serving, state restoration, KV cache, hidden states, TTFT

## 一句话结论

HCache 的核心是“缓存 hidden states 而不是直接缓存 KV”，并在恢复时把“传输 hidden states + 从 hidden states 重建 KV”做流水并行，从而同时利用 I/O 与计算资源，在不牺牲精度的前提下显著降低状态恢复延迟。

## 1. 论文要解决的问题

在多轮对话与 RAG 这类 stateful LLM 场景中，新请求通常要复用历史上下文状态。

已有两类主流恢复方式：

1. Token recomputation
- 从历史 token 重新前向一遍得到 KV。
- 问题: 计算开销大，尤其 attention 为长序列时开销高。

2. KV offload
- 把 KV 存在主机侧，复用时再搬回 GPU。
- 问题: I/O 传输量大，TTFT 受带宽限制明显。

论文观点是：这两类方法都在“单资源主导”模式下工作（偏计算或偏 I/O），资源利用不均，导致恢复慢。

## 2. HCache 的核心思想

不直接恢复 KV，而是恢复 hidden states，并在 GPU 上快速投影回 KV。

### 2.1 为什么 hidden states 更合适

1. 传输更省
- hidden states 大小约为 KV 的一半。
- 因而纯传输时间理论上约减半。

2. 计算更省
- 从 hidden states 到 KV 主要是线性投影（GEMM）。
- 相比从 token 全量重算，跳过了 attention 与 FFN 的大头开销。
- 论文给出下界: 计算部分至少约 6x 加速。

3. 易于流水
- hidden states 传输与 KV 重建可并行流水，端到端由二者较慢者决定。

## 3. 论文的两个关键增强

### 3.1 Bubble-Free Restoration Scheduler

问题: 在不同硬件上，传输和计算速度不匹配会产生 pipeline bubble。

做法:
1. 分层切分恢复策略（layer-wise partition）。
2. 大部分层用 HCache；剩余层用互补方法填泡泡：
- 计算慢时，混入 KV offload（减少重建计算）。
- I/O 慢时，混入 token recomputation（减少传输）。
3. 通过离线 profile 解一个 min-max 目标，令“总传输时间”和“总计算时间”尽量对齐。

效果: 降低资源偏斜平台上的空泡损失，让 HCache 在更多硬件上稳定获益。

### 3.2 Chunk-Based Storage Manager

问题: hidden states 生成顺序与恢复访问顺序不一致。
- 生成: layer-before-token（自回归逐层产生）
- 恢复: token-before-layer（批量按层恢复）

做法:
1. 采用按层友好的 chunk 化存储（默认 64 tokens/chunk）。
2. 多 SSD 轮转分布 chunk，聚合带宽。
3. 两阶段写入:
- 阶段一: GPU 快速 snapshot 到 host memory（减少阻塞）
- 阶段二: 后台线程整理并批量刷盘（避免大量小随机写）

效果: 在优化恢复路径的同时，把保存开销尽量挪出关键路径。

## 4. 实验结果（核心数字）

### 4.1 总体性能

1. 相比 KV offload
- TTFT 最高降低 1.93x。
- 在多轮对话负载中常见提升约 1.27x 到 1.90x。

2. 相比 token recomputation
- TTFT 最高降低 5.73x。
- 恢复速度在多平台上常见约 5.04x 到 9.05x 提升。

3. 对解码阶段影响
- TBT 增加很小，论文报告通常低于约 4%。

### 4.2 空间与成本

1. 存储开销
- 每 token 状态存储空间比 KV offload 少约 1.92x 到 2.40x。

2. 可扩展性
- 对长上下文更友好，恢复速度随长度变化更稳定（优于重算）。

### 4.3 消融实验结论

1. Bubble-free scheduler 有效
- 在资源偏斜平台上显著弥补 HCache-only 的 pipeline bubble。

2. Layer-wise partition 优于 token-wise partition
- 更贴合 GEMM 实际性能特性，避免不规则矩阵带来的效率损失。

3. 两阶段保存有效
- 避免批量解码时因直接小写入而拉高 TBT。

## 5. 论文价值与局限

### 5.1 价值

1. 提出了“第三条状态恢复路径”
- 既不是纯重算，也不是纯 KV 搬运，而是中间态重建。

2. 系统思路完整
- 从恢复算法、调度到存储布局都给出可落地设计。

3. 对 stateful 场景针对性强
- 对多轮对话、RAG 这种高复用上下文任务非常实用。

### 5.2 局限

1. 需要额外保存 hidden states，系统实现复杂度上升。
2. 最优收益依赖硬件平衡（算力/带宽比），需要 profile 与调参。
3. 主要优化“缓存未命中时的恢复路径”，与 GPU 常驻缓存策略需联合设计才能全局最优。

## 6. 与 KVDrive 的关系（简短对比）

1. HCache
- 关注点: “恢复表示”本身（hidden states 作为 KV 替代恢复介质）。
- 强项: 在 miss 恢复路径上降低计算与 I/O 总成本。

2. KVDrive
- 关注点: 跨 HBM/DRAM/SSD 的系统级 KV 管理与调度。
- 强项: 端到端多层缓存协同、弹性流水线与长期吞吐优化。

3. 组合潜力
- HCache 可视作“恢复介质优化”，KVDrive 可视作“全栈调度优化”；二者理论上存在融合空间。

## 7. 个人总结

HCache 的关键贡献是把“要不要保存 KV”这个问题，转化成“保存哪种中间状态更划算”。

通过 hidden states 这个折中介质，它在传输体积和恢复计算之间取得更好的平衡，再叠加 bubble-free 调度把硬件短板补齐，最终把 TTFT 明显拉低。这篇工作对 stateful LLM serving 的工程实践价值很高。