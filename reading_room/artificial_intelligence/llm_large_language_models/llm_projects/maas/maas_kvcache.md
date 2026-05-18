# MaaS 架构下的 KV Cache 优化全景

> KV Cache（Key-Value Cache）是 Transformer 推理的核心热点。在 MaaS 规模化部署后，KV Cache 的存储、复用与调度已演变成独立的技术方向，并催生了若干专注于此的开源项目与创业公司。

---

## 目录

- [为什么 KV Cache 是 MaaS 的关键瓶颈](#为什么-kv-cache-是-maas-的关键瓶颈)
- [技术分类框架](#技术分类框架)
- [A. 框架内置 KV Cache 管理](#a-框架内置-kv-cache-管理)
- [B. Disaggregated KV Cache 架构](#b-disaggregated-kv-cache-架构)
- [C. 分级存储与 KV Cache 卸载](#c-分级存储与-kv-cache-卸载)
- [D. KV Cache 压缩与选择性驱逐](#d-kv-cache-压缩与选择性驱逐)
- [E. RAG 场景 KV Cache 融合](#e-rag-场景-kv-cache-融合)
- [F. API 层 Prompt Caching（云厂商产品）](#f-api-层-prompt-caching云厂商产品)
- [创业公司与商业产品](#创业公司与商业产品)
- [功能对比矩阵](#功能对比矩阵)
- [参考资料](#参考资料)

---

## 为什么 KV Cache 是 MaaS 的关键瓶颈

Transformer Decoder 在自回归生成时，每个 token 的 Attention 计算需要访问**所有历史 token 的 Key/Value 向量**。KV Cache 将这些向量存储起来避免重复计算，但带来了三个核心挑战：

```
问题 1：内存容量
  每个 token 占用约 2 × num_layers × num_heads × head_dim × 2 bytes (fp16)
  → Llama-3-70B，上下文 128K：≈ 160 GB，超过单张 H100

问题 2：内存带宽
  Decode 阶段：计算强度极低，每生成一个 token 需读取整份 KV cache
  → 成为带宽密集型瓶颈（Roofline Model 左侧）

问题 3：复用率
  多用户请求的公共前缀（System Prompt / 文档片段）被反复计算
  → 相同 Prompt 在不同请求间 KV cache 无法共享
```

在 MaaS 平台（多租户、高并发、长上下文）下，这三个问题被同时放大。

---

## 技术分类框架

```
KV Cache 优化技术栈
├── A. 框架内置管理（单实例内）
│   ├── 分页内存（PagedAttention）
│   └── 前缀树复用（RadixAttention / Prefix Caching）
│
├── B. Disaggregated KV Cache（跨实例 / 跨集群）
│   ├── Prefill-Decode 分离 + KV Cache Pool
│   └── 弹性内存池（MemPool）
│
├── C. 分级存储与卸载（GPU → DRAM → Flash）
│   ├── Offloading（FlexGen / HCache）
│   └── 专用 KV 存储后端（Tair KVCache）
│
├── D. 压缩与裁剪（减少 KV 体积）
│   ├── 量化（FP8 / INT4 KV）
│   ├── 低秩压缩（MLA / CacheGen）
│   └── 选择性驱逐（H2O / SnapKV / PyramidKV）
│
├── E. RAG 场景融合（非前缀 KV 复用）
│   ├── KV Cache 混合（CacheBlend）
│   └── 知识树（RAGCache）
│
└── F. API 层 Prompt Caching（云厂商）
    └── 输入 Token 折扣 / 自动前缀检测
```

---

## A. 框架内置 KV Cache 管理

### PagedAttention（vLLM）
- **来源**：UC Berkeley，SOSP 2023
- **论文**：*Efficient Memory Management for Large Language Model Serving with PagedAttention*
- **核心思想**：借鉴操作系统虚拟内存分页，将 KV cache 切分为固定大小的 page block，按需分配，彻底消除内存碎片
- **效果**：GPU 内存利用率从 ~20% 提升至 ~96%；支持 Beam Search / Parallel Sampling 共享物理 page
- **覆盖功能**：单实例内存管理；Prefix Caching（基于 hash 的物理 block 复用）
- **GitHub**：[vllm-project/vllm](https://github.com/vllm-project/vllm)

### RadixAttention（SGLang）
- **来源**：LMSYS / UC Berkeley，MLSys 2024
- **论文**：*SGLang: Efficient Execution of Structured Language Model Programs*
- **核心思想**：用 Radix Tree（前缀基数树）索引已计算的 KV cache，精确追踪公共前缀，自动触发 cache hit
- **效果**：多轮对话 / 共享 System Prompt 场景，TTFT 降低 5-10×
- **亮点**：支持 Chunked Prefill + ChunkCache，MLA（DeepSeek Multi-head Latent Attention）优化
- **GitHub**：[sgl-project/sglang](https://github.com/sgl-project/sglang)

---

## B. Disaggregated KV Cache 架构

### Mooncake（Moonshot AI / Kimi）
- **来源**：Moonshot AI（月之暗面），arXiv:2407.00079，Jun 2024（v4: Sep 2025）
- **论文**：*Mooncake: A KVCache-centric Disaggregated Architecture for LLM Serving*
- **背景**：Kimi 的线上服务框架，支撑长上下文（128K+）的高并发商业部署

**核心架构**：

```
传统架构：
  [GPU 节点：Prefill + Decode + KV 存储 → 三者耦合]

Mooncake 架构：
  ┌─────────────────┐     KV Transfer    ┌─────────────────┐
  │   Prefill 集群  │ ─────────────────→ │   Decode 集群   │
  │  (计算密集型)   │                    │  (带宽密集型)   │
  └─────────────────┘                    └─────────────────┘
          ↕ 缓存                                  ↕
  ┌──────────────────────────────────────────────┐
  │         Disaggregated KV Cache Pool          │
  │   GPU HBM → CPU DRAM → SSD（分层存储）       │
  └──────────────────────────────────────────────┘
```

**关键技术**：
- **KV Cache-centric Scheduler**：全局调度器，在 SLO 约束下最大化有效吞吐
- **预测式早期拒绝（Prediction-based Early Rejection）**：过载时提前拒绝低优先级请求，避免队列雪崩
- **跨节点 KV Transfer**：利用 RDMA / InfiniBand 高速传输 KV cache
- **分层 KV 存储**：GPU HBM（热） → CPU DRAM（温） → SSD（冷）

**效果**：
- 模拟场景下吞吐提升最高 **525%**
- 真实负载下 Kimi 多处理 **75% 请求**（与基线相比）
- 长上下文场景下优势尤为明显

**侧重点**：生产级大规模部署；长上下文；SLO 合规；利用集群异构资源

---

### MemServe
- **来源**：华中科技大学等，arXiv:2406.17565，Jun 2024（EuroSys 2025）
- **论文**：*MemServe: Context Caching for Disaggregated LLM Serving with Elastic Memory Pool*

**核心思想**：
- **MemPool**：弹性分布式内存池，跨推理实例统一管理 KV cache
- **首次统一** inter-request（跨请求复用）和 intra-request（P-D 分离传输）两类优化
- **Global Prompt Tree**：基于局部性感知调度（locality-aware policy），用 Trie 树跟踪历史前缀，调度时优先复用已缓存的 KV

**与 Mooncake 的区别**：
- MemServe 更偏向学术系统化，重点在**统一的抽象层**（MemPool API）
- Mooncake 更偏向大规模工程落地，有完整的生产运行数据

---

## C. 分级存储与 KV Cache 卸载

### Tair KVCache（阿里云）
- **来源**：Alibaba Cloud / Tair 团队
- **背景**：Tair 是阿里自研高性能 KV 存储引擎（云上 Redis 增强版，服务双十一等超大规模场景），在此基础上扩展了对 LLM KV cache 的专项支持

**核心能力**：
- **专用 KV Cache 存储后端**：利用 Tair 的高吞吐、低延迟 KV API 替代通用 Redis/Memcached
- **分层存储**：GPU HBM（在线） → Tair DRAM（近线） → Flash/NVMe SSD（离线），三层自动冷热迁移
- **分布式 KV Cache 集群**：跨 GPU 节点共享 KV cache，支持多机多卡场景
- **云原生集成**：与阿里云 GPU 实例（IaaS）/ PAI（MLPaaS）/ 函数计算深度集成

**侧重点**：云服务商视角的 KV cache 存储即服务；与阿里云生态强绑定；大规模集群的 KV cache 共享

---

### FlexGen
- **来源**：Stanford，arXiv:2305.05765，ICML 2023
- **论文**：*FlexGen: High-Throughput Generative Inference of Large Language Models with a Single GPU*
- **核心思想**：系统性将 KV cache、权重卸载至 CPU DRAM / SSD，实现单 GPU 运行 175B 模型
- **侧重点**：高吞吐（batch size 大）的离线推理场景；牺牲延迟换吞吐

---

### HCache（EuroSys 2025）
- **来源**：清华大学，arXiv:2410.05004，EuroSys 2025
- **核心思想**：从**中间激活值**（Intermediate Activations）恢复 KV cache，而非直接存储/恢复完整 KV
  - 存储体积比存 KV cache 小 1.92-2.40×（激活值比 KV 更紧凑）
  - 恢复时用计算补偿 I/O，利用 bubble-free 调度器平衡计算与 I/O
- **效果**：TTFT 比 KV offload 降低 1.93×；比 token recomputation 降低 5.73×
- **侧重点**：多轮对话 / RAG 场景的 KV cache 持久化恢复

---

## D. KV Cache 压缩与选择性驱逐

### MLA（Multi-head Latent Attention）— DeepSeek
- **来源**：DeepSeek，DeepSeek-V2（arXiv:2405.04434）
- **核心思想**：低秩联合压缩 Key/Value，将完整 KV 投影到低维潜空间存储，推理时解压
- **效果**：KV cache 减少 **93.3%**（相比 MHA），同时性能优于 GQA/MQA
- **产品化**：DeepSeek-V2/V3/R1 全系标配；vLLM / SGLang 均已支持 MLA 优化

### KV Cache 量化
| 方案 | 精度 | 典型框架 | 备注 |
|------|------|---------|------|
| FP8 KV Cache | 8-bit | vLLM / SGLang | 精度损失极小，显存减半 |
| INT4/INT8 KV | 4-8 bit | TensorRT-LLM | 需标定 |
| KVQuant | 非均匀量化 | 学术（arXiv:2401.18079） | 感知重要性分配 bit |

### 选择性 KV 驱逐（Long-context 场景）

| 项目 | 策略 | 特点 |
|------|------|------|
| **H2O** (Heavy-Hitter Oracle) | 保留高 attention score token | 贪心驱逐低权重 token |
| **Scissorhands** | 重要性评估后截断 | 减少 KV budget |
| **SnapKV** | Pooling + 重要性 | 聚焦 Window 内关键 token |
| **StreamingLLM** | Sink token + 滑动窗口 | 无限流式生成 |
| **PyramidKV** | 层级差异化 budget | 低层 KV 更多，高层更少 |
| **MagicPocketAI** | 基于 Attention entropy | 动态感知 |

### CacheGen（LMCache / UChicago）
- **来源**：arXiv:2310.07240，UChicago
- **论文**：*CacheGen: KV Cache Compression and Streaming for Fast Large Language Model Serving*
- **核心思想**：将 KV cache **压缩编码**并**流式传输**，结合专用 codec（类似视频编解码）
- **效果**：KV cache 体积减少 3.7-4.3×，TTFT 降低 3.5-4.3×，可存储于慢速设备（SSD）
- **侧重点**：KV cache 的传输效率；跨节点 KV 复用时的带宽优化

---

## E. RAG 场景 KV Cache 融合

**核心问题**：RAG 场景中多个文档片段插入到 Prompt 的**非前缀位置**，导致传统 prefix caching 无法复用其 KV cache（因为每个文档的 cross-attention 取决于在它之前的所有 token）。

### CacheBlend（LMCache / UChicago）
- **来源**：UChicago，arXiv:2405.16444，MLSys 2025
- **核心思想**：
  1. 预先计算并存储每个文档片段的 KV cache（忽略跨文档 attention）
  2. 推理时**选择性重计算少量关键 token** 的 KV（约 10-15%）以校正 cross-attention 误差
  3. KV 检索与少量重计算**并行流水线**执行，不增加总延迟
- **效果**：TTFT 降低 2.2-3.3×；吞吐提升 2.8-5×（vs. full prefill）
- **GitHub**：[LMCache/LMCache](https://github.com/LMCache/LMCache)

### RAGCache
- **来源**：arXiv:2404.12527，2024
- **核心思想**：构建**知识树（Knowledge Tree）**，将 RAG 文档的 KV cache 按语义组织为树形结构，支持高效检索与复用
- **与 CacheBlend 的区别**：RAGCache 侧重知识的**组织与索引**；CacheBlend 侧重**融合质量**（如何正确混合多份 KV）

---

## F. API 层 Prompt Caching（云厂商产品）

云厂商将 prefix caching 产品化，在 API 层直接给用户折扣，无需用户改代码：

| 厂商 | 产品 | 发布时间 | 缓存策略 | 价格折扣 |
|------|------|---------|---------|---------|
| **OpenAI** | Prompt Caching | 2024-10 | ≥1024 token 前缀自动命中 | Input token 50% 折扣 |
| **Anthropic** | Prompt Caching (Beta) | 2024-08 | 需显式 `cache_control` 标记 | 90% 折扣（写入 +25%）|
| **Google** | Gemini Context Caching | 2024-06 | 显式创建 cached content | 按 token 小时数计费 |
| **阿里云百炼** | Prefix Cache | 2024 | 自动前缀命中 | 命中部分免费 |
| **字节跳动火山引擎** | 上下文缓存 | 2024 | 自动 | 价格优惠 |

> **注意**：API 层 Prompt Caching 是单租户视角的优化，底层通常是 prefix caching（vLLM/SGLang）；云厂商将其包装为计费产品。

---

## 创业公司与商业产品

### 趋境科技（Qujing Technology）
- **定位**：专注 KV Cache 基础设施的中国 AI 创业公司，聚焦 KV cache 服务化（KV Cache as a Service）
- **核心方向**：
  - Disaggregated KV Cache Pool：将 KV cache 从推理引擎中独立出来，作为独立存储服务
  - 跨实例、跨会话的 KV cache 持久化与高速检索
  - 针对国内云平台（GPU 集群）的优化适配
- **技术背景**：团队有深厚学术背景，方向与 Mooncake / MemServe 类似但侧重工程产品化
- **生态**：与国内推理框架（vLLM-fork、LMDeploy 等）集成

> 注：趋境科技属于 2024-2025 年涌现的新兴创业公司，公开技术资料有限，以上信息来自公开报道，具体产品细节以官方为准。

---

### LMCache（UChicago 衍生项目）
- **定位**：首个面向企业级 LLM 推理的开源 **Knowledge Delivery Network (KDN)**
- **核心产品**：
  - KV cache 跨实例存储（Redis / 本地磁盘 / 远程内存）
  - CacheGen 压缩传输
  - CacheBlend RAG 融合
- **集成**：原生支持 vLLM、HuggingFace TGI
- **效果**：最高 **8× 加速，8× 降本**（长上下文/RAG 场景）
- **GitHub**：[LMCache/LMCache](https://github.com/LMCache/LMCache)
- **官网**：[lmcache.ai](https://lmcache.ai)

---

### Friendli AI（韩国）
- **定位**：LLM 推理加速商业产品，核心技术之一是高效 KV cache 管理
- **产品**：Friendli Engine（推理引擎，支持 continuous batching + prefix cache）
- **特点**：针对 A100/H100 的 KV cache 优化，支持私有化部署

---

### KVCache.AI（初创探索）
- 围绕 KV cache 服务化进行探索，市场仍在早期教育阶段

---

## 功能对比矩阵

| 项目 | 单机内存管理 | P-D 分离 | 分层存储 | KV 压缩 | RAG 融合 | 跨实例共享 | API 层产品 |
|------|:-----------:|:-------:|:-------:|:-------:|:-------:|:---------:|:---------:|
| **vLLM PagedAttention** | ★★★ | — | — | ★（FP8）| — | ★（prefix）| — |
| **SGLang RadixAttention** | ★★★ | — | — | ★（FP8）| — | ★（prefix）| — |
| **Mooncake** | ★ | ★★★ | ★★★ | — | — | ★★★ | — |
| **MemServe** | ★★ | ★★★ | ★★ | — | — | ★★★ | — |
| **Tair KVCache** | — | ★★ | ★★★ | — | — | ★★★ | ★★（云产品）|
| **FlexGen** | ★★ | — | ★★★ | — | — | — | — |
| **HCache** | ★★ | — | ★★★ | ★★★（激活）| — | — | — |
| **LMCache** | ★★ | — | ★★ | ★★（CacheGen）| ★★★（CacheBlend）| ★★★ | — |
| **CacheBlend** | — | — | — | — | ★★★ | ★★ | — |
| **MLA（DeepSeek）** | ★★★ | — | — | ★★★（结构）| — | — | — |
| **H2O / SnapKV** | ★★★（裁剪）| — | — | ★★★（驱逐）| — | — | — |
| **趋境科技** | — | ★★★ | ★★★ | — | — | ★★★ | ★★ |
| **OpenAI Prompt Cache** | — | — | — | — | — | — | ★★★ |
| **Anthropic Prompt Cache** | — | — | — | — | — | — | ★★★ |

> ★★★ 核心差异化能力 ★★ 有支持 ★ 基础支持 — 不覆盖

---

## 各项目侧重点总结

```
专注 GPU 内部效率     → PagedAttention（vLLM） / RadixAttention（SGLang）
专注 P-D 分离 + 大规模 → Mooncake（工程）/ MemServe（学术）
专注 分层存储后端      → Tair KVCache（云产品）/ FlexGen（单机 offload）
专注 快速恢复         → HCache（激活值恢复）
专注 RAG + 多知识融合  → CacheBlend / LMCache
专注 KV 体积压缩      → MLA / CacheGen / H2O / SnapKV
专注 API 产品化       → OpenAI/Anthropic/Google Prompt Caching
专注 KV Cache 服务化   → 趋境科技 / LMCache
```

---

## 参考资料

| 文献/资料 | 类型 | 对应章节 |
|----------|------|---------|
| [Mooncake: A KVCache-centric Disaggregated Architecture for LLM Serving](https://arxiv.org/abs/2407.00079)（Qin et al., Moonshot AI, 2024） | 论文 | §B Mooncake |
| [MemServe: Context Caching for Disaggregated LLM Serving](https://arxiv.org/abs/2406.17565)（Hu et al., 2024, EuroSys 2025） | 论文 | §B MemServe |
| [Fast State Restoration in LLM Serving with HCache](https://arxiv.org/abs/2410.05004)（Gao et al., 清华, EuroSys 2025） | 论文 | §C HCache |
| [CacheBlend: Fast LLM Serving for RAG with Cached Knowledge Fusion](https://arxiv.org/abs/2405.16444)（Yao et al., UChicago, MLSys 2025） | 论文 | §E CacheBlend |
| [CacheGen: KV Cache Compression and Streaming](https://arxiv.org/abs/2310.07240)（Liu et al., UChicago） | 论文 | §D CacheGen |
| [LMCache Tech Report](https://lmcache.ai/tech_report.pdf)（Cheng et al., UChicago） | 技术报告 | §创业公司 LMCache |
| [Efficient Memory Management for LLM Serving with PagedAttention](https://arxiv.org/abs/2309.06180)（Kwon et al., Berkeley, SOSP 2023） | 论文 | §A PagedAttention |
| [LLM Inference Serving: Survey of Recent Advances](../../../llm_readings/inference/LLM-Inference-Serving_Survey-of-Recent-Advances-and-Opportunities.md)（Li et al., 2024） | 综述 | 全文 |
| [maas_features.md](maas_features.md) — §2 推理性能优化、§6 成本管理与缓存 | 本站 | 功能全景 |
| [kvcache/mooncake.fast25-qin](../../../llm_readings/kvcache/mooncake.fast25-qin) | 本站笔记 | §B Mooncake |
