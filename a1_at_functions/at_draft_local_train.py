# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_local_train.py:7
# Component id: at.source.a1_at_functions.local_train
from __future__ import annotations

__version__ = "0.1.0"

def local_train(
    collect: bool = typer.Option(False, "--collect", help="Collect training data from the current project."),
    run: bool = typer.Option(False, "--run", help="Run LoRA fine-tuning (GPU) or print Colab instructions."),
    serve: bool = typer.Option(False, "--serve", help="Start the local adapter server at localhost:8081."),
    root: Path = typer.Option(Path("."), "--root", help="Project root to scan when collecting (default: cwd)."),
    data_path: Path = typer.Option(
        Path("training_data/training_data.jsonl"),
        "--data",
        help="Training data JSONL path.",
    ),
    output_dir: Path = typer.Option(
        Path("models/lora_adapter"),
        "--output-dir",
        help="Adapter output directory.",
    ),
    base_model: str = typer.Option(
        "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        "--base-model",
        help="Base model HF id.",
    ),
    epochs: int = typer.Option(3, "--epochs", help="Training epochs."),
    lora_rank: int = typer.Option(8, "--lora-rank", help="LoRA rank (default: 8)."),
    port: int = typer.Option(8081, "--port", help="HTTP port for serve mode."),
    preload: bool = typer.Option(False, "--preload", help="Pre-load model on server startup."),
) -> None:
    """Local LoRA training pipeline — bootstrapped from ASS-ADE's own development data.

    Free-tier, self-contained: no Nexus token required.

    Workflow:
      ass-ade train --collect        # scan project and write training_data/training_data.jsonl
      ass-ade train --run            # fine-tune locally (GPU) or print Colab instructions
      ass-ade train --serve          # start adapter server at localhost:8081/generate

    See scripts/lora_training/ for standalone scripts and the Colab notebook.
    See docs/TRAINING_GUIDE.md for the full guide.
    """
    import subprocess as _sp

    if not collect and not run and not serve:
        console.print(
            "[yellow]Specify at least one flag:[/yellow]\n"
            "  [cyan]ass-ade train --collect[/cyan]   collect training data\n"
            "  [cyan]ass-ade train --run[/cyan]        run fine-tuning (or Colab instructions)\n"
            "  [cyan]ass-ade train --serve[/cyan]      start local adapter server"
        )
        raise typer.Exit(code=1)

    collect_script = Path(__file__).parent.parent.parent / "scripts" / "lora_training" / "collect_training_data.py"
    train_script = Path(__file__).parent.parent.parent / "scripts" / "lora_training" / "train_lora.py"
    serve_script = Path(__file__).parent.parent.parent / "scripts" / "lora_training" / "serve_lora.py"

    if collect:
        console.print("[bold]Collecting training data…[/bold]")
        rc = _sp.call([
            sys.executable, str(collect_script),
            "--root", str(root.resolve()),
            "--out", str(data_path),
        ])
        if rc != 0:
            raise typer.Exit(code=rc)
        console.print(f"[green]Done.[/green] Training data saved to [bold]{data_path}[/bold]")

    if run:
        import torch as _torch
        has_gpu = _torch.cuda.is_available()
        if not has_gpu:
            _sp.call([sys.executable, "-c",
                "from scripts.lora_training.train_lora import print_colab_instructions; "
                "from pathlib import Path; "
                f"print_colab_instructions(Path('{data_path}'))"])
        else:
            console.print("[bold]Starting LoRA fine-tuning…[/bold]")
            rc = _sp.call([
                sys.executable, str(train_script),
                "--data", str(data_path),
                "--output-dir", str(output_dir),
                "--base", base_model,
                "--epochs", str(epochs),
                "--lora-rank", str(lora_rank),
            ])
            if rc != 0:
                raise typer.Exit(code=rc)
            console.print(f"[green]Adapter saved to {output_dir}[/green]")

    if serve:
        console.print(f"[bold]Starting adapter server at http://127.0.0.1:{port}/generate…[/bold]")
        rc = _sp.call([
            sys.executable, str(serve_script),
            "--adapter-dir", str(output_dir),
            "--base", base_model,
            "--port", str(port),
            *(["--preload"] if preload else []),
        ])
        raise typer.Exit(code=rc)
        console.print("[dim]Demo files cleaned up.[/dim]")
