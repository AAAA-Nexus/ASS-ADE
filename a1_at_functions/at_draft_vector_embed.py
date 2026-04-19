# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_vector_embed.py:7
# Component id: at.source.a1_at_functions.vector_embed
from __future__ import annotations

__version__ = "0.1.0"

def vector_embed(text: str, dimensions: int = VECTOR_DIMENSIONS) -> list[float]:
    """Embed text into a deterministic signed hashing vector."""
    if dimensions <= 0:
        raise ValueError("dimensions must be positive")

    vector = [0.0] * dimensions
    for token in _tokens(text):
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        index = int.from_bytes(digest[:4], "big") % dimensions
        sign = 1.0 if digest[4] % 2 == 0 else -1.0
        weight = 1.0 + (len(token) % 7) / 10.0
        vector[index] += sign * weight

    norm = math.sqrt(sum(value * value for value in vector))
    if norm == 0:
        return vector
    return [value / norm for value in vector]
