# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_trainconfig.py:7
# Component id: mo.source.a2_mo_composites.trainconfig
from __future__ import annotations

__version__ = "0.1.0"

class TrainConfig:
    language: str = "python"
    base_model: str = _BASE_MODEL_BY_PROFILE["fast"]
    epochs: int = 3
    lora_rank: int = 8
    lora_alpha: int = 16
    lora_dropout: float = 0.05
    learning_rate: float = 2e-4
    batch_size: int = 4
    max_samples: int = 1000
    max_length: int = 1024
    min_samples_to_train: int = 20  # don't waste cycles on fewer
    output_dir: Path = Path(".lora-train-output")
    upload_backend: str = "hf"  # "hf" (HuggingFace Hub) | "r2" | "local"
    hf_repo: str | None = None  # for upload_backend=hf
    r2_bucket_url: str | None = None  # for upload_backend=r2
    storefront_url: str = "https://atomadic.tech"
    owner_token: str | None = None  # AAAA_NEXUS_OWNER_TOKEN
