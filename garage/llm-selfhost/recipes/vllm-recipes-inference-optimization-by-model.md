---
title: vLLM Recipes Inference Optimization By Model
---

# 基于 vllm-recipes 的推理优化方法汇总（按模型分类）

数据来源目录：`garage/llm-selfhost/recipes/vllm-recipes/models`，共扫描 **115** 个模型配方文件。

说明：同一个模型可属于多个分类（例如 MoE + 长上下文 + 多模态）。

## Dense 文本通用模型

模型数量：**10**

### 该类常见优化方法（从高到低）

- 精度: bf16（10）: 例子 Qwen/Qwen-Image, Qwen/Qwen3-32B, Qwen/Qwen3-4B
- 策略: 单机 Tensor Parallel (TP)（7）: 例子 Qwen/Qwen-Image, Qwen/Qwen3-32B, Qwen/Qwen3-4B
- 策略: 多机 TP（6）: 例子 Qwen/Qwen3-32B, Qwen/Qwen3-4B, Qwen/Qwen3Guard-Gen-8B
- 参数: --max-model-len（5）: 例子 Qwen/Qwen3-32B, Qwen/Qwen3-4B, Qwen/Qwen3Guard-Gen-8B
- 参数: --tensor-parallel-size（4）: 例子 Qwen/Qwen-Image, Qwen/Qwen3-32B, Qwen/Qwen3-4B
- 参数: --gpu-memory-utilization（4）: 例子 Qwen/Qwen3-32B, Qwen/Qwen3-4B, pfnet/plamo-2-translate
- 量化/精度: fp8（3）: 例子 Qwen/Qwen-Image, Qwen/Qwen3-32B, Qwen/Qwen3-4B
- 参数: --enforce-eager（2）: 例子 Qwen/Qwen-Image, stabilityai/stable-audio-open-1.0
- 特性: reasoning（2）: 例子 Qwen/Qwen3-32B, Qwen/Qwen3-4B
- 特性: tool_calling（2）: 例子 Qwen/Qwen3-32B, Qwen/Qwen3-4B
- 参数: --no-enable-prefix-caching（2）: 例子 Qwen/Qwen3-32B, Qwen/Qwen3-4B
- 参数: --max-num-batched-tokens（2）: 例子 Qwen/Qwen3-32B, Qwen/Qwen3-4B
- 特性: prefix_caching（2）: 例子 Qwen/Qwen3-32B, Qwen/Qwen3-4B
- 参数: --max-num-seqs（2）: 例子 Qwen/Qwen3-32B, Qwen/Qwen3-4B
- 策略: 多机 TP+PP (Pipeline Parallel)（2）: 例子 pfnet/plamo-2-translate, pfnet/plamo-3-nict-31b-base
- 参数: --kv-cache-dtype（1）: 例子 Qwen/Qwen3-32B
- 量化/精度: int4（1）: 例子 Qwen/Qwen3-32B
- 参数: --data-parallel-size（1）: 例子 Qwen/Qwen3-32B
- 参数: --async-scheduling（1）: 例子 Qwen/Qwen3-32B

### 该类模型清单

| 模型 | Provider | 架构 | 上下文长度 | 关键优化方法（节选） |
| --- | --- | --- | --- | --- |
| meituan-longcat/LongCat-Image-Edit | LongCat (Meituan) | dense | 0 | 精度: bf16 |
| pfnet/plamo-2-translate | Preferred Networks | dense | 8192 | 参数: --gpu-memory-utilization；参数: --max-model-len；策略: 单机 Tensor Parallel (TP)；策略: 多机 TP；策略: 多机 TP+PP (Pipeline Parallel)；精度: bf16 |
| pfnet/plamo-3-nict-31b-base | Preferred Networks | dense | 4096 | 参数: --max-model-len；参数: --tensor-parallel-size；策略: 单机 Tensor Parallel (TP)；策略: 多机 TP；策略: 多机 TP+PP (Pipeline Parallel)；精度: bf16 |
| Qwen/Qwen-Image | Qwen | dense | 0 | 参数: --enforce-eager；参数: --tensor-parallel-size；策略: 单机 Tensor Parallel (TP)；精度: bf16；量化/精度: fp8 |
| Qwen/Qwen3-32B | Qwen | dense | 40960 | 参数: --async-scheduling；参数: --data-parallel-size；参数: --gpu-memory-utilization；参数: --kv-cache-dtype；参数: --max-model-len；参数: --max-num-batched-tokens |
| Qwen/Qwen3-4B | Qwen | dense | 40960 | 参数: --gpu-memory-utilization；参数: --max-model-len；参数: --max-num-batched-tokens；参数: --max-num-seqs；参数: --no-enable-prefix-caching；参数: --tensor-parallel-size |
| Qwen/Qwen3Guard-Gen-8B | Qwen | dense | 32768 | 参数: --max-model-len；策略: 单机 Tensor Parallel (TP)；策略: 多机 TP；精度: bf16 |
| stabilityai/stable-audio-open-1.0 | Stability AI | dense | 0 | 参数: --enforce-eager；参数: --gpu-memory-utilization；精度: bf16 |
| stabilityai/stable-diffusion-3.5-medium | Stability AI | dense | 0 | 精度: bf16 |
| zai-org/GLM-Image | GLM (Z-AI) | dense | 4096 | 策略: 单机 Tensor Parallel (TP)；策略: 多机 TP；精度: bf16 |

## MoE 模型

模型数量：**61**

### 该类常见优化方法（从高到低）

- 策略: 单机 Tensor Parallel (TP)（60）: 例子 google/gemma-4-26B-A4B-it, JetBrains/Mellum2-12B-A2.5B-Instruct, JetBrains/Mellum2-12B-A2.5B-Thinking
- 策略: 多机 TP（53）: 例子 google/gemma-4-26B-A4B-it, MiniMaxAI/MiniMax-M2.1, MiniMaxAI/MiniMax-M2.5
- 策略: 多机 DEP（52）: 例子 google/gemma-4-26B-A4B-it, MiniMaxAI/MiniMax-M2.1, MiniMaxAI/MiniMax-M2.5
- 策略: 多机 TEP（51）: 例子 google/gemma-4-26B-A4B-it, MiniMaxAI/MiniMax-M2.1, MiniMaxAI/MiniMax-M2.5
- 量化/精度: fp8（51）: 例子 google/gemma-4-26B-A4B-it, MiniMaxAI/MiniMax-M2.1, MiniMaxAI/MiniMax-M2.5
- 参数: --tensor-parallel-size（50）: 例子 google/gemma-4-26B-A4B-it, MiniMaxAI/MiniMax-M2.1, MiniMaxAI/MiniMax-M2.5
- 特性: tool_calling（50）: 例子 google/gemma-4-26B-A4B-it, JetBrains/Mellum2-12B-A2.5B-Instruct, JetBrains/Mellum2-12B-A2.5B-Thinking
- 策略: 单机 Tensor+Expert Parallel (TEP)（43）: 例子 google/gemma-4-26B-A4B-it, JetBrains/Mellum2-12B-A2.5B-Instruct, JetBrains/Mellum2-12B-A2.5B-Thinking
- 特性: reasoning（42）: 例子 google/gemma-4-26B-A4B-it, JetBrains/Mellum2-12B-A2.5B-Thinking, MiniMaxAI/MiniMax-M2.1
- 策略: 多机 TP+PP (Pipeline Parallel)（40）: 例子 MiniMaxAI/MiniMax-M2.1, MiniMaxAI/MiniMax-M2.5, MiniMaxAI/MiniMax-M2.7
- 策略: 单机 Data+Expert Parallel (DEP)（37）: 例子 google/gemma-4-26B-A4B-it, JetBrains/Mellum2-12B-A2.5B-Instruct, JetBrains/Mellum2-12B-A2.5B-Thinking
- 精度: bf16（36）: 例子 google/gemma-4-26B-A4B-it, JetBrains/Mellum2-12B-A2.5B-Instruct, JetBrains/Mellum2-12B-A2.5B-Thinking
- 参数: --kv-cache-dtype（35）: 例子 google/gemma-4-26B-A4B-it, MiniMaxAI/MiniMax-M2.5, MiniMaxAI/MiniMax-M2.7
- 参数: --max-model-len（34）: 例子 google/gemma-4-26B-A4B-it, JetBrains/Mellum2-12B-A2.5B-Instruct, JetBrains/Mellum2-12B-A2.5B-Thinking
- 策略: Prefill/Decode 解耦集群 (PD)（33）: 例子 MiniMaxAI/MiniMax-M2.1, MiniMaxAI/MiniMax-M2.5, MiniMaxAI/MiniMax-M2.7
- 参数: --gpu-memory-utilization（32）: 例子 google/gemma-4-26B-A4B-it, Qwen/Qwen3-235B-A22B-Instruct-2507, Qwen/Qwen3-Coder-480B-A35B-Instruct
- 环境优化: VLLM_ROCM_USE_AITER（29）: 例子 MiniMaxAI/MiniMax-M2.1, MiniMaxAI/MiniMax-M2.5, MiniMaxAI/MiniMax-M2.7
- 量化/精度: nvfp4（27）: 例子 google/gemma-4-26B-A4B-it, MiniMaxAI/MiniMax-M2.5, MiniMaxAI/MiniMax-M2.7
- 特性: spec_decoding（27）: 例子 google/gemma-4-26B-A4B-it, Qwen/Qwen3-Next-80B-A3B-Instruct, Qwen/Qwen3.5-122B-A10B
- 可选特性: spec_decoding（24）: 例子 google/gemma-4-26B-A4B-it, Qwen/Qwen3-Next-80B-A3B-Instruct, Qwen/Qwen3.5-122B-A10B
- 参数: --max-num-batched-tokens（20）: 例子 MiniMaxAI/MiniMax-M2.5, Qwen/Qwen3-235B-A22B-Instruct-2507, Qwen/Qwen3.6-35B-A3B
- 参数: --speculative-config（18）: 例子 google/gemma-4-26B-A4B-it, Qwen/Qwen3-Next-80B-A3B-Instruct, Qwen/Qwen3.5-122B-A10B
- 可选特性: text_only（14）: 例子 google/gemma-4-26B-A4B-it, Qwen/Qwen3-VL-235B-A22B-Instruct, Qwen/Qwen3.5-122B-A10B
- 特性: prefix_caching（14）: 例子 Qwen/Qwen3-235B-A22B-Instruct-2507, Qwen/Qwen3-Next-80B-A3B-Instruct, Qwen/Qwen3.5-122B-A10B

### 该类模型清单

| 模型 | Provider | 架构 | 上下文长度 | 关键优化方法（节选） |
| --- | --- | --- | --- | --- |
| arcee-ai/Trinity-Large-Thinking | Arcee AI | moe | 262144 | 参数: --data-parallel-size；参数: --kv-cache-dtype；参数: --max-model-len；参数: --tensor-parallel-size；特性: reasoning；特性: tool_calling |
| baidu/ERNIE-4.5-21B-A3B-PT | Ernie (Baidu) | moe | 131072 | 参数: --gpu-memory-utilization；参数: --speculative-config；参数: --tensor-parallel-size；可选特性: spec_decoding；特性: spec_decoding；环境优化: VLLM_ROCM_USE_AITER |
| baidu/ERNIE-4.5-VL-28B-A3B-PT | Ernie (Baidu) | moe | 131072 | 参数: --cpu-offload-gb；参数: --gpu-memory-utilization；参数: --tensor-parallel-size；可选特性: text_only；策略: 单机 Tensor Parallel (TP)；策略: 多机 DEP |
| deepseek-ai/DeepSeek-R1 | DeepSeek | moe | 163840 | 参数: --data-parallel-size；参数: --kv-cache-dtype；参数: --no-enable-prefix-caching；参数: --tensor-parallel-size；特性: prefix_caching；特性: reasoning |
| deepseek-ai/DeepSeek-V3 | DeepSeek | moe | 163840 | 参数: --data-parallel-size；参数: --no-enable-prefix-caching；参数: --tensor-parallel-size；特性: prefix_caching；特性: reasoning；特性: tool_calling |
| deepseek-ai/DeepSeek-V3.1 | DeepSeek | moe | 163840 | 参数: --kv-cache-dtype；参数: --tensor-parallel-size；特性: reasoning；特性: tool_calling；环境优化: VLLM_ROCM_USE_AITER；环境优化: VLLM_ROCM_USE_AITER_MOE |
| deepseek-ai/DeepSeek-V3.2 | DeepSeek | moe | 163840 | 参数: --kv-cache-dtype；参数: --tensor-parallel-size；可选特性: spec_decoding；特性: reasoning；特性: spec_decoding；特性: tool_calling |
| deepseek-ai/DeepSeek-V3.2-Exp | DeepSeek | moe | 163840 | 参数: --kv-cache-dtype；参数: --max-num-batched-tokens；参数: --max-num-seqs；参数: --no-enable-prefix-caching；特性: reasoning；特性: tool_calling |
| deepseek-ai/DeepSeek-V4-Flash | DeepSeek | moe | 1048576 | 参数: --compilation-config；参数: --data-parallel-size；参数: --enforce-eager；参数: --gpu-memory-utilization；参数: --kv-cache-dtype；参数: --kv-transfer-config |
| deepseek-ai/DeepSeek-V4-Pro | DeepSeek | moe | 1048576 | 参数: --compilation-config；参数: --data-parallel-size；参数: --gpu-memory-utilization；参数: --kv-cache-dtype；参数: --max-model-len；参数: --max-num-batched-tokens |
| google/gemma-4-26B-A4B-it | Google | moe | 131072 | 参数: --async-scheduling；参数: --disable_chunked_mm_input；参数: --gpu-memory-utilization；参数: --kv-cache-dtype；参数: --max-model-len；参数: --max-num-seqs |
| inclusionAI/Ling-2.6-1T | inclusionAI | moe | 262144 | 参数: --tensor-parallel-size；环境优化: VLLM_ROCM_USE_AITER；策略: 单机 Tensor Parallel (TP)；策略: 多机 DEP；策略: 多机 TEP；策略: 多机 TP |
| inclusionAI/Ling-2.6-flash | inclusionAI | moe | 131072 | 参数: --tensor-parallel-size；环境优化: VLLM_ROCM_USE_AITER；策略: 单机 Tensor Parallel (TP)；策略: 多机 DEP；策略: 多机 TEP；策略: 多机 TP |
| inclusionAI/Ring-1T-FP8 | inclusionAI | moe | 65536 | 参数: --compilation-config；参数: --gpu-memory-utilization；参数: --kv-cache-dtype；参数: --max-model-len；参数: --max-num-batched-tokens；参数: --tensor-parallel-size |
| inclusionAI/Ring-2.6-1T | inclusionAI | moe | 131072 | 参数: --tensor-parallel-size；环境优化: VLLM_ROCM_USE_AITER；策略: Prefill/Decode 解耦集群 (PD)；策略: 单机 Tensor Parallel (TP)；策略: 多机 DEP；策略: 多机 TEP |
| internlm/Intern-S1 | InternLM | moe | 65536 | 参数: --gpu-memory-utilization；参数: --tensor-parallel-size；可选特性: text_only；特性: reasoning；特性: tool_calling；环境优化: VLLM_ROCM_USE_AITER |
| internlm/Intern-S2-Preview | InternLM | moe | 262144 | 参数: --gpu-memory-utilization；参数: --max-model-len；参数: --speculative-config；参数: --tensor-parallel-size；可选特性: spec_decoding；可选特性: text_only |
| JetBrains/Mellum2-12B-A2.5B-Instruct | JetBrains | moe | 131072 | 参数: --max-model-len；特性: tool_calling；策略: 单机 Data+Expert Parallel (DEP)；策略: 单机 Tensor Parallel (TP)；策略: 单机 Tensor+Expert Parallel (TEP)；精度: bf16 |
| JetBrains/Mellum2-12B-A2.5B-Thinking | JetBrains | moe | 131072 | 参数: --max-model-len；特性: reasoning；特性: tool_calling；策略: 单机 Data+Expert Parallel (DEP)；策略: 单机 Tensor Parallel (TP)；策略: 单机 Tensor+Expert Parallel (TEP) |
| meta-llama/Llama-4-Scout-17B-16E-Instruct | Meta | moe | 10485760 | 参数: --async-scheduling；参数: --compilation-config；参数: --kv-cache-dtype；参数: --max-model-len；参数: --max-num-batched-tokens；参数: --max-num-seqs |
| MiniMaxAI/MiniMax-M2 | MiniMax | moe | 196608 | 参数: --compilation-config；参数: --data-parallel-size；参数: --kv-cache-dtype；参数: --tensor-parallel-size；特性: reasoning；特性: tool_calling |
| MiniMaxAI/MiniMax-M2.1 | MiniMax | moe | 196608 | 参数: --compilation-config；参数: --tensor-parallel-size；特性: reasoning；特性: tool_calling；环境优化: VLLM_ROCM_USE_AITER；策略: Prefill/Decode 解耦集群 (PD) |
| MiniMaxAI/MiniMax-M2.5 | MiniMax | moe | 196608 | 参数: --compilation-config；参数: --enable-flashinfer-autotune；参数: --kv-cache-dtype；参数: --max-num-batched-tokens；参数: --max-num-seqs；参数: --tensor-parallel-size |
| MiniMaxAI/MiniMax-M2.7 | MiniMax | moe | 196608 | 参数: --compilation-config；参数: --data-parallel-size；参数: --kv-cache-dtype；参数: --tensor-parallel-size；特性: reasoning；特性: tool_calling |
| mistralai/Mistral-Large-3-675B-Instruct-2512 | Mistral AI | moe | 294912 | 参数: --kv-cache-dtype；参数: --max-model-len；参数: --max-num-batched-tokens；参数: --no-enable-prefix-caching；参数: --tensor-parallel-size；可选特性: text_only |
| mistralai/Mistral-Small-4-119B-2603 | Mistral AI | moe | 262144 | 参数: --max-model-len；参数: --no-enable-prefix-caching；参数: --speculative_config；参数: --tensor-parallel-size；可选特性: spec_decoding；特性: reasoning |
| moonshotai/Kimi-K2-Instruct | Moonshot AI | moe | 131072 | 参数: --data-parallel-size；参数: --gpu-memory-utilization；参数: --kv-cache-dtype；参数: --max-model-len；参数: --max-num-batched-tokens；参数: --max-num-seqs |
| moonshotai/Kimi-K2-Thinking | Moonshot AI | moe | 262144 | 参数: --kv-cache-dtype；参数: --tensor-parallel-size；特性: reasoning；特性: tool_calling；策略: Prefill/Decode 解耦集群 (PD)；策略: 单机 Data+Expert Parallel (DEP) |
| moonshotai/Kimi-K2.5 | Moonshot AI | moe | 262144 | 参数: --gpu-memory-utilization；参数: --kv-cache-dtype；可选特性: text_only；特性: reasoning；特性: spec_decoding；特性: tool_calling |
| moonshotai/Kimi-K2.6 | Moonshot AI | moe | 262144 | 参数: --gpu-memory-utilization；参数: --kv-cache-dtype；可选特性: text_only；特性: reasoning；特性: spec_decoding；特性: tool_calling |
| moonshotai/Kimi-Linear-48B-A3B-Instruct | Moonshot AI | moe | 1048576 | 参数: --gpu-memory-utilization；参数: --max-model-len；参数: --tensor-parallel-size；策略: 单机 Tensor Parallel (TP)；策略: 多机 DEP；策略: 多机 TEP |
| nvidia/Nemotron-3-Nano-Omni-30B-A3B-Reasoning-BF16 | NVIDIA | moe | 262144 | 参数: --gpu-memory-utilization；参数: --kv-cache-dtype；参数: --max-model-len；参数: --max-num-seqs；参数: --tensor-parallel-size；特性: reasoning |
| nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-BF16 | NVIDIA | moe | 262144 | 参数: --async-scheduling；参数: --kv-cache-dtype；参数: --max-model-len；参数: --max-num-seqs；参数: --tensor-parallel-size；特性: reasoning |
| nvidia/NVIDIA-Nemotron-3-Super-120B-A12B-BF16 | NVIDIA | moe | 262144 | 参数: --kv-cache-dtype；参数: --tensor-parallel-size；特性: reasoning；特性: tool_calling；策略: 单机 Tensor Parallel (TP)；策略: 多机 DEP |
| nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-BF16 | NVIDIA | moe | 262144 | 参数: --async-scheduling；参数: --enable-flashinfer-autotune；参数: --gpu-memory-utilization；参数: --kv-cache-dtype；参数: --max-model-len；参数: --max-num-batched-tokens |
| openai/gpt-oss-120b | OpenAI | moe | 131072 | 参数: --async-scheduling；参数: --data-parallel-size；参数: --gpu-memory-utilization；参数: --kv-cache-dtype；参数: --max-model-len；参数: --max-num-batched-tokens |
| openai/gpt-oss-20b | OpenAI | moe | 131072 | 参数: --gpu-memory-utilization；参数: --kv-cache-dtype；参数: --max-num-batched-tokens；参数: --no-enable-prefix-caching；特性: prefix_caching；特性: tool_calling |
| poolside/Laguna-XS.2 | Poolside | moe | 131072 | 参数: --max-model-len；参数: --speculative-config；可选特性: spec_decoding；特性: reasoning；特性: spec_decoding；特性: tool_calling |
| Qwen/Qwen3-235B-A22B-Instruct-2507 | Qwen | moe | 262144 | 参数: --distributed-executor-backend；参数: --gpu-memory-utilization；参数: --kv-cache-dtype；参数: --max-model-len；参数: --max-num-batched-tokens；参数: --no-enable-prefix-caching |
| Qwen/Qwen3-Coder-480B-A35B-Instruct | Qwen | moe | 262144 | 参数: --data-parallel-size；参数: --gpu-memory-utilization；参数: --kv-cache-dtype；参数: --max-model-len；参数: --tensor-parallel-size；特性: tool_calling |
| Qwen/Qwen3-Next-80B-A3B-Instruct | Qwen | moe | 262144 | 参数: --enable-prefix-caching；参数: --gpu-memory-utilization；参数: --kv-cache-dtype；参数: --max-model-len；参数: --no-enable-prefix-caching；参数: --speculative-config |
| Qwen/Qwen3-VL-235B-A22B-Instruct | Qwen | moe | 262144 | 参数: --async-scheduling；参数: --gpu-memory-utilization；参数: --kv-cache-dtype；参数: --max-model-len；参数: --max-num-seqs；参数: --tensor-parallel-size |
| Qwen/Qwen3.5-122B-A10B | Qwen | moe | 262144 | 参数: --enable-prefix-caching；参数: --max-model-len；参数: --speculative-config；参数: --tensor-parallel-size；可选特性: spec_decoding；可选特性: text_only |
| Qwen/Qwen3.5-35B-A3B | Qwen | moe | 262144 | 参数: --max-model-len；参数: --speculative-config；参数: --tensor-parallel-size；可选特性: spec_decoding；可选特性: text_only；特性: prefix_caching |
| Qwen/Qwen3.5-397B-A17B | Qwen | moe | 262144 | 参数: --enable-prefix-caching；参数: --gpu-memory-utilization；参数: --kv-cache-dtype；参数: --max-model-len；参数: --speculative-config；参数: --tensor-parallel-size |
| Qwen/Qwen3.6-35B-A3B | Qwen | moe | 262144 | 参数: --async-scheduling；参数: --gpu-memory-utilization；参数: --kv-cache-dtype；参数: --max-model-len；参数: --max-num-batched-tokens；参数: --max-num-seqs |
| stepfun-ai/Step-3.5-Flash | StepFun | moe | 262144 | 参数: --data-parallel-size；参数: --speculative-config；参数: --tensor-parallel-size；可选特性: spec_decoding；特性: reasoning；特性: spec_decoding |
| stepfun-ai/Step-3.7-Flash | StepFun | moe | 262144 | 参数: --async-scheduling；参数: --gpu-memory-utilization；参数: --kv-cache-dtype；参数: --speculative-config；参数: --tensor-parallel-size；可选特性: spec_decoding |
| tencent/Hunyuan-A13B-Instruct | Hunyuan (Tencent) | moe | 32768 | 参数: --kv-cache-dtype；参数: --tensor-parallel-size；环境优化: VLLM_ROCM_USE_AITER；策略: 单机 Tensor Parallel (TP)；策略: 单机 Tensor+Expert Parallel (TEP)；策略: 多机 DEP |
| tencent/Hy3-preview | Hunyuan (Tencent) | moe | 262144 | 参数: --gpu-memory-utilization；参数: --no-enable-prefix-caching；参数: --speculative-config；参数: --tensor-parallel-size；可选特性: spec_decoding；特性: prefix_caching |
| Wan-AI/Wan2.2-T2V-A14B-Diffusers | Wan (Alibaba) | moe | 0 | 环境优化: VLLM_ROCM_USE_AITER；精度: bf16 |
| XiaomiMiMo/MiMo-V2-Flash | MiMo (Xiaomi) | moe | 262144 | 参数: --data-parallel-size；参数: --gpu-memory-utilization；参数: --max-model-len；参数: --max-num-batched-tokens；参数: --tensor-parallel-size；特性: reasoning |
| XiaomiMiMo/MiMo-V2.5 | MiMo (Xiaomi) | moe | 1048576 | 参数: --gpu-memory-utilization；参数: --max-model-len；参数: --max-num-batched-tokens；参数: --no-enable-prefix-caching；参数: --tensor-parallel-size；可选特性: spec_decoding |
| XiaomiMiMo/MiMo-V2.5-Pro | MiMo (Xiaomi) | moe | 1048576 | 参数: --gpu-memory-utilization；参数: --max-model-len；参数: --tensor-parallel-size；可选特性: spec_decoding；特性: reasoning；特性: spec_decoding |
| zai-org/GLM-4.5 | GLM (Z-AI) | moe | 131072 | 参数: --gpu-memory-utilization；参数: --max-model-len；参数: --max-num-batched-tokens；参数: --no-enable-prefix-caching；参数: --speculative-config；参数: --tensor-parallel-size |
| zai-org/GLM-4.5V | GLM (Z-AI) | moe | 65536 | 参数: --gpu-memory-utilization；参数: --max-model-len；参数: --max-num-batched-tokens；参数: --tensor-parallel-size；可选特性: text_only；特性: reasoning |
| zai-org/GLM-4.6 | GLM (Z-AI) | moe | 202752 | 参数: --gpu-memory-utilization；参数: --max-model-len；参数: --max-num-batched-tokens；参数: --speculative-config；参数: --tensor-parallel-size；可选特性: spec_decoding |
| zai-org/GLM-4.6V | GLM (Z-AI) | moe | 131072 | 参数: --gpu-memory-utilization；参数: --max-model-len；参数: --max-num-batched-tokens；参数: --tensor-parallel-size；可选特性: text_only；特性: reasoning |
| zai-org/GLM-4.7 | GLM (Z-AI) | moe | 202752 | 参数: --gpu-memory-utilization；参数: --kv-cache-dtype；参数: --max-model-len；参数: --max-num-batched-tokens；参数: --no-enable-prefix-caching；参数: --speculative-config |
| zai-org/GLM-5 | GLM (Z-AI) | moe | 202752 | 参数: --kv-cache-dtype；参数: --speculative-config；参数: --tensor-parallel-size；可选特性: spec_decoding；特性: reasoning；特性: spec_decoding |
| zai-org/GLM-5.1 | GLM (Z-AI) | moe | 202752 | 参数: --kv-cache-dtype；参数: --speculative-config；参数: --tensor-parallel-size；可选特性: spec_decoding；特性: reasoning；特性: spec_decoding |

## 长上下文模型 (>=131K)

模型数量：**90**

### 该类常见优化方法（从高到低）

- 策略: 单机 Tensor Parallel (TP)（86）: 例子 ByteDance-Seed/Seed-OSS-36B-Instruct, google/gemma-4-12B-it, google/gemma-4-26B-A4B-it
- 策略: 多机 TP（76）: 例子 ByteDance-Seed/Seed-OSS-36B-Instruct, google/gemma-4-12B-it, google/gemma-4-26B-A4B-it
- 特性: tool_calling（65）: 例子 ByteDance-Seed/Seed-OSS-36B-Instruct, google/gemma-4-12B-it, google/gemma-4-26B-A4B-it
- 精度: bf16（64）: 例子 ByteDance-Seed/Seed-OSS-36B-Instruct, google/gemma-4-12B-it, google/gemma-4-26B-A4B-it
- 参数: --tensor-parallel-size（62）: 例子 ByteDance-Seed/Seed-OSS-36B-Instruct, google/gemma-4-26B-A4B-it, google/gemma-4-31B-it
- 量化/精度: fp8（60）: 例子 google/gemma-4-12B-it, google/gemma-4-26B-A4B-it, google/gemma-4-31B-it
- 参数: --max-model-len（57）: 例子 ByteDance-Seed/Seed-OSS-36B-Instruct, google/gemma-4-12B-it, google/gemma-4-26B-A4B-it
- 特性: reasoning（55）: 例子 google/gemma-4-12B-it, google/gemma-4-26B-A4B-it, google/gemma-4-31B-it
- 策略: 多机 DEP（48）: 例子 google/gemma-4-26B-A4B-it, MiniMaxAI/MiniMax-M2.1, MiniMaxAI/MiniMax-M2.5
- 策略: 多机 TEP（47）: 例子 google/gemma-4-26B-A4B-it, MiniMaxAI/MiniMax-M2.1, MiniMaxAI/MiniMax-M2.5
- 参数: --kv-cache-dtype（41）: 例子 google/gemma-4-12B-it, google/gemma-4-26B-A4B-it, google/gemma-4-31B-it
- 策略: 单机 Tensor+Expert Parallel (TEP)（41）: 例子 google/gemma-4-26B-A4B-it, JetBrains/Mellum2-12B-A2.5B-Instruct, JetBrains/Mellum2-12B-A2.5B-Thinking
- 策略: 多机 TP+PP (Pipeline Parallel)（41）: 例子 MiniMaxAI/MiniMax-M2.1, MiniMaxAI/MiniMax-M2.5, MiniMaxAI/MiniMax-M2.7
- 参数: --gpu-memory-utilization（40）: 例子 ByteDance-Seed/Seed-OSS-36B-Instruct, google/gemma-4-12B-it, google/gemma-4-26B-A4B-it
- 特性: spec_decoding（39）: 例子 google/gemma-4-12B-it, google/gemma-4-26B-A4B-it, google/gemma-4-31B-it
- 策略: 单机 Data+Expert Parallel (DEP)（36）: 例子 google/gemma-4-26B-A4B-it, JetBrains/Mellum2-12B-A2.5B-Instruct, JetBrains/Mellum2-12B-A2.5B-Thinking
- 可选特性: spec_decoding（35）: 例子 google/gemma-4-12B-it, google/gemma-4-26B-A4B-it, google/gemma-4-31B-it
- 量化/精度: nvfp4（33）: 例子 google/gemma-4-26B-A4B-it, google/gemma-4-31B-it, MiniMaxAI/MiniMax-M2.5
- 策略: Prefill/Decode 解耦集群 (PD)（32）: 例子 MiniMaxAI/MiniMax-M2.1, MiniMaxAI/MiniMax-M2.5, MiniMaxAI/MiniMax-M2.7
- 环境优化: VLLM_ROCM_USE_AITER（31）: 例子 ByteDance-Seed/Seed-OSS-36B-Instruct, MiniMaxAI/MiniMax-M2.1, MiniMaxAI/MiniMax-M2.5
- 可选特性: text_only（31）: 例子 google/gemma-4-26B-A4B-it, google/gemma-4-31B-it, google/gemma-4-E2B-it
- 参数: --max-num-batched-tokens（28）: 例子 ByteDance-Seed/Seed-OSS-36B-Instruct, MiniMaxAI/MiniMax-M2.5, PaddlePaddle/PaddleOCR-VL-1.5
- 参数: --speculative-config（28）: 例子 google/gemma-4-12B-it, google/gemma-4-26B-A4B-it, google/gemma-4-31B-it
- 参数: --no-enable-prefix-caching（21）: 例子 PaddlePaddle/PaddleOCR-VL-1.5, PaddlePaddle/PaddleOCR-VL, Qwen/Qwen2.5-32B

### 该类模型清单

| 模型 | Provider | 架构 | 上下文长度 | 关键优化方法（节选） |
| --- | --- | --- | --- | --- |
| arcee-ai/Trinity-Large-Thinking | Arcee AI | moe | 262144 | 参数: --data-parallel-size；参数: --kv-cache-dtype；参数: --max-model-len；参数: --tensor-parallel-size；特性: reasoning；特性: tool_calling |
| baidu/ERNIE-4.5-21B-A3B-PT | Ernie (Baidu) | moe | 131072 | 参数: --gpu-memory-utilization；参数: --speculative-config；参数: --tensor-parallel-size；可选特性: spec_decoding；特性: spec_decoding；环境优化: VLLM_ROCM_USE_AITER |
| baidu/ERNIE-4.5-VL-28B-A3B-PT | Ernie (Baidu) | moe | 131072 | 参数: --cpu-offload-gb；参数: --gpu-memory-utilization；参数: --tensor-parallel-size；可选特性: text_only；策略: 单机 Tensor Parallel (TP)；策略: 多机 DEP |
| ByteDance-Seed/Seed-OSS-36B-Instruct | Seed (ByteDance) | dense | 524288 | 参数: --gpu-memory-utilization；参数: --max-model-len；参数: --max-num-batched-tokens；参数: --tensor-parallel-size；特性: tool_calling；环境优化: VLLM_ROCM_USE_AITER |
| deepseek-ai/DeepSeek-R1 | DeepSeek | moe | 163840 | 参数: --data-parallel-size；参数: --kv-cache-dtype；参数: --no-enable-prefix-caching；参数: --tensor-parallel-size；特性: prefix_caching；特性: reasoning |
| deepseek-ai/DeepSeek-V3 | DeepSeek | moe | 163840 | 参数: --data-parallel-size；参数: --no-enable-prefix-caching；参数: --tensor-parallel-size；特性: prefix_caching；特性: reasoning；特性: tool_calling |
| deepseek-ai/DeepSeek-V3.1 | DeepSeek | moe | 163840 | 参数: --kv-cache-dtype；参数: --tensor-parallel-size；特性: reasoning；特性: tool_calling；环境优化: VLLM_ROCM_USE_AITER；环境优化: VLLM_ROCM_USE_AITER_MOE |
| deepseek-ai/DeepSeek-V3.2 | DeepSeek | moe | 163840 | 参数: --kv-cache-dtype；参数: --tensor-parallel-size；可选特性: spec_decoding；特性: reasoning；特性: spec_decoding；特性: tool_calling |
| deepseek-ai/DeepSeek-V3.2-Exp | DeepSeek | moe | 163840 | 参数: --kv-cache-dtype；参数: --max-num-batched-tokens；参数: --max-num-seqs；参数: --no-enable-prefix-caching；特性: reasoning；特性: tool_calling |
| deepseek-ai/DeepSeek-V4-Flash | DeepSeek | moe | 1048576 | 参数: --compilation-config；参数: --data-parallel-size；参数: --enforce-eager；参数: --gpu-memory-utilization；参数: --kv-cache-dtype；参数: --kv-transfer-config |
| deepseek-ai/DeepSeek-V4-Pro | DeepSeek | moe | 1048576 | 参数: --compilation-config；参数: --data-parallel-size；参数: --gpu-memory-utilization；参数: --kv-cache-dtype；参数: --max-model-len；参数: --max-num-batched-tokens |
| google/gemma-4-12B-it | Google | dense | 131072 | 参数: --async-scheduling；参数: --disable_chunked_mm_input；参数: --gpu-memory-utilization；参数: --kv-cache-dtype；参数: --max-model-len；参数: --speculative-config |
| google/gemma-4-26B-A4B-it | Google | moe | 131072 | 参数: --async-scheduling；参数: --disable_chunked_mm_input；参数: --gpu-memory-utilization；参数: --kv-cache-dtype；参数: --max-model-len；参数: --max-num-seqs |
| google/gemma-4-31B-it | Google | dense | 262144 | 参数: --async-scheduling；参数: --disable_chunked_mm_input；参数: --gpu-memory-utilization；参数: --kv-cache-dtype；参数: --max-model-len；参数: --max-num-seqs |
| google/gemma-4-E2B-it | Google | dense | 131072 | 参数: --async-scheduling；参数: --disable_chunked_mm_input；参数: --gpu-memory-utilization；参数: --kv-cache-dtype；参数: --max-model-len；参数: --speculative-config |
| google/gemma-4-E4B-it | Google | dense | 131072 | 参数: --async-scheduling；参数: --disable_chunked_mm_input；参数: --gpu-memory-utilization；参数: --kv-cache-dtype；参数: --max-model-len；参数: --speculative-config |
| google/translategemma-27b-it | Google | dense | 131072 | 参数: --gpu-memory-utilization；策略: 单机 Tensor Parallel (TP)；策略: 多机 TP；精度: bf16 |
| inclusionAI/Ling-2.6-1T | inclusionAI | moe | 262144 | 参数: --tensor-parallel-size；环境优化: VLLM_ROCM_USE_AITER；策略: 单机 Tensor Parallel (TP)；策略: 多机 DEP；策略: 多机 TEP；策略: 多机 TP |
| inclusionAI/Ling-2.6-flash | inclusionAI | moe | 131072 | 参数: --tensor-parallel-size；环境优化: VLLM_ROCM_USE_AITER；策略: 单机 Tensor Parallel (TP)；策略: 多机 DEP；策略: 多机 TEP；策略: 多机 TP |
| inclusionAI/Ring-2.6-1T | inclusionAI | moe | 131072 | 参数: --tensor-parallel-size；环境优化: VLLM_ROCM_USE_AITER；策略: Prefill/Decode 解耦集群 (PD)；策略: 单机 Tensor Parallel (TP)；策略: 多机 DEP；策略: 多机 TEP |
| internlm/Intern-S2-Preview | InternLM | moe | 262144 | 参数: --gpu-memory-utilization；参数: --max-model-len；参数: --speculative-config；参数: --tensor-parallel-size；可选特性: spec_decoding；可选特性: text_only |
| JetBrains/Mellum2-12B-A2.5B-Instruct | JetBrains | moe | 131072 | 参数: --max-model-len；特性: tool_calling；策略: 单机 Data+Expert Parallel (DEP)；策略: 单机 Tensor Parallel (TP)；策略: 单机 Tensor+Expert Parallel (TEP)；精度: bf16 |
| JetBrains/Mellum2-12B-A2.5B-Thinking | JetBrains | moe | 131072 | 参数: --max-model-len；特性: reasoning；特性: tool_calling；策略: 单机 Data+Expert Parallel (DEP)；策略: 单机 Tensor Parallel (TP)；策略: 单机 Tensor+Expert Parallel (TEP) |
| meta-llama/Llama-3.1-8B-Instruct | Meta | dense | 131072 | 参数: --gpu-memory-utilization；参数: --kv-cache-dtype；参数: --max-model-len；参数: --speculative-config；参数: --tensor-parallel-size；可选特性: spec_decoding |
| meta-llama/Llama-3.3-70B-Instruct | Meta | dense | 131072 | 参数: --async-scheduling；参数: --compilation-config；参数: --kv-cache-dtype；参数: --max-model-len；参数: --max-num-batched-tokens；参数: --no-enable-prefix-caching |
| meta-llama/Llama-4-Scout-17B-16E-Instruct | Meta | moe | 10485760 | 参数: --async-scheduling；参数: --compilation-config；参数: --kv-cache-dtype；参数: --max-model-len；参数: --max-num-batched-tokens；参数: --max-num-seqs |
| microsoft/Phi-4-mini-instruct | Microsoft | dense | 131072 | 参数: --max-model-len；可选特性: encoder_parallel；可选特性: text_only；策略: 单机 Tensor Parallel (TP)；策略: 多机 TP；精度: bf16 |
| MiniMaxAI/MiniMax-M2 | MiniMax | moe | 196608 | 参数: --compilation-config；参数: --data-parallel-size；参数: --kv-cache-dtype；参数: --tensor-parallel-size；特性: reasoning；特性: tool_calling |
| MiniMaxAI/MiniMax-M2.1 | MiniMax | moe | 196608 | 参数: --compilation-config；参数: --tensor-parallel-size；特性: reasoning；特性: tool_calling；环境优化: VLLM_ROCM_USE_AITER；策略: Prefill/Decode 解耦集群 (PD) |
| MiniMaxAI/MiniMax-M2.5 | MiniMax | moe | 196608 | 参数: --compilation-config；参数: --enable-flashinfer-autotune；参数: --kv-cache-dtype；参数: --max-num-batched-tokens；参数: --max-num-seqs；参数: --tensor-parallel-size |
| MiniMaxAI/MiniMax-M2.7 | MiniMax | moe | 196608 | 参数: --compilation-config；参数: --data-parallel-size；参数: --kv-cache-dtype；参数: --tensor-parallel-size；特性: reasoning；特性: tool_calling |
| mistralai/Ministral-3-14B-Instruct-2512 | Mistral AI | dense | 262144 | 参数: --gpu-memory-utilization；参数: --kv-cache-dtype；参数: --max-model-len；参数: --max-num-batched-tokens；参数: --max-num-seqs；参数: --tensor-parallel-size |
| mistralai/Ministral-3-8B-Reasoning-2512 | Mistral AI | dense | 262144 | 参数: --max-model-len；参数: --no-enable-prefix-caching；参数: --tensor-parallel-size；可选特性: encoder_parallel；可选特性: text_only；特性: reasoning |
| mistralai/Mistral-Large-3-675B-Instruct-2512 | Mistral AI | moe | 294912 | 参数: --kv-cache-dtype；参数: --max-model-len；参数: --max-num-batched-tokens；参数: --no-enable-prefix-caching；参数: --tensor-parallel-size；可选特性: text_only |
| mistralai/Mistral-Medium-3.5-128B | Mistral AI | dense | 262144 | 参数: --gpu-memory-utilization；参数: --max-model-len；参数: --max-num-batched-tokens；参数: --no-enable-prefix-caching；参数: --speculative_config；参数: --tensor-parallel-size |
| mistralai/Mistral-Small-4-119B-2603 | Mistral AI | moe | 262144 | 参数: --max-model-len；参数: --no-enable-prefix-caching；参数: --speculative_config；参数: --tensor-parallel-size；可选特性: spec_decoding；特性: reasoning |
| mistralai/Voxtral-Mini-4B-Realtime-2602 | Mistral AI | dense | 131072 | 参数: --max-model-len；参数: --max-num-batched-tokens；策略: 单机 Tensor Parallel (TP)；策略: 多机 TP；精度: bf16 |
| moonshotai/Kimi-K2-Instruct | Moonshot AI | moe | 131072 | 参数: --data-parallel-size；参数: --gpu-memory-utilization；参数: --kv-cache-dtype；参数: --max-model-len；参数: --max-num-batched-tokens；参数: --max-num-seqs |
| moonshotai/Kimi-K2-Thinking | Moonshot AI | moe | 262144 | 参数: --kv-cache-dtype；参数: --tensor-parallel-size；特性: reasoning；特性: tool_calling；策略: Prefill/Decode 解耦集群 (PD)；策略: 单机 Data+Expert Parallel (DEP) |
| moonshotai/Kimi-K2.5 | Moonshot AI | moe | 262144 | 参数: --gpu-memory-utilization；参数: --kv-cache-dtype；可选特性: text_only；特性: reasoning；特性: spec_decoding；特性: tool_calling |
| moonshotai/Kimi-K2.6 | Moonshot AI | moe | 262144 | 参数: --gpu-memory-utilization；参数: --kv-cache-dtype；可选特性: text_only；特性: reasoning；特性: spec_decoding；特性: tool_calling |
| moonshotai/Kimi-Linear-48B-A3B-Instruct | Moonshot AI | moe | 1048576 | 参数: --gpu-memory-utilization；参数: --max-model-len；参数: --tensor-parallel-size；策略: 单机 Tensor Parallel (TP)；策略: 多机 DEP；策略: 多机 TEP |
| nvidia/Cosmos3-Nano | NVIDIA | dense | 262144 | 参数: --async-scheduling；参数: --tensor-parallel-size；精度: bf16 |
| nvidia/Cosmos3-Super | NVIDIA | dense | 262144 | 参数: --async-scheduling；参数: --tensor-parallel-size；精度: bf16 |
| nvidia/Cosmos3-Super-Image2Video | NVIDIA | dense | 262144 | 参数: --tensor-parallel-size；精度: bf16 |
| nvidia/Cosmos3-Super-Text2Image | NVIDIA | dense | 262144 | 参数: --tensor-parallel-size；精度: bf16 |
| nvidia/Nemotron-3-Nano-Omni-30B-A3B-Reasoning-BF16 | NVIDIA | moe | 262144 | 参数: --gpu-memory-utilization；参数: --kv-cache-dtype；参数: --max-model-len；参数: --max-num-seqs；参数: --tensor-parallel-size；特性: reasoning |
| nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-BF16 | NVIDIA | moe | 262144 | 参数: --async-scheduling；参数: --kv-cache-dtype；参数: --max-model-len；参数: --max-num-seqs；参数: --tensor-parallel-size；特性: reasoning |
| nvidia/NVIDIA-Nemotron-3-Nano-4B-BF16 | NVIDIA | dense | 262144 | 参数: --async-scheduling；参数: --kv-cache-dtype；参数: --max-model-len；参数: --tensor-parallel-size；特性: reasoning；特性: tool_calling |
| nvidia/NVIDIA-Nemotron-3-Super-120B-A12B-BF16 | NVIDIA | moe | 262144 | 参数: --kv-cache-dtype；参数: --tensor-parallel-size；特性: reasoning；特性: tool_calling；策略: 单机 Tensor Parallel (TP)；策略: 多机 DEP |
| nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-BF16 | NVIDIA | moe | 262144 | 参数: --async-scheduling；参数: --enable-flashinfer-autotune；参数: --gpu-memory-utilization；参数: --kv-cache-dtype；参数: --max-model-len；参数: --max-num-batched-tokens |
| nvidia/NVIDIA-Nemotron-Nano-12B-v2-VL-BF16 | NVIDIA | dense | 131072 | 参数: --data-parallel-size；参数: --max-model-len；可选特性: encoder_parallel；可选特性: text_only；策略: 单机 Tensor Parallel (TP)；策略: 多机 TP |
| nvidia/NVIDIA-Nemotron-Nano-9B-v2 | NVIDIA | dense | 131072 | 参数: --max-model-len；参数: --tensor-parallel-size；特性: tool_calling；策略: 单机 Tensor Parallel (TP)；策略: 多机 TP；策略: 多机 TP+PP (Pipeline Parallel) |
| openai/gpt-oss-120b | OpenAI | moe | 131072 | 参数: --async-scheduling；参数: --data-parallel-size；参数: --gpu-memory-utilization；参数: --kv-cache-dtype；参数: --max-model-len；参数: --max-num-batched-tokens |
| openai/gpt-oss-20b | OpenAI | moe | 131072 | 参数: --gpu-memory-utilization；参数: --kv-cache-dtype；参数: --max-num-batched-tokens；参数: --no-enable-prefix-caching；特性: prefix_caching；特性: tool_calling |
| openbmb/MiniCPM-V-4.6 | MiniCPM (OpenBMB) | dense | 262144 | 参数: --max-model-len；特性: tool_calling；策略: 单机 Tensor Parallel (TP)；策略: 多机 TP；精度: bf16 |
| openbmb/MiniCPM5-1B | MiniCPM (OpenBMB) | dense | 131072 | 参数: --enforce-eager；参数: --max-model-len；可选特性: reasoning；特性: reasoning；策略: 单机 Tensor Parallel (TP)；策略: 多机 TP |
| PaddlePaddle/PaddleOCR-VL | PaddlePaddle | dense | 131072 | 参数: --max-num-batched-tokens；参数: --no-enable-prefix-caching；可选特性: encoder_parallel；可选特性: text_only；特性: prefix_caching；策略: 单机 Tensor Parallel (TP) |
| PaddlePaddle/PaddleOCR-VL-1.5 | PaddlePaddle | dense | 131072 | 参数: --max-num-batched-tokens；参数: --no-enable-prefix-caching；可选特性: encoder_parallel；可选特性: text_only；特性: prefix_caching；策略: 单机 Tensor Parallel (TP) |
| poolside/Laguna-XS.2 | Poolside | moe | 131072 | 参数: --max-model-len；参数: --speculative-config；可选特性: spec_decoding；特性: reasoning；特性: spec_decoding；特性: tool_calling |
| Qwen/Qwen2.5-32B | Qwen | dense | 131072 | 参数: --gpu-memory-utilization；参数: --max-model-len；参数: --max-num-batched-tokens；参数: --max-num-seqs；参数: --no-enable-prefix-caching；参数: --tensor-parallel-size |
| Qwen/Qwen3-235B-A22B-Instruct-2507 | Qwen | moe | 262144 | 参数: --distributed-executor-backend；参数: --gpu-memory-utilization；参数: --kv-cache-dtype；参数: --max-model-len；参数: --max-num-batched-tokens；参数: --no-enable-prefix-caching |
| Qwen/Qwen3-Coder-480B-A35B-Instruct | Qwen | moe | 262144 | 参数: --data-parallel-size；参数: --gpu-memory-utilization；参数: --kv-cache-dtype；参数: --max-model-len；参数: --tensor-parallel-size；特性: tool_calling |
| Qwen/Qwen3-Next-80B-A3B-Instruct | Qwen | moe | 262144 | 参数: --enable-prefix-caching；参数: --gpu-memory-utilization；参数: --kv-cache-dtype；参数: --max-model-len；参数: --no-enable-prefix-caching；参数: --speculative-config |
| Qwen/Qwen3-VL-235B-A22B-Instruct | Qwen | moe | 262144 | 参数: --async-scheduling；参数: --gpu-memory-utilization；参数: --kv-cache-dtype；参数: --max-model-len；参数: --max-num-seqs；参数: --tensor-parallel-size |
| Qwen/Qwen3.5-0.8B | Qwen | dense | 262144 | 参数: --max-model-len；可选特性: text_only；特性: reasoning；特性: tool_calling；策略: 单机 Tensor Parallel (TP)；精度: bf16 |
| Qwen/Qwen3.5-122B-A10B | Qwen | moe | 262144 | 参数: --enable-prefix-caching；参数: --max-model-len；参数: --speculative-config；参数: --tensor-parallel-size；可选特性: spec_decoding；可选特性: text_only |
| Qwen/Qwen3.5-27B | Qwen | dense | 262144 | 参数: --enable-prefix-caching；参数: --max-model-len；参数: --speculative-config；参数: --tensor-parallel-size；可选特性: spec_decoding；可选特性: text_only |
| Qwen/Qwen3.5-2B | Qwen | dense | 262144 | 参数: --max-model-len；可选特性: spec_decoding；可选特性: text_only；特性: reasoning；特性: spec_decoding；特性: tool_calling |
| Qwen/Qwen3.5-35B-A3B | Qwen | moe | 262144 | 参数: --max-model-len；参数: --speculative-config；参数: --tensor-parallel-size；可选特性: spec_decoding；可选特性: text_only；特性: prefix_caching |
| Qwen/Qwen3.5-397B-A17B | Qwen | moe | 262144 | 参数: --enable-prefix-caching；参数: --gpu-memory-utilization；参数: --kv-cache-dtype；参数: --max-model-len；参数: --speculative-config；参数: --tensor-parallel-size |
| Qwen/Qwen3.5-4B | Qwen | dense | 262144 | 参数: --max-model-len；参数: --speculative-config；可选特性: spec_decoding；可选特性: text_only；特性: reasoning；特性: spec_decoding |
| Qwen/Qwen3.5-9B | Qwen | dense | 262144 | 参数: --max-model-len；参数: --speculative-config；可选特性: spec_decoding；可选特性: text_only；特性: reasoning；特性: spec_decoding |
| Qwen/Qwen3.6-27B | Qwen | dense | 262144 | 参数: --enable-prefix-caching；参数: --max-model-len；参数: --speculative-config；参数: --tensor-parallel-size；可选特性: spec_decoding；可选特性: text_only |
| Qwen/Qwen3.6-35B-A3B | Qwen | moe | 262144 | 参数: --async-scheduling；参数: --gpu-memory-utilization；参数: --kv-cache-dtype；参数: --max-model-len；参数: --max-num-batched-tokens；参数: --max-num-seqs |
| stepfun-ai/Step-3.5-Flash | StepFun | moe | 262144 | 参数: --data-parallel-size；参数: --speculative-config；参数: --tensor-parallel-size；可选特性: spec_decoding；特性: reasoning；特性: spec_decoding |
| stepfun-ai/Step-3.7-Flash | StepFun | moe | 262144 | 参数: --async-scheduling；参数: --gpu-memory-utilization；参数: --kv-cache-dtype；参数: --speculative-config；参数: --tensor-parallel-size；可选特性: spec_decoding |
| tencent/Hy3-preview | Hunyuan (Tencent) | moe | 262144 | 参数: --gpu-memory-utilization；参数: --no-enable-prefix-caching；参数: --speculative-config；参数: --tensor-parallel-size；可选特性: spec_decoding；特性: prefix_caching |
| XiaomiMiMo/MiMo-V2-Flash | MiMo (Xiaomi) | moe | 262144 | 参数: --data-parallel-size；参数: --gpu-memory-utilization；参数: --max-model-len；参数: --max-num-batched-tokens；参数: --tensor-parallel-size；特性: reasoning |
| XiaomiMiMo/MiMo-V2.5 | MiMo (Xiaomi) | moe | 1048576 | 参数: --gpu-memory-utilization；参数: --max-model-len；参数: --max-num-batched-tokens；参数: --no-enable-prefix-caching；参数: --tensor-parallel-size；可选特性: spec_decoding |
| XiaomiMiMo/MiMo-V2.5-Pro | MiMo (Xiaomi) | moe | 1048576 | 参数: --gpu-memory-utilization；参数: --max-model-len；参数: --tensor-parallel-size；可选特性: spec_decoding；特性: reasoning；特性: spec_decoding |
| zai-org/GLM-4.5 | GLM (Z-AI) | moe | 131072 | 参数: --gpu-memory-utilization；参数: --max-model-len；参数: --max-num-batched-tokens；参数: --no-enable-prefix-caching；参数: --speculative-config；参数: --tensor-parallel-size |
| zai-org/GLM-4.6 | GLM (Z-AI) | moe | 202752 | 参数: --gpu-memory-utilization；参数: --max-model-len；参数: --max-num-batched-tokens；参数: --speculative-config；参数: --tensor-parallel-size；可选特性: spec_decoding |
| zai-org/GLM-4.6V | GLM (Z-AI) | moe | 131072 | 参数: --gpu-memory-utilization；参数: --max-model-len；参数: --max-num-batched-tokens；参数: --tensor-parallel-size；可选特性: text_only；特性: reasoning |
| zai-org/GLM-4.7 | GLM (Z-AI) | moe | 202752 | 参数: --gpu-memory-utilization；参数: --kv-cache-dtype；参数: --max-model-len；参数: --max-num-batched-tokens；参数: --no-enable-prefix-caching；参数: --speculative-config |
| zai-org/GLM-5 | GLM (Z-AI) | moe | 202752 | 参数: --kv-cache-dtype；参数: --speculative-config；参数: --tensor-parallel-size；可选特性: spec_decoding；特性: reasoning；特性: spec_decoding |
| zai-org/GLM-5.1 | GLM (Z-AI) | moe | 202752 | 参数: --kv-cache-dtype；参数: --speculative-config；参数: --tensor-parallel-size；可选特性: spec_decoding；特性: reasoning；特性: spec_decoding |
| zai-org/GLM-GA | GLM (Z-AI) | dense | 131072 | 参数: --gpu-memory-utilization；参数: --max-model-len；参数: --max-num-batched-tokens；可选特性: text_only；策略: 单机 Tensor Parallel (TP)；策略: 多机 TP |
| zai-org/GLM-OCR | GLM (Z-AI) | dense | 131072 | 参数: --speculative-config；可选特性: encoder_parallel；可选特性: text_only；特性: spec_decoding；策略: 单机 Tensor Parallel (TP)；策略: 多机 TP |
| zai-org/Glyph | GLM (Z-AI) | dense | 131072 | 参数: --max-num-batched-tokens；参数: --no-enable-prefix-caching；可选特性: encoder_parallel；可选特性: text_only；特性: prefix_caching；特性: reasoning |

## 多模态模型

模型数量：**48**

### 该类常见优化方法（从高到低）

- 策略: 单机 Tensor Parallel (TP)（48）: 例子 google/gemma-4-12B-it, google/gemma-4-26B-A4B-it, google/gemma-4-31B-it
- 策略: 多机 TP（45）: 例子 google/gemma-4-12B-it, google/gemma-4-26B-A4B-it, google/gemma-4-31B-it
- 精度: bf16（41）: 例子 google/gemma-4-12B-it, google/gemma-4-26B-A4B-it, google/gemma-4-31B-it
- 可选特性: text_only（39）: 例子 google/gemma-4-26B-A4B-it, google/gemma-4-31B-it, google/gemma-4-E2B-it
- 参数: --max-model-len（33）: 例子 google/gemma-4-12B-it, google/gemma-4-26B-A4B-it, google/gemma-4-31B-it
- 特性: tool_calling（30）: 例子 google/gemma-4-12B-it, google/gemma-4-26B-A4B-it, google/gemma-4-31B-it
- 特性: reasoning（28）: 例子 google/gemma-4-12B-it, google/gemma-4-26B-A4B-it, google/gemma-4-31B-it
- 量化/精度: fp8（25）: 例子 google/gemma-4-12B-it, google/gemma-4-26B-A4B-it, google/gemma-4-31B-it
- 参数: --tensor-parallel-size（24）: 例子 google/gemma-4-26B-A4B-it, google/gemma-4-31B-it, Qwen/Qwen2.5-VL-72B-Instruct
- 参数: --gpu-memory-utilization（23）: 例子 google/gemma-4-12B-it, google/gemma-4-26B-A4B-it, google/gemma-4-31B-it
- 特性: spec_decoding（22）: 例子 google/gemma-4-12B-it, google/gemma-4-26B-A4B-it, google/gemma-4-31B-it
- 可选特性: spec_decoding（19）: 例子 google/gemma-4-12B-it, google/gemma-4-26B-A4B-it, google/gemma-4-31B-it
- 参数: --speculative-config（16）: 例子 google/gemma-4-12B-it, google/gemma-4-26B-A4B-it, google/gemma-4-31B-it
- 策略: 多机 TEP（16）: 例子 google/gemma-4-26B-A4B-it, Qwen/Qwen3-VL-235B-A22B-Instruct, Qwen/Qwen3.5-122B-A10B
- 策略: 多机 DEP（16）: 例子 google/gemma-4-26B-A4B-it, Qwen/Qwen3-VL-235B-A22B-Instruct, Qwen/Qwen3.5-122B-A10B
- 特性: prefix_caching（16）: 例子 PaddlePaddle/PaddleOCR-VL-1.5, PaddlePaddle/PaddleOCR-VL, Qwen/Qwen2.5-VL-72B-Instruct
- 参数: --kv-cache-dtype（14）: 例子 google/gemma-4-12B-it, google/gemma-4-26B-A4B-it, google/gemma-4-31B-it
- 环境优化: VLLM_ROCM_USE_AITER（14）: 例子 Qwen/Qwen2.5-VL-72B-Instruct, Qwen/Qwen3-ASR-1.7B, Qwen/Qwen3.6-35B-A3B
- 量化/精度: nvfp4（13）: 例子 google/gemma-4-26B-A4B-it, google/gemma-4-31B-it, Qwen/Qwen3-VL-235B-A22B-Instruct
- 策略: 单机 Tensor+Expert Parallel (TEP)（13）: 例子 google/gemma-4-26B-A4B-it, Qwen/Qwen3-VL-235B-A22B-Instruct, Qwen/Qwen3.5-122B-A10B
- 可选特性: encoder_parallel（13）: 例子 OpenGVLab/InternVL3_5-8B, PaddlePaddle/PaddleOCR-VL-1.5, PaddlePaddle/PaddleOCR-VL
- 参数: --no-enable-prefix-caching（13）: 例子 PaddlePaddle/PaddleOCR-VL-1.5, PaddlePaddle/PaddleOCR-VL, Qwen/Qwen2.5-VL-72B-Instruct
- 参数: --max-num-batched-tokens（13）: 例子 PaddlePaddle/PaddleOCR-VL-1.5, PaddlePaddle/PaddleOCR-VL, Qwen/Qwen3.6-35B-A3B
- 量化/精度: int4（12）: 例子 google/gemma-4-12B-it, google/gemma-4-31B-it, google/gemma-4-E2B-it

### 该类模型清单

| 模型 | Provider | 架构 | 上下文长度 | 关键优化方法（节选） |
| --- | --- | --- | --- | --- |
| baidu/ERNIE-4.5-VL-28B-A3B-PT | Ernie (Baidu) | moe | 131072 | 参数: --cpu-offload-gb；参数: --gpu-memory-utilization；参数: --tensor-parallel-size；可选特性: text_only；策略: 单机 Tensor Parallel (TP)；策略: 多机 DEP |
| deepseek-ai/DeepSeek-OCR | DeepSeek | dense | 8192 | 参数: --no-enable-prefix-caching；可选特性: encoder_parallel；可选特性: text_only；特性: prefix_caching；环境优化: VLLM_ROCM_USE_AITER；策略: 单机 Tensor Parallel (TP) |
| deepseek-ai/DeepSeek-OCR-2 | DeepSeek | dense | 8192 | 参数: --no-enable-prefix-caching；可选特性: encoder_parallel；可选特性: text_only；特性: prefix_caching；策略: 单机 Tensor Parallel (TP)；策略: 多机 TP |
| google/gemma-4-12B-it | Google | dense | 131072 | 参数: --async-scheduling；参数: --disable_chunked_mm_input；参数: --gpu-memory-utilization；参数: --kv-cache-dtype；参数: --max-model-len；参数: --speculative-config |
| google/gemma-4-26B-A4B-it | Google | moe | 131072 | 参数: --async-scheduling；参数: --disable_chunked_mm_input；参数: --gpu-memory-utilization；参数: --kv-cache-dtype；参数: --max-model-len；参数: --max-num-seqs |
| google/gemma-4-31B-it | Google | dense | 262144 | 参数: --async-scheduling；参数: --disable_chunked_mm_input；参数: --gpu-memory-utilization；参数: --kv-cache-dtype；参数: --max-model-len；参数: --max-num-seqs |
| google/gemma-4-E2B-it | Google | dense | 131072 | 参数: --async-scheduling；参数: --disable_chunked_mm_input；参数: --gpu-memory-utilization；参数: --kv-cache-dtype；参数: --max-model-len；参数: --speculative-config |
| google/gemma-4-E4B-it | Google | dense | 131072 | 参数: --async-scheduling；参数: --disable_chunked_mm_input；参数: --gpu-memory-utilization；参数: --kv-cache-dtype；参数: --max-model-len；参数: --speculative-config |
| internlm/Intern-S1 | InternLM | moe | 65536 | 参数: --gpu-memory-utilization；参数: --tensor-parallel-size；可选特性: text_only；特性: reasoning；特性: tool_calling；环境优化: VLLM_ROCM_USE_AITER |
| internlm/Intern-S2-Preview | InternLM | moe | 262144 | 参数: --gpu-memory-utilization；参数: --max-model-len；参数: --speculative-config；参数: --tensor-parallel-size；可选特性: spec_decoding；可选特性: text_only |
| microsoft/Phi-4-mini-instruct | Microsoft | dense | 131072 | 参数: --max-model-len；可选特性: encoder_parallel；可选特性: text_only；策略: 单机 Tensor Parallel (TP)；策略: 多机 TP；精度: bf16 |
| mistralai/Ministral-3-14B-Instruct-2512 | Mistral AI | dense | 262144 | 参数: --gpu-memory-utilization；参数: --kv-cache-dtype；参数: --max-model-len；参数: --max-num-batched-tokens；参数: --max-num-seqs；参数: --tensor-parallel-size |
| mistralai/Ministral-3-8B-Reasoning-2512 | Mistral AI | dense | 262144 | 参数: --max-model-len；参数: --no-enable-prefix-caching；参数: --tensor-parallel-size；可选特性: encoder_parallel；可选特性: text_only；特性: reasoning |
| mistralai/Mistral-Large-3-675B-Instruct-2512 | Mistral AI | moe | 294912 | 参数: --kv-cache-dtype；参数: --max-model-len；参数: --max-num-batched-tokens；参数: --no-enable-prefix-caching；参数: --tensor-parallel-size；可选特性: text_only |
| mistralai/Mistral-Medium-3.5-128B | Mistral AI | dense | 262144 | 参数: --gpu-memory-utilization；参数: --max-model-len；参数: --max-num-batched-tokens；参数: --no-enable-prefix-caching；参数: --speculative_config；参数: --tensor-parallel-size |
| mistralai/Mistral-Small-4-119B-2603 | Mistral AI | moe | 262144 | 参数: --max-model-len；参数: --no-enable-prefix-caching；参数: --speculative_config；参数: --tensor-parallel-size；可选特性: spec_decoding；特性: reasoning |
| mistralai/Voxtral-Mini-4B-Realtime-2602 | Mistral AI | dense | 131072 | 参数: --max-model-len；参数: --max-num-batched-tokens；策略: 单机 Tensor Parallel (TP)；策略: 多机 TP；精度: bf16 |
| moonshotai/Kimi-K2.5 | Moonshot AI | moe | 262144 | 参数: --gpu-memory-utilization；参数: --kv-cache-dtype；可选特性: text_only；特性: reasoning；特性: spec_decoding；特性: tool_calling |
| moonshotai/Kimi-K2.6 | Moonshot AI | moe | 262144 | 参数: --gpu-memory-utilization；参数: --kv-cache-dtype；可选特性: text_only；特性: reasoning；特性: spec_decoding；特性: tool_calling |
| nvidia/Nemotron-3-Nano-Omni-30B-A3B-Reasoning-BF16 | NVIDIA | moe | 262144 | 参数: --gpu-memory-utilization；参数: --kv-cache-dtype；参数: --max-model-len；参数: --max-num-seqs；参数: --tensor-parallel-size；特性: reasoning |
| nvidia/NVIDIA-Nemotron-Nano-12B-v2-VL-BF16 | NVIDIA | dense | 131072 | 参数: --data-parallel-size；参数: --max-model-len；可选特性: encoder_parallel；可选特性: text_only；策略: 单机 Tensor Parallel (TP)；策略: 多机 TP |
| openbmb/MiniCPM-V-4.6 | MiniCPM (OpenBMB) | dense | 262144 | 参数: --max-model-len；特性: tool_calling；策略: 单机 Tensor Parallel (TP)；策略: 多机 TP；精度: bf16 |
| OpenGVLab/InternVL3_5-8B | InternVL (OpenGVLab) | dense | 40960 | 可选特性: encoder_parallel；可选特性: text_only；策略: 单机 Tensor Parallel (TP)；策略: 多机 TP；精度: bf16 |
| PaddlePaddle/PaddleOCR-VL | PaddlePaddle | dense | 131072 | 参数: --max-num-batched-tokens；参数: --no-enable-prefix-caching；可选特性: encoder_parallel；可选特性: text_only；特性: prefix_caching；策略: 单机 Tensor Parallel (TP) |
| PaddlePaddle/PaddleOCR-VL-1.5 | PaddlePaddle | dense | 131072 | 参数: --max-num-batched-tokens；参数: --no-enable-prefix-caching；可选特性: encoder_parallel；可选特性: text_only；特性: prefix_caching；策略: 单机 Tensor Parallel (TP) |
| Qwen/Qwen2.5-VL-72B-Instruct | Qwen | dense | 128000 | 参数: --data-parallel-size；参数: --gpu-memory-utilization；参数: --max-model-len；参数: --no-enable-prefix-caching；参数: --tensor-parallel-size；可选特性: text_only |
| Qwen/Qwen2.5-VL-7B-Instruct | Qwen | dense | 128000 | 参数: --data-parallel-size；参数: --gpu-memory-utilization；参数: --max-model-len；参数: --no-enable-prefix-caching；参数: --pipeline-parallel-size；参数: --tensor-parallel-size |
| Qwen/Qwen3-ASR-1.7B | Qwen | dense | 65536 | 环境优化: VLLM_ROCM_USE_AITER；策略: 单机 Tensor Parallel (TP)；策略: 多机 TP；精度: bf16 |
| Qwen/Qwen3-VL-235B-A22B-Instruct | Qwen | moe | 262144 | 参数: --async-scheduling；参数: --gpu-memory-utilization；参数: --kv-cache-dtype；参数: --max-model-len；参数: --max-num-seqs；参数: --tensor-parallel-size |
| Qwen/Qwen3.5-0.8B | Qwen | dense | 262144 | 参数: --max-model-len；可选特性: text_only；特性: reasoning；特性: tool_calling；策略: 单机 Tensor Parallel (TP)；精度: bf16 |
| Qwen/Qwen3.5-122B-A10B | Qwen | moe | 262144 | 参数: --enable-prefix-caching；参数: --max-model-len；参数: --speculative-config；参数: --tensor-parallel-size；可选特性: spec_decoding；可选特性: text_only |
| Qwen/Qwen3.5-27B | Qwen | dense | 262144 | 参数: --enable-prefix-caching；参数: --max-model-len；参数: --speculative-config；参数: --tensor-parallel-size；可选特性: spec_decoding；可选特性: text_only |
| Qwen/Qwen3.5-2B | Qwen | dense | 262144 | 参数: --max-model-len；可选特性: spec_decoding；可选特性: text_only；特性: reasoning；特性: spec_decoding；特性: tool_calling |
| Qwen/Qwen3.5-35B-A3B | Qwen | moe | 262144 | 参数: --max-model-len；参数: --speculative-config；参数: --tensor-parallel-size；可选特性: spec_decoding；可选特性: text_only；特性: prefix_caching |
| Qwen/Qwen3.5-397B-A17B | Qwen | moe | 262144 | 参数: --enable-prefix-caching；参数: --gpu-memory-utilization；参数: --kv-cache-dtype；参数: --max-model-len；参数: --speculative-config；参数: --tensor-parallel-size |
| Qwen/Qwen3.5-4B | Qwen | dense | 262144 | 参数: --max-model-len；参数: --speculative-config；可选特性: spec_decoding；可选特性: text_only；特性: reasoning；特性: spec_decoding |
| Qwen/Qwen3.5-9B | Qwen | dense | 262144 | 参数: --max-model-len；参数: --speculative-config；可选特性: spec_decoding；可选特性: text_only；特性: reasoning；特性: spec_decoding |
| Qwen/Qwen3.6-27B | Qwen | dense | 262144 | 参数: --enable-prefix-caching；参数: --max-model-len；参数: --speculative-config；参数: --tensor-parallel-size；可选特性: spec_decoding；可选特性: text_only |
| Qwen/Qwen3.6-35B-A3B | Qwen | moe | 262144 | 参数: --async-scheduling；参数: --gpu-memory-utilization；参数: --kv-cache-dtype；参数: --max-model-len；参数: --max-num-batched-tokens；参数: --max-num-seqs |
| stepfun-ai/Step-3.7-Flash | StepFun | moe | 262144 | 参数: --async-scheduling；参数: --gpu-memory-utilization；参数: --kv-cache-dtype；参数: --speculative-config；参数: --tensor-parallel-size；可选特性: spec_decoding |
| tencent/HunyuanOCR | Hunyuan (Tencent) | dense | 32768 | 参数: --max-num-batched-tokens；参数: --no-enable-prefix-caching；可选特性: encoder_parallel；可选特性: text_only；特性: prefix_caching；策略: 单机 Tensor Parallel (TP) |
| XiaomiMiMo/MiMo-V2.5 | MiMo (Xiaomi) | moe | 1048576 | 参数: --gpu-memory-utilization；参数: --max-model-len；参数: --max-num-batched-tokens；参数: --no-enable-prefix-caching；参数: --tensor-parallel-size；可选特性: spec_decoding |
| zai-org/GLM-4.5V | GLM (Z-AI) | moe | 65536 | 参数: --gpu-memory-utilization；参数: --max-model-len；参数: --max-num-batched-tokens；参数: --tensor-parallel-size；可选特性: text_only；特性: reasoning |
| zai-org/GLM-4.6V | GLM (Z-AI) | moe | 131072 | 参数: --gpu-memory-utilization；参数: --max-model-len；参数: --max-num-batched-tokens；参数: --tensor-parallel-size；可选特性: text_only；特性: reasoning |
| zai-org/GLM-ASR-Nano-2512 | GLM (Z-AI) | dense | 8192 | 策略: 单机 Tensor Parallel (TP)；策略: 多机 TP；精度: bf16 |
| zai-org/GLM-GA | GLM (Z-AI) | dense | 131072 | 参数: --gpu-memory-utilization；参数: --max-model-len；参数: --max-num-batched-tokens；可选特性: text_only；策略: 单机 Tensor Parallel (TP)；策略: 多机 TP |
| zai-org/GLM-OCR | GLM (Z-AI) | dense | 131072 | 参数: --speculative-config；可选特性: encoder_parallel；可选特性: text_only；特性: spec_decoding；策略: 单机 Tensor Parallel (TP)；策略: 多机 TP |
| zai-org/Glyph | GLM (Z-AI) | dense | 131072 | 参数: --max-num-batched-tokens；参数: --no-enable-prefix-caching；可选特性: encoder_parallel；可选特性: text_only；特性: prefix_caching；特性: reasoning |

## Embedding / Reranker 模型

模型数量：**2**

### 该类常见优化方法（从高到低）

- 策略: 单机 Tensor Parallel (TP)（2）: 例子 jinaai/jina-embeddings-v5-text-small, jinaai/jina-reranker-m0
- 精度: bf16（2）: 例子 jinaai/jina-embeddings-v5-text-small, jinaai/jina-reranker-m0
- 环境优化: VLLM_ROCM_USE_AITER（1）: 例子 jinaai/jina-reranker-m0
- 策略: 多机 TP（1）: 例子 jinaai/jina-reranker-m0
- 量化/精度: fp8（1）: 例子 jinaai/jina-reranker-m0
- 参数: --gpu-memory-utilization（1）: 例子 jinaai/jina-reranker-m0
- 参数: --max-num-seqs（1）: 例子 jinaai/jina-reranker-m0

### 该类模型清单

| 模型 | Provider | 架构 | 上下文长度 | 关键优化方法（节选） |
| --- | --- | --- | --- | --- |
| jinaai/jina-embeddings-v5-text-small | Jina AI | dense | 32768 | 策略: 单机 Tensor Parallel (TP)；精度: bf16 |
| jinaai/jina-reranker-m0 | Jina AI | dense | 32768 | 参数: --gpu-memory-utilization；参数: --max-num-seqs；环境优化: VLLM_ROCM_USE_AITER；策略: 单机 Tensor Parallel (TP)；策略: 多机 TP；精度: bf16 |

## 全局优化方法覆盖度

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
- 特性: spec_decoding: 39
- 可选特性: text_only: 39
- 策略: 单机 Data+Expert Parallel (DEP): 37
- 可选特性: spec_decoding: 35
- 参数: --max-num-batched-tokens: 33
- 量化/精度: nvfp4: 33
- 策略: Prefill/Decode 解耦集群 (PD): 33
- 参数: --speculative-config: 28
- 参数: --no-enable-prefix-caching: 28
- 特性: prefix_caching: 28
- 参数: --max-num-seqs: 19
- 参数: --async-scheduling: 17
- 参数: --data-parallel-size: 16
- 量化/精度: int4: 15
- 可选特性: encoder_parallel: 13
- 参数: --compilation-config: 9
- 环境优化: VLLM_ROCM_USE_AITER_MOE: 7
- 参数: --disable_chunked_mm_input: 5
- 参数: --enable-prefix-caching: 5
- 环境优化: VLLM_USE_FLASHINFER_MOE_FP8: 5
- 参数: --enforce-eager: 4
- 参数: --pipeline-parallel-size: 3
- 参数: --speculative_config: 3
- 环境优化: VLLM_ROCM_USE_AITER_RMSNORM: 3
- 参数: --enable-flashinfer-autotune: 2
