# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_lora_train.py:5
# Component id: at.source.ass_ade.lora_train
__version__ = "0.1.0"

def lora_train(
    lang: str = typer.Option("python", help="Target language."),
    profile: str = typer.Option("fast", help="Model profile: fast | medium | large."),
    base_model: str = typer.Option("", help="Override base-model HF id (blank = use profile default)."),
    epochs: int = typer.Option(3, help="Training epochs."),
    lora_rank: int = typer.Option(8, help="LoRA adapter rank."),
    max_samples: int = typer.Option(1000, help="Max samples to pull."),
    min_samples: int = typer.Option(20, help="Skip training if pool < this."),
    upload: str = typer.Option("hf", help="Upload backend: hf | r2 | local."),
    hf_repo: str = typer.Option("", help="HuggingFace repo id (blank = don't upload to HF)."),
    output_dir: Path = typer.Option(Path(".lora-train-output"), help="Where to stash checkpoints + receipts."),
    config: Path | None = CONFIG_OPTION,
) -> None:
    """Fine-tune a shared LoRA adapter from the live sample pool and promote it.

    Prerequisites:
      - pip install 'ass-ade[lora]'
      - AAAA_NEXUS_OWNER_TOKEN env var (owner-only samples export)
      - HF_TOKEN env var if uploading to Hugging Face

    Runs: fetch_samples -> LoRA fine-tune -> upload -> promote on atomadic.tech.
    """
    import os as _os
    import subprocess as _sp

    _, settings = _resolve_config(config)

    env = {
        **_os.environ,
        "AAAA_NEXUS_BASE_URL": settings.nexus_base_url,
    }
    cmd = [
        sys.executable, "-m", "scripts.lora_train",
        "--lang", lang,
        "--profile", profile,
        "--epochs", str(epochs),
        "--lora-rank", str(lora_rank),
        "--max-samples", str(max_samples),
        "--min-samples", str(min_samples),
        "--upload", upload,
        "--output-dir", str(output_dir),
        "--storefront", settings.nexus_base_url,
    ]
    if base_model:
        cmd.extend(["--base-model", base_model])
    if hf_repo:
        cmd.extend(["--hf-repo", hf_repo])
    _ = config  # acknowledge param, used only to resolve settings above
    console.print(f"[dim]$ {' '.join(cmd)}[/dim]")
    # Stream stdout/stderr so the user sees training progress live.
    rc = _sp.call(cmd, env=env)
    raise typer.Exit(code=rc)
