---
title: Taxonomy of Efficient Inference Methods (arXiv 2404.14294)
---

# Taxonomy of Efficient Inference Methods for Large Language Models

来源论文：
- A Survey on Efficient Inference for Large Language Models  
  https://arxiv.org/abs/2404.14294

说明：
- 下表按论文 Fig.4（Taxonomy of efficient inference methods for Large Language Models）整理。
- 表格结构与之前一致：一级维度 / 二级方向 / 三级子项 / 文本中对应项目（示例）。
- 重复文本已用 `-` 替代。

| 一级维度 | 二级方向 | 三级子项（taxonomy 原词） | 文本中对应项目（示例） |
|---|---|---|---|
| Data-level Optimization | Input Compression (Sec. 4.1) | Prompt Pruning | [LongLLMLingua](https://arxiv.org/abs/2310.06839), [Prompt Compression](https://arxiv.org/abs/2210.03162) |
| - | - | Prompt Summary | [RECOMP](https://arxiv.org/abs/2310.04408), [AutoCompressors](https://arxiv.org/abs/2305.01673) |
| - | - | Soft Prompt-based Compression | [Gisting](https://arxiv.org/abs/2304.08467), [ICAE](https://arxiv.org/abs/2307.06945) |
| - | - | Retrieval-Augmented Generation | [FLARE](https://arxiv.org/abs/2305.14788), [RAG](https://arxiv.org/abs/2005.11401) |
| - | Output Organization (Sec. 4.2) | - | [Chain-of-Thought](https://arxiv.org/abs/2201.11903), [Self-Consistency](https://arxiv.org/abs/2203.11171), [Tree of Thoughts](https://arxiv.org/abs/2305.10601), [SGLang](https://arxiv.org/abs/2312.07104) |
| Model-level Optimization | Efficient Structure Design (Sec. 5.1) | Efficient FFN Design | [Switch Transformer](https://arxiv.org/abs/2101.03961), [Mixtral](https://arxiv.org/abs/2401.04088) |
| - | - | Efficient Attention Design | [MQA](https://arxiv.org/abs/1911.02150), [GQA](https://arxiv.org/abs/2305.13245), [Linformer](https://arxiv.org/abs/2006.04768), [Longformer](https://arxiv.org/abs/2004.05150) |
| - | - | Transformer Alternate | [Mamba](https://arxiv.org/abs/2312.00752), [MambaFormer](https://arxiv.org/abs/2402.04248) |
| - | Model Compression (Sec. 5.2) | Quantization | [GPTQ](https://arxiv.org/abs/2210.17323), [AWQ](https://arxiv.org/abs/2306.00978), [KVQuant](https://arxiv.org/abs/2401.18079), [KIVI](https://arxiv.org/abs/2402.02750) |
| - | - | Sparsification | [SparseGPT](https://arxiv.org/abs/2301.00774), [PowerInfer](https://arxiv.org/abs/2312.12456) |
| - | - | Structure Optimization | [LoRA](https://arxiv.org/abs/2106.09685), [QLoRA](https://arxiv.org/abs/2305.14314) |
| - | - | Knowledge Distillation | [DistilBERT](https://arxiv.org/abs/1910.01108), [MiniLLM](https://arxiv.org/abs/2306.08543) |
| - | - | Dynamic Inference | [DistillSpec](https://arxiv.org/abs/2310.08461), [REST](https://arxiv.org/abs/2311.08252), [PaSS](https://arxiv.org/abs/2311.13581) |
| System-level Optimization | Inference Engine (Sec. 6.1) | Graph and Operator Optimization | [TensorRT-LLM](https://github.com/NVIDIA/TensorRT-LLM), [DeepSpeed-Inference](https://arxiv.org/abs/2207.00032), [FasterTransformer](https://github.com/NVIDIA/FasterTransformer) |
| - | - | Offloading | [FlexGen](https://proceedings.mlr.press/v202/sheng23a.html), [ZeRO-Inference](https://arxiv.org/abs/2212.04017) |
| - | - | Speculative Decoding | [Speculative Decoding](https://arxiv.org/abs/2302.01318), [Medusa](https://github.com/FasterDecoding/Medusa), [DistillSpec](https://arxiv.org/abs/2310.08461) |
| - | Serving System (Sec. 6.2) | Memory Management | [vLLM / PagedAttention](https://arxiv.org/abs/2309.06180), [LightLLM](https://github.com/ModelTC/lightllm) |
| - | - | Batching | [Orca](https://www.usenix.org/conference/osdi22/presentation/yu), [continuous batching in vLLM](https://github.com/vllm-project/vllm) |
| - | - | Scheduling | [Sarathi-Serve](https://www.usenix.org/conference/osdi24/presentation/agrawal), [FastServe](https://arxiv.org/abs/2305.05920) |
| - | - | Distributed Systems | [DistServe](https://www.usenix.org/conference/osdi24/presentation/zhong-yinmin), [Llumnix](https://www.usenix.org/conference/osdi24/presentation/sun-biao) |

## 备注

- Fig.4 在 arXiv HTML 中给出了明确层级：Data-level / Model-level / System-level，以及对应二级与三级节点。
- Output Organization 在图中未继续细分到显式三级子项，因此以 `-` 标记。