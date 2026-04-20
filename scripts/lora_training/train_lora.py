"""LoRA fine-tuning on locally collected ASS-ADE training data.

Uses HuggingFace transformers + peft (from the [lora] extra).
Default base: TinyLlama/TinyLlama-1.1B-Chat-v1.0 — small enough for:
  - Google Colab free T4 (~15 min for 500 samples, 3 epochs)
  - Local CPU (~2-4 hours for 200 samples)

Saves adapter weights to models/lora_adapter/ (PEFT format, ~8 MB for rank 8).

Usage:
    pip install -e ".[lora]"
    python scripts/lora_training/train_lora.py
    python scripts/lora_training/train_lora.py --base Qwen/Qwen2.5-Coder-1.5B-Instruct --epochs 5

On Colab / GPU the script auto-detects and uses bfloat16 + device_map=auto.
On CPU it falls back to float32 and disables gradient checkpointing.
"""
from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Any

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
_log = logging.getLogger("train_lora")

_DEFAULT_BASE = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
_FAST_BASE = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
_MEDIUM_BASE = "Qwen/Qwen2.5-Coder-1.5B-Instruct"


def _load_samples(jsonl_path: Path) -> list[dict[str, Any]]:
    samples: list[dict[str, Any]] = []
    with jsonl_path.open(encoding="utf-8") as f:
        for raw in f:
            raw = raw.strip()
            if raw:
                try:
                    samples.append(json.loads(raw))
                except Exception:
                    pass
    return samples


def _format_sample(s: dict[str, Any], add_eos: bool = True) -> str:
    instruction = s.get("instruction", "")
    input_ = s.get("input", "")
    output = s.get("output", "")
    prompt = f"### Instruction:\n{instruction}"
    if input_:
        prompt += f"\n\n### Input:\n{input_}"
    prompt += f"\n\n### Response:\n{output}"
    return prompt


def train(
    data_path: Path,
    output_dir: Path,
    base_model: str = _DEFAULT_BASE,
    epochs: int = 3,
    lora_rank: int = 8,
    lora_alpha: int = 16,
    lora_dropout: float = 0.05,
    learning_rate: float = 2e-4,
    batch_size: int = 4,
    max_length: int = 512,
    min_samples: int = 10,
) -> Path:
    """Run LoRA fine-tuning. Returns the adapter directory path."""
    try:
        import torch
        from datasets import Dataset
        from peft import LoraConfig, TaskType, get_peft_model
        from transformers import (
            AutoModelForCausalLM,
            AutoTokenizer,
            DataCollatorForLanguageModeling,
            Trainer,
            TrainingArguments,
        )
    except ImportError as exc:
        raise RuntimeError(
            f"LoRA deps missing ({exc}). Run: pip install -e '.[lora]'"
        ) from exc

    samples = _load_samples(data_path)
    _log.info("loaded %d samples from %s", len(samples), data_path)
    if len(samples) < min_samples:
        raise RuntimeError(
            f"Only {len(samples)} samples — need at least {min_samples}. "
            "Run collect_training_data.py first."
        )

    use_gpu = torch.cuda.is_available()
    _log.info("device: %s", "cuda" if use_gpu else "cpu (slow, consider Colab)")

    tokenizer = AutoTokenizer.from_pretrained(base_model, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        base_model,
        torch_dtype=torch.bfloat16 if use_gpu else torch.float32,
        device_map="auto" if use_gpu else None,
        trust_remote_code=True,
    )

    texts = [_format_sample(s) for s in samples]
    ds = Dataset.from_dict({"text": texts})

    def _tokenize(batch: dict[str, list[str]]) -> dict[str, Any]:
        enc = tokenizer(batch["text"], truncation=True, max_length=max_length, padding=False)
        enc["labels"] = [ids.copy() for ids in enc["input_ids"]]
        return enc

    ds = ds.map(_tokenize, batched=True, remove_columns=["text"])

    lora_cfg = LoraConfig(
        r=lora_rank,
        lora_alpha=lora_alpha,
        lora_dropout=lora_dropout,
        bias="none",
        task_type=TaskType.CAUSAL_LM,
        target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
    )
    model = get_peft_model(model, lora_cfg)
    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    total = sum(p.numel() for p in model.parameters())
    _log.info("trainable params: %d / %d (%.2f%%)", trainable, total, 100 * trainable / max(total, 1))

    output_dir.mkdir(parents=True, exist_ok=True)
    training_args = TrainingArguments(
        output_dir=str(output_dir / "checkpoints"),
        num_train_epochs=epochs,
        per_device_train_batch_size=batch_size,
        gradient_accumulation_steps=max(1, 8 // batch_size),
        learning_rate=learning_rate,
        lr_scheduler_type="cosine",
        warmup_ratio=0.05,
        logging_steps=10,
        save_steps=100,
        save_total_limit=2,
        fp16=use_gpu,
        bf16=False,
        gradient_checkpointing=use_gpu,
        report_to="none",
        dataloader_pin_memory=use_gpu,
        remove_unused_columns=False,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=ds,
        data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False),
    )

    _log.info("starting training (%d samples, %d epochs)…", len(samples), epochs)
    trainer.train()

    adapter_dir = output_dir
    model.save_pretrained(str(adapter_dir))
    tokenizer.save_pretrained(str(adapter_dir))
    _log.info("adapter saved → %s", adapter_dir)
    return adapter_dir


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument(
        "--data",
        type=Path,
        default=Path("training_data/training_data.jsonl"),
        help="Path to training_data.jsonl.",
    )
    ap.add_argument(
        "--output-dir",
        type=Path,
        default=Path("models/lora_adapter"),
        help="Where to save the adapter (default: models/lora_adapter/).",
    )
    ap.add_argument("--base", default=_DEFAULT_BASE, help="Base model HF id.")
    ap.add_argument("--epochs", type=int, default=3)
    ap.add_argument("--lora-rank", type=int, default=8)
    ap.add_argument("--batch-size", type=int, default=4)
    ap.add_argument("--max-length", type=int, default=512)
    ap.add_argument("--min-samples", type=int, default=10)
    args = ap.parse_args()

    if not args.data.exists():
        print(f"[train] ERROR: {args.data} not found. Run collect_training_data.py first.", file=sys.stderr)
        sys.exit(1)

    adapter_dir = train(
        data_path=args.data.resolve(),
        output_dir=args.output_dir.resolve(),
        base_model=args.base,
        epochs=args.epochs,
        lora_rank=args.lora_rank,
        batch_size=args.batch_size,
        max_length=args.max_length,
        min_samples=args.min_samples,
    )
    print(f"[train] done — adapter at {adapter_dir}", file=sys.stderr)


def print_colab_instructions(data_path: Path = Path("training_data/training_data.jsonl")) -> None:
    """Print step-by-step Colab instructions when no GPU is available locally."""
    print(
        "\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "  No GPU detected — use Google Colab free T4:\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "\n"
        "  1. Open scripts/lora_training/colab_notebook.ipynb in Colab\n"
        "     → File > Upload notebook\n"
        "\n"
        "  2. Runtime > Change runtime type → T4 GPU\n"
        "\n"
        f"  3. Upload {data_path} when the notebook prompts\n"
        "\n"
        "  4. Run all cells (~15 min for 500 samples / 3 epochs)\n"
        "\n"
        "  5. Download the adapter zip and unzip to models/lora_adapter/\n"
        "\n"
        "  6. Then run: ass-ade train --serve\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    )


if __name__ == "__main__":
    main()
