"""ASS-ADE LoRA training on a Hugging Face Space with ZeroGPU.

HF Spaces with the ZeroGPU hardware flag get free, time-sliced A100s on demand.
Perfect for on-demand LoRA fine-tunes triggered via a Gradio button or an
external webhook / scheduled job.

## Setup

1. Create a new Space at https://huggingface.co/new-space
   - Hardware: **ZeroGPU** (free; requires HF Pro for "best" tier, but the free
     tier gets 5 min A100 slots which is enough for a LoRA fine-tune)
2. Copy this `app.py` into the Space
3. Add these Secrets (in Space Settings → Variables and secrets):
   - `AAAA_NEXUS_OWNER_TOKEN`
   - `HF_TOKEN`
4. Push. The Space exposes a Gradio UI for manual triggers plus a POST
   endpoint at `/train` you can call from a cron externally.

## Why ZeroGPU

- Free tier: ~300 sec per request of A100 access, queued fairly
- No spin-up cost — the Space is dormant until called
- Runs Qwen2.5-Coder-7B + LoRA rank 16 in under the free time budget

Files:
- app.py            — this file
- requirements.txt  — deps (next to this file)
- README.md         — with `hardware: zero-gpu` front-matter
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import gradio as gr
import spaces

# ZeroGPU: the @spaces.GPU decorator hands us a time-sliced A100.
# `duration=280` means request ≤ 280 seconds of GPU per call (free-tier friendly).


@spaces.GPU(duration=280)
def run_training(language: str, profile: str, epochs: int, max_samples: int, hf_repo: str) -> str:
    env = {
        **os.environ,
        "AAAA_NEXUS_BASE_URL": "https://atomadic.tech",
    }
    cmd = [
        sys.executable,
        "-m",
        "scripts.lora_train",
        "--lang",
        language,
        "--profile",
        profile,
        "--epochs",
        str(epochs),
        "--max-samples",
        str(max_samples),
        "--min-samples",
        "20",
        "--upload",
        "hf",
        "--hf-repo",
        hf_repo,
        "--storefront",
        "https://atomadic.tech",
    ]
    log: list[str] = [f"$ {' '.join(cmd)}"]
    try:
        proc = subprocess.run(
            cmd,
            env=env,
            capture_output=True,
            text=True,
            timeout=270,
        )
        log.append(proc.stdout[-4000:] if proc.stdout else "")
        if proc.returncode != 0:
            log.append(f"\n[stderr]\n{proc.stderr[-2000:]}")
        log.append(f"\nexit code: {proc.returncode}")
    except subprocess.TimeoutExpired:
        log.append("\n⚠ hit ZeroGPU time limit; try `fast` profile or fewer samples")
    return "\n".join(log)


with gr.Blocks(title="ASS-ADE LoRA Training (ZeroGPU)") as demo:
    gr.Markdown("# ASS-ADE LoRA Training\n\n"
                "Fine-tune a shared LoRA adapter from the live sample pool on atomadic.tech, "
                "upload to HuggingFace Hub, and promote on the storefront.\n\n"
                "**Free via HF Spaces ZeroGPU** — queued A100 access, no cost.")
    with gr.Row():
        lang = gr.Dropdown(
            choices=["python", "rust", "typescript", "javascript", "go", "java", "c", "cpp"],
            value="python",
            label="Language",
        )
        profile = gr.Dropdown(
            choices=["fast", "medium", "large"],
            value="fast",
            label="Model profile (fast=1.5B, medium=7B, large=32B)",
        )
    with gr.Row():
        epochs = gr.Number(value=3, precision=0, label="Epochs")
        max_samples = gr.Number(value=500, precision=0, label="Max samples")
    hf_repo = gr.Textbox(
        value="atomadic/lora-python",
        label="HF repo id (where adapter is pushed)",
    )
    btn = gr.Button("▶ Run training", variant="primary")
    out = gr.Textbox(label="Log", lines=25, max_lines=40)
    btn.click(
        run_training,
        inputs=[lang, profile, epochs, max_samples, hf_repo],
        outputs=out,
    )

if __name__ == "__main__":
    demo.launch()
