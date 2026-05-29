---
title: KVCache Arena 项目对比总结报告
permalink: /reading_room/artificial_intelligence/llm_large_language_models/llm_projects/kvcache/kvcache_arena/
---

# KVCache Arena 项目对比总结报告

> 对比对象：HiCache、LMCache、Mooncake、Pegaflow、ShadowKV  
> 目标：基于部署架构进行分层归类，明确能力边界、侧重点、优缺点与选型建议。

---

## 1. 结论先行（Executive Summary）

这五个项目并不是同类替代关系，更准确是覆盖了不同架构层级：

1. ShadowKV：算法/算子层（A 层）
- 核心是 decode 阶段的稀疏 KV 访问与 CPU-offload 友好策略。
- 优势是 training-free、长上下文降本增效明显。

2. HiCache：框架内缓存管理层（B 层）
- 核心是 SGLang 内部的分层 KV 管理与前缀复用扩展。
- 优势是框架内改造成本相对可控，适合先从单实例做收益闭环。

3. LMCache / Pegaflow：引擎外 KV 数据层（C 层）
- 核心是“推理引擎 + 可插拔 KV sidecar/connector”模式。
- 优势是不改模型、增强复用与分层存储，适合在线服务工程化。

4. Mooncake：分布式数据平面与解耦架构层（D 层）
- 核心是 Transfer Engine + Mooncake Store + PD/xPyD 解耦。
- 优势是跨节点高吞吐、高扩展上限，适合大规模集群。

一句话：
- 追求“单机快收益”优先看 ShadowKV/HiCache。  
- 追求“多实例复用与工程落地”优先看 LMCache/Pegaflow。  
- 追求“跨节点与解耦上限”优先看 Mooncake。

---

## 2. 基于部署架构的分层级归类

## 2.1 四层模型

1. A 层：推理算法/内核层（Attention/KV 访问路径）
- 代表：ShadowKV

2. B 层：框架内 KV 管理层（Prefix/HiCache/分层策略）
- 代表：HiCache

3. C 层：引擎外 KV 服务层（Connector + Sidecar + Tiered KV）
- 代表：LMCache、Pegaflow

4. D 层：分布式传输与解耦数据平面（PD Disagg / KV Pool）
- 代表：Mooncake

## 2.2 次级分层（L0-L4）

为提升跨项目对齐精度，在 A/B/C/D 主层之下引入次级分层：

1. L0 请求编排层
- Router/Proxy、请求路由、P/D 流程编排。

2. L1 引擎连接层
- vLLM/SGLang connector、调度器与 worker 侧 KV 对接。

3. L2 传输执行层
- NIXL/RDMA/IPC 等 KV 传输路径与握手执行。

4. L3 存储与索引层
- CPU/SSD/对象存储、KV 索引、命中与回收策略。

5. L4 控制与观测层
- 元数据注册、服务发现、监控指标与运维控制。

## 2.3 项目归类总表（按 U/E/L 统一口径）

| 项目 | 用户主目标（U） | 主作用阶段（E） | 主层级（L） | 次级分类 | 次作用阶段 | 典型部署形态 |
|---|---|---|---|---|---|---|
| ShadowKV | U1/U3 | E4 | A | A-1 Decode 访问优化型 | E5 | 运行时算法模块嵌入推理进程 |
| HiCache | U1/U3 | E2 | B | B-1 框架内分层缓存型 | E5 | SGLang 内部分层缓存 + 外部后端 |
| LMCache | U1/U3 | E5 | C | C-1 复用能力优先型 | E2/E3 | vLLM/SGLang + Connector + KV 服务 |
| Pegaflow | U2/U4 | E5 | C | C-2 服务化治理优先型 | E3/E6 | vLLM + Pegaflow sidecar/server |
| Mooncake | U2/U4 | E3 | D | D-1 数据平面解耦型 | E0/E6 | Prefill/Decode 解耦 + TE + Store |

口径约束：
1. U 表示用户交互主诉求，E 表示主作用流程阶段，L 表示系统主层级。
2. 主层级 A/B/C/D 仅允许唯一归属；次级分类仅用于同层内部细分。
3. 先判定 U，再判定 E，最后判定 L，避免技术关键词直接驱动跨层归类。

---

## 3. 能力边界对比（What It Can / Cannot）

## 3.1 能力覆盖矩阵

| 能力项 | ShadowKV | HiCache | LMCache | Pegaflow | Mooncake |
|---|---|---|---|---|---|
| 长上下文 decode 优化 | 强 | 中 | 中 | 中 | 中 |
| 前缀复用增强 | 中 | 强 | 强 | 强 | 强 |
| 单实例分层缓存 | 中（GPU+CPU） | 强 | 强 | 强 | 中 |
| 多实例 KV 共享 | 弱 | 中 | 强 | 强 | 强 |
| 跨节点高性能传输 | 弱 | 弱-中 | 中-强 | 强 | 很强 |
| PD/xPyD 解耦支撑 | 弱 | 弱（可叠加） | 中 | 中 | 很强 |
| 平台级可观测性 | 弱 | 中 | 强 | 强 | 强 |
| training-free | 强 | 强 | 强 | 强 | 强 |

## 3.2 边界差异（关键）

1. ShadowKV 的边界
- 强在算法侧，不是完整 KV 平台。
- 更像“把同样算力用得更高效”的方法学。

2. HiCache 的边界
- 强在 SGLang 框架内缓存管理，不是全局控制平面。
- 不直接等价于跨集群 KV 服务。

3. LMCache / Pegaflow 的边界
- 强在可插拔 KV 数据层，不替代推理引擎本体。
- 需要与上层路由、鉴权、计费系统协同。
- 两者同属 C 层，但次级分层不同：
	- LMCache 偏 L1/L2/L3 的能力拼装与复用。
	- Pegaflow 偏 L1/L2/L3 并向 L4 控制面延展。

4. Mooncake 的边界
- 强在分布式数据平面与解耦能力，但对网络/运维要求高。
- 小规模场景可能“能力过剩”。
- 在次级分层中，Mooncake 的核心落点是 L0/L2/L4 联动，而非单点缓存策略。

---

## 4. 项目侧重点与优缺点

## 4.1 ShadowKV

侧重点：长上下文下 decode 阶段稀疏访问与 CPU-offload 协同。

优点：
1. Training-free，实验与接入路径明确。
2. 对长上下文负载有直接收益。
3. 可与 prefill 优化（如 MInference）叠加。

缺点：
1. 不是平台化 KV 服务，跨实例共享能力有限。
2. 对参数调优与任务分布敏感。
3. 环境依赖偏研究工程栈。

## 4.2 HiCache

侧重点：SGLang 框架内的分层缓存与复用策略。

优点：
1. 与框架内部调度协同自然。
2. 对多轮对话/Agent 场景友好。
3. 可作为单机到集群优化的过渡层。

缺点：
1. 框架绑定明显，跨框架通用性相对弱。
2. 单靠 HiCache 难覆盖跨节点数据平面瓶颈。

## 4.3 LMCache

侧重点：引擎外 KV 数据层 + 跨实例复用 + 分层存储。

优点：
1. 生态接入广，文档完善。
2. 项目形态适合线上服务演进。
3. 对 TTFT 与复用收益优化明确。

缺点：
1. 需要较好的版本与环境治理。
2. 复用率低时收益打折。

## 4.4 Pegaflow

侧重点：sidecar 解耦、KV 生命周期独立、RDMA 跨节点共享。

优点：
1. 独立生命周期，便于弹性扩缩。
2. Rust 热路径与可观测性设计偏生产化。
3. vLLM 接入直观，warm 路径收益明显。

缺点：
1. 当前公开“ready”生态以 vLLM 为主。
2. 高收益依赖 RDMA/NUMA 与部署质量。

## 4.5 Mooncake

侧重点：分布式传输平面 + KV 池化 + PD/xPyD 解耦。

优点：
1. 跨节点吞吐与扩展上限高。
2. 生态集成广，适合大规模生产场景。
3. 数据平面能力（多协议/多网卡/拓扑感知）强。

缺点：
1. 运维和系统复杂度最高。
2. 在小规模或低复用场景投入产出可能不划算。

---

## 5. 组合关系（不是非此即彼）

推荐理解为“可叠加能力栈”：

1. A+B 组合：ShadowKV + HiCache
- 用于先把单实例效率做深。

2. B+C 组合：HiCache + LMCache/Pegaflow
- 用于把框架内复用扩展到服务层复用。

3. C+D 组合：LMCache/Pegaflow + Mooncake
- 用于大规模跨节点与解耦架构演进。

4. A+C+D 组合：ShadowKV + (LMCache/Pegaflow) + Mooncake
- 用于“算法降开销 + 数据层复用 + 分布式传输”全栈优化。

---

## 6. 选型建议（按阶段）

## 6.1 阶段一：单机或小规模集群（快速见效）

建议优先：
1. HiCache（若主框架是 SGLang）
2. ShadowKV（长上下文 decode 压力高时）

目标：快速验证 TTFT、吞吐、显存占用改善。

## 6.2 阶段二：多实例线上服务（工程化复用）

建议优先：
1. LMCache 或 Pegaflow
2. 结合可观测与灰度策略逐步放量

目标：提升跨实例复用率与资源利用率。

## 6.3 阶段三：多机多卡大规模服务（架构上限）

建议优先：
1. Mooncake（PD/xPyD、高性能传输、分布式 KV 池）
2. 视情况叠加 C 层（LMCache/Pegaflow）与 A 层（ShadowKV）

目标：提高系统上限并保持尾延迟可控。

---

## 7. 风险与治理建议

1. 不要只看平均 TTFT
- 必须同时看 p95/p99、超时率、重试率。

2. 不要忽略复用画像
- 复用率决定 KV 系统的收益天花板。

3. 不要把“算法收益”直接等同“平台收益”
- 单模型测试结果到线上多租户仍有落差。

4. 版本治理要前置
- 推理框架、CUDA、网络栈、存储后端必须固定组合验证。

---

## 8. 最终建议（给负责人）

如果你要一个可执行的路线：

1. 先做两周基线压测
- 按业务分层（对话/RAG/Agent）输出复用率与瓶颈定位。

2. 先上“低风险增益层”
- SGLang 体系优先 HiCache；长上下文 decode 压力大可试 ShadowKV。

3. 再上“服务层复用”
- vLLM 体系优先评估 LMCache 或 Pegaflow（看团队对 sidecar/RDMA 的掌控能力）。

4. 最后再做“集群级解耦升级”
- 当跨节点带宽与并发成为主要瓶颈，再引入 Mooncake 类 D 层能力。

这条路线的核心是：按收益与复杂度递进，不一次性引入全栈复杂系统。
