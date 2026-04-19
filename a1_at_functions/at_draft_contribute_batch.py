# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_contribute_batch.py:7
# Component id: at.source.a1_at_functions.contribute_batch
from __future__ import annotations

__version__ = "0.1.0"

def contribute_batch(self) -> BatchResult:
    """Batch all pending contributions → nexus.lora_contribute()."""
    if not self._pending:
        return BatchResult(submitted=0, contribution_id=None)
    to_submit = list(self._pending)
    try:
        contribution_id = self._submit_to_nexus(to_submit)
        # When nexus is present but returns None → treat as a submission failure
        if self._nexus is not None and contribution_id is None:
            raise RuntimeError("nexus lora_contribute returned no contribution_id")
        self._total_contributed += len(to_submit)
        self._ratchet_epoch = self._total_contributed // RG_LOOP
        reward = self._claim_reward(contribution_id)
        result = BatchResult(
            submitted=len(to_submit),
            contribution_id=contribution_id,
            reward_claimed=reward,
        )
        self._append_contribution_log(result, to_submit)
        self._pending.clear()
        self._save_pending()
        _log.info("LoRAFlywheel: submitted %d contributions (epoch %d)", len(to_submit), self._ratchet_epoch)
        return result
    except Exception as exc:
        _log.warning("LoRAFlywheel: batch submit failed (will retry): %s", exc)
        return BatchResult(submitted=0, contribution_id=None, error=str(exc))
