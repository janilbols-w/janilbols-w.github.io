---
title: FAST'26 论文集摘要（按 Efficient Inference Taxonomy 排序）
---

# FAST'26 论文集摘要（Taxonomy 视角）

来源：
- FAST 2026 Proceedings: https://www.usenix.org/system/files/fast26_full_proceedings_interior.pdf

说明：
- 本页基于论文集文本抽取后整理。
- 排序结构沿用 [taxonomy_of_efficient_inference_methods_2404_14294.md](taxonomy_of_efficient_inference_methods_2404_14294.md) 的一级/二级分类。
- FAST 会议主题以存储系统为主，因此多数论文与 LLM 高效推理 taxonomy 不完全重合；不重合项标记为 N/A（但保留为“可迁移优化思路”）。

---

## 总体摘要

FAST'26 的主线不是“LLM 推理算法”本身，而是：
1. 高性能存储路径（内核/文件系统/远程存储/RDMA）
2. 分层缓存与冷热管理
3. 任务调度与尾延迟控制
4. 云存储冷启动、镜像加载、压缩与索引优化

对 MaaS 的直接启发：
- 对推理服务最有价值的是“内存与 I/O 路径优化”与“缓存体系优化”。
- 对 LMCache/Mooncake 类方案最有价值的是“跨层缓存协调”“读取路径优化”“远程存储高带宽化”。

---

## 按 Taxonomy 排序的摘要表

| 一级维度 | 二级方向 | 论文 | 摘要（整理） | 与 MaaS 关系 |
|---|---|---|---|---|
| System-level Optimization | Serving System > Memory Management | Bidaw: Enhancing Key-Value Caching for Interactive LLM Serving | 面向交互式 LLM 服务，分析了两级 KV 存储（主存+SSD）在加载延迟与吞吐退化上的问题，提出计算引擎与存储协同优化方法，目标是降低 KV 读取开销。 | 直接相关，可作为 LMCache/Mooncake 接入后的本地缓存层优化参考。 |
| System-level Optimization | Serving System > Memory Management | CacheSlide: Unlocking Cross Position-Aware KV Cache Reuse for LLMs | 针对 agent 场景中“相对位置稳定、绝对位置变化”的 prompt 结构，提出跨位置 KV 复用方式，缓解传统前缀缓存在位置错位下的复用损失。 | 直接相关，适合补到多轮 Agent 工作流的 KV 命中策略。 |
| System-level Optimization | Inference Engine > Offloading | Accelerating Model Loading in LLM Inference by Programmable Page Cache | 聚焦 LLM 推理启动阶段的模型加载瓶颈，强调在不破坏兼容性的前提下提升加载性能。核心方向是页缓存可编程化和加载路径优化。 | 与冷启动优化强相关，可用于缩短实例扩容和故障恢复时间。 |
| System-level Optimization | Inference Engine > Offloading | Fast Cloud Storage for AI Jobs via Grouped I/O API with Transparent Read/Write | 面向 AI 作业高带宽读写需求，提出利用计算侧高带宽互连并配合分组 I/O 接口提升云存储有效带宽。 | 可迁移到模型权重加载、KV spill/restore 等大流量场景。 |
| System-level Optimization | Serving System > Scheduling | Holistic and Automated Task Scheduling for Distributed LSM-tree-based Storage | 通过协同调度前台读任务与后台 compaction 任务，降低延迟波动并提升系统整体稳定性。 | 可借鉴到推理前台请求与后台缓存整理/写回任务的协同调度。 |
| System-level Optimization | Serving System > Distributed Systems | CETO FS: A High-Performance File System with Host-Server Collaboration for Disaggregated Storage | 面向解耦存储场景，减少内核栈开销并优化远程访问路径，以提升并发访问能力和故障一致性。 | 可借鉴于 P/D 分离 + 远程 KV 池架构的数据通路设计。 |
| System-level Optimization | Serving System > Distributed Systems | DMTree: Towards Efficient Tree Indexing on Disaggregated Memory via RDMA | 研究解耦内存架构下索引结构在网络带宽与 RDMA IOPS 约束中的效率问题。 | 对远程 KV 索引和分布式缓存元数据结构有参考价值。 |
| System-level Optimization | Inference Engine > Offloading | RosenBridge: A Framework for Enabling Express I/O Paths | 在虚拟化场景下打通“快速 I/O 路径”跨虚拟化边界能力，降低高速设备路径损耗。 | 可用于云上推理集群的虚拟化 I/O 优化评估。 |
| System-level Optimization | Inference Engine > Offloading | Rearchitecting Buffered I/O in the Era of High-Bandwidth SSDs | 重新设计 Buffered I/O 写路径，降低关键路径缓存与并发管理开销，以更好利用高带宽 SSD。 | 可迁移到 KV 冷层写入与权重/索引落盘路径优化。 |
| N/A | N/A | AdaCheck: An Adaptive Checkpointing System for Efficient LLM Training | 关注大规模 LLM 训练中的检查点效率与故障恢复，强调自适应策略而非固定周期方案。 | 训练侧优化，不属于推理 taxonomy 主范围；可用于训练推理一体平台。 |
| N/A | N/A | GPU Checkpoint/Restore Made Fast and Lightweight | 提出更低开销 GPU C/R 机制，目标是兼顾低停顿和低运行时负担，并支持增量检查点。 | 与在线推理弹性伸缩、故障恢复相关，但不在该 taxonomy 主轴。 |
| N/A | N/A | Preparation Meets Opportunity (Seneca) | 关注多任务 ML 训练的数据预处理瓶颈，通过缓存分区和采样策略协同提升吞吐。 | 更偏训练数据管线；对离线 embedding 构建链路有借鉴。 |
| N/A | N/A | CoFS: A Filesystem for Fast Container Startup | 通过改进镜像下载/解包路径降低容器冷启动时延。 | 对推理实例冷启动（模型服务容器）有间接价值。 |
| N/A | N/A | ThinkAhead: Preloading Images for Virtual Disks | 通过数据驱动预加载减少虚拟磁盘首次访问慢 I/O。 | 可借鉴到模型权重和热 KV 分页的预热策略。 |
| N/A | N/A | OdinANN: Direct Insert for Billion-Scale Graph-Based Vector Search | 解决大规模磁盘型图索引在持续插入下性能不稳定问题。 | 与 RAG 向量检索系统强相关，但不属于 LLM 推理 taxonomy 主分类。 |

---

## 结论（给 MaaS 的落地优先级）

1. P0：KV 路径优化
- 优先吸收 Bidaw/CacheSlide 思路，补齐“跨位置复用 + 多层存储协同”。

2. P1：冷启动与大 I/O 路径
- 结合 Programmable Page Cache、ThinkAhead、CoFS，优化模型加载和实例预热。

3. P1：调度与稳定性
- 参考 HATS 类协同调度，把前台推理与后台缓存整理/落盘解耦，目标是降低 P99 抖动。

4. P2：分离式与远程化路径
- 评估 CETO FS、DMTree、RosenBridge 类技术在“远程 KV 池 + RDMA”场景的工程可行性。

---

## 备注

- 若你希望，我可以下一步把这 15 篇再细化成“可直接进入 roadmap 的模块卡片”（每项包含：接入点、依赖、风险、监控指标）。