---
name: local-llm-inference
description: "Local LLM inference umbrella: llama.cpp/GGUF, vLLM serving, and Hugging Face Hub model management."
version: 1.0.0
author: Hermes Agent (curator)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [LLM, Inference, llama.cpp, GGUF, vLLM, HuggingFace, Local, Quantization, Serving, OpenAI-API]
    related_skills: [ml-evaluation]
---

# Local LLM Inference

Three complementary tools for running, discovering, and serving large language models locally. Choose the right tool for your workload:

## MLOps Skill Map

| Phase | Skill | Load when… |
|---|---|---|
| **Discover & download** | `local-llm-inference` (this skill, Section 3 `hf` CLI) | Finding GGUF variants on HF Hub, downloading checkpoints |
| **Run locally** | `local-llm-inference` (Section 1 llama.cpp) | Single-user CPU/GPU inference, edge devices, GGUF quants |
| **Serve in production** | `local-llm-inference` (Section 2 vLLM) | Production API servers, high-throughput multi-user deployments |
| **Benchmark / evaluate** | `ml-evaluation` | Running lm-eval-harness benchmarks, tracking runs with W&B |
| **Generate images / video** | `comfyui` | ComfyUI workflows with SD, Flux, Wan, Hunyuan models |
| **Segment images** | `segment-anything-model` | Zero-shot image segmentation with SAM |

## Tool Selection (this skill)

| Tool | Best for | GPU required? |
|------|----------|--------------|\n| **llama.cpp** | CPU/edge/single-user, GGUF quants | No (GPU optional) |
| **vLLM** | Production API servers, high throughput | Yes (NVIDIA primary) |
| **Hugging Face `hf` CLI** | Discovering, downloading, uploading models/datasets | No |

---

## Section 1 — llama.cpp + GGUF

Use for local GGUF inference, quant selection, or HF Hub model discovery for llama.cpp.

### When to use
- Run local models on CPU, Apple Silicon, CUDA, ROCm, or Intel GPUs
- Find the right GGUF for a specific Hugging Face repo
- Build a `llama-server` or `llama-cli` command from the Hub
- Search the Hub for models that already support llama.cpp

### Model Discovery (URL-first workflow)

Prefer URL workflows before asking for `hf`, Python, or custom scripts.

1. Search for candidate repos: `https://huggingface.co/models?apps=llama.cpp&sort=trending`
2. Open with llama.cpp local-app view: `https://huggingface.co/<repo>?local-app=llama.cpp`
3. Treat the local-app snippet as source of truth — copy exact `llama-server` command
4. Confirm what exists via tree API: `https://huggingface.co/api/models/<repo>/tree/main?recursive=true`
   - Keep entries where `type=file` and `path` ends with `.gguf`
   - Use `path` and `size` as truth for filenames and byte sizes
5. If local-app snippet not visible, reconstruct: `llama-server -hf <repo>:<QUANT>`

### Quick start

```bash
# macOS / Linux
brew install llama.cpp

# Run directly from HF Hub
llama-cli -hf bartowski/Llama-3.2-3B-Instruct-GGUF:Q8_0
llama-server -hf bartowski/Llama-3.2-3B-Instruct-GGUF:Q8_0

# Run a specific GGUF file
llama-server \
    --hf-repo microsoft/Phi-3-mini-4k-instruct-gguf \
    --hf-file Phi-3-mini-4k-instruct-q4.gguf \
    -c 4096

# Test OpenAI-compatible endpoint
curl http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "Hello"}]}'
```

### Python bindings (llama-cpp-python)

```bash
pip install llama-cpp-python
# CUDA: CMAKE_ARGS="-DGGML_CUDA=on" pip install llama-cpp-python --force-reinstall --no-cache-dir
# Metal: CMAKE_ARGS="-DGGML_METAL=on" pip install llama-cpp-python --force-reinstall --no-cache-dir
```

```python
from llama_cpp import Llama

llm = Llama(model_path="./model-q4_k_m.gguf", n_ctx=4096, n_gpu_layers=35, n_threads=8)
out = llm("What is ML?", max_tokens=256, temperature=0.7)
print(out["choices"][0]["text"])

# Load straight from Hub
llm = Llama.from_pretrained(repo_id="bartowski/Llama-3.2-3B-Instruct-GGUF", filename="*Q4_K_M.gguf", n_gpu_layers=35)
```

### Choosing a quant

- **Q4_K_M** — general chat, balanced quality/size (default starting point)
- **Q5_K_M / Q6_K** — code or technical work, more VRAM available
- **Q3_K_M / IQ / Q2** — very tight RAM only; quality degrades noticeably
- For multimodal repos, `mmproj-*.gguf` is the projector, not the main model
- Do NOT normalize repo-native labels (`UD-Q4_K_M` stays `UD-Q4_K_M`)

### URL search patterns

```text
https://huggingface.co/models?apps=llama.cpp&sort=trending
https://huggingface.co/models?search=<term>&apps=llama.cpp&sort=trending
https://huggingface.co/models?search=<term>&apps=llama.cpp&num_parameters=min:0,max:24B&sort=trending
https://huggingface.co/<repo>?local-app=llama.cpp
https://huggingface.co/api/models/<repo>/tree/main?recursive=true
```

### Deep references (in llama-cpp skill's references/ directory)

- `references/hub-discovery.md` — URL-only HF workflows, GGUF extraction, command reconstruction
- `references/advanced-usage.md` — speculative decoding, batched inference, grammar, LoRA, multi-GPU
- `references/quantization.md` — quant quality tradeoffs, imatrix, RAM scaling
- `references/server.md` — direct-from-Hub server launch, OpenAI API, Docker, NGINX
- `references/optimization.md` — CPU threading, BLAS, GPU offload, batch tuning
- `references/troubleshooting.md` — install/convert/quantize/inference/server issues

---

## Section 2 — vLLM: High-Throughput Serving

Use when deploying production LLM APIs (100+ req/sec), serving OpenAI-compatible endpoints, or handling multi-user applications.

vLLM achieves 24x higher throughput than standard transformers through **PagedAttention** (block-based KV cache) and **continuous batching**.

### When to use vLLM vs alternatives

| Use vLLM when | Use alternative when |
|---------------|----------------------|
| Production API (100+ req/sec) | CPU/edge/single-user → **llama.cpp** |
| OpenAI-compatible endpoint | Research/prototyping → HF transformers |
| Limited GPU memory + large model | NVIDIA-only max perf → TensorRT-LLM |
| Multi-user chatbot/assistant | Already in HF ecosystem → TGI |

### Quick start

```bash
pip install vllm

# Serve a model
vllm serve meta-llama/Llama-3-8B-Instruct

# Query via OpenAI SDK
python -c "
from openai import OpenAI
client = OpenAI(base_url='http://localhost:8000/v1', api_key='EMPTY')
print(client.chat.completions.create(
    model='meta-llama/Llama-3-8B-Instruct',
    messages=[{'role': 'user', 'content': 'Hello!'}]
).choices[0].message.content)
"
```

### Production deployment

```bash
# 7B-13B models on single GPU
vllm serve meta-llama/Llama-3-8B-Instruct \
  --gpu-memory-utilization 0.9 \
  --max-model-len 8192 \
  --enable-prefix-caching \
  --enable-metrics --metrics-port 9090 \
  --port 8000 --host 0.0.0.0

# 70B+ with tensor parallelism + AWQ quantization
vllm serve meta-llama/Llama-2-70b-hf \
  --tensor-parallel-size 4 \
  --gpu-memory-utilization 0.9 \
  --quantization awq
```

### Batch offline inference

```python
from vllm import LLM, SamplingParams

llm = LLM(model="meta-llama/Llama-3-8B-Instruct", tensor_parallel_size=2, max_model_len=4096)
sampling = SamplingParams(temperature=0.7, max_tokens=512)

outputs = llm.generate(["prompt 1", "prompt 2", "prompt 3"], sampling)
for output in outputs:
    print(output.outputs[0].text)
```

### Quantization (fit large models in limited VRAM)

- **AWQ** — best for 70B, minimal accuracy loss
- **GPTQ** — wide model support, good compression
- **FP8** — fastest on H100 GPUs

```bash
vllm serve TheBloke/Llama-2-70B-AWQ --quantization awq --gpu-memory-utilization 0.95
# Result: 70B model in ~40GB VRAM
```

### Hardware requirements

| Model size | GPU recommendation |
|------------|-------------------|
| 7B–13B | 1x A10 (24GB) or A100 (40GB) |
| 30B–40B | 2x A100 (40GB) with tensor parallelism |
| 70B+ | 4x A100 (40GB) or 2x A100 (80GB) + AWQ/GPTQ |

### Common issues

| Issue | Fix |
|-------|-----|
| OOM during model load | `--gpu-memory-utilization 0.7` or `--quantization awq` |
| TTFT > 1s | `--enable-prefix-caching` or `--enable-chunked-prefill` |
| Model not found | `--trust-remote-code` |
| Low throughput | `--max-num-seqs 512`; verify tensor-parallel size is power of 2 |

### Deep references

- `references/vllm/server-deployment.md` — Docker, Kubernetes, load balancing
- `references/vllm/optimization.md` — PagedAttention tuning, continuous batching, benchmarks
- `references/vllm/quantization.md` — AWQ/GPTQ/FP8 setup and accuracy comparisons
- `references/vllm/troubleshooting.md` — error messages, debugging, performance diagnostics

---

## Section 3 — Hugging Face `hf` CLI

The `hf` command is the modern HF Hub CLI. **Replaces the deprecated `huggingface-cli`.**

### Quick start

```bash
# Install
curl -LsSf https://hf.co/cli/install.sh | bash -s

# Authenticate (use HF_TOKEN env var or --token flag)
hf auth login

# Download a model
hf download meta-llama/Llama-3.2-3B-Instruct

# Upload files
hf upload my-org/my-repo ./local-files/
```

### Core commands

**Download / Upload:**
- `hf download REPO_ID` — download files from Hub
- `hf upload REPO_ID` — upload files/folders (single commit)
- `hf upload-large-folder REPO_ID LOCAL_PATH` — resumable large-directory uploads
- `hf sync` — sync between local dir and bucket

**Authentication:**
- `hf auth login / logout / list / switch / whoami`

**Repository management:**
- `hf repos create / delete / duplicate / move / branch / tag / delete-files`

**Models & Datasets:**
- `hf models list` / `hf models info REPO_ID`
- `hf datasets list` / `hf datasets info REPO_ID`
- `hf datasets sql SQL` — query parquet files via DuckDB
- `hf papers list` — daily papers

**Infrastructure:**
- `hf jobs uv` — run Python scripts on HF compute
- `hf jobs stats` — monitor resource usage
- Inference Endpoints: `deploy`, `pause`, `resume`, `scale-to-zero`, `catalog`

**Cache:**
- `hf cache list / prune / verify`

### Automation flags

- `--format json` — machine-readable output
- `-q / --quiet` — IDs only

### Extensions

```bash
hf extensions install REPO_ID
```

---

## Resources

- llama.cpp: https://github.com/ggml-org/llama.cpp
- vLLM docs: https://docs.vllm.ai
- HF Hub docs: https://huggingface.co/docs/hub
- HF CLI: https://hf.co/docs/hub/cli
