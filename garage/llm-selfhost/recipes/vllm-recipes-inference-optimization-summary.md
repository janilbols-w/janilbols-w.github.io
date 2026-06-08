---
title: vLLM Recipes Inference Optimization Summary
---

# vLLM Recipes 推理优化 Summary

扫描模型：**115**；Provider：**29**。

## 按模型分类的优化重点

### Dense 文本通用模型（10）
- 默认从单机 TP 起步，再按吞吐扩展到多机 TP。
- 高频旋钮：--max-num-seqs、--max-num-batched-tokens、--gpu-memory-utilization。
- 常见精度路径：BF16 为基线，部分模型提供 FP8/INT4 变体。
- 常见方法关键词：精度: bf16, 策略: 单机 Tensor Parallel (TP), 策略: 多机 TP, 参数: --max-model-len, 参数: --tensor-parallel-size, 参数: --gpu-memory-utilization, 量化/精度: fp8, 参数: --enforce-eager

### MoE 模型（61）
- 重点不是盲目加 batch，而是并行策略选型：TP / TEP / DEP / TP+PP / PD。
- MoE 常配合 FP8/NVFP4 与 FlashInfer/AITER 相关环境优化。
- 跨节点通信与专家负载均衡是稳定性关键。
- 常见方法关键词：策略: 单机 Tensor Parallel (TP), 策略: 多机 TP, 策略: 多机 DEP, 策略: 多机 TEP, 量化/精度: fp8, 参数: --tensor-parallel-size, 特性: tool_calling, 策略: 单机 Tensor+Expert Parallel (TEP)

### 长上下文模型 (>=131K)（90）
- 长上下文模型高频使用 KV 相关优化：--kv-cache-dtype、--max-model-len。
- 常见搭配：--async-scheduling、PD 解耦、必要时关闭 prefix caching 以控显存。
- 重点平衡 TTFT、P99 与可用并发。
- 常见方法关键词：策略: 单机 Tensor Parallel (TP), 策略: 多机 TP, 特性: tool_calling, 精度: bf16, 参数: --tensor-parallel-size, 量化/精度: fp8, 参数: --max-model-len, 特性: reasoning

### 多模态模型（48）
- 优先保证模态链路可用（图像/音频依赖、chat template、parser）。
- 再做性能优化：异步调度、显存利用率、模态输入限制。
- 部分模型支持 speculative decoding 进一步降延迟。
- 常见方法关键词：策略: 单机 Tensor Parallel (TP), 策略: 多机 TP, 精度: bf16, 可选特性: text_only, 参数: --max-model-len, 特性: tool_calling, 特性: reasoning, 量化/精度: fp8

### Embedding / Reranker 模型（2）
- 侧重 pooling / score / rerank 路径，非生成式 decode 优化。
- 参数通常更保守：较低 --gpu-memory-utilization、较低 --max-num-seqs。
- 高优先级目标是稳定时延与一致性评分。
- 常见方法关键词：策略: 单机 Tensor Parallel (TP), 精度: bf16, 环境优化: VLLM_ROCM_USE_AITER, 策略: 多机 TP, 量化/精度: fp8, 参数: --gpu-memory-utilization, 参数: --max-num-seqs

## 全局高频优化方法 Top 15

- 策略: 单机 Tensor Parallel (TP): 107
- 策略: 多机 TP: 95
- 精度: bf16: 88
- 参数: --tensor-parallel-size: 72
- 特性: tool_calling: 69
- 量化/精度: fp8: 68
- 参数: --max-model-len: 66
- 特性: reasoning: 59
- 策略: 多机 DEP: 52
- 策略: 多机 TEP: 51
- 参数: --gpu-memory-utilization: 50
- 策略: 多机 TP+PP (Pipeline Parallel): 47
- 参数: --kv-cache-dtype: 44
- 策略: 单机 Tensor+Expert Parallel (TEP): 43
- 环境优化: VLLM_ROCM_USE_AITER: 39

## 产出文件

- 详细汇总：`garage/llm-selfhost/recipes/vllm-recipes-inference-optimization-by-model.md`
- 精简总结：`garage/llm-selfhost/recipes/vllm-recipes-inference-optimization-summary.md`