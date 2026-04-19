# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_print_colab_instructions.py:7
# Component id: at.source.a1_at_functions.print_colab_instructions
from __future__ import annotations

__version__ = "0.1.0"

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
