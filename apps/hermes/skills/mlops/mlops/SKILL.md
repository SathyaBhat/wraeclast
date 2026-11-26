---
name: mlops
description: "MLOps umbrella: local LLM inference, model evaluation, image segmentation (SAM) — route to the right skill."
version: 1.0.0
author: Hermes Agent (curator)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [mlops, llm, inference, evaluation, benchmarking, segmentation, sam, llama, vllm, lm-eval, gguf, quantization]
    related_skills: [local-llm-inference, ml-evaluation, segment-anything-model]
---

# MLOps Umbrella

Three sibling skills cover the MLOps space — serving local LLMs, benchmarking model quality, and applying specialist models for image segmentation. Load this umbrella to orient; load the specific skill for execution.

## Skill Map

| Skill | Load when… |
|---|---|
| **local-llm-inference** | Run LLMs locally — llama.cpp/GGUF, vLLM serving, Ollama; download models, set quantization, expose an OpenAI-compatible API endpoint |
| **ml-evaluation** | Benchmark LLMs with lm-eval-harness; run standard tasks (MMLU, HellaSwag, etc.); compare model quality metrics |
| **segment-anything-model** | Zero-shot image segmentation using SAM (Segment Anything Model) — points, boxes, or mask prompts; output masks and bounding boxes |

## Routing Guide

**"Run / serve a local LLM"** → **local-llm-inference**

**"Download and quantize a model / set up Ollama"** → **local-llm-inference**

**"Benchmark this model / run MMLU / compare models"** → **ml-evaluation**

**"Segment objects in this image"** → **segment-anything-model**

**"Generate images / video / audio with ComfyUI"** → NOT this umbrella → load **comfyui** (in the `creative` category)

## Shared Infrastructure Notes

### GPU/VRAM requirements

| Task | Minimum VRAM |
|---|---|
| 7B model (GGUF Q4) | 6 GB |
| 13B model (GGUF Q4) | 10 GB |
| 70B model (GGUF Q4) | 40+ GB |
| SAM (ViT-H) | 16 GB |
| lm-eval full suite | Depends on model |

### Python environment pattern

All three skills use Python. Use `uv` for fast environment setup:

```bash
uv venv .venv && source .venv/bin/activate
uv pip install <skill-specific deps>
```

### Model storage convention

Store models under `~/models/` (or configure via the skill-specific env var). Heavy models should not go in the project repo.

## Pitfalls

- **CUDA version mismatch** — llama.cpp GPU builds, vLLM, and PyTorch all pin to specific CUDA versions; mismatch causes silent CPU fallback or import errors. Check `nvcc --version` and `nvidia-smi` before installing
- **lm-eval GPU memory** — benchmarks run many forward passes; reduce `--batch-size` if you get CUDA OOM
- **SAM model size** — ViT-H is most accurate but requires 16 GB VRAM; ViT-B is the fast/small option at ~1 GB
- **Ollama vs llama.cpp** — Ollama is higher-level (model management built in); llama.cpp is lower-level (fine-grained control over quantization, context length). Use Ollama for convenience, llama.cpp when you need exact control
