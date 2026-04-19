# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_train_adapter.py:7
# Component id: at.source.a1_at_functions.train_adapter
from __future__ import annotations

__version__ = "0.1.0"

def train_adapter(cfg: TrainConfig, samples: list[dict[str, Any]]) -> Path:
    """Run a LoRA fine-tune on `samples`. Returns the adapter directory path."""
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
            f"LoRA training deps missing ({exc}). Install with: "
            "pip install 'ass-ade[lora]' (pulls torch, transformers, peft, datasets, accelerate)"
        ) from exc

    _log.info("loading base model %s", cfg.base_model)
    tokenizer = AutoTokenizer.from_pretrained(cfg.base_model, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(
        cfg.base_model,
        torch_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
        device_map="auto" if torch.cuda.is_available() else None,
        trust_remote_code=True,
    )

    # Build the instruction-tuning dataset
    def _format(sample: dict[str, Any]) -> str:
        instruction = sample.get("instruction", "Fix the code.")
        bad = sample.get("input", "")
        good = sample.get("output", "")
        return (
            f"<|im_start|>user\n{instruction}\n\n```\n{bad}\n```<|im_end|>\n"
            f"<|im_start|>assistant\n```\n{good}\n```<|im_end|>"
        )

    texts = [_format(s) for s in samples]
    ds = Dataset.from_dict({"text": texts})

    def _tok(batch: dict[str, list[str]]) -> dict[str, Any]:
        out = tokenizer(
            batch["text"],
            truncation=True,
            max_length=cfg.max_length,
            padding=False,
        )
        out["labels"] = out["input_ids"].copy()
        return out

    ds = ds.map(_tok, batched=True, remove_columns=["text"])

    # Attach LoRA adapter
    lora_cfg = LoraConfig(
        r=cfg.lora_rank,
        lora_alpha=cfg.lora_alpha,
        lora_dropout=cfg.lora_dropout,
        bias="none",
        task_type=TaskType.CAUSAL_LM,
        target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
    )
    model = get_peft_model(model, lora_cfg)
    trainable, total = 0, 0
    for p in model.parameters():
        total += p.numel()
        if p.requires_grad:
            trainable += p.numel()
    _log.info(
        "LoRA parameters: trainable=%d total=%d (%.3f%%)",
        trainable,
        total,
        100 * trainable / max(total, 1),
    )

    cfg.output_dir.mkdir(parents=True, exist_ok=True)
    args = TrainingArguments(
        output_dir=str(cfg.output_dir / "checkpoints"),
        num_train_epochs=cfg.epochs,
        per_device_train_batch_size=cfg.batch_size,
        learning_rate=cfg.learning_rate,
        logging_steps=10,
        save_strategy="no",
        report_to=[],
        fp16=False,  # use bf16 when on CUDA
        bf16=bool(torch.cuda.is_available()),
        gradient_accumulation_steps=2,
        warmup_ratio=0.03,
        lr_scheduler_type="cosine",
        remove_unused_columns=False,
    )

    collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)
    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=ds,
        data_collator=collator,
    )
    trainer.train()

    # Save just the adapter (small, portable)
    adapter_dir = cfg.output_dir / f"adapter-{cfg.language}-{int(time.time())}"
    model.save_pretrained(str(adapter_dir))
    tokenizer.save_pretrained(str(adapter_dir))
    _log.info("adapter saved to %s", adapter_dir)
    return adapter_dir
