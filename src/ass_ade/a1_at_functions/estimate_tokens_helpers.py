"""Tier a1 — assimilated function 'estimate_tokens'

Assimilated from: tokens.py:88-103
"""

from __future__ import annotations


# --- assimilated symbol ---
def estimate_tokens(text: str) -> int:
    """Estimate token count for a text string.

    Uses tiktoken cl100k_base when available (exact for GPT-4/Claude-class
    tokenizers within ~2%). Falls back to a calibrated heuristic:

        tokens ≈ ceil(len(text) / 3.7)

    The constant 3.7 is the empirical mean bytes-per-token across a corpus
    of mixed English prose + Python/TypeScript code measured against
    cl100k_base.  Error is bounded: |estimate - actual| / actual < 0.12
    for inputs > 100 chars.
    """
    if _tiktoken_enc is not None:
        return max(1, len(_tiktoken_enc.encode(text)))
    return max(1, math.ceil(len(text) / 3.7))

