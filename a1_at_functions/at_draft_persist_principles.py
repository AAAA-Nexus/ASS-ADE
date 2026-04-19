# Extracted from C:/!ass-ade/src/ass_ade/agent/wisdom.py:212
# Component id: at.source.ass_ade.persist_principles
from __future__ import annotations

__version__ = "0.1.0"

def persist_principles(self, lora_flywheel: Any = None) -> int:
    """Persist distilled principles to context_memory and optionally LoRA flywheel.

    Returns the count of new principles contributed.
    """
    if not self._principles:
        return 0
    new_count = 0
    # Store in context_memory for cross-session recall
    try:
        from ass_ade.context_memory import store_vector_memory
        for p in self._principles:
            store_vector_memory(
                text=p,
                namespace="wisdom_principle",
                metadata={"type": "wisdom_principle", "conviction": self._conviction},
            )
        new_count = len(self._principles)
    except Exception as exc:
        _log.debug("WisdomEngine: context_memory persist failed: %s", exc)

    # Contribute to LoRA flywheel if conviction is high enough
    if lora_flywheel is not None and self._conviction >= 0.7 and new_count >= 3:
        try:
            for p in self._principles:
                lora_flywheel.capture_principle(p, confidence=self._conviction)
        except Exception as exc:
            _log.debug("WisdomEngine: LoRA flywheel capture failed: %s", exc)

    return new_count
    return list(self._principles)
