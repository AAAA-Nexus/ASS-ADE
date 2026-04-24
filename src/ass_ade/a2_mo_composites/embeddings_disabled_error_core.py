"""Tier a2 — assimilated class 'EmbeddingsDisabledError'

Assimilated from: types.py:355-369
"""

from __future__ import annotations


# --- assimilated symbol ---
class EmbeddingsDisabledError(EngineError):
    """Embedding-based registry lookup was attempted without the flag.

    Raised by :meth:`Registry.search_by_embedding` and
    :meth:`Registry.retrieve_then_rerank` when the
    ``ATOMADIC_USE_EMBEDDINGS`` environment flag is not enabled. The
    feature is additive and default-off per Lane W's T-A+1 / T-A+2
    contract (signal
    ``20260421T045050Z-P1-reroute-wave-3-parallel-activation-enhancement-planner``);
    callers that do not opt-in never pay any embedding-model cost.
    Fail-closed matches the RULES.md "MAP = TERRAIN" posture: no
    silent fallback to a non-embedding search path, because a
    silent fallback would hide a real capability gap from the
    caller.
    """

