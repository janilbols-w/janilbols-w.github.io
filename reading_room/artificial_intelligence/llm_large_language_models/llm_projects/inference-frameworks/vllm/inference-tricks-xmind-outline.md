---
title: vLLM Inference Tricks XMind Outline
---

# 大模型在 vLLM 上的推理优化参数配置

## A. 通用优化（General）

### A1. 并发与吞吐

- `max-num-seqs`
  - 作用：单步调度并发序列上限
  - 建议：64~512（按显存和负载）
  - 指标：QPS、TTFT、P95
  - 风险：过高导致排队抖动和显存紧张

- `max-num-batched-tokens`
  - 作用：每步批处理 token 上限
  - 建议：8k~64k
  - 指标：tokens/s、P95/P99
  - 风险：过大时短请求尾延迟升高

- `scheduling-policy`
  - 作用：调度策略（FCFS/priority）
  - 建议：先 FCFS，SLA 场景再上 priority
  - 风险：优先级配置不当会让低优请求饥饿

### A2. 显存与 KV Cache

- `gpu-memory-utilization`
  - 作用：可用显存占比
  - 建议：0.88~0.94
  - 指标：OOM 次数、吞吐稳定性
  - 风险：过高导致碎片化和瞬时 OOM

- `kv-cache-dtype`
  - 作用：KV 精度（如 fp8）
  - 建议：默认起步，回归后再降精度
  - 指标：TTFT、质量回归
  - 风险：质量下降

- `swap-space`
  - 作用：CPU 交换缓冲
  - 建议：8~32 GiB
  - 风险：频繁交换导致延迟飙升

- `cpu-offload-gb`
  - 作用：CPU offload 容量
  - 建议：0 起步，必要时 8~40 GiB
  - 风险：吞吐下降、延迟上升

### A3. 前缀复用

- `enable-prefix-caching`
  - 作用：开启前缀缓存
  - 建议：多轮对话默认开启
  - 指标：TTFT、命中率

- `max-model-len`
  - 作用：服务最大上下文
  - 建议：按真实业务分位设置
  - 风险：盲目设大显著降低并发

### A4. 并行策略

- `tensor-parallel-size`
  - 建议：2/4/8（看卡数与通信）

- `pipeline-parallel-size`
  - 建议：超大模型再启用

- `distributed-executor-backend`
  - 建议：单机 mp；多机 ray

---

## B. 模型限制优化（Model-Constrained）

### B1. Dense（7B/14B/32B/70B）

- 关键约束
  - 显存容量
  - 通信开销
  - 上下文长度

- 调优优先级
  - 先量化（模型支持前提）
  - 再调整 TP
  - 最后才扩 `max-model-len`

### B2. MoE（Mixtral/DeepSeek-MoE 类）

- 关键约束
  - all-to-all 通信重
  - 专家负载不均
  - 显存碎片

- 参数建议
  - 并行度保守递增
  - `gpu-memory-utilization` 更保守（0.86~0.9）
  - 监控专家负载分布后再提 batch 上限

### B3. 长上下文模型

- 关键约束
  - KV 占用线性增长
  - TTFT 显著上升

- 参数建议
  - 下调 `max-num-seqs`
  - 开 `enable-prefix-caching`
  - 可选 KV 低精度
  - 按租户设置不同 `max-model-len`

### B4. 多模态模型（VLM）

- 关键约束
  - 图像编码时延高
  - 显存波动大

- 参数建议
  - 图文流量分池
  - 多模态实例降低 `max-num-seqs`
  - 限制输入图像大小

### B5. 推测解码（Speculative Decoding）

- 关键约束
  - 草稿模型质量
  - acceptance rate

- 参数建议
  - 低 acceptance rate 自动降级关闭
  - 对短请求流量灰度启用

---

## C. 三方服务插件优化（Ecosystem）

### C1. LMCache

- 适用
  - 多副本部署
  - 重复前缀多

- 配置维度
  - 缓存后端：本地层 + 远端层
  - 容量与淘汰：LRU + TTL
  - 一致性：时效敏感场景缩 TTL
  - 网络：与 vLLM 同可用区，低 RTT

- 核心指标
  - LMCache 命中率
  - 回源比例
  - eviction rate
  - TTFT/P99

- 上线策略
  - 先旁路只读
  - 命中稳定后再扩容
  - 必须有缓存故障降级开关

### C2. Higress

- 适用
  - 多模型路由
  - 多租户鉴权限流
  - 网关统一观测

- 配置维度
  - 超时与重试：低重试（1~2）
  - 限流与并发保护：tenant/API key 维度
  - 熔断降级：慢模型熔断 + 兜底模型
  - 缓存策略：短 TTL + 可控失效
  - 可观测性：trace id 贯穿网关到 vLLM

- 核心指标
  - 网关 P99
  - 5xx
  - 降级命中率
  - 后端稳定性

- 上线策略
  - 先路由/限流，再逐步叠插件
  - 网关超时略大于 vLLM 超时
  - 高优租户单独保底算力池

---

## D. 实施流程（落地顺序）

- 第 1 步：只开通用优化，建立基线
- 第 2 步：分短/长/混合流量压测
- 第 3 步：每次只改 1~2 个参数并记录指标
- 第 4 步：按模型类型应用限制优化
- 第 5 步：接入 LMCache
- 第 6 步：接入 Higress 做治理
- 第 7 步：保留全链路降级开关

---

## E. 最小观测面板

- 延迟：TTFT、TPOT、P50/P95/P99
- 吞吐：req/s、tokens/s（prefill/decode 分开）
- 资源：GPU 利用率、显存水位、CPU、网络 RTT
- 缓存：prefix hit rate、LMCache hit rate、eviction
- 稳定性：OOM、5xx、重试率、降级触发率
