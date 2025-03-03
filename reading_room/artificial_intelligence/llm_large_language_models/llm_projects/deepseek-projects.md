# DeepSeek Projects

- ✔ https://github.com/deepseek-ai/open-infra-index
  - [**FlashMLA GitHub Repo**](https://github.com/deepseek-ai/FlashMLA)
  - [**DeepEP GitHub Repo**](https://github.com/deepseek-ai/DeepEP)
  - [**DeepGEMM GitHub Repo**](https://github.com/deepseek-ai/DeepGEMM)
  - **DualPipe**
  - **Fire-Flyer File System (3FS)**

# DeepSeek R1

- https://github.com/deepseek-ai/DeepSeek-R1
- https://huggingface.co/deepseek-ai/DeepSeek-R1

| **Model** | **#Total Params** | **#Activated Params** | **Context Length** |                         **Download**                         |
| :--------------: | :---------------------: | :-------------------------: | :----------------------: | :----------------------------------------------------------------: |
| DeepSeek-R1-Zero |          671B          |             37B             |           128K           | [🤗 HuggingFace](https://huggingface.co/deepseek-ai/DeepSeek-R1-Zero) |
|   DeepSeek-R1   |          671B          |             37B             |           128K           |   [🤗 HuggingFace](https://huggingface.co/deepseek-ai/DeepSeek-R1)   |

|        **Model**        |                              **Base Model**                              |                               **Download**                               |
| :---------------------------: | :-----------------------------------------------------------------------------: | :-----------------------------------------------------------------------------: |
| DeepSeek-R1-Distill-Qwen-1.5B |         [Qwen2.5-Math-1.5B](https://huggingface.co/Qwen/Qwen2.5-Math-1.5B)         | [🤗 HuggingFace](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B) |
|  DeepSeek-R1-Distill-Qwen-7B  |           [Qwen2.5-Math-7B](https://huggingface.co/Qwen/Qwen2.5-Math-7B)           |  [🤗 HuggingFace](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-7B)  |
| DeepSeek-R1-Distill-Llama-8B |           [Llama-3.1-8B](https://huggingface.co/meta-llama/Llama-3.1-8B)           | [🤗 HuggingFace](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Llama-8B) |
| DeepSeek-R1-Distill-Qwen-14B |               [Qwen2.5-14B](https://huggingface.co/Qwen/Qwen2.5-14B)               | [🤗 HuggingFace](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-14B) |
| DeepSeek-R1-Distill-Qwen-32B |               [Qwen2.5-32B](https://huggingface.co/Qwen/Qwen2.5-32B)               | [🤗 HuggingFace](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-32B) |
| DeepSeek-R1-Distill-Llama-70B | [Llama-3.3-70B-Instruct](https://huggingface.co/meta-llama/Llama-3.3-70B-Instruct) | [🤗 HuggingFace](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Llama-70B) |

- deployment requirement same as Deepseek-V3
- quickstart

```bash
vllm serve deepseek-ai/DeepSeek-R1-Distill-Qwen-32B --tensor-parallel-size 2 --max-model-len 32768 --enforce-eager
```

```bash
python3 -m sglang.launch_server --model deepseek-ai/DeepSeek-R1-Distill-Qwen-32B --trust-remote-code --tp 2
```

# DeepSeek V3

- https://github.com/deepseek-ai/DeepSeek-V3
- https://huggingface.co/deepseek-ai/DeepSeek-V3

| **Model** | **#Total Params** | **#Activated Params** | **Context Length** |                         **Download**                         |
| :--------------: | :---------------------: | :-------------------------: | :----------------------: | :-----------------------------------------------------------------: |
| DeepSeek-V3-Base |          671B          |             37B             |           128K           | [🤗 Hugging Face](https://huggingface.co/deepseek-ai/DeepSeek-V3-Base) |
|   DeepSeek-V3   |          671B          |             37B             |           128K           |   [🤗 Hugging Face](https://huggingface.co/deepseek-ai/DeepSeek-V3)   |

## 6. How to Run Locally

DeepSeek-V3 can be deployed locally using the following hardware and open-source community software:

1. **DeepSeek-Infer Demo**: We provide a simple and lightweight demo for FP8 and BF16 inference.
2. **SGLang**: Fully support the DeepSeek-V3 model in both BF16 and FP8 inference modes, with Multi-Token Prediction [coming soon](https://github.com/sgl-project/sglang/issues/2591).
3. **LMDeploy**: Enables efficient FP8 and BF16 inference for local and cloud deployment.
4. **TensorRT-LLM**: Currently supports BF16 inference and INT4/8 quantization, with FP8 support coming soon.
5. **vLLM**: Support DeepSeek-V3 model with FP8 and BF16 modes for tensor parallelism and pipeline parallelism.
6. **AMD GPU**: Enables running the DeepSeek-V3 model on AMD GPUs via SGLang in both BF16 and FP8 modes.
7. **Huawei Ascend NPU**: Supports running DeepSeek-V3 on Huawei Ascend devices.

Since FP8 training is natively adopted in our framework, we only provide FP8 weights. If you require BF16 weights for experimentation, you can use the provided conversion script to perform the transformation.

Here is an example of converting FP8 weights to BF16:

```shell
cd inference
python fp8_cast_bf16.py --input-fp8-hf-path /path/to/fp8_weights --output-bf16-hf-path /path/to/bf16_weights
```

> [!NOTE]
> Hugging Face's Transformers has not been directly supported yet.

### 6.1 Inference with DeepSeek-Infer Demo (example only)

#### System Requirements

> [!NOTE]
> Linux with Python 3.10 only. Mac and Windows are not supported.

Dependencies:

```pip-requirements
torch==2.4.1
triton==3.0.0
transformers==4.46.3
safetensors==0.4.5
```

#### Model Weights & Demo Code Preparation

First, clone our DeepSeek-V3 GitHub repository:

```shell
git clone https://github.com/deepseek-ai/DeepSeek-V3.git
```

Navigate to the `inference` folder and install dependencies listed in `requirements.txt`. Easiest way is to use a package manager like `conda` or `uv` to create a new virtual environment and install the dependencies.

```shell
cd DeepSeek-V3/inference
pip install -r requirements.txt
```

Download the model weights from Hugging Face, and put them into `/path/to/DeepSeek-V3` folder.

#### Model Weights Conversion

Convert Hugging Face model weights to a specific format:

```shell
python convert.py --hf-ckpt-path /path/to/DeepSeek-V3 --save-path /path/to/DeepSeek-V3-Demo --n-experts 256 --model-parallel 16
```

#### Run

Then you can chat with DeepSeek-V3:

```shell
torchrun --nnodes 2 --nproc-per-node 8 --node-rank $RANK --master-addr $ADDR generate.py --ckpt-path /path/to/DeepSeek-V3-Demo --config configs/config_671B.json --interactive --temperature 0.7 --max-new-tokens 200
```

Or batch inference on a given file:

```shell
torchrun --nnodes 2 --nproc-per-node 8 --node-rank $RANK --master-addr $ADDR generate.py --ckpt-path /path/to/DeepSeek-V3-Demo --config configs/config_671B.json --input-file $FILE
```

### Inference with SGLang (recommended)

[SGLang](https://github.com/sgl-project/sglang) currently supports [MLA optimizations](https://lmsys.org/blog/2024-09-04-sglang-v0-3/#deepseek-multi-head-latent-attention-mla-throughput-optimizations), [DP Attention](https://lmsys.org/blog/2024-12-04-sglang-v0-4/#data-parallelism-attention-for-deepseek-models), FP8 (W8A8), FP8 KV Cache, and Torch Compile, delivering state-of-the-art latency and throughput performance among open-source frameworks.

Notably, [SGLang v0.4.1](https://github.com/sgl-project/sglang/releases/tag/v0.4.1) fully supports running DeepSeek-V3 on both **NVIDIA and AMD GPUs**, making it a highly versatile and robust solution.

SGLang also supports [multi-node tensor parallelism](https://github.com/sgl-project/sglang/tree/main/benchmark/deepseek_v3#example-serving-with-2-h208), enabling you to run this model on multiple network-connected machines.

Multi-Token Prediction (MTP) is in development, and progress can be tracked in the [optimization plan](https://github.com/sgl-project/sglang/issues/2591).

Here are the launch instructions from the SGLang team: https://github.com/sgl-project/sglang/tree/main/benchmark/deepseek_v3

### Inference with LMDeploy (recommended)

[LMDeploy](https://github.com/InternLM/lmdeploy), a flexible and high-performance inference and serving framework tailored for large language models, now supports DeepSeek-V3. It offers both offline pipeline processing and online deployment capabilities, seamlessly integrating with PyTorch-based workflows.

For comprehensive step-by-step instructions on running DeepSeek-V3 with LMDeploy, please refer to here: https://github.com/InternLM/lmdeploy/issues/2960

### Inference with TRT-LLM (recommended)

[TensorRT-LLM](https://github.com/NVIDIA/TensorRT-LLM) now supports the DeepSeek-V3 model, offering precision options such as BF16 and INT4/INT8 weight-only. Support for FP8 is currently in progress and will be released soon. You can access the custom branch of TRTLLM specifically for DeepSeek-V3 support through the following link to experience the new features directly: https://github.com/NVIDIA/TensorRT-LLM/tree/deepseek/examples/deepseek_v3.

### Inference with vLLM (recommended)

[vLLM](https://github.com/vllm-project/vllm) v0.6.6 supports DeepSeek-V3 inference for FP8 and BF16 modes on both NVIDIA and AMD GPUs. Aside from standard techniques, vLLM offers _pipeline parallelism_ allowing you to run this model on multiple machines connected by networks. For detailed guidance, please refer to the [vLLM instructions](https://docs.vllm.ai/en/latest/serving/distributed_serving.html). Please feel free to follow [the enhancement plan](https://github.com/vllm-project/vllm/issues/11539) as well.

### Recommended Inference Functionality with AMD GPUs

In collaboration with the AMD team, we have achieved Day-One support for AMD GPUs using SGLang, with full compatibility for both FP8 and BF16 precision. For detailed guidance, please refer to the [SGLang instructions](#63-inference-with-lmdeploy-recommended).

### Recommended Inference Functionality with Huawei Ascend NPUs

The [MindIE](https://www.hiascend.com/en/software/mindie) framework from the Huawei Ascend community has successfully adapted the BF16 version of DeepSeek-V3. For step-by-step guidance on Ascend NPUs, please follow the [instructions here](https://modelers.cn/models/MindIE/deepseekv3).

## Ollama
