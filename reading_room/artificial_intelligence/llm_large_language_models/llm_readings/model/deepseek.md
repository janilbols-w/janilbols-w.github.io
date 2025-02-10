# DeepSeek Paper Reading

部分摘要基于LLM自动生成

|    | date     | project              | title                                                                                                                 | link                                 | abstract                                                                                                                                                                                                                                                                                                                                                                                                                      | details                                                                                                     |
| -- | -------- | -------------------- | --------------------------------------------------------------------------------------------------------------------- | ------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| 1  | 20240105 | DeepSeek LLM         | DeepSeek LLM: Scaling Open-Source<br />Language Models with Longtermism                                               | [link](http://arxiv.org/abs/2401.02954) | 深入研究缩放定律，为大规模模型缩放提供指导，开发 DeepSeek LLM 项目，<br />通过收集 2 万亿标记数据集预训练，进行监督微调和直接偏好优化，创建 <br />DeepSeek Chat 模型，该模型在多个基准测试中表现出色，<br />超过 LLaMA-2 70B，在代码、数学和推理等领域优势明显。                                                                                                                                                              | ✅[details](./deepseek-paper/01-DeepSeekLLM.2401.02954v1.md)                                                   |
| 2  | 20240111 | DeepSeek MoE         | DeepSeekMoE: Towards Ultimate Expert<br />Specialization in Mixture-of-Experts Language Models                        | [link](http://arxiv.org/abs/2401.06066) | 提出 DeepSeekMoE 架构，以实现专家的终极专业化，通过细粒度的专家分<br />割和共享专家隔离策略，提高模型的性能和效率。在训练过程中，采用多种<br />策略来验证架构的有效性，并将模型扩展到更大规模，与其他先进模型进行<br />比较，展示了其在性能和可扩展性方面的优势。                                                                                                                                                             | ✅[details](./deepseek-paper/02-DeepSeekMoE.2401.06066v1.md)                                                   |
| 3  | 20240126 | DeepSeek Coder       | DeepSeek-Coder: When the Large Language<br />Model Meets Programming -- The Rise of Code Intelligence                 | [link](http://arxiv.org/abs/2401.14196) | 介绍 DeepSeek-Coder 系列代码模型，包括模型的训练、数据收集和处理、<br />训练策略等。通过在大规模代码数据集上的训练，DeepSeek-Coder 在代码<br />生成、代码完成和数学推理等任务上表现出色，超过了许多开源和闭源模型，<br />为开发人员提供了更强大的代码智能支持。                                                                                                                                                               | [details](./deepseek-paper/03-DeepSeek-Coder.2401.14196v2.md)                                                  |
| 4  | 20240311 | DeepSeek VL          | DeepSeek-VL: Towards Real-World<br />Vision-Language Understanding                                                    | [link](http://arxiv.org/abs/2403.05525) | 提出 DeepSeek-VL，这是一种面向现实世界视觉和语言理解的开源模型。通<br />过数据构建、模型架构和训练策略的优化，DeepSeek-VL 在视觉语言任务中<br />展现出优越的性能，能够处理图像描述、问答、推理等多种任务，为实现智<br />能的视觉和语言交互提供了有力支持。                                                                                                                                                                    | [details](./deepseek-paper/04-Deepseek-vl.2403.05525v2.md)                                                     |
| 5  | 20240523 | DeepSeek Prover      | DeepSeek-Prover: Advancing Theorem<br />Proving in LLMs through Large-Scale Synthetic Data                            | [link](http://arxiv.org/abs/2405.14333) | 通过从高中和本科数学竞赛问题中生成大量 Lean 4 证明数据，来解决语言<br />模型在定理证明方面缺乏训练数据的问题。具体方法包括将自然语言问题转<br />化为形式化陈述，过滤低质量陈述，并使用迭代证明生成来创建合成数据。<br />经过在合成数据集上的微调，DeepSeekMath 7B 模型在定理证明任务上取<br />得了显著进展。                                                                                                                  | [details](./deepseek-paper/05-DeepSeek-Prover.2405.14333v1.md)                                                 |
| 6  | 20240617 | DeepSeek Coder-V2    | DeepSeek-Coder-V2: Breaking the Barrier<br /> of Closed-Source Models in Code Intelligence                            | [link](http://arxiv.org/abs/2406.11931) | 是 DeepSeek-Coder 的进一步发展，基于 DeepSeek-V2 进行预训练，支持<br />更多编程语言和更长的上下文长度。在代码生成、代码完成、代码修复和数<br />学推理等任务上，取得了优于之前版本和闭源模型的性能，为开发人员提供<br />了更高效、更智能的代码开发工具。                                                                                                                                                                       | [details](./deepseek-paper/06-DeepSeek-Coder-V2.2406.11931v1.md)                                               |
| 7  | 20240619 | DeepSeek V2          | DeepSeek-V2: A Strong, Economical, and Efficient<br />Mixture-of-Experts Language Model                               | [link](http://arxiv.org/abs/2405.04434) | 介绍 DeepSeek-V2，这是一个强大、经济和高效的混合专家语言模型。采用<br />多头潜在注意力（MLA）和 DeepSeekMoE 架构，在保持强大性能的同时，<br />实现了经济的训练和高效的推理。通过在高质量和多源语料库上的预训练，<br />以及后续的监督微调和强化学习，DeepSeek-V2 在多个基准测试中表现出<br />色，成为最强的开源 MoE 语言模型之一。<br /><br />🤔 **Token-Dropping Strategy？** <br /> 🤔 GRPO?                           | [❓✅details](./deepseek-paper/07-DeepSeek-V2.2405.04434v5.md)                                                 |
| 8  | 20240815 | DeepSeek Prover-V1.5 | DeepSeek-Prover-V1.5: Harnessing Proof Assistant<br />Feedback for Reinforcement Learning and Monte-Carlo Tree Search | [link](http://arxiv.org/abs/2408.08152) | 在 DeepSeek-Prover-V1 的基础上进行优化，通过进一步预训练、监督微<br />调和强化学习，引入 RMaxTS 蒙特卡洛树搜索算法，显著提高了定理证明<br />能力。在多个基准测试中取得了新的最先进结果，为语言模型在定理证明<br />领域的应用提供了更强大的工具。                                                                                                                                                                              | [details](./deepseek-paper/08-DeepSeek-Prover-V1.5.2408.08152v1.md)                                            |
| 9  | 20241213 | DeepSeek VL2         | DeepSeek-VL2: Mixture-of-Experts Vision-Language<br />Models for Advanced Multimodal Understanding                    | [link](http://arxiv.org/abs/2412.10302) | 是 DeepSeek-VL 的改进版本，采用动态平铺视觉编码策略和<br />DeepSeekMoE 模型，在视觉语言理解方面有了显著提升。它能够处理多<br />种视觉语言任务，在多个基准测试中取得了领先成绩，为先进的多模态理<br />解提供了更强大的模型支持。                                                                                                                                                                                               | [details](./deepseek-paper/09-Deepseek-vl2.2412.10302v1.md)                                                    |
| 10 | 20241227 | DeepSeek v3          | DeepSeek-V3 Technical Report                                                                                          | [link](http://arxiv.org/abs/2412.19437) | 具有 671B 总参数和 37B 激活令牌，采用多头潜在注意力（MLA）和<br /> DeepSeekMoE 架构，通过创新的负载平衡策略和多令牌预测训练目标，<br />在性能和效率方面取得了显著提升。在预训练、上下文扩展、监督微调、<br />强化学习等阶段进行了全面的优化和评估，在多个基准测试中表现出色，<br />超过了其他开源模型，达到了与领先闭源模型相当的性能。<br />🤔MTP (multi token prediction)<br />🤔Complementary Sequence-Wise Auxiliary Loss | ❓[✅](./deepseek-paper/07-DeepSeek-V2.2405.04434v5.md)[details](./deepseek-paper/10-DeepSeek-V3.2412.19437v1.md) |
| 11 | 20250122 | DeepSeek R1          | DeepSeek-R1: Incentivizing Reasoning Capability<br /> in LLMs via Reinforcement Learning                              | [link](http://arxiv.org/abs/2501.12948) | 通过大规模强化学习开发第一代推理模型 DeepSeek-R1-Zero，该模型在<br />推理任务中展现出强大的能力，但存在一些问题，如可读性差和语言混合。<br />为解决这些问题，引入 DeepSeek-R1，通过多阶段训练和冷启动数据，<br />使其在推理任务上的性能与 OpenAI-o1-1217 相当。此外，还探索了从 <br />DeepSeek-R1 到较小密集模型的蒸馏，提高了模型的推理能力。                                                                                | [❓details](./deepseek-paper/11-DeepSeek-R1.2501.12948v1.md)                                                   |
| 12 | 20250129 | Janus-Pro            | Janus-Pro: Unified Multimodal Understanding and<br />Generation with Data and Model Scaling                           | [link](http://arxiv.org/abs/2501.17811) | 对 Janus 模型进行改进，优化训练策略，扩展训练数据，增加模型规模，<br />提升了多模态理解和文本到图像指令跟随能力。在多个基准测试中表现<br />出色，优于之前的统一多模态模型和一些任务特定模型，为多模态理解<br />和生成领域的发展提供了新的解决方案。                                                                                                                                                                           | [details](./deepseek-paper/12-Janus-Pro.2501.17811v1.md)                                                       |

## 1 **DeepSeek LLM**

* **模型与数据** ：DeepSeek LLM 基于 Transformer 架构，7B 和 67B 模型在数据收集和预处理上有严格流程，如采用多种策略进行数据 deduplication、filtering 和 remixing。
* **训练与架构** ：遵循特定的训练流程，使用 HAI-LLM 框架，采用多种并行策略和优化技术，如 flash attention、ZeRO-1 等。模型架构在遵循 LLaMA 设计的基础上，有微调和宏观层面的调整。
* **评估与性能** ：在多个基准测试中表现出色，超过 LLaMA-2 70B，尤其在代码、数学和推理领域。67B Chat 模型在开放端评估中优于 GPT-3.5，安全评估显示其能提供无害响应。

## 2 **DeepSeekMoE**

* **架构创新** ：DeepSeekMoE 采用细粒度专家分割和共享专家隔离策略，由混合视觉编码器、视觉适配器和语言模型组成，能有效处理高分辨率图像。
* **训练与优化** ：训练过程包括多个阶段，如视觉语言适配器热身、联合视觉语言预训练和监督微调。采用多种优化技术，如专家级和设备级平衡损失、令牌丢弃策略等，以提高模型性能和训练效率。
* **性能评估** ：在多个基准测试中与其他模型进行比较，结果表明 DeepSeekMoE 在性能和可扩展性方面具有显著优势，能以较少的计算资源实现与其他先进模型相当的性能。

## 3 **DeepSeek-Coder**

* **数据收集** ：DeepSeek-Coder 的数据收集包括从 GitHub 和 CommonCrawl 等来源收集代码，以及从 StackExchange 和 GitHub Markdown 等收集自然语言文本，还进行了过滤、依赖解析、存储库级去重和质量筛选等操作。
* **训练策略** ：采用 next token prediction 和 Fill-in-the-Middle（FIM）训练目标，使用特定的令牌器和模型架构，如基于 DeepSeek LLM 开发，采用 Rotary Position Embedding 等。训练过程中还进行了长上下文扩展和指令微调。
* **性能表现** ：在代码生成、FIM 代码完成、跨文件代码完成和程序数学推理等任务上进行评估，与其他先进模型相比，DeepSeek-Coder 在多个基准测试中表现出色，支持多种编程语言，具有较强的代码智能能力。

## 4 **Deepseek-vl**

* **模型架构** ：DeepSeek-VL 由混合视觉编码器、视觉适配器和语言模型组成，采用 SigLIP 作为视觉编码器，引入 Decoupled Rotary Position Embedding 策略解决与低秩 KV 压缩的兼容性问题。
* **数据构建** ：数据构建包括视觉语言预训练数据和监督微调数据，涉及多种数据来源，如 Interleaved image-text data、Image caption data、Table and chart data 等，并进行了质量筛选和去重。
* **评估结果** ：在多个公共基准测试和人类评估中表现优异，在视觉语言理解、多模态推理和语言生成等任务上具有较强的能力，能够处理各种复杂的视觉和语言任务，为实际应用提供了有力支持。

## 5 **DeepSeek-Prover**

* **方法创新** ：通过将高中和本科数学竞赛问题转化为形式化陈述，过滤低质量陈述，并使用迭代证明生成和强化学习来创建合成数据，解决了语言模型在定理证明方面缺乏训练数据的问题。
* **实验设置** ：使用 DeepSeekMath 7B 作为基础模型，进行预训练、监督微调和强化学习。在多个定理证明基准测试中进行评估，与 GPT-4 等模型进行比较。
* **成果显著** ：经过在合成数据集上的微调，DeepSeekMath 7B 模型在定理证明任务上取得了显著进展，在 miniF2F 和 FIMO 基准测试中表现优于 GPT-4 等模型，成功证明了一些复杂的数学定理。

## 6 **DeepSeek-Coder-V2**

* **模型发展** ：是 DeepSeek-Coder 的进一步发展，基于 DeepSeek-V2 进行预训练，支持更多编程语言和更长的上下文长度。
* **训练优化** ：在训练过程中，采用了多种优化策略，如使用特定的数据集、调整学习率和优化器参数、进行长上下文扩展等，以提高模型的性能。
* **性能优势** ：在代码生成、代码完成、代码修复和数学推理等任务上，取得了优于之前版本和闭源模型的性能，能够满足开发人员在不同任务中的需求。

## 7 **DeepSeek-V2**

* **架构特点** ：采用多头潜在注意力（MLA）和 DeepSeekMoE 架构，MLA 通过低秩键值联合压缩减少 KV 缓存，DeepSeekMoE 实现了经济的训练和高效的推理。
* **训练过程** ：在高质量和多源语料库上进行预训练，包括多个训练阶段和优化策略，如使用特定的学习率调度、平衡损失等。
* **性能表现** ：DeepSeek-V2 在多个基准测试中表现出色，成为最强的开源 MoE 语言模型之一，在语言理解、知识推理和多模态任务等方面具有较强的能力。

## 8 **DeepSeek-Prover-V1.5**

* **技术改进** ：在 DeepSeek-Prover-V1 的基础上进行优化，引入 RMaxTS 蒙特卡洛树搜索算法，通过进一步预训练、监督微调和强化学习，提高了定理证明能力。
* **算法创新** ：RMaxTS 算法采用内在奖励驱动的探索策略，能够有效地搜索证明空间，提高了定理证明的效率和准确性。
* **实验成果** ：在多个定理证明基准测试中取得了新的最先进结果，证明了该方法在定理证明领域的有效性和优势。

## 9 **DeepSeek-VL2**

* **模型升级** ：DeepSeek-VL2 是 DeepSeek-VL 的改进版本，采用动态平铺视觉编码策略和 DeepSeekMoE 模型，提高了模型的性能和效率。
* **数据增强** ：在数据构建方面进行了优化，包括收集更多的视觉语言数据、进行数据增强和预处理等，以提高模型的泛化能力。
* **性能评估** ：在多个基准测试中进行评估，结果表明 DeepSeek-VL2 在视觉语言理解、多模态推理和视觉基础等任务上具有较强的能力，能够满足实际应用的需求。

## 10 **DeepSeek-V3**

* **架构创新** ：采用多头潜在注意力（MLA）和 DeepSeekMoE 架构，引入辅助损失无负载平衡策略和多令牌预测训练目标，提高了模型的性能和效率。
* **训练优化** ：在训练过程中，进行了大规模的预训练、上下文扩展、监督微调和强化学习，采用了多种优化技术，如 FP8 混合精度训练、高效的通信和计算重叠等。
* **性能表现** ：DeepSeek-V3 在多个基准测试中表现出色，超过了其他开源模型，达到了与领先闭源模型相当的性能，在知识、代码、数学和推理等领域具有较强的能力。

## 11 **DeepSeek-R1**

* **模型开发** ：通过大规模强化学习开发第一代推理模型 DeepSeek-R1-Zero，该模型在推理任务中展现出强大的能力，但存在一些问题，如可读性差和语言混合。
* **模型改进** ：为解决这些问题，引入 DeepSeek-R1，通过多阶段训练和冷启动数据，使其在推理任务上的性能与 OpenAI-o1-1217 相当。
* **应用探索** ：还探索了从 DeepSeek-R1 到较小密集模型的蒸馏，提高了模型的推理能力，并将其应用于多个任务领域，取得了较好的效果。

## 12 **Janus-Pro**

* **模型改进** ：对 Janus 模型进行改进，优化训练策略，扩展训练数据，增加模型规模，提升了多模态理解和文本到图像指令跟随能力。
* **性能评估** ：在多个基准测试中进行评估，结果表明 Janus-Pro 在多模态理解和视觉生成任务上表现出色，优于之前的模型。
* **应用前景** ：为多模态理解和生成领域的发展提供了新的解决方案，具有广阔的应用前景。
