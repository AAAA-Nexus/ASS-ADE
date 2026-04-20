# ASS-ADE LoRA Training Guide

This guide covers the local LoRA training pipeline introduced in v0.0.1. The pipeline is **free-tier and self-contained** — no Nexus token, no cloud GPU subscription, and no data leaves your machine unless you explicitly opt in.

---

## How it works

### Local training (private by default)

Your own development data — rebuild certificates, enhancement reports, cycle outputs — is collected from the project directory and used to fine-tune a small language model adapter on your own hardware. Nothing leaves your machine.

```
Your project data → collect → train (local or Colab) → adapter → serve locally
```

The adapter is saved to `models/lora_adapter/` and served over a local HTTP endpoint at `localhost:8081`. The ASS-ADE interpreter can call this endpoint for enhanced synthesis without touching any external API.

### Submission (optional, anonymized)

If you choose to submit via `ass-ade lora capture`, your data is anonymized to structural patterns before transmission. See [DATA_AGREEMENT.md](DATA_AGREEMENT.md) for exactly what is and is not sent.

### Cloud training (optional, paid)

The existing `ass-ade lora-train` command uses a dedicated GPU on atomadic.tech. This is separate from the local pipeline and requires an `AAAA_NEXUS_OWNER_TOKEN`. The local pipeline described in this guide is entirely independent.

---

## Step by step

### Step 1 — Collect training data

```bash
ass-ade train --collect
```

This scans your project for:
- `CERTIFICATE.json` — rebuild certificates from past runs
- `benchmarks/*.txt` — self-rebuild, self-enhance, self-certify terminal outputs
- `.ass-ade/reports/*.md` and `*.json` — enhancement cycle reports
- `NEXT_ENHANCEMENT.md` — suggestion quality data
- `REBUILD_REPORT.md` — rebuild summaries if present
- `memory/conversation_history.jsonl` — conversation history if present
- `.ass-ade/lora_buffer.jsonl` — captured code transformations from the flywheel

Output: `training_data/training_data.jsonl` in HuggingFace instruction format:
```json
{"instruction": "...", "input": "...", "output": "..."}
```

To scan a specific directory:
```bash
ass-ade train --collect --root /path/to/your/project
```

### Step 2 — Train locally or on Colab

**With a GPU (local or Colab):**
```bash
ass-ade train --run
```

**Without a GPU (CPU only):**
The command automatically detects no GPU and prints Colab instructions instead.

**Custom options:**
```bash
ass-ade train --run --base Qwen/Qwen2.5-Coder-1.5B-Instruct --epochs 5 --lora-rank 16
```

**Standalone script:**
```bash
python scripts/lora_training/train_lora.py --data training_data/training_data.jsonl --epochs 3
```

#### Using the Colab notebook

1. Open `scripts/lora_training/colab_notebook.ipynb`
2. In Colab: File → Upload notebook
3. Runtime → Change runtime type → **T4 GPU** (free tier)
4. Run Cell 1 to verify GPU is available
5. Run Cell 2 to install dependencies
6. Run Cell 3 to upload your `training_data/training_data.jsonl`
7. Run Cells 4–9 to train (~15 min for 500 samples, 3 epochs)
8. Run Cell 10 to download `lora_adapter.zip`
9. Unzip into `models/lora_adapter/` in your project
10. Run `ass-ade train --serve`

### Step 3 — Serve the adapter

```bash
ass-ade train --serve
```

Starts a local HTTP server at `http://127.0.0.1:8081`. The ASS-ADE interpreter will use this automatically when it is running.

**Endpoints:**
```
POST /generate
  Body: {"prompt": "...", "max_new_tokens": 256, "temperature": 0.7}
  Response: {"text": "...", "model": "...", "tokens": 256}

GET /health
  Response: {"status": "ok", "model": "...", "adapter": "...", "loaded": true}
```

**Quick test:**
```bash
curl -s -X POST http://localhost:8081/generate \
  -H 'Content-Type: application/json' \
  -d '{"prompt": "### Instruction:\nAnalyze this code for issues.\n\n### Input:\nprint(eval(input()))\n\n### Response:\n", "max_new_tokens": 128}'
```

**Pre-load model on startup (avoids first-request latency):**
```bash
ass-ade train --serve --preload
```

### Step 4 — Grow the dataset over time

After every rebuild, the post-rebuild hook `hooks/post_rebuild_collect_training.py` automatically appends new samples to `training_data/training_data.jsonl`. Re-run `--run` periodically to incorporate new data.

---

## Base model options

| Profile | Model | Size | Colab time | Notes |
|---|---|---|---|---|
| **fast** (default) | `TinyLlama/TinyLlama-1.1B-Chat-v1.0` | 1.1B | ~15 min | Free T4 OK, CPU feasible |
| **medium** | `Qwen/Qwen2.5-Coder-1.5B-Instruct` | 1.5B | ~20 min | Better code quality |
| **large** | `Qwen/Qwen2.5-Coder-7B-Instruct` | 7B | ~60 min | Needs T4 or better |

Switch models with `--base`:
```bash
ass-ade train --run --base Qwen/Qwen2.5-Coder-1.5B-Instruct
```

---

## Install dependencies

```bash
pip install -e ".[lora]"
```

This installs: `torch`, `transformers`, `peft`, `datasets`, `accelerate`, `safetensors`, `huggingface_hub`, `sentencepiece`.

---

## Credit rewards (optional)

When you submit anonymized patterns via `ass-ade lora capture`, the Nexus quality gate scores each submission. Patterns that clear the threshold are incorporated into the shared community adapter and you earn API credits applied automatically on your next paid calls.

Reward tiers:
- **Accepted** (score ≥ 0.7): 1 credit per accepted sample
- **High quality** (score ≥ 0.9): 5 credits per sample
- **Featured** (selected for major adapter update): 50 credits

Check your balance: `ass-ade lora-credit`

---

## FAQ

**Q: Does `--collect` send any data to atomadic.tech?**
No. `--collect`, `--run`, and `--serve` are fully local. Data only leaves your machine if you explicitly run `ass-ade lora capture`.

**Q: What format does the training data use?**
HuggingFace instruction format, one JSON object per line:
```json
{"instruction": "...", "input": "...", "output": "..."}
```

**Q: Can I add my own training samples?**
Yes. Append any line in the above format to `training_data/training_data.jsonl` and re-run `--run`.

**Q: The model is bad after training. What should I do?**
Collect more data (run more rebuild/enhance cycles first), increase epochs (`--epochs 5`), or switch to a larger base model.

**Q: Do I need a HuggingFace account?**
No, not for local training. You only need one if you want to push the adapter to the Hub (optional Cell in the Colab notebook).

**Q: Where is the adapter stored?**
`models/lora_adapter/` by default. Override with `--output-dir`.

**Q: Can I use a different base model?**
Yes — any causal LM on HuggingFace with `q_proj`/`v_proj`/`k_proj`/`o_proj` attention layers works with the default LoRA target modules. Pass `--base your/model-id`.

---

## Troubleshooting

**`ModuleNotFoundError: No module named 'peft'`**
Run `pip install -e ".[lora]"`.

**`Only N samples — need at least 10`**
Run `ass-ade train --collect` first. If you still get too few, run some rebuild/enhance cycles to generate more data.

**`adapter not found at models/lora_adapter`**
Either run `ass-ade train --run` to train, or download `lora_adapter.zip` from Colab and unzip to `models/lora_adapter/`.

**Out of memory on GPU**
Reduce `--batch-size 1` or `--max-length 256`.

**Very slow on CPU**
Expected. Use `--max-length 256` and `--epochs 1` for a quick smoke-test, then move to Colab for full training.
