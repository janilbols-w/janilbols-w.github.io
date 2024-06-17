# Implementations for LLM Train

For general AI Infra, we need to know about how different LLM projects implements their training code, to ensure how we could make a more general solution.

## 1 LLM Training Frameworks

based on  https://github.com/Hannibal046/Awesome-LLM

|                                                                    | notes                                                                                                                                                                    |
| ------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [DeepSpeed](https://github.com/microsoft/DeepSpeed)                   | DeepSpeed is a deep learning optimization library that makes distributed training and inference easy, efficient, and effective<br />https://www.deepspeed.ai/training/   |
| [Megatron-DeepSpeed](https://github.com/microsoft/Megatron-DeepSpeed) | DeepSpeed version of NVIDIA's Megatron-LM that adds additional support for several features such as MoE model training, Curriculum Learning, 3D Parallelism, and others. |
| [torchtune](https://github.com/pytorch/torchtune)                     | A Native-PyTorch Library for LLM Fine-tuning.                                                                                                                            |
| [torchtitan](https://github.com/pytorch/torchtitan)                   | A native PyTorch Library for large model training.                                                                                                                       |
| [Megatron-LM](https://github.com/NVIDIA/Megatron-LM)                  | Ongoing research training transformer models at scale.                                                                                                                   |
| [Colossal-AI](https://github.com/hpcaitech/ColossalAI)                | Making large AI models cheaper, faster, and more accessible.                                                                                                             |
| [BMTrain](https://github.com/OpenBMB/BMTrain)                         | Efficient Training for Big Models.                                                                                                                                       |
| [Mesh Tensorflow](https://github.com/tensorflow/mesh)                 | Mesh TensorFlow: Model Parallelism Made Easier.                                                                                                                          |
| [maxtext](https://github.com/google/maxtext)                          | A simple, performant and scalable Jax LLM                                                                                                                                |
| [Alpa](https://alpa.ai/index.html)                                    | Alpa is a system for training and serving large-scale neural networks.                                                                                                   |
| [GPT-NeoX](https://github.com/EleutherAI/gpt-neox)                    | An implementation of model parallel autoregressive transformers on GPUs, based on the DeepSpeed library.                                                                 |
| Transformers                                                       |                                                                                                                                                                          |
| PEFT                                                               |                                                                                                                                                                          |
| Accelerate                                                         |                                                                                                                                                                          |

## 2 LLM Projects

all opensource projects are default with basic modeling and inferencing capability

- modeling: pre-defined uniform layer/methods/module, maybe customized raw code or well-packed library.
- dist methods: frameworks to achieve dp/tp/pp.
- data pipe: dataloader with given dataset, preprocess if neccesery.
- inferrer: pre-defined scripts or pipeline to do inference or maybe eval.
- trainer: pre-defined training process to do training.
- pipeline: whole e2e solution, with simple scripts or simple code interface to run train or infer tasks.
- other: placeholder, other comments if any.

| model                                        | project                                                                                                                                                                                            | DL Framework    | modeling                      | distributed framework                                             | data pipe                                          | inferrer                                 | trainer                                      | pipeline                                     | other                                                           |
| -------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------- | ----------------------------- | ----------------------------------------------------------------- | -------------------------------------------------- | ---------------------------------------- | -------------------------------------------- | -------------------------------------------- | --------------------------------------------------------------- |
| [llama1/2](https://github.com/meta-llama/llama) | meta/[llama1/2](https://github.com/meta-llama/llama)                                                                                                                                                  | torch           | customized                    | fairscale                                                         | NA                                                 | customized                               | NA                                           | NA                                           | infer only                                                      |
| [llama3](https://github.com/meta-llama/llama3)  | meta/[llama3](https://github.com/meta-llama/llama3)                                                                                                                                                   | torch           | customized                    | fairscale                                                         | NA                                                 | customized                               | NA                                           | NA                                           | infer only                                                      |
|                                              | pytorch/[torchtune](https://github.com/pytorch/torchtune/tree/main?tab=readme-ov-file#llama3)                                                                                                         | torch           | torchtune                     | torch.FSDP                                                        | torchtune                                          | torchtune                                | torchtune                                    | torchtune recipe                             |                                                                 |
| opt                                          | facebookresearch/[metaseq](https://github.com/facebookresearch/metaseq)                                                                                                                               | torch           | metaseq                       | metaseq                                                           | customized                                         | metaseq                                  | metaseq                                      | metaseq                                      |                                                                 |
|                                              | huggingface/[transformers](https://github.com/huggingface/transformers/)                                                                                                                              | torch           | Transformers                  | accelerate(hf)/<br />deepspeed/<br />torch.FSDP/<br />Megatron-LM | datasets (hf)                                      | transformers                             | transformers                                 | transformers                                 |                                                                 |
|                                              | hpcaitech/[ColossalAI](https://github.com/hpcaitech/ColossalAI#OPT)                                                                                                                                   | torch           | Transformers                  | colossalai                                                        | datasets (hf)                                      | colossalai                               | colossalai                                   | colossalai                                   |                                                                 |
|                                              | OpenNMT/[OpenNMT](https://github.com/OpenNMT/OpenNMT-py)                                                                                                                                              | torch/tf        | OpenNMT                       | OpenNMT                                                           | OpenNMT                                            | OpenNMT                                  | OpenNMT                                      | OpenNMT                                      |                                                                 |
|                                              | NVIDIA/[FasterTransformer](https://github.com/NVIDIA/FasterTransformer/tree/main/examples/pytorch/gpt)                                                                                                | torch           | Transformers/ customized      | FasterTransformer                                                 | NA                                                 | customized                               | NA                                           | NA                                           | infer only                                                      |
|                                              | Microsoft/[Deepspeed](https://github.com/microsoft/DeepSpeedExamples/tree/master/applications/DeepSpeed-Chat)                                                                                         | torch           | Transormers                   | deepspeed                                                         | torch                                              | customized                               | customized                                   | NA                                           |                                                                 |
| mistral                                      | mistralai/[mistral](https://github.com/mistralai/mistral-finetune)                                                                                                                                    | torch           | customized                    | torch.FSDP                                                        | customized                                         | customized                               | customized                                   | NA                                           |                                                                 |
| Gemma                                        | google-deepmind/[gemma](https://github.com/google-deepmind/gemma)                                                                                                                                     | JAX             | customized                    | NA                                                                | NA                                                 | customized                               | NA                                           | NA                                           | customized jax project                                          |
| Recurrent Gemma                              | google-deepmind/[recurrentgemma](https://github.com/google-deepmind/recurrentgemma)                                                                                                                   | JAX/torch       | flax                          | NA                                                                | tensorflow_datasets                                | customized                               | customized                                   | NA                                           | finetune with jax only                                          |
| T5                                           | google-research/<br />[text-to-text-transfer-transformer](https://github.com/google-research/text-to-text-transfer-transformer)                                                                       | mesh-tensorflow | mesh_tensorflow[transformers] | tf.dist                                                           | tensorflow_datasets                                | customized                               | customized                                   | NA                                           |                                                                 |
| OpenELM                                      | apple/corenet ->[OpenELM](https://github.com/apple/corenet/tree/main/mlx_examples/open_elm)                                                                                                           | torch/MLX       | corenet/ Transformers         | deepspeed/ torch.FSDP                                             | [corenet](https://github.com/apple/corenet)           | [corenet](https://github.com/apple/corenet) | [corenet](https://github.com/apple/corenet)     | [corenet](https://github.com/apple/corenet)     | apple specific                                                  |
| Phi-3                                        | microsoft/[Phi-3](https://github.com/microsoft/Phi-3CookBook)                                                                                                                                         | torch           | Transformers/ flash_attn      | accelerate                                                        | datasets                                           | transormers                              | [tri](https://github.com/huggingface/trl) (hf) | [tri](https://github.com/huggingface/trl) (hf) | deeply based on<br />huggingface pkgs                           |
| OLMo                                         | allenai/[OLMo](https://github.com/allenai/OLMo)                                                                                                                                                       | torch           | OLMo/<br />Transformers       | torch.FSDP/ DDP                                                   | OLMo                                               | OLMo                                     | OLMo                                         | OLMo                                         | self-defined training<br />process; <br />hf-model convertable; |
| Grok                                         | xai-org/[grok-1](https://github.com/xai-org/grok-1)                                                                                                                                                   | jax             | customized/<br />Transformers | jax                                                               | customized                                         | customized                               | customized                                   | NA                                           | custom process<br />based on jax                                |
| Command R                                    | cohere/[command-r](https://docs.cohere.com/docs/chat-starting-the-training) <br />[cohere-toolkit](https://github.com/cohere-ai/cohere-toolkit?tab=readme-ov-file#how-to-add-your-own-model-deployment) | NA              | NA                            | NA                                                                | NA                                                 | NA<br />cohere-toolkit                   | NA                                           | NA<br />cohere-toolkit                       | website online training<br />offline inference only            |
| DeepSeek                                     | deepspeek-ai/[deepseek-v2](https://github.com/deepseek-ai/DeepSeek-V2)                                                                                                                                | torch           | Transformers                  | NA                                                                | NA                                                 | NA                                       | NA                                           | NA                                           | hf model only                                                   |
| Qwen                                         | QwenLM/[Qwen ](https://github.com/QwenLM/Qwen)(Alibaba)                                                                                                                                               | torch           | Transformers/ PEFT            | transformers.deepspeed                                            | customized                                         | transformers                             | transformers                                 | transformers                                 | deeply based on<br />huggingface pkgs                          |
| Yi                                           | 01-ai/[Yi](https://github.com/01-ai/Yi/)                                                                                                                                                              | torch           | Transformers                  | deepspeed                                                         | datasets (hf)/<br />torch.data / <br />customized | customized                               | customed                                     | NA                                           |                                                                 |
| Baichuan                                     | baichuan-inc/[baichuan-7b](https://github.com/baichuan-inc/Baichuan-7B)                                                                                                                               | torch           | Transformers/ xformers        | deepspeed                                                         | customized                                         | customized                               | deepspeed                                    | NA                                           |                                                                 |
|                                              | baichuan-inc/[baichuan2](https://github.com/baichuan-inc/Baichuan2)                                                                                                                                   | torch           | Transformers/ xformers        | deepspeed                                                         | customized                                         | customized                               | transformers                                 | NA                                           |                                                                 |
| ChatGLM                                      | THUDM/[ChatGLM-6B](https://github.com/THUDM/ChatGLM-6B)                                                                                                                                               | torch           | Transformers                  | deepspeed                                                         | datasets                                           | customized                               | Transformers/customized                      | NA                                           |                                                                 |
|                                              | THUDM/[ChatGLM2-6B](https://github.com/THUDM/ChatGLM2-6B)                                                                                                                                             | torch           | Transformers                  | deepspeed                                                         | datasets                                           | customized                               | Transformers/customized                      | NA                                           |                                                                 |
|                                              | THUDM/[chatGLM3](https://github.com/THUDM/ChatGLM3)                                                                                                                                                   | torch           | Transformers                  | deepspeed                                                         | customized                                         | customized                               | Transformers/PEFT                            | NA                                           |                                                                 |
|                                              | THUDM/[GLM-4](https://github.com/THUDM/GLM-4)                                                                                                                                                         | torch           | Transformers                  | deepspeed                                                         | customized                                         | customized                               | Transformers/PEFT                            | NA                                           |                                                                 |
| BLOOM                                        | bigscience/BLOOM                                                                                                                                                                                   | torch           | Transformers                  | accelerate                                                        | datasets (hf)                                      | Transformers                             | Transformers                                 | Transformers                                 | hf project                                                      |
|                                              |                                                                                                                                                                                                    |                 |                               |                                                                   |                                                    |                                          |                                              |                                              |                                                                 |



**TODO**

- OpenBMB
  - [MiniCPM-2B](https://huggingface.co/collections/openbmb/minicpm-2b-65d48bf958302b9fd25b698f)
  - [OmniLLM-12B](https://huggingface.co/openbmb/OmniLMM-12B)
  - [VisCPM-10B](https://huggingface.co/openbmb/VisCPM-Chat)
  - [CPM-Bee-1|2|5|10B](https://huggingface.co/collections/openbmb/cpm-bee-65d491cc84fc93350d789361)
- RWKV Foundation
  - [RWKV-v4|5|6](https://huggingface.co/RWKV)
- ElutherAI
  - [Pythia-1|1.4|2.8|6.9|12B](https://github.com/EleutherAI/pythia)
- Stability AI
  - [StableLM-3B](https://huggingface.co/collections/stabilityai/stable-lm-650852cfd55dd4e15cdcb30a)
  - [StableLM-v2-1.6|12B](https://huggingface.co/collections/stabilityai/stable-lm-650852cfd55dd4e15cdcb30a)
  - [StableCode-3B](https://huggingface.co/collections/stabilityai/stable-code-64f9dfb4ebc8a1be0a3f7650)
- BigCode
  - [StarCoder-1|3|7B](https://huggingface.co/collections/bigcode/%E2%AD%90-starcoder-64f9bd5740eb5daaeb81dbec)
  - [StarCoder2-3|7|15B](https://huggingface.co/collections/bigcode/starcoder2-65de6da6e87db3383572be1a)
- DataBricks
  - [MPT-7B](https://www.databricks.com/blog/mpt-7b)
- Shanghai AI Laboratory
  - [InternLM2-1.8|7|20B](https://huggingface.co/collections/internlm/internlm2-65b0ce04970888799707893c)
  - [InternLM-Math-7B|20B](https://huggingface.co/collections/internlm/internlm2-math-65b0ce88bf7d3327d0a5ad9f)
  - [InternLM-XComposer2-1.8|7B](https://huggingface.co/collections/internlm/internlm-xcomposer2-65b3706bf5d76208998e7477)
  - [InternVL-2|6|14|26](https://huggingface.co/collections/OpenGVLab/internvl-65b92d6be81c86166ca0dde4)