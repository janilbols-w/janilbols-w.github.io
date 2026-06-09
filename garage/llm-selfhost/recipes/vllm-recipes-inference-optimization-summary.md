---
title: vLLM Recipes Inference Optimization Summary
---

# vLLM Recipes 推理优化 Summary（去重 + 可操作 Recipe）

扫描模型：**115**；Provider：**29**。

## 统计口径（先去重）

- 口径 1：同义参数合并。
	- `--speculative_config` 与 `--speculative-config` 视为同一参数。
- 口径 2：同一 feature 的“特性/可选特性”标签合并。
	- 例如 `特性: spec_decoding` 与 `可选特性: spec_decoding` 合并计数。
- 口径 3：组合开关按一个配置项统计。
	- 例如 `spec_decoding` 需要 `--speculative-config + feature 开关`，按 1 个 feature 配置计算。
	- 例如 `prefix_caching` 的开/关（`--enable-prefix-caching` / `--no-enable-prefix-caching`）按 1 个 feature 配置计算。

## 配置指令使用频次（去重后排序）

以下优先采用全局汇总统计（按模型级统计），可直接作为“默认调参优先级”。

### A. 并行与部署策略（高优先级）

1. 策略: 单机 Tensor Parallel (TP)（107） -> `--tensor-parallel-size <TP>`
2. 策略: 多机 TP（95） -> `--tensor-parallel-size <TP>`（跨机部署）
3. 策略: 多机 DEP（52） -> `--data-parallel-size <DP>` + 跨机 DP 参数
4. 策略: 多机 TEP（51） -> `--enable-expert-parallel` + TP/DP 参数
5. 策略: 多机 TP+PP (Pipeline Parallel)（47） -> `--tensor-parallel-size <TP>` + `--pipeline-parallel-size <PP>`
6. 策略: 单机 Tensor+Expert Parallel (TEP)（43） -> `--tensor-parallel-size <TP>` + `--enable-expert-parallel`

### A-1. 策略参数映射（可复制）

#### 1) 单机 TP

```bash
vllm serve <model> \
	--tensor-parallel-size <TP>
```

#### 2) 多机 TP（最小骨架）

```bash
vllm serve <model> \
	--tensor-parallel-size <TP> \
	--distributed-executor-backend <ray|mp>
```

#### 3) 单机 TEP（TP+EP）

```bash
vllm serve <model> \
	--tensor-parallel-size <TP> \
	--enable-expert-parallel
```

#### 4) 多机 DEP+EP（双节点示例）

```bash
# node 0
vllm serve <model> \
	--data-parallel-size <GLOBAL_DP> \
	--data-parallel-size-local <LOCAL_DP> \
	--data-parallel-address <MASTER_IP> \
	--data-parallel-rpc-port <PORT> \
	--enable-expert-parallel

# node 1+
vllm serve <model> \
	--headless \
	--data-parallel-start-rank <START_RANK> \
	--data-parallel-size <GLOBAL_DP> \
	--data-parallel-size-local <LOCAL_DP> \
	--data-parallel-address <MASTER_IP> \
	--data-parallel-rpc-port <PORT> \
	--enable-expert-parallel
```

#### 5) TP+PP

```bash
vllm serve <model> \
	--tensor-parallel-size <TP> \
	--pipeline-parallel-size <PP>
```

#### 6) PD（Prefill/Decode 解耦）

```bash
# Prefill 服务
vllm serve <model> \
	--port 8000 \
	--data-parallel-size <DP_PREFILL> \
	--enable-expert-parallel \
	--kv-transfer-config '{"kv_connector":"MooncakeConnector","kv_role":"kv_both"}'

# Decode 服务
vllm serve <model> \
	--port 8001 \
	--data-parallel-size <DP_DECODE> \
	--enable-expert-parallel \
	--kv-transfer-config '{"kv_connector":"MooncakeConnector","kv_role":"kv_both"}'

# Router
vllm-router --vllm-pd-disaggregation \
	--prefill http://localhost:8000 \
	--decode http://localhost:8001
```

### B. 核心参数与精度（高频）

1. 精度: bf16（88）
2. 参数: --tensor-parallel-size（72）
3. 量化/精度: fp8（68）
4. 参数: --max-model-len（66）
5. 参数: --gpu-memory-utilization（50）
6. 参数: --kv-cache-dtype（44）
7. 环境优化: VLLM_ROCM_USE_AITER（39）

### C. Feature 开关（按 feature 去重后）

1. tool_calling（69）
2. reasoning（59）
3. spec_decoding（合并特性/可选特性；组合配置）
4. prefix_caching（合并开/关参数；互斥配置）
5. text_only（多模态降级为纯文本）
6. encoder_parallel（多模态编码并行）

## 可直接上手的 Recipe（按落地顺序）

### Step 1: 建立稳定基线（先跑通）

```bash
vllm serve <model> \
	--dtype bf16 \
	--tensor-parallel-size <tp> \
	--max-model-len <context_len> \
	--gpu-memory-utilization 0.90
```

建议：先单机 TP（常见起点），再扩展到多机 TP。

### Step 2: 长上下文与显存控制

```bash
vllm serve <model> \
	--max-model-len <context_len> \
	--kv-cache-dtype <bf16|fp8_e4m3|fp8_e5m2> \
	--max-num-batched-tokens <tokens> \
	--max-num-seqs <seqs>
```

建议：长上下文优先调 `--max-model-len` 与 `--kv-cache-dtype`，并结合批量并发参数控制 P99。

### Step 3: MoE/超大模型并行拓扑

- 单机 TP：`--tensor-parallel-size <TP>`
- 单机 TEP：`--tensor-parallel-size <TP> --enable-expert-parallel`
- 多机 DEP：`--data-parallel-size <DP> --data-parallel-size-local <LOCAL_DP> --data-parallel-address <MASTER_IP> --data-parallel-rpc-port <PORT>`
- 多机 TEP：`--enable-expert-parallel` + `--tensor-parallel-size <TP>` 或 `--data-parallel-size <DP>`
- 多机 TP+PP：`--tensor-parallel-size <TP> --pipeline-parallel-size <PP>`
- PD 解耦：两套服务分别启动并使用 `--kv-transfer-config <JSON>`，再由 `vllm-router --vllm-pd-disaggregation` 汇聚。

### Step 4: 精度与量化路径

- 默认：bf16。
- 追求吞吐/显存：fp8（必要时结合平台优化，如 AITER）。
- 特定模型可选：int4 / nvfp4（需结合模型支持矩阵）。

## Feature 开关配置清单（组合算一个配置）

### 1) tool_calling

- 作用：函数调用/工具调用链路。
- 最小可用参数（通用形态）：
	- `--enable-auto-tool-choice`
	- `--tool-call-parser <parser_name>`
	- 可选：`--chat-template <template_path>`
- 可复制模板：

```bash
vllm serve <model> \
	--enable-auto-tool-choice \
	--tool-call-parser <parser_name> \
	--chat-template <template_path>
```

### 2) reasoning

- 作用：思考型/推理型输出路径。
- 最小可用参数：`--reasoning-parser <parser_name>`
- 关闭 thinking（按需）：`--default-chat-template-kwargs '{"enable_thinking": false}'`
- 可复制模板：

```bash
vllm serve <model> \
	--reasoning-parser <parser_name>
```

### 3) spec_decoding（组合配置）

- 组合项：`feature: spec_decoding` + `--speculative-config`。
- 作用：降低首 token 延迟/提升吞吐（模型与草稿策略相关）。
- 最小可用参数：`--speculative-config '{"method":"mtp","num_speculative_tokens":<N>}'`
- 可复制模板：

```bash
vllm serve <model_or_fp8_model> \
	--speculative-config '{"method":"mtp","num_speculative_tokens":4}'
```

### 4) prefix_caching（互斥配置）

- 组合项（视作一个 feature 配置）：
	- 开：`--enable-prefix-caching`
	- 关：`--no-enable-prefix-caching`
- 作用：复用前缀以降低重复上下文开销。
- 可复制模板：

```bash
# 开启
vllm serve <model> --enable-prefix-caching

# 关闭
vllm serve <model> --no-enable-prefix-caching
```

### 5) text_only（多模态降级）

- 作用：把多模态模型以纯文本路径运行。
- 最小可用参数：`--language-model-only`
- 可复制模板：

```bash
vllm serve <multimodal_model> \
	--language-model-only
```

### 6) encoder_parallel（多模态编码并行）

- 作用：提升视觉/音频编码阶段吞吐。
- 最小可用参数：`--mm-encoder-tp-mode data`
- 与 `text_only` 互斥，不可同时开启。
- 可复制模板：

```bash
vllm serve <multimodal_model> \
	--mm-encoder-tp-mode data
```

## 一页式执行顺序（推荐）

1. 先定并行策略：单机 TP 起步，容量不足再上多机 TP/DEP/TEP/TP+PP。
2. 再定精度路径：bf16 基线，瓶颈明显时切 fp8。
3. 再调上下文与 KV：`--max-model-len` + `--kv-cache-dtype`。
4. 再调并发：`--max-num-batched-tokens` + `--max-num-seqs`。
5. 最后开 feature：按业务需要启用 tool_calling/reasoning/spec_decoding/prefix_caching/text_only/encoder_parallel。

## 产出文件

- 详细汇总：`garage/llm-selfhost/recipes/vllm-recipes-inference-optimization-by-model.md`
- 精简总结：`garage/llm-selfhost/recipes/vllm-recipes-inference-optimization-summary.md`