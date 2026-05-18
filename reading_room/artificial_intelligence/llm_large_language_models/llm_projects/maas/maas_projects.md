# MaaS (Model as a Service) 产品与开源项目全景

> 广度优先收录。按类别分层梳理，覆盖商业平台、推理框架、本地工具、API 网关、应用层及企业私有化方案。
>
> 最后更新：2026-05

---

## 目录

- [1. 商业云端 MaaS 平台](#1-商业云端-maas-平台)
  - [1.1 国际平台](#11-国际平台)
  - [1.2 国内平台](#12-国内平台)
- [2. 开源推理框架](#2-开源推理框架)
- [3. 本地运行工具](#3-本地运行工具)
- [4. API 网关 / 代理层](#4-api-网关--代理层)
- [5. 应用层 MaaS（Chat UI / RAG 平台）](#5-应用层-maaschat-ui--rag-平台)
- [6. 企业级私有化平台](#6-企业级私有化平台)
- [7. 模型市场 / Hub](#7-模型市场--hub)

---

## 1. 商业云端 MaaS 平台

### 1.1 国际平台

| 厂商 | 产品 / API | 代表模型 | 链接 |
|------|-----------|---------|------|
| OpenAI | OpenAI API | GPT-4o, o3, o4-mini | https://platform.openai.com |
| Anthropic | Claude API | Claude Sonnet 4 / Opus | https://www.anthropic.com/api |
| Google | Gemini API / Vertex AI | Gemini 2.5 Pro | https://ai.google.dev |
| Microsoft | Azure OpenAI Service | GPT-4o, o3 | https://azure.microsoft.com/en-us/products/ai-services/openai-service |
| Amazon | AWS Bedrock | Claude, Llama, Titan, Nova | https://aws.amazon.com/bedrock |
| Meta | Llama API | Llama 4 | https://llama.meta.com |
| Mistral AI | Mistral API | Mistral Large, Codestral | https://mistral.ai |
| Cohere | Cohere API | Command R+, Embed | https://cohere.com |
| xAI | xAI API | Grok-3 | https://x.ai |
| Groq | Groq Cloud | Llama, Mixtral, Gemma | https://groq.com |
| Together AI | Together API | 多模型聚合 | https://www.together.ai |
| Fireworks AI | Fireworks API | 多模型，低延迟推理 | https://fireworks.ai |
| Perplexity | Perplexity API | pplx-70b-online | https://docs.perplexity.ai |
| Replicate | Replicate API | 大量开源模型 | https://replicate.com |
| OpenRouter | OpenRouter API | 聚合路由 200+ 模型 | https://openrouter.ai |
| NVIDIA | NIM (NVIDIA Inference Microservices) | Llama, Mistral, 多模态 | https://build.nvidia.com |
| Cloudflare | Workers AI | Llama, Mistral, BERT | https://developers.cloudflare.com/workers-ai |
| Hugging Face | Inference API / Serverless | 数万开源模型 | https://huggingface.co/inference-api |
| Deepseek | DeepSeek Platform | DeepSeek-V3, R1 | https://platform.deepseek.com |
| SambaNova | SambaNova Cloud | Llama 4, DeepSeek-R1 | https://cloud.sambanova.ai |
| Hyperbolic | Hyperbolic API | Llama, Qwen | https://app.hyperbolic.xyz |
| DeepInfra | DeepInfra API | 多模型 | https://deepinfra.com |
| Novita AI | Novita API | 多模型 | https://novita.ai |
| Lambda Labs | Lambda API | Llama, Hermes | https://lambda.ai |
| Cerebras | Cerebras Inference | Llama 3.3 70B, 超低延迟 | https://inference.cerebras.ai |
| AI21 | AI21 Studio | Jamba | https://studio.ai21.com |
| Anyscale | Anyscale Endpoints | Llama, Mistral | https://www.anyscale.com |

### 1.2 国内平台

| 厂商 | 产品 | 代表模型 | 链接 |
|------|------|---------|------|
| 阿里巴巴 | 阿里云百炼 / Model Studio | 通义千问 Qwen 系列 | https://bailian.aliyun.com |
| 百度 | 文心千帆 (Qianfan) | ERNIE 4.0 | https://cloud.baidu.com/product/wenxinworkshop |
| 腾讯 | 腾讯云 TI-MaaS / 混元 | 混元大模型 | https://cloud.tencent.com/product/hunyuan |
| 字节跳动 | 火山方舟 (Volcengine Ark) | 豆包 Doubao | https://www.volcengine.com/product/ark |
| 科大讯飞 | 讯飞星火 | Spark 4.0 Ultra | https://xinghuo.xfyun.cn |
| 智谱 AI | BigModel / 智谱 API | GLM-4 | https://bigmodel.cn |
| Moonshot AI | Kimi API | Moonshot-v1 | https://platform.moonshot.cn |
| MiniMax | MiniMax API | MiniMax-Text-01 | https://api.minimax.chat |
| 百川智能 | 百川 API | Baichuan4 | https://platform.baichuan-ai.com |
| 零一万物 | 零一 API | Yi-Large | https://platform.lingyiwanwu.com |
| 阶跃星辰 | 阶跃 API | Step-2 | https://platform.stepfun.com |
| 硅基流动 | SiliconCloud | 多模型聚合（含 DeepSeek、Qwen） | https://cloud.siliconflow.cn |
| 360 | 360 智脑 | 360GPT2 | https://ai.360.cn |
| 商汤 | SenseMaaS / 日日新 | SenseChat | https://console.sensecore.cn |
| 华为 | 盘古 MaaS | 盘古 NLP | https://www.huaweicloud.com/product/pangu.html |
| 网易有道 | 有道 AI | Ziya | https://ai.youdao.com |

---

## 2. 开源推理框架

> 主要用于自托管模型服务，提供高效的模型推理能力。

| 项目 | 语言 | 特点 | Stars | 链接 |
|------|------|------|-------|------|
| **vLLM** | Python | PagedAttention，吞吐量极高 | ~50k | https://github.com/vllm-project/vllm |
| **SGLang** | Python | 结构化生成，高性能 serving | ~15k | https://github.com/sgl-project/sglang |
| **TGI** (Text Generation Inference) | Rust/Python | HuggingFace 官方，生产级 | ~10k | https://github.com/huggingface/text-generation-inference |
| **Triton Inference Server** | C++/Python | NVIDIA 出品，支持多框架 | ~8k | https://github.com/triton-inference-server/server |
| **llama.cpp** | C++ | CPU/GPU 通用，量化支持 | ~70k | https://github.com/ggerganov/llama.cpp |
| **MLC LLM** | C++/Python | 跨平台编译（手机、Web、桌面） | ~20k | https://github.com/mlc-ai/mlc-llm |
| **Ray Serve** | Python | Ray 生态，分布式 serving | ~35k | https://github.com/ray-project/ray |
| **OpenLLM** (BentoML) | Python | BentoML 封装，易部署 | ~10k | https://github.com/bentoml/OpenLLM |
| **DeepSpeed-MII** | Python | 微软出品，低延迟推理 | ~4k | https://github.com/microsoft/DeepSpeed-MII |
| **Xinference** | Python | 多框架后端，含 embedding/reranker | ~5k | https://github.com/xorbitsai/inference |
| **LMDeploy** | Python | 上海AI实验室，TurboMind 引擎 | ~5k | https://github.com/InternLM/lmdeploy |
| **Ollama** | Go | 本地一键运行，API 兼容 OpenAI | ~120k | https://github.com/ollama/ollama |
| **LocalAI** | Go | 本地 OpenAI 兼容 API | ~25k | https://github.com/mudler/LocalAI |
| **TensorRT-LLM** | C++/Python | NVIDIA TensorRT 推理优化 | ~9k | https://github.com/NVIDIA/TensorRT-LLM |
| **PowerInfer** | C++ | 稀疏激活，消费级 GPU 高效推理 | ~7k | https://github.com/SJTU-IPADS/PowerInfer |

---

## 3. 本地运行工具

> 面向开发者和普通用户的桌面/本地运行工具，通常封装推理框架并提供 UI。

| 项目 | 类型 | 特点 | 链接 |
|------|------|------|------|
| **Ollama** | CLI + API | 最流行的本地运行工具，支持 GGUF | https://ollama.com |
| **LM Studio** | 桌面 GUI | Windows/Mac，可视化模型管理 | https://lmstudio.ai |
| **Jan** | 桌面 GUI | 开源，离线优先 | https://github.com/janhq/jan |
| **GPT4All** | 桌面 GUI | Nomic 出品，注重隐私 | https://github.com/nomic-ai/gpt4all |
| **llamafile** | 单文件可执行 | Mozilla 出品，一个文件运行模型 | https://github.com/Mozilla-Ocho/llamafile |
| **Lemonade** (AMD) | CLI + API | AMD Ryzen AI 优化 | https://lemonade-server.ai |
| **Microsoft Foundry Local** | CLI | 微软出品，本地推理 | https://github.com/microsoft/Foundry-Local |
| **koboldcpp** | CLI + Web UI | 游戏/创作向，完整 UI | https://github.com/LostRuins/koboldcpp |
| **text-generation-webui** | Web UI | oobabooga 出品，功能全面 | https://github.com/oobabooga/text-generation-webui |

---

## 4. API 网关 / 代理层

> 统一多个 LLM 提供商 API，提供负载均衡、Key 管理、计费等能力。

| 项目 | 语言 | 特点 | Stars | 链接 |
|------|------|------|-------|------|
| **LiteLLM** | Python | 支持 100+ 提供商，OpenAI 格式统一 | ~47k | https://github.com/BerriAI/litellm |
| **One API** | Go | 国内最流行的 Key 管理 & 分发系统 | ~34k | https://github.com/songquanpeng/one-api |
| **New API** | Go | One API 分叉，更多功能 | ~10k | https://github.com/Calcium-Ion/new-api |
| **Portkey Gateway** | TypeScript | 企业级，<1ms 延迟，Guardrails | ~12k | https://github.com/Portkey-AI/gateway |
| **Higress AI Gateway** | Go | 阿里云开源，云原生 AI 网关 | ~5k | https://github.com/alibaba/higress |
| **AI Gateway** (Cloudflare) | - | Cloudflare 托管，全球分布 | - | https://developers.cloudflare.com/ai-gateway |
| **Kong AI Gateway** | Lua/Go | Kong 插件，企业级 | - | https://konghq.com/products/kong-ai-gateway |
| **MLflow AI Gateway** | Python | MLflow 生态，模型路由 | - | https://mlflow.org/docs/latest/llms/gateway |

---

## 5. 应用层 MaaS（Chat UI / RAG 平台）

> 在推理层之上提供完整的对话、知识库、Agent 能力的应用平台。

| 项目 | 类型 | 特点 | Stars | 链接 |
|------|------|------|-------|------|
| **Open WebUI** | Chat UI | Ollama 前端，功能丰富 | ~70k | https://github.com/open-webui/open-webui |
| **AnythingLLM** | RAG + Agent | 私有知识库，多用户，Agent | ~60k | https://github.com/Mintplex-Labs/anything-llm |
| **FastGPT** | RAG 平台 | 知识库问答，工作流编排 | ~25k | https://github.com/labring/FastGPT |
| **Dify** | LLMOps 平台 | 应用构建，RAG，工作流 | ~90k | https://github.com/langgenius/dify |
| **LobeHub / Lobe Chat** | Chat UI | 多模型，插件扩展 | ~55k | https://github.com/lobehub/lobe-chat |
| **ChatGPT Next Web** | Chat UI | 极简部署，Vercel 一键 | ~80k | https://github.com/ChatGPTNextWeb/ChatGPT-Next-Web |
| **Flowise** | 可视化工作流 | LangChain 拖拽 UI | ~35k | https://github.com/FlowiseAI/Flowise |
| **Langflow** | 可视化工作流 | DataStax 支持 | ~40k | https://github.com/langflow-ai/langflow |
| **MaxKB** | RAG 平台 | 飞致云出品，企业知识库 | ~15k | https://github.com/1Panel-dev/MaxKB |
| **RAGFlow** | RAG 平台 | DeepDoc，深度文档解析 | ~35k | https://github.com/infiniflow/ragflow |
| **Coze** | Agent 平台 | 字节跳动，国内版扣子 | - | https://www.coze.com |
| **Taskingai** | Agent 平台 | 多模型，工具调用 | ~5k | https://github.com/TaskingAI/TaskingAI |

---

## 6. 企业级私有化平台

> 面向企业提供完整私有化部署方案，含模型管理、安全、计费等。

| 厂商 / 项目 | 定位 | 特点 | 链接 |
|-------------|------|------|------|
| **阿里云百炼** | 云端 + 私有化 | 模型微调、评估、RAG、工作流 | https://bailian.aliyun.com |
| **华为 ModelArts / 盘古** | 企业 AI 平台 | 全栈 AI，支持私有部署 | https://www.huaweicloud.com/product/modelarts.html |
| **IBM watsonx.ai** | 企业 AI 平台 | 多云，Granite 模型，治理 | https://www.ibm.com/watsonx |
| **Azure AI Foundry** | 云端 MaaS | 企业级，集成 Azure 生态 | https://ai.azure.com |
| **AWS SageMaker** | 云端训练 + 推理 | 托管推理端点，JumpStart | https://aws.amazon.com/sagemaker |
| **Google Vertex AI** | 云端 MaaS | Gemini + 第三方模型，MLOps | https://cloud.google.com/vertex-ai |
| **Databricks** | 数据 + AI 平台 | DBRX，MosaicAI，联邦学习 | https://www.databricks.com/product/machine-learning |
| **Snowflake Cortex AI** | 数据仓库内 AI | SQL 调用 LLM | https://www.snowflake.com/en/data-cloud/cortex |
| **NVIDIA AI Enterprise** | 企业 AI 软件 | NIM 私有化部署 | https://www.nvidia.com/en-us/data-center/products/ai-enterprise |
| **vLLM Enterprise** / **Anyscale Private Endpoints** | 推理私有化 | 企业支持版 vLLM | - |
| **LiteLLM Enterprise** | API 网关私有化 | SSO、审计、高可用 | https://litellm.ai/enterprise |
| **Portkey Enterprise** | AI 网关私有化 | SOC2/HIPAA，私有部署 | https://portkey.ai/enterprise |

---

## 7. 模型市场 / Hub

> 模型存储、发现、下载和托管的中心化平台。

| 平台 | 特点 | 链接 |
|------|------|------|
| **Hugging Face Hub** | 最大开源模型社区，10万+ 模型 | https://huggingface.co/models |
| **ModelScope** (魔搭) | 阿里达摩院，国内最大模型社区 | https://modelscope.cn |
| **Ollama Library** | GGUF 量化模型，一键 pull | https://ollama.com/library |
| **Civitai** | Stable Diffusion 及图像模型社区 | https://civitai.com |
| **GitHub Models** | GitHub 内嵌模型体验 & API | https://github.com/marketplace/models |
| **Replicate Model Library** | 数千个开源模型，API 即用 | https://replicate.com/explore |
| **NVIDIA NGC** | 企业级预训练模型目录 | https://catalog.ngc.nvidia.com |
| **OpenCSG** (开放智汇) | 国内开源模型托管 | https://opencsg.com |
| **魔乐社区** (MoLeH) | 开源模型托管，中文优先 | https://modelers.cn |

---

## 参考资料

- 信通院《MaaS框架与应用研究报告2024》（`llm_readings/maas/`）
- 阿里云 Model Studio 官方文档（`llm_readings/maas/项目官方信息/`）
- [LiteLLM Supported Providers](https://docs.litellm.ai/docs/providers)
- [One API README](https://github.com/songquanpeng/one-api)
- [Portkey AI Gateway](https://github.com/Portkey-AI/gateway)
