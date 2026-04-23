#!/usr/bin/env python3
"""Fine-tune a small causal LM with LoRA on ASS-ADE dev JSONL (from collect_ass_ade_dev_corpus).

Prerequisites:
  pip install -e ".[lora]"

Typical flow:
  python scripts/collect_ass_ade_dev_corpus.py --out training_data/ass_ade_dev.jsonl
  python scripts/train_lora_local.py --data training_data/ass_ade_dev.jsonl

Uses HuggingFace transformers + PEFT. GPU strongly recommended; CPU works for --max-steps smoke tests.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _load_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def _target_modules_for(model_name: str) -> list[str]:
    m = model_name.lower()
    if "distilgpt2" in m:
        return ["q_lin", "v_lin", "out_lin"]
    if "gpt2" in m:
        return ["c_attn", "c_fc"]
    # Llama / Mistral-style
    return ["q_proj", "v_proj", "k_proj", "o_proj"]


def main() -> int:
    ap = argparse.ArgumentParser(description="LoRA fine-tune on ASS-ADE dev JSONL corpus.")
    ap.add_argument(
        "--data",
        type=Path,
        default=None,
        help="JSONL from collect_ass_ade_dev_corpus (default: training_data/ass_ade_dev.jsonl).",
    )
    ap.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Adapter output directory (default: training_data/lora_adapter).",
    )
    ap.add_argument(
        "--base-model",
        default="distilgpt2",
        help="HF model id (default: distilgpt2, small; e.g. TinyLlama for better quality).",
    )
    ap.add_argument("--epochs", type=int, default=1)
    ap.add_argument("--batch-size", type=int, default=1)
    ap.add_argument("--grad-accum", type=int, default=8)
    ap.add_argument("--lr", type=float, default=2e-4)
    ap.add_argument("--lora-r", type=int, default=8)
    ap.add_argument("--lora-alpha", type=int, default=16)
    ap.add_argument("--max-length", type=int, default=512)
    ap.add_argument(
        "--max-steps",
        type=int,
        default=-1,
        help="If > 0, cap total optimizer steps (smoke tests).",
    )
    ap.add_argument("--max-samples", type=int, default=-1, help="If > 0, only use first N records.")
    args = ap.parse_args()

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
    except ImportError:
        print(
            "Missing dependencies. Install with:  pip install -e \".[lora]\"",
            file=sys.stderr,
        )
        return 2

    root = _repo_root()
    data_path = args.data or (root / "training_data" / "ass_ade_dev.jsonl")
    data_path = (data_path if data_path.is_absolute() else (Path.cwd() / data_path)).resolve()
    if not data_path.is_file():
        print(f"Corpus not found: {data_path}\nRun: python scripts/collect_ass_ade_dev_corpus.py", file=sys.stderr)
        return 1

    out_dir = args.output_dir or (root / "training_data" / "lora_adapter")
    out_dir = (out_dir if out_dir.is_absolute() else (Path.cwd() / out_dir)).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    raw = _load_jsonl(data_path)
    texts = [r.get("text") or "" for r in raw if r.get("text")]
    if args.max_samples > 0:
        texts = texts[: args.max_samples]
    if not texts:
        print("No 'text' fields in JSONL.", file=sys.stderr)
        return 1

    tokenizer = AutoTokenizer.from_pretrained(args.base_model, use_fast=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    def _tok(batch: dict) -> dict:
        return tokenizer(
            batch["text"],
            truncation=True,
            max_length=args.max_length,
            padding=False,
        )

    ds = Dataset.from_dict({"text": texts})
    ds = ds.map(_tok, batched=True, remove_columns=["text"])
    ds = ds.map(lambda x: {"labels": x["input_ids"]})

    dtype = torch.bfloat16 if torch.cuda.is_available() else torch.float32
    model = AutoModelForCausalLM.from_pretrained(
        args.base_model,
        torch_dtype=dtype,
        device_map="auto" if torch.cuda.is_available() else None,
        low_cpu_mem_usage=True,
    )
    if not torch.cuda.is_available():
        model = model.to(dtype)

    tmods = _target_modules_for(args.base_model)
    peft_cfg = LoraConfig(
        r=args.lora_r,
        lora_alpha=args.lora_alpha,
        lora_dropout=0.05,
        bias="none",
        task_type=TaskType.CAUSAL_LM,
        target_modules=tmods,
    )
    model = get_peft_model(model, peft_cfg)
    model.print_trainable_parameters()

    collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

    targs = TrainingArguments(
        output_dir=str(out_dir / "checkpoints"),
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.batch_size,
        gradient_accumulation_steps=args.grad_accum,
        learning_rate=args.lr,
        logging_steps=5,
        save_strategy="no",
        report_to=[],
        bf16=torch.cuda.is_available(),
        fp16=False,
        max_steps=args.max_steps if args.max_steps > 0 else -1,
    )

    trainer = Trainer(
        model=model,
        args=targs,
        train_dataset=ds,
        data_collator=collator,
    )
    trainer.train()

    adapter_dir = out_dir / f"adapter-{args.base_model.replace('/', '_')}"
    model.save_pretrained(str(adapter_dir))
    tokenizer.save_pretrained(str(adapter_dir))
    print(f"Saved LoRA adapter to {adapter_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
