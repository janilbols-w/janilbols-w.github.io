# MaaS 功能分类与典型项目

> 从功能维度对 MaaS 进行分层拆解，覆盖从底层推理到上层应用的完整功能栈。
>
> 最后更新：2026-05

---

## 功能全景图

> 完整交互式图示见 [maas-feature-landscape.drawio](maas-feature-landscape.drawio)（draw.io 格式，1700×1010，4层架构 + 11功能类别）

```
┌──────────────────────────────────────────────────────────────┬──────────────┐
│                   应用层 (Application)                        │              │
│  〔8〕RAG&知识库  〔9〕Agent&工作流  〔10〕多模态             │              │
├──────────────────────────────────────────────────────────────┤  〔11〕      │
│                   平台层 (Platform)                           │  部署        │
│  〔1〕API统一  〔3〕路由可靠性  〔4〕安全合规                 │  灵活性      │
│  〔5〕可观测性  〔6〕成本缓存  〔7〕模型微调                  │              │
├──────────────────────────────────────────────────────────────┤  公有云      │
│                   推理层 (Inference)                          │  私有化      │
│  〔2〕推理性能优化             本地运行工具                   │  混合云      │
├──────────────────────────────────────────────────────────────┤  边缘推理    │
│                   基础设施层 (Infrastructure)                 │  Serverless  │
│  模型市场 / Hub                GPU / 专用硬件 & 算力平台      │  K8s编排     │
└──────────────────────────────────────────────────────────────┴──────────────┘
```

---

## 1. 模型访问标准化（API Unification）

**核心问题**：不同提供商 API 格式不一，开发者需要适配多套 SDK。

**关键功能**：
- 统一 OpenAI 兼容格式（`/chat/completions`、`/embeddings`、`/images`）
- 多提供商透明路由，应用代码零改动切换模型
- 支持流式输出（SSE streaming）
- Function Calling / Tool Use 标准化

**典型项目**：

| 项目 | 定位 | 说明 |
|------|------|------|
| [LiteLLM](https://github.com/BerriAI/litellm) | Python SDK + Proxy | 支持 100+ 提供商，统一调用格式 |
| [One API](https://github.com/songquanpeng/one-api) | API 分发系统 | 统一 Key 管理，多渠道转发 |
| [Portkey Gateway](https://github.com/Portkey-AI/gateway) | AI Gateway | 支持 250+ LLM，<1ms 额外延迟 |
| [OpenRouter](https://openrouter.ai) | 云端聚合路由 | 200+ 模型统一 API |
| [Ollama](https://github.com/ollama/ollama) | 本地推理 | 本地模型的 OpenAI 兼容 API |

---

## 2. 推理性能优化（Inference Optimization）

**核心问题**：LLM 推理延迟高、吞吐量低、GPU 利用率不足。

**关键功能**：
- **连续批处理**（Continuous Batching）：动态合并请求，提升 GPU 利用率
- **KV Cache 管理**：PagedAttention（vLLM）、Chunked Prefill
- **投机解码**（Speculative Decoding）：小模型草稿 + 大模型验证
- **量化**（Quantization）：INT4/INT8/GPTQ/AWQ/GGUF
- **张量并行 / 流水线并行**：多卡分布式推理
- **前缀缓存**（Prefix Caching）：复用公共 system prompt 的 KV

**典型项目**：

| 项目 | 核心技术 | 适用场景 |
|------|---------|---------|
| [vLLM](https://github.com/vllm-project/vllm) | PagedAttention，连续批处理 | 高并发在线服务 |
| [SGLang](https://github.com/sgl-project/sglang) | RadixAttention，结构化生成 | 复杂推理，高吞吐 |
| [TGI](https://github.com/huggingface/text-generation-inference) | Flash Attention，张量并行 | HuggingFace 模型生产部署 |
| [TensorRT-LLM](https://github.com/NVIDIA/TensorRT-LLM) | TensorRT 图优化，INT8/FP8 | NVIDIA GPU 极致性能 |
| [LMDeploy](https://github.com/InternLM/lmdeploy) | TurboMind 引擎，AWQ | InternLM 系，国产优化 |
| [llama.cpp](https://github.com/ggerganov/llama.cpp) | GGUF 量化，CPU/Metal | 消费级硬件，本地推理 |
| [MLC LLM](https://github.com/mlc-ai/mlc-llm) | TVM 编译，跨平台 | 移动端/Web/桌面 |
| [PowerInfer](https://github.com/SJTU-IPADS/PowerInfer) | 稀疏激活 | 消费级单卡大模型 |
| [Cerebras Inference](https://inference.cerebras.ai) | 专用 WSE 芯片 | 超低延迟（~2000 token/s） |
| [Groq](https://groq.com) | LPU 专用硬件 | 全球最快商业推理 API |

---

## 3. 模型路由与可靠性（Routing & Reliability）

**核心问题**：单一提供商故障、高峰限流、成本差异大。

**关键功能**：
- **负载均衡**（Load Balancing）：多 Key / 多端点权重分发
- **自动重试**（Auto Retry）：指数退避，错误分类
- **故障转移**（Fallback）：主备模型切换（如 GPT-4o → Claude）
- **条件路由**（Conditional Routing）：按 prompt 类型、用户分组路由不同模型
- **请求超时管理**：防止长尾延迟影响 P99
- **健康检查**：定期探测渠道可用性

**典型项目**：

| 项目 | 路由能力 | 说明 |
|------|---------|------|
| [LiteLLM Proxy](https://docs.litellm.ai/docs/simple_proxy) | Fallback、负载均衡、重试 | 配置驱动，企业级 |
| [Portkey Gateway](https://github.com/Portkey-AI/gateway) | Config 级路由、Guardrails | 声明式 JSON 配置 |
| [One API](https://github.com/songquanpeng/one-api) | 渠道权重、自动禁用、测试 | 国内最常用 |
| [New API](https://github.com/Calcium-Ion/new-api) | One API 增强版 | 更多渠道，前端优化 |
| [Higress](https://github.com/alibaba/higress) | 云原生 AI 网关，WASM 插件 | 阿里云开源，K8s 原生 |

---

## 4. 安全与内容合规（Security & Guardrails）

**核心问题**：LLM 输出不可控、存在越狱/注入风险、企业合规要求高。

**关键功能**：
- **输入/输出过滤**（Guardrails）：关键词过滤、分类器检测
- **PII 脱敏**（PII Redaction）：自动检测并替换个人隐私信息
- **Prompt 注入防护**：检测恶意 prompt 劫持
- **内容安全**（Content Moderation）：暴力、色情、仇恨内容检测
- **API Key 安全**：虚拟 Key（Virtual Keys），权限隔离
- **网络隔离**：VPC、私有端点、IP 白名单
- **合规认证**：SOC2、HIPAA、GDPR、等保

**典型项目**：

| 项目 / 服务 | 类型 | 说明 |
|------------|------|------|
| [LlamaGuard](https://github.com/meta-llama/PurpleLlama) | 开源内容安全模型 | Meta 出品，多类别分类 |
| [NeMo Guardrails](https://github.com/NVIDIA/NeMo-Guardrails) | 开源对话护栏 | NVIDIA，对话流程约束 |
| [Portkey Guardrails](https://portkey.ai/docs/product/guardrails) | 40+ 内置规则 | 支持自定义 + 第三方 |
| [AWS Bedrock Guardrails](https://aws.amazon.com/bedrock/guardrails/) | 托管服务 | 内容过滤、话题屏蔽、PII |
| [Azure Content Safety](https://azure.microsoft.com/en-us/products/ai-services/ai-content-safety) | 托管服务 | 多模态内容审核 |
| [OpenAI Moderation API](https://platform.openai.com/docs/guides/moderation) | 免费 API | 基础内容分类 |
| [Rebuff](https://github.com/protectai/rebuff) | Prompt 注入检测 | 开源 |

---

## 5. 可观测性与监控（Observability & Monitoring）

**核心问题**：LLM 调用是黑盒，难以追踪性能、质量和成本。

**关键功能**：
- **请求日志**：完整 prompt/response 记录，可审计
- **指标监控**：延迟（TTFT、ITL）、吞吐量、错误率、Token 消耗
- **成本追踪**：按模型/用户/项目分摊费用
- **链路追踪**（Tracing）：多步 LLM 调用的端到端追踪
- **评估集成**（Evals）：在线/离线模型质量评估
- **告警**：阈值告警，异常检测

**典型项目**：

| 项目 | 类型 | 说明 |
|------|------|------|
| [Langfuse](https://github.com/langfuse/langfuse) | 开源 LLM 可观测性 | Trace、评估、Prompt 管理 |
| [Helicone](https://github.com/Helicone/helicone) | 开源 LLM 监控 | OpenAI 代理，零侵入 |
| [Phoenix (Arize)](https://github.com/Arize-ai/phoenix) | 开源 AI 可观测性 | Trace、Evals，本地部署 |
| [MLflow Tracing](https://mlflow.org/docs/latest/llms/tracing) | 开源 MLOps | 集成 LLM 追踪 |
| [Weights & Biases](https://wandb.ai) | 商业 MLOps | 实验追踪 + LLM 监控 |
| [LiteLLM 内置监控](https://docs.litellm.ai/docs/proxy/logging) | Proxy 内置 | Prometheus + Grafana 集成 |
| [One API 日志](https://github.com/songquanpeng/one-api) | Proxy 内置 | 消费明细，渠道统计 |
| [Datadog LLM Observability](https://www.datadoghq.com/product/llm-observability/) | 商业 APM | 企业级全栈可观测 |

---

## 6. 成本管理与缓存（Cost Management & Caching）

**核心问题**：LLM API 调用费用高，重复请求浪费严重。

**关键功能**：
- **语义缓存**（Semantic Caching）：相似 prompt 复用历史响应
- **精确缓存**（Exact Cache）：相同 prompt 直接命中
- **Token 预算管理**：按用户/项目设置调用限额
- **模型降级策略**：高峰期自动切换更便宜的模型
- **Prompt 压缩**（Prompt Compression）：减少输入 Token 数
- **批量推理**（Batch API）：离线任务批量提交，价格更低
- **费率倍率管理**：内部结算，不同用户组不同定价

**典型项目**：

| 项目 | 功能 | 说明 |
|------|------|------|
| [GPTCache](https://github.com/zilliztech/GPTCache) | 语义缓存 | Zilliz 出品，独立缓存层 |
| [LiteLLM Caching](https://docs.litellm.ai/docs/proxy/caching) | 精确 + 语义缓存 | Redis/S3 后端 |
| [LLMLingua](https://github.com/microsoft/LLMLingua) | Prompt 压缩 | 微软，压缩率 20x |
| [OpenAI Batch API](https://platform.openai.com/docs/guides/batch) | 批量推理 | 50% 折扣，24h 内返回 |
| [One API 倍率](https://github.com/songquanpeng/one-api) | 计费倍率 | 分组倍率，内部结算 |
| [Portkey Cost Tracking](https://portkey.ai/docs/product/observability/costs) | 成本分析 | 按虚拟 Key 追踪 |

---

## 7. 模型微调（Fine-tuning & Customization）

**核心问题**：通用模型在垂直领域效果不足，需要业务数据定制。

**关键功能**：
- **全量微调**（Full Fine-tuning）：更新全部权重
- **PEFT / LoRA**：参数高效微调，低显存需求
- **RLHF / DPO / GRPO**：基于反馈的对齐训练
- **数据管理**：训练集版本、标注工具集成
- **微调后评估**：自动 Benchmark + 人工评估
- **模型合并**（Model Merging）：多 LoRA 合并

**典型项目**：

| 项目 | 类型 | 说明 |
|------|------|------|
| [LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory) | 开源微调框架 | 100+ 模型，多种 PEFT 方法 |
| [Unsloth](https://github.com/unslothai/unsloth) | 开源微调框架 | 2x 速度，60% 显存节省 |
| [Axolotl](https://github.com/OpenAccess-AI-Collective/axolotl) | 开源微调框架 | 配置驱动，灵活 |
| [Swift](https://github.com/modelscope/swift) | 开源微调框架 | 魔搭社区，国产模型友好 |
| [OpenAI Fine-tuning](https://platform.openai.com/docs/guides/fine-tuning) | 云端托管 | GPT-4o mini 微调 |
| [Together Fine-tuning](https://www.together.ai/fine-tuning) | 云端托管 | 开源模型微调 API |
| [阿里云百炼微调](https://bailian.aliyun.com) | 云端托管 | Qwen 系列微调 |
| [Vertex AI Tuning](https://cloud.google.com/vertex-ai/generative-ai/docs/models/tune-models) | 云端托管 | Gemini 监督微调 |

---

## 8. 检索增强生成（RAG & Knowledge Base）

**核心问题**：LLM 知识截止，无法访问私有/实时数据。

**关键功能**：
- **文档解析**：PDF/Word/Excel/HTML 结构化提取
- **文本切块**（Chunking）：固定大小、语义切块、递归切块
- **向量化**（Embedding）：文本转向量，语义检索
- **向量数据库**：存储和检索向量
- **混合检索**：向量检索 + BM25 关键词检索
- **重排序**（Reranking）：Cross-Encoder 精排
- **引用溯源**：响应中标注知识来源

**典型项目**：

| 项目 | 类型 | 说明 |
|------|------|------|
| [RAGFlow](https://github.com/infiniflow/ragflow) | 开源 RAG 平台 | DeepDoc 深度文档解析 |
| [FastGPT](https://github.com/labring/FastGPT) | 开源 RAG 平台 | 知识库 + 工作流编排 |
| [AnythingLLM](https://github.com/Mintplex-Labs/anything-llm) | 开源 RAG 平台 | 多用户，私有部署 |
| [Dify](https://github.com/langgenius/dify) | LLMOps 平台 | RAG + Agent + 工作流 |
| [LlamaIndex](https://github.com/run-llama/llama_index) | RAG 框架 | 数据连接器，查询引擎 |
| [LangChain](https://github.com/langchain-ai/langchain) | RAG / Agent 框架 | 生态最丰富 |
| [Chroma](https://github.com/chroma-core/chroma) | 向量数据库 | 开源，轻量嵌入 |
| [Qdrant](https://github.com/qdrant/qdrant) | 向量数据库 | Rust，高性能 |
| [Milvus](https://github.com/milvus-io/milvus) | 向量数据库 | 分布式，生产级 |
| [Cohere Rerank](https://cohere.com/rerank) | 重排序 API | 商业 Reranker |
| [BGE-Reranker](https://huggingface.co/BAAI/bge-reranker-v2-m3) | 开源重排序 | 北京智源，多语言 |

---

## 9. Agent 与工作流编排（Agent & Workflow）

**核心问题**：单次 LLM 调用无法完成复杂任务，需要多步推理和工具调用。

**关键功能**：
- **Function Calling / Tool Use**：LLM 调用外部工具（搜索、代码执行、API）
- **MCP（Model Context Protocol）**：工具调用标准协议
- **多 Agent 协作**：角色分工，消息传递
- **可视化工作流**：拖拽编排 LLM 调用链
- **计划-执行循环**（ReAct / Plan-and-Execute）
- **记忆管理**：短期对话记忆 + 长期向量记忆
- **代码执行沙箱**：安全运行 LLM 生成的代码

**典型项目**：

| 项目 | 类型 | 说明 |
|------|------|------|
| [Dify](https://github.com/langgenius/dify) | 可视化 LLMOps | Agent + 工作流，低代码 |
| [Flowise](https://github.com/FlowiseAI/Flowise) | 可视化工作流 | LangChain 拖拽 UI |
| [Langflow](https://github.com/langflow-ai/langflow) | 可视化工作流 | DataStax 支持 |
| [AutoGen](https://github.com/microsoft/autogen) | 多 Agent 框架 | 微软，对话式多 Agent |
| [CrewAI](https://github.com/crewAIInc/crewAI) | 多 Agent 框架 | 角色扮演，任务协作 |
| [LangGraph](https://github.com/langchain-ai/langgraph) | Agent 编排 | 有向图状态机 |
| [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) | Agent 框架 | OpenAI 官方 |
| [Coze](https://www.coze.com) | 无代码 Agent 平台 | 字节跳动，Bot 构建 |
| [n8n](https://github.com/n8n-io/n8n) | 自动化工作流 | 含 AI 节点 |
| [AnythingLLM Agent](https://docs.anythingllm.com/agent) | 内置 Agent | 浏览器、代码执行等技能 |

---

## 10. 多模态能力（Multimodal）

**核心问题**：纯文本无法处理图像、语音、视频等业务场景。

**关键功能**：
- **视觉理解**（Vision）：图像输入 + 文本输出
- **文生图**（Text-to-Image）：Prompt 生成图像
- **语音转文字**（STT / ASR）
- **文字转语音**（TTS）
- **视频理解**：视频帧分析
- **文档 OCR + 理解**：PDF 图像解析

**典型项目**：

| 项目 / 服务 | 模态 | 说明 |
|------------|------|------|
| GPT-4o (OpenAI) | 文本 + 视觉 + 语音 | 全模态旗舰模型 |
| Gemini 2.5 (Google) | 文本 + 视觉 + 视频 + 代码 | 长上下文多模态 |
| Claude 3.5 (Anthropic) | 文本 + 视觉 | 强文档理解 |
| [Whisper](https://github.com/openai/whisper) | STT | OpenAI 开源，多语言 |
| [CosyVoice](https://github.com/FunAudioLLM/CosyVoice) | TTS | 阿里达摩院，自然语音合成 |
| [ElevenLabs](https://elevenlabs.io) | TTS | 商业，高拟真语音 |
| [Stable Diffusion](https://github.com/Stability-AI/stablediffusion) | 文生图 | 开源，生态最丰富 |
| [DALL-E 3](https://openai.com/dall-e-3) | 文生图 | OpenAI 商业 |
| [Flux](https://github.com/black-forest-labs/flux) | 文生图 | Black Forest Labs |
| [InternVL](https://github.com/OpenGVLab/InternVL) | 视觉语言模型 | 上海AI实验室开源 |
| [Qwen-VL](https://github.com/QwenLM/Qwen-VL) | 视觉语言模型 | 阿里开源 |

---

## 11. 部署灵活性（Deployment Flexibility）

**核心问题**：不同场景对数据主权、延迟、成本的要求差异巨大。

**关键功能**：
- **公有云 API**：按量付费，零运维
- **私有化部署**（On-premise）：数据不出域
- **混合云**（Hybrid）：敏感数据本地，通用能力上云
- **边缘推理**（Edge / On-device）：手机、IoT 设备
- **Serverless 推理**：按请求计费，无需管理 GPU
- **容器化 / Kubernetes 编排**：Helm Chart，弹性扩缩容

**典型项目**：

| 项目 | 部署模式 | 说明 |
|------|---------|------|
| [Ollama](https://ollama.com) | 本地 / 私有 | 最简单的本地部署 |
| [vLLM + Kubernetes](https://docs.vllm.ai/en/latest/serving/deploying_with_k8s.html) | 私有云 | 生产级弹性部署 |
| [NVIDIA NIM](https://build.nvidia.com) | 私有云 / 企业 | 容器化微服务，支持私有化 |
| [LM Studio](https://lmstudio.ai) | 桌面本地 | 开发者个人使用 |
| [MLC LLM](https://github.com/mlc-ai/mlc-llm) | 移动端 / Web | iOS/Android/Web 端侧推理 |
| [Xinference](https://github.com/xorbitsai/inference) | 私有集群 | 多框架后端，分布式 |
| [HuggingFace Inference Endpoints](https://huggingface.co/inference-endpoints) | 云端托管 | 一键私有端点 |
| [Replicate](https://replicate.com) | Serverless | 按请求计费 |
| [Modal](https://modal.com) | Serverless GPU | Python 原生，弹性 GPU |
| [RunPod](https://runpod.io) | GPU 云 | 低成本 GPU 租用 + 推理 |

---

## 功能-项目矩阵（快速参考）

| 项目 | API 统一 | 推理优化 | 路由可靠性 | 安全合规 | 可观测性 | 成本管理 | 微调 | RAG | Agent |
|------|:-------:|:-------:|:---------:|:-------:|:-------:|:-------:|:---:|:---:|:-----:|
| vLLM | — | ★★★ | — | — | — | — | — | — | — |
| SGLang | — | ★★★ | — | — | — | — | — | — | — |
| LiteLLM | ★★★ | — | ★★★ | ★★ | ★★ | ★★ | — | — | — |
| One API | ★★★ | — | ★★★ | ★ | ★★ | ★★★ | — | — | — |
| Portkey | ★★★ | — | ★★★ | ★★★ | ★★★ | ★★ | — | — | — |
| Dify | ★★ | — | ★ | ★ | ★ | — | — | ★★★ | ★★★ |
| AnythingLLM | ★★ | — | ★ | ★ | — | — | — | ★★★ | ★★ |
| LlamaIndex | ★★ | — | — | — | — | — | — | ★★★ | ★★ |
| LangChain | ★★ | — | — | — | — | — | — | ★★ | ★★★ |
| LLaMA-Factory | — | — | — | — | — | — | ★★★ | — | — |
| Langfuse | — | — | — | — | ★★★ | ★ | — | — | — |
| AWS Bedrock | ★★★ | — | ★★ | ★★★ | ★★ | ★★ | ★★ | ★★ | ★★ |
| Azure AI Foundry | ★★★ | — | ★★ | ★★★ | ★★ | ★★ | ★★ | ★★ | ★★ |

> ★★★ 核心能力 ★★ 有支持 ★ 基础支持 — 不覆盖

---

## 参考
## 参考与交叉验证

本文功能分类与以下权威来源交叉对照，各来源对应章节已标注。

### 关联文件

- [maas_projects.md](maas_projects.md) — MaaS 产品广度收录（7 大类 100+ 项目）
- [maas-feature-landscape.drawio](maas-feature-landscape.drawio) — 本文可视化版本

### 学术 Survey（系统侧）

| 来源 | 对应章节 | 说明 |
|------|---------|------|
| **arXiv:2407.12391** *LLM Inference Serving: Survey of Recent Advances and Opportunities* (Li et al., Northeastern/MIT, Jul 2024) | §2 推理优化, §6 成本缓存 | 将 LLM serving 研究分为 4 类：KV Cache & 内存管理、计算调度（Continuous Batching / Disaggregated Inference / 模型并行）、云端部署（SpotServe / ServerlessLLM / FrugalGPT / RouteLLM）、新兴方向（RAG / MoE）—— 与本文推理层高度吻合 |
| **arXiv:2312.15234** *Towards Efficient Generative LLM Serving* (Miao et al., CMU; ACM Computing Surveys 2025) | §2 推理优化 | 覆盖量化/剪枝/蒸馏（算法侧）+ 内存调度/系统并行（系统侧），验证推理优化功能分类 |
| **arXiv:2305.05176** *FrugalGPT* (Chen, Zaharia & Zou, Stanford, 2023) | §6 成本缓存 | 提出 LLM 级联调用（弱模型→强模型）+ Prompt 缓存，直接支撑成本管理类功能 |
| **arXiv:2406.18665** *RouteLLM* (Ong et al., Berkeley, 2024) | §3 路由可靠性, §6 成本缓存 | 学习路由策略，在质量约束下选弱/强 LLM，验证"条件路由"功能需求 |

### 行业参考架构

| 来源 | 对应章节 | 说明 |
|------|---------|------|
| **a16z "Emerging Architectures for LLM Applications"** (Bornstein & Radovanovic, Jun 2023; [llm-app-stack](https://github.com/a16z-infra/llm-app-stack)) | §1 §5 §6 §8 §9 | 定义 LLM App Stack 七层：Data Pipelines → Embedding Models → Vector DB → Orchestration → LLM APIs → LLM Cache → Ops Tooling（Logging / Caching / Validation / Guardrails / Prompt Injection Detection）—— 覆盖本文平台层所有功能 |
| **信通院《大模型即服务（MaaS）框架与应用研究报告》(2024)** | 全文 | 中国工业界 MaaS 概念界定与分层框架，验证国内平台分类 |
| **NIST AI RMF 1.0** (Jan 2023) | §4 安全合规 | AI 系统治理四维框架（GOVERN / MAP / MEASURE / MANAGE），支撑安全合规功能分类 |

### 安全标准

| 来源 | 对应章节 | 核心内容 |
|------|---------|---------|
| **OWASP Top 10 for LLM Applications 2025** ([genai.owasp.org/llm-top-10](https://genai.owasp.org/llm-top-10/)) | §4 安全合规 | LLM01 Prompt Injection · LLM02 Sensitive Info Disclosure · LLM06 Excessive Agency · LLM08 Vector & Embedding Weaknesses —— 直接对应 Guardrails / PII脱敏 / Prompt注入防护需求 |

### 项目官方文档（功能分类验证）

| 功能类别 | 主要验证来源 |
|---------|-----------|
| API 统一化 | [LiteLLM](https://docs.litellm.ai/docs/providers)（100+ providers）· [Portkey Gateway](https://portkey.ai/docs)（250+ LLMs）· [One API](https://github.com/songquanpeng/one-api) |
| 推理优化 | [vLLM](https://vllm.ai/)（PagedAttention, OSDI'23）· [SGLang](https://github.com/sgl-project/sglang)（RadixAttention, MLSys'24）· [TGI](https://github.com/huggingface/text-generation-inference) |
| 可观测性 | [Langfuse](https://langfuse.com/docs)（trace/eval/cost）· [Helicone](https://docs.helicone.ai)（request logging）|
| 安全合规 | [LlamaGuard](https://ai.meta.com/research/publications/llama-guard-llm-based-input-output-safeguard-for-human-ai-conversations/)（Meta 2023）· [NeMo Guardrails](https://github.com/NVIDIA/NeMo-Guardrails) |
| RAG | [RAGFlow](https://github.com/infiniflow/ragflow)（DeepDoc）· [LlamaIndex](https://docs.llamaindex.ai) |
| 成本优化 | [LiteLLM Caching](https://docs.litellm.ai/docs/caching/all_caches)（Redis/Semantic）· [LLMLingua](https://github.com/microsoft/LLMLingua)（MS Research）|

---

### 与 a16z LLM App Stack 的对应关系

```
a16z 分层                        → 本文功能类别
──────────────────────────────────────────────────────────────
Data Pipelines (ETL)             → §8 RAG（文档处理）
Embedding Models                 → §8 RAG（向量化）
Vector Databases                 → §8 RAG（Milvus / Qdrant / Chroma）
Orchestration (LangChain…)       → §9 Agent & 工作流
APIs / Plugins                   → §1 API 统一化
LLM Cache                        → §6 成本&缓存（GPTCache / Semantic Cache）
Logging / Validation / Guardrails → §4 安全合规 + §5 可观测性
Hosting / Serverless             → §11 部署灵活性
Language Models (OpenAI / OSS)   → §2 推理优化 + 基础设施层
```

> **a16z 未显式覆盖**（2024 年后新增为独立类别）：§3 路由可靠性（负载均衡 / 故障转移）、§7 模型微调
