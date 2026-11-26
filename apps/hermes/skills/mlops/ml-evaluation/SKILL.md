---
name: ml-evaluation
description: "ML evaluation umbrella: LM benchmarking (lm-eval-harness) + experiment tracking (W&B)."
version: 1.0.0
author: Orchestra Research
license: MIT
dependencies: [lm-eval, wandb, transformers, vllm]
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Evaluation, LM Evaluation Harness, Benchmarking, MMLU, HumanEval, GSM8K, EleutherAI, MLOps, Weights And Biases, WandB, Experiment Tracking, Hyperparameter Tuning, Model Registry, Collaboration, Real-Time Visualization, PyTorch, TensorFlow, HuggingFace, Academic Benchmarks, Industry Standard]

---

# ML Evaluation — LLM Benchmarking & Experiment Tracking

This umbrella skill covers two complementary ML evaluation workflows:

1. **[LM Evaluation Harness (EleutherAI)](#lm-evaluation-harness-eleutherai)** — benchmark LLMs across 60+ academic tasks (MMLU, GSM8K, HumanEval, HellaSwag, etc.)
2. **[Weights & Biases (W&B)](#weights--biases-wb)** — log experiments, sweep hyperparameters, manage models and artifacts

---

## LM Evaluation Harness (EleutherAI)

Evaluates LLMs across 60+ academic benchmarks using standardized prompts and metrics. Industry standard used by EleutherAI, HuggingFace, and major labs. Supports HuggingFace, vLLM, OpenAI, and Anthropic APIs.

### Quick start

**Installation**:
```bash
pip install lm-eval
```

**Evaluate any HuggingFace model**:
```bash
lm_eval --model hf \
  --model_args pretrained=meta-llama/Llama-2-7b-hf \
  --tasks mmlu,gsm8k,hellaswag \
  --device cuda:0 \
  --batch_size 8
```

**View available tasks**:
```bash
lm_eval --tasks list
```

### Common workflows

#### Workflow 1: Standard benchmark evaluation

```bash
# Full standard suite (recommended for model releases)
lm_eval --model hf \
  --model_args pretrained=meta-llama/Llama-2-7b-hf \
  --tasks mmlu,gsm8k,hellaswag,truthfulqa,arc_challenge \
  --num_fewshot 5 \
  --batch_size 8 \
  --output_path results/llama2-7b-eval.json \
  --log_samples
```

**Core benchmarks**:
- **MMLU** — 57 subjects, multiple choice, broad knowledge
- **GSM8K** — grade school math word problems
- **HellaSwag** — common sense reasoning
- **TruthfulQA** — truthfulness and factuality
- **ARC** — science questions
- **HumanEval** — Python code generation (164 problems)

#### Workflow 2: Track training progress

```bash
#!/bin/bash
# eval_checkpoint.sh
CHECKPOINT_DIR=$1
STEP=$2

lm_eval --model hf \
  --model_args pretrained=$CHECKPOINT_DIR/checkpoint-$STEP \
  --tasks gsm8k,hellaswag \
  --num_fewshot 0 \
  --batch_size 16 \
  --output_path results/step-$STEP.json
```

Fast benchmarks for frequent evaluation: **HellaSwag** (~10 min), **GSM8K** (~5 min), **PIQA** (~2 min).

#### Workflow 3: Compare multiple models

```bash
#!/bin/bash
# eval_all_models.sh
TASKS="mmlu,gsm8k,hellaswag,truthfulqa"

while read model; do
    model_name=$(echo $model | sed 's/\\//-/g')
    lm_eval --model hf \
      --model_args pretrained=$model,dtype=bfloat16 \
      --tasks $TASKS \
      --num_fewshot 5 \
      --batch_size auto \
      --output_path results/$model_name.json
done < models.txt
```

#### Workflow 4: Evaluate with vLLM (5–10× faster)

```bash
lm_eval --model vllm \
  --model_args pretrained=meta-llama/Llama-2-7b-hf,tensor_parallel_size=2 \
  --tasks mmlu \
  --batch_size auto
```

### Common issues

| Issue | Fix |
|-------|-----|
| Too slow | Use vLLM backend or reduce `--num_fewshot 0` |
| Out of memory | `--batch_size 1` or `--model_args load_in_8bit=True` |
| Different results than reported | Check `--num_fewshot 5` and exact task name |
| HumanEval not executing | `pip install human-eval` + `--allow_code_execution` |

### Hardware requirements

- **GPU**: NVIDIA (CUDA 11.8+)
- **VRAM**: 7B model = 16GB (bf16) or 8GB (8-bit); 13B = 28GB (bf16)
- **Time** (7B, single A100): HellaSwag 10 min, GSM8K 5 min, MMLU 2 hr

### Advanced references

- **Benchmark descriptions**: [references/lm-harness-benchmark-guide.md](references/lm-harness-benchmark-guide.md) — all 60+ tasks, what they measure, interpretation
- **Custom tasks**: [references/lm-harness-custom-tasks.md](references/lm-harness-custom-tasks.md) — domain-specific evaluation tasks via YAML + Python
- **API evaluation**: [references/lm-harness-api-evaluation.md](references/lm-harness-api-evaluation.md) — OpenAI, Anthropic, local API models
- **Multi-GPU strategies**: [references/lm-harness-distributed-eval.md](references/lm-harness-distributed-eval.md) — data parallel and tensor parallel evaluation

### Resources

- GitHub: https://github.com/EleutherAI/lm-evaluation-harness
- Leaderboard: https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard

---

## Weights & Biases (W&B)

Track ML experiments with automatic metric logging, real-time dashboards, hyperparameter sweeps, model registry, and artifact lineage. Supports PyTorch, TensorFlow, HuggingFace, Lightning, and 100+ other integrations.

**Users**: 200,000+ ML practitioners | **GitHub Stars**: 10.5k+

### Installation

```bash
pip install wandb
wandb login
# Or: export WANDB_API_KEY=your_api_key_here
```

### Quick start

```python
import wandb

run = wandb.init(
    project="my-project",
    config={"learning_rate": 0.001, "epochs": 10, "batch_size": 32}
)

for epoch in range(run.config.epochs):
    train_loss = train_epoch()
    val_loss = validate()
    wandb.log({"train/loss": train_loss, "val/loss": val_loss, "epoch": epoch})

wandb.finish()
```

### Core concepts

#### Experiment tracking

```python
# Log scalars, media, histograms, tables
wandb.log({"loss": 0.5, "accuracy": 0.92})
wandb.log({"examples": [wandb.Image(img) for img in images]})
wandb.log({"gradients": wandb.Histogram(gradients)})
```

#### Hyperparameter sweeps

```python
sweep_config = {
    'method': 'bayes',  # or 'grid', 'random'
    'metric': {'name': 'val/accuracy', 'goal': 'maximize'},
    'parameters': {
        'learning_rate': {'distribution': 'log_uniform', 'min': 1e-5, 'max': 1e-1},
        'batch_size': {'values': [16, 32, 64, 128]},
    }
}

sweep_id = wandb.sweep(sweep_config, project="my-project")
wandb.agent(sweep_id, function=train, count=50)
```

#### Artifacts & model registry

```python
# Create and log artifact
artifact = wandb.Artifact('model', type='model', metadata={'accuracy': 0.95})
artifact.add_file('model.pth')
wandb.log_artifact(artifact)

# Link to model registry
run.link_artifact(artifact, 'model-registry/production-models', aliases=['staging'])

# Use artifact in another run
artifact = run.use_artifact('training-data:latest')
artifact_dir = artifact.download()
```

### HuggingFace integration

```python
from transformers import Trainer, TrainingArguments

training_args = TrainingArguments(
    output_dir="./results",
    report_to="wandb",
    run_name="bert-finetuning",
    logging_steps=100,
    save_steps=500
)

trainer = Trainer(model=model, args=training_args, ...)
trainer.train()
```

### PyTorch Lightning integration

```python
from pytorch_lightning.loggers import WandbLogger

wandb_logger = WandbLogger(project="lightning-demo", log_model=True)
trainer = pl.Trainer(logger=wandb_logger, max_epochs=10)
trainer.fit(model, datamodule=dm)
```

### Best practices

1. **Organize with tags and groups**: `tags=["baseline", "resnet50"]`, `group="resnet-experiments"`
2. **Use descriptive run names**: `name="bert-base-lr0.001-bs32-epoch10"`
3. **Log system metrics**: GPU/CPU utilization, memory
4. **Use offline mode** when connection is unstable: `os.environ["WANDB_MODE"] = "offline"`
5. **Use Bayesian sweeps** for expensive experiments — most sample-efficient strategy

### Pricing

- **Free**: Unlimited public projects, 100GB storage
- **Academic**: Free for students/researchers
- **Teams**: $50/seat/month, private projects
- **Enterprise**: Custom pricing, on-prem options

### Advanced references

- **Hyperparameter sweeps**: [references/wandb-sweeps.md](references/wandb-sweeps.md) — all search strategies, distributions, early termination, parallel execution
- **Artifacts & model registry**: [references/wandb-artifacts.md](references/wandb-artifacts.md) — versioning, lineage, team collaboration patterns
- **Framework integrations**: [references/wandb-integrations.md](references/wandb-integrations.md) — HuggingFace, Lightning, Keras, fast.ai, XGBoost, LightGBM examples

### Resources

- **Documentation**: https://docs.wandb.ai
- **GitHub**: https://github.com/wandb/wandb
- **Examples**: https://github.com/wandb/examples
