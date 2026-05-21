---
title: LLM Inference Acceleration Survey List (2026)
---

# LLM Inference Acceleration 调研清单（2025+）

基准论文：
- [A Survey on Efficient Inference for Large Language Models](https://arxiv.org/abs/2404.14294)

## 1) 方向框架（基于 2404.14294 扩展）

- 推理系统总览与架构分层（算法层/运行时层/集群层）
- 推理引擎与内核优化（kernel fusion、调度、异构执行）
- Serving 优化（continuous batching、prefill-decode 解耦、SLO-aware）
- 动态路由与级联推理（小模型前置、按难度分流）
- 流式与长上下文推理（streaming、KV cache 生命周期）
- 外部知识增强推理（RAG/工具调用对时延与吞吐的影响）
- 推理 scaling 与 agentic 形态（与系统加速部分重叠）

## 2) 阅读清单（2025+ 优先）

> 说明：先收录 2025+ 的 survey/review。部分条目与“纯系统加速”有交叉但不完全重合，已在重要程度里标注原因。

| 分类 | 论文 | 时间 | 链接 | 2句摘要 | 重要程度 |
|---|---|---|---|---|---|
| 推理系统总览 | A Survey of LLM Inference Systems | 2025-06 | https://arxiv.org/abs/2506.21901 | 从系统视角梳理 LLM 推理链路中的关键组件与性能瓶颈。通常覆盖调度、并行、内存与部署策略，适合作为后续专题阅读入口。 | High: 与推理加速主线最直接对齐 |
| 推理引擎优化 | A Survey on Inference Engines for Large Language Models: Perspectives on Optimization and Efficiency | 2025-05 | https://arxiv.org/abs/2505.01658 | 聚焦引擎层优化与效率问题，强调 runtime、算子与资源利用。对比不同 engine 的设计取舍，便于做技术选型。 | High: 工程落地和框架选型价值高 |
| Serving 优化 | Taming the Titans: A Survey of Efficient LLM Inference Serving | 2025-04 | https://arxiv.org/abs/2504.19720 | 面向线上服务场景，讨论低时延与高吞吐之间的平衡。重点在批处理策略、缓存、并行与部署形态。 | High: 直接覆盖生产环境加速与成本 |
| 动态路由/级联 | Dynamic Model Routing and Cascading for Efficient LLM Inference: A Survey | 2026-02 | https://arxiv.org/abs/2603.04445 | 系统总结“按请求难度分流”的推理加速路线。讨论精度-成本-时延三者权衡及路由策略设计。 | High: 2025 后 ROI 很高的新方向 |
| 流式推理 | From Static Inference to Dynamic Interaction: A Survey of Streaming Large Language Models | 2026-03 | https://arxiv.org/abs/2603.04592 | 从静态一次性推理转向 streaming 交互式推理范式。涉及增量计算、状态维护与在线服务体验优化。 | Medium-High: 对交互式产品价值很高 |
| 知识增强推理 | LLM Inference Enhanced by External Knowledge: A Survey | 2025-05 | https://arxiv.org/abs/2505.24377 | 关注外部知识接入（如检索）对推理质量与效率的共同影响。对 RAG 场景中的推理成本结构有直接参考价值。 | Medium: 偏应用系统，但与加速实践强相关 |
| 推理/推理能力前沿 | A Survey of Frontiers in LLM Reasoning: Inference Scaling, Learning to Reason, and Agentic Systems | 2025-04 | https://arxiv.org/abs/2504.09037 | 讨论 inference scaling 与 agentic 体系，偏能力边界与方法演进。可用于评估“增加推理计算是否值得”。 | Low-Medium: 与纯 serving 加速不是一一对应 |

## 3) 基线补充（2024，建议保留）

| 分类 | 论文 | 时间 | 链接 | 2句摘要 | 重要程度 |
|---|---|---|---|---|---|
| 基线总综述 | A Survey on Efficient Inference for Large Language Models | 2024-04 | https://arxiv.org/abs/2404.14294 | 给出 data/model/system 三层分类。是后续将新论文映射进统一 taxonomy 的起点。 | High: 本调研主锚点 |
| 基线 serving 综述 | LLM Inference Serving: Survey of Recent Advances and Opportunities | 2024-07 | https://arxiv.org/abs/2407.12391 | 对 serving 研究脉络做集中整理，覆盖缓存、调度、部署与新兴方向。适合作为 2025+ 论文的对照组。 | High: 和线上系统最贴近 |
| 基线算法到系统 | Towards Efficient Generative Large Language Model Serving: A Survey from Algorithms to Systems | 2023/2025修订 | https://arxiv.org/abs/2312.15234 | 从算法改造到系统设计形成完整效率优化链。2025 年有修订版本，仍是高引用基础综述。 | High: 经典必读 |

## 4) 推荐阅读顺序（10天）

1. Day 1-2: 2404.14294，建立统一 taxonomy。
2. Day 3-4: 2506.21901 + 2505.01658，建立系统与引擎主线。
3. Day 5: 2504.19720，深入 serving 落地策略。
4. Day 6-7: 2603.04445 + 2603.04592，跟进 2026 新热点。
5. Day 8: 2505.24377，结合你自己的 RAG 场景看成本结构。
6. Day 9-10: 2407.12391 + 2312.15234，回顾补齐遗漏并收敛结论。

## 5) 可继续补全的子方向

- KV cache 服务化与分层缓存专门 survey（若出现 2026 新综述可并入）
- MoE 在线推理调度专门 survey
- 推理 SLA/SLO 驱动调度与成本建模专门 survey
