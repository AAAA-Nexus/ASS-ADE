# Extracted from C:/!ass-ade/src/ass_ade/nexus/validation.py:95
# Component id: at.source.ass_ade.validate_prompt
from __future__ import annotations

__version__ = "0.1.0"

def validate_prompt(value: str) -> str:
    """Non-empty, max 32 KB, strip control characters."""
    if not value or not value.strip():
        raise ValueError("Prompt must not be empty.")
    # Strip control chars except newline and tab
    cleaned = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", value)
    if len(cleaned.encode("utf-8")) > MAX_PROMPT_BYTES:
        raise ValueError(f"Prompt exceeds {MAX_PROMPT_BYTES:,} bytes.")
    return cleaned
