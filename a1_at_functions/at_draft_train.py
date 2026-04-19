# Extracted from C:/!ass-ade/scripts/lora_training/train_lora.py:59
# Component id: at.source.ass_ade.train
from __future__ import annotations

__version__ = "0.1.0"

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
