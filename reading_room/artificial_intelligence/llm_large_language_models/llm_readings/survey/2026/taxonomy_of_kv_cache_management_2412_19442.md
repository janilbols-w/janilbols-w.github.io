---
title: Taxonomy of KV Cache Management (arXiv 2412.19442)
---

# Taxonomy of KV Cache Management for Large Language Models

来源论文：
- A Survey on Large Language Model Acceleration based on KV Cache Management  
  https://arxiv.org/abs/2412.19442

说明：
- 下表按论文 Fig.2（Taxonomy of KV Cache Management for Large Language Models）整理。
- 表格结构与之前一致：一级维度 / 二级方向 / 三级子项 / 文本中对应项目（示例）。
- 重复文本已用 `-` 替代。

| 一级维度 | 二级方向 | 三级子项（taxonomy 原词） | 文本中对应项目（示例） |
|---|---|---|---|
| Token-level Optimization | KV Cache Selection | Static KV Cache Selection | [FastGen](https://arxiv.org/abs/2402.14864), [SnapKV](https://arxiv.org/abs/2404.14469), [L2Compress](https://arxiv.org/abs/2406.11430), [Attention-Gate](https://arxiv.org/abs/2410.12876) |
| - | - | Dynamic Selection with Permanent Eviction | [StreamingLLM](https://arxiv.org/abs/2309.17453), [LM-Infinite](https://arxiv.org/abs/2402.04617), [H2O](https://arxiv.org/abs/2306.14048), [Scissorhands](https://arxiv.org/abs/2305.17118), [Keyformer](https://openreview.net/forum?id=JrC7LMowQJ) |
| - | - | Dynamic Selection without Permanent Eviction | [InfLLM](https://arxiv.org/abs/2402.04617), [Quest](https://openreview.net/forum?id=h56qXKaNpF), [PQCache](https://arxiv.org/abs/2407.12820), [RetrievalAttention](https://arxiv.org/abs/2409.10516), [InfiniGen](https://arxiv.org/abs/2406.19707), [MagicPIG](https://arxiv.org/abs/2410.16179) |
| - | KV Cache Budget Allocation | Layer-wise Budget Allocation | [PyramidKV](https://arxiv.org/abs/2406.02069), [PyramidInfer](https://aclanthology.org/2024.acl-long.195/), [DynamicKV](https://openreview.net/forum?id=uHkfU4TaPh), [PrefixKV](https://arxiv.org/abs/2412.03409), [CAKE](https://openreview.net/forum?id=EQgEMAD4kv), [SimLayerKV](https://arxiv.org/abs/2410.13846) |
| - | - | Head-wise Budget Allocation | [AdaKV](https://arxiv.org/abs/2407.11550), [CriticalKV](https://openreview.net/forum?id=lRTDMGYCpy), [LeanKV](https://arxiv.org/abs/2412.03131) |
| - | - | Retrieval Head-based Allocation | [RazorAttention](https://arxiv.org/abs/2407.15891), [HeadKV](https://arxiv.org/abs/2410.19258), [DuoAttention](https://arxiv.org/abs/2410.10819) |
| - | KV Cache Merging | Intra-layer Merging | [CCM](https://openreview.net/forum?id=64kSvC4iPg), [LoMA](https://arxiv.org/abs/2401.09486), [DMC](https://openreview.net/forum?id=tDRYrAkOB7), [CaM](https://openreview.net/forum?id=LCTmppB165), [D2O](https://arxiv.org/abs/2406.13035), [KVMerger](https://arxiv.org/abs/2407.08454), [CHAI](https://arxiv.org/abs/2403.08058) |
| - | - | Cross-layer Merging | [MiniCache](https://arxiv.org/abs/2405.14366), [KVSharer](https://arxiv.org/abs/2410.18517) |
| - | KV Cache Quantization | Fixed-precision Quantization | [ZeroQuant](https://arxiv.org/abs/2206.01861), [FlexGen](https://proceedings.mlr.press/v202/sheng23a.html), [QJL](https://arxiv.org/abs/2406.03482), [PQCache](https://arxiv.org/abs/2407.12820) |
| - | - | Mixed-precision Quantization | [KVQuant](https://arxiv.org/abs/2401.18079), [KIVI](https://arxiv.org/abs/2402.02750), [WKVQuant](https://arxiv.org/abs/2402.12065), [GEAR](https://arxiv.org/abs/2403.05527), [MiKV](https://arxiv.org/abs/2402.18096), [ZipCache](https://arxiv.org/abs/2405.14256), [PrefixQuant](https://arxiv.org/abs/2410.05265), [SKVQ](https://arxiv.org/abs/2405.06219), [Atom](https://proceedings.mlsys.org/paper_files/paper/2024/hash/98f7e0f0de322f6df6f74c7f8fc80f8b-Abstract-Conference.html) |
| - | - | Outlier Redistribution | [MassiveActivation](https://arxiv.org/abs/2402.17762), [QuaRot](https://arxiv.org/abs/2404.00456), [QServe](https://arxiv.org/abs/2405.04532), [SmoothQuant](https://arxiv.org/abs/2211.10438), [AffineQuant](https://arxiv.org/abs/2403.12544), [AWQ](https://arxiv.org/abs/2306.00978), [OmniQuant](https://arxiv.org/abs/2308.13137) |
| - | KV Cache Low-rank Decomposition | Singular Value Decomposition | [ECKVH](https://arxiv.org/abs/2406.07056), [EigenAttention](https://arxiv.org/abs/2408.05646), [ZDC](https://arxiv.org/abs/2408.04107), [LoRC](https://arxiv.org/abs/2410.03111), [ShadowKV](https://arxiv.org/abs/2410.21465), [Palu](https://arxiv.org/abs/2407.21118) |
| - | - | Tensor Decomposition | [DecoQuant](https://arxiv.org/abs/2405.12591) |
| - | - | Learned Low-rank Approximation | [LESS](https://arxiv.org/abs/2402.09398), [MatryoshkaKV](https://arxiv.org/abs/2410.14731) |
| Model-level Optimization | Attention Grouping and Sharing | Intra-layer Grouping | [MQA](https://arxiv.org/abs/1911.02150), [GQA](https://arxiv.org/abs/2305.13245), [AsymGQA](https://openreview.net/forum?id=13MMghY6Kh), [QCQA](https://arxiv.org/abs/2406.10247) |
| - | - | Cross-layer Sharing | [CLA](https://arxiv.org/abs/2405.12981), [LCKV](https://aclanthology.org/2024.acl-long.602/), [Shared Attention](https://arxiv.org/abs/2407.12866), [MLKV](https://arxiv.org/abs/2406.09297), [LISA](https://arxiv.org/abs/2408.01890), [CLLA](https://arxiv.org/abs/2410.15252), [DHA](https://arxiv.org/abs/2406.06567) |
| - | Architecture Alteration | Enhanced Attention | [MLA (DeepSeek-V2)](https://arxiv.org/abs/2405.04434), [FLASH](https://proceedings.mlr.press/v162/hua22a.html), [Infini-Attention](https://arxiv.org/abs/2404.07143) |
| - | - | Augmented Architecture | [YOCO](https://arxiv.org/abs/2405.05254), [CEPE](https://aclanthology.org/2024.acl-long.142/), [XC-Cache](https://aclanthology.org/2024.findings-emnlp.896/), [Block Transformer](https://arxiv.org/abs/2406.02657) |
| - | Non-transformer Architecture | Adaptive Sequence Processing Architecture | [RWKV](https://arxiv.org/abs/2305.13048), [Mamba](https://arxiv.org/abs/2312.00752), [RetNet](https://arxiv.org/abs/2307.08621), [MCSD](https://arxiv.org/abs/2406.12230) |
| - | - | Hybrid Architecture | [MixCon](https://ebooks.iospress.nl/doi/10.3233/FAIA240593), [GoldFinch](https://arxiv.org/abs/2407.12077), [RecurFormer](https://arxiv.org/abs/2410.12850) |
| System-level Optimization | Memory Management | Architectural Design | [vLLM / PagedAttention](https://arxiv.org/abs/2309.06180), [vTensor](https://arxiv.org/abs/2407.15309), [LeanKV](https://arxiv.org/abs/2412.03131), [eLLM](https://arxiv.org/abs/2506.15155), [Apt-Serve](https://dl.acm.org/doi/10.1145/3725394) |
| - | - | Prefix-aware Design | [ChunkAttention](https://arxiv.org/abs/2402.15220), [MemServe](https://arxiv.org/abs/2406.17565), [FlashForge](https://arxiv.org/abs/2505.17694) |
| - | Scheduling | Prefix-aware Scheduling | [BatchLLM](https://arxiv.org/abs/2412.03594), [RadixAttention / SGLang](https://arxiv.org/abs/2312.07104), [Echo](https://arxiv.org/abs/2504.03651) |
| - | - | Preemptive and Fairness-oriented Scheduling | [FastServe](https://arxiv.org/abs/2305.05920), [FastSwitch](https://arxiv.org/abs/2411.18424), [FlowKV](https://arxiv.org/abs/2504.03775) |
| - | - | Layer-specific and Hierarchical Scheduling | [LayerKV](https://arxiv.org/abs/2410.00428), [CachedAttention](https://arxiv.org/abs/2403.19708), [ALISA](https://arxiv.org/abs/2403.17312), [LAMPS](https://arxiv.org/abs/2410.18248), [FGOS](https://arxiv.org/abs/2504.11320) |
| - | Hardware-aware Design | Single/Multi-GPU Design | [HydraGen](https://arxiv.org/abs/2402.05099), [DeFT](https://arxiv.org/abs/2404.00242), [DistServe](https://www.usenix.org/conference/osdi24/presentation/zhong-yinmin), [Tree Attention](https://arxiv.org/abs/2408.04093), [FairKV](https://arxiv.org/abs/2502.15804), [MELL](https://arxiv.org/abs/2501.06709) |
| - | - | I/O-based Design | [FlashAttention](https://arxiv.org/abs/2205.14135), [FlashAttention-2](https://arxiv.org/abs/2307.08691), [FlashAttention-3](https://arxiv.org/abs/2407.08608), [Bifurcated Attention](https://arxiv.org/abs/2403.08845), [PartKVRec](https://arxiv.org/abs/2411.17089), [HCache](https://arxiv.org/abs/2410.05004), [Cake](https://arxiv.org/abs/2410.03065) |
| - | - | Heterogeneous Design | [NEO](https://arxiv.org/abs/2411.01142), [FastDecode](https://arxiv.org/abs/2403.11421), [HeadInfer](https://arxiv.org/abs/2502.12574), [Pensieve](https://arxiv.org/abs/2312.05516), [APEX](https://arxiv.org/abs/2506.03296) |
| - | - | SSD-based Design | [FlexGen](https://proceedings.mlr.press/v202/sheng23a.html), [InstInfer](https://arxiv.org/abs/2409.04992) |

## 备注

- 该表是 Fig.2 主 taxonomy 的结构化展开，并结合正文章节中的代表方法补充了示例链接。
- 你上一条消息里的图题实际上对应 arXiv:2412.19442（不是 arXiv:2404.14294）。