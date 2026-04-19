# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_run_training.py:7
# Component id: at.source.a1_at_functions.run_training
from __future__ import annotations

__version__ = "0.1.0"

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
