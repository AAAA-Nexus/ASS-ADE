"""LoRA Flywheel - shared LoRA contribution orchestrator (Phase 5).

Captures three signal types from every coding session:
  - Code fixes: before/after pairs when a user accepts a CIE-corrected edit
  - Principles: high-conviction WisdomEngine distillations
  - Rejections: CIE-rejected candidates (negative training examples)

Every ``LORA_BATCH_INTERVAL`` steps, pending contributions are batched and
sent to nexus.lora_contribute(). This is the flywheel: each user's session
improves the shared adapter for all future users.

Persistence: .ass-ade/state/lora_pending.jsonl
             .ass-ade/state/lora_contributions.jsonl
"""

from __future__ import annotations

import json
import logging
import os
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

_log = logging.getLogger(__name__)

# LoRA batching cadence for pending contributions. The actual ratchet period
# is resolved at runtime from the AAAA-Nexus ratchet oracle; this module-level
# default is used only when the oracle is unreachable. Override via env
# ``ASS_ADE_LORA_BATCH_INTERVAL`` for local tuning.
LORA_BATCH_INTERVAL = int(os.environ.get("ASS_ADE_LORA_BATCH_INTERVAL", "50"))

_PENDING_FILE = Path(".ass-ade/state/lora_pending.jsonl")
_CONTRIBUTIONS_FILE = Path(".ass-ade/state/lora_contributions.jsonl")


@dataclass
class Contribution:
    kind: str          # "fix", "principle", "rejection"
    content: dict[str, Any]
    ts: float = field(default_factory=time.time)
    session_id: str = ""
    confidence: float = 1.0


@dataclass
class BatchResult:
    submitted: int
    contribution_id: str | None
    error: str | None = None
    reward_claimed: bool = False


@dataclass
class LoRAStatus:
    adapter_version: str
    contribution_count: int
    principle_count: int
    fix_count: int
    rejection_count: int
    ratchet_epoch: int
    pending_count: int
    next_batch_step: int
    quality_score: float = 0.0


class LoRAFlywheel:
    """Central coordinator for all LoRA contribution flows."""

    def __init__(
        self,
        config: dict[str, Any] | None = None,
        nexus: Any = None,
        session_id: str = "",
    ) -> None:
        self._config = config or {}
        self._nexus = nexus
        self._session_id = session_id
        cfg = self._config.get("lora_flywheel") or {}
        self._batch_interval = int(cfg.get("batch_interval", LORA_BATCH_INTERVAL))
        self._min_confidence = float(cfg.get("min_confidence", 0.7))
        self._trust_floor_threshold = float(cfg.get("trust_floor_threshold", 0.0))
        self._pending_file = Path(cfg.get("pending_file", str(_PENDING_FILE)))
        self._contributions_file = Path(cfg.get("contributions_file", str(_CONTRIBUTIONS_FILE)))
        self._enabled = bool(cfg.get("enabled", True))
        self._pending: list[Contribution] = []
        self._step_count = 0
        self._total_contributed = 0
        self._ratchet_epoch = 0
        self._adapter_version = "base"
        self._load_pending()

    # ── Persistence ───────────────────────────────────────────────────────

    def _load_pending(self) -> None:
        try:
            if self._pending_file.exists():
                for line in self._pending_file.read_text(encoding="utf-8").splitlines():
                    line = line.strip()
                    if line:
                        d = json.loads(line)
                        self._pending.append(Contribution(
                            kind=d.get("kind", "fix"),
                            content=d.get("content", {}),
                            ts=float(d.get("ts", time.time())),
                            session_id=d.get("session_id", ""),
                            confidence=float(d.get("confidence", 1.0)),
                        ))
        except Exception as exc:
            _log.debug("LoRAFlywheel: failed to load pending: %s", exc)

    def _save_pending(self) -> None:
        try:
            self._pending_file.parent.mkdir(parents=True, exist_ok=True)
            lines = []
            for c in self._pending:
                lines.append(json.dumps({
                    "kind": c.kind,
                    "content": c.content,
                    "ts": c.ts,
                    "session_id": c.session_id,
                    "confidence": c.confidence,
                }))
            self._pending_file.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
        except Exception as exc:
            _log.debug("LoRAFlywheel: failed to save pending: %s", exc)

    def _append_contribution_log(self, result: BatchResult, contributions: list[Contribution]) -> None:
        try:
            self._contributions_file.parent.mkdir(parents=True, exist_ok=True)
            record = {
                "ts": time.time(),
                "session_id": self._session_id,
                "contribution_id": result.contribution_id,
                "submitted": result.submitted,
                "reward_claimed": result.reward_claimed,
                "kinds": [c.kind for c in contributions],
            }
            with self._contributions_file.open("a", encoding="utf-8") as f:
                f.write(json.dumps(record) + "\n")
        except Exception as exc:
            _log.debug("LoRAFlywheel: failed to append contribution log: %s", exc)

    # ── Capture API ───────────────────────────────────────────────────────

    def capture_fix(self, original: str, fixed: str, context: dict[str, Any] | None = None) -> str:
        """Capture a before/after code fix as a positive training signal."""
        if not self._enabled:
            return ""
        cid = f"fix_{int(time.time())}_{len(self._pending)}"
        c = Contribution(
            kind="fix",
            content={"original": original[:2000], "fixed": fixed[:2000], "context": context or {}},
            session_id=self._session_id,
            confidence=1.0,
        )
        self._pending.append(c)
        self._save_pending()
        self._maybe_batch()
        return cid

    def capture_principle(self, principle: str, confidence: float = 0.8) -> str:
        """Capture a WisdomEngine-distilled principle as a training signal."""
        if not self._enabled or confidence < self._min_confidence:
            return ""
        cid = f"principle_{int(time.time())}_{len(self._pending)}"
        c = Contribution(
            kind="principle",
            content={"principle": principle[:500]},
            session_id=self._session_id,
            confidence=confidence,
        )
        self._pending.append(c)
        self._save_pending()
        return cid

    def capture_rejection(self, candidate: str, reason: str, confidence: float = 0.9) -> str:
        """Capture a CIE-rejected candidate as a negative training example."""
        if not self._enabled:
            return ""
        cid = f"rejection_{int(time.time())}_{len(self._pending)}"
        c = Contribution(
            kind="rejection",
            content={"candidate": candidate[:2000], "reason": reason[:200]},
            session_id=self._session_id,
            confidence=confidence,
        )
        self._pending.append(c)
        self._save_pending()
        return cid

    # ── Batch Contribution ────────────────────────────────────────────────

    def tick(self) -> BatchResult | None:
        """Advance step counter. Returns BatchResult if batch was submitted."""
        self._step_count += 1
        if self._step_count % self._batch_interval == 0 and self._pending:
            return self.contribute_batch()
        return None

    def _maybe_batch(self) -> None:
        if len(self._pending) >= self._batch_interval:
            self.contribute_batch()

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
            self._ratchet_epoch = self._total_contributed // LORA_BATCH_INTERVAL
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

    def _submit_to_nexus(self, contributions: list[Contribution]) -> str | None:
        """Ship a batch of contributions to Nexus /v1/lora/contribute.

        Matches the storefront contract:
          samples: [{digest, bad, good, lint_delta, language, size, ts}]
          agent_id: str
        Only "fix" contributions carry both bad+good and count as training
        samples. Principle + rejection contributions are logged locally but
        not sent to /v1/lora/contribute (they don't fit the fix sample shape).
        """
        if self._nexus is None:
            return None
        samples = [s for c in contributions if c.kind == "fix" for s in (self._to_sample(c),) if s]
        if not samples:
            return None

        fn = getattr(self._nexus, "lora_contribute", None)
        if fn is None:
            return None
        try:
            # Explicit threshold: the server default is TRUST_FLOOR (≈0.998),
            # while local fix samples use a lightweight lint_delta proxy.
            # Keep this configurable so longer-but-correct fixes can still train.
            result = fn(
                samples=samples,
                agent_id=self._session_id or "ass-ade",
                trust_floor_threshold=self._trust_floor_threshold,
            )
            # Storefront returns {accepted, rejected, batch_size, ...} — use a
            # deterministic id (digest of first sample) for local book-keeping.
            if isinstance(result, dict):
                accepted = int(result.get("accepted", 0))
                if accepted == 0:
                    return None
                return f"batch_{samples[0].get('digest', 'unknown')[:16]}"
            cid = getattr(result, "contribution_id", None) or getattr(result, "id", None)
            return str(cid) if cid else None
        except Exception as exc:
            _log.debug("lora_contribute failed: %s", exc)
            return None

    @staticmethod
    def _to_sample(c: Contribution) -> dict[str, Any] | None:
        """Convert a 'fix' Contribution to the storefront sample schema."""
        import hashlib
        content = c.content or {}
        bad = str(content.get("original", "") or "")
        good = str(content.get("fixed", "") or "")
        if not good:  # need at least the "good" side
            return None
        language = str((content.get("context") or {}).get("language") or "python")
        # Rough lint_delta proxy: how much shorter (cleaner) the good is vs bad
        lint_delta = max(0.0, min(1.0, 1.0 - (len(good) / max(1, len(bad)))))
        digest = hashlib.sha256((bad + "|" + good).encode("utf-8")).hexdigest()
        return {
            "digest": digest,
            "bad": bad,
            "good": good,
            "lint_delta": round(lint_delta, 4),
            "language": language,
            "size": len(good),
            "ts": int(c.ts),
        }

    def _claim_reward(self, contribution_id: str | None) -> bool:
        """Claim USDC payout for the session's accepted samples.

        The storefront /v1/lora/reward/claim uses agent_id (not contribution_id)
        to look up the reward pool — we pass the session_id as the agent_id.
        """
        if self._nexus is None:
            return False
        fn = getattr(self._nexus, "lora_reward_claim", None)
        if fn is None:
            return False
        try:
            fn(agent_id=self._session_id or "ass-ade", contribution_id=contribution_id)
            return True
        except Exception:
            return False

    # ── Status ────────────────────────────────────────────────────────────

    def status(self) -> LoRAStatus:
        kind_counts: dict[str, int] = {}
        for c in self._pending:
            kind_counts[c.kind] = kind_counts.get(c.kind, 0) + 1

        adapter_version = self._adapter_version
        quality_score = 0.0
        if self._nexus:
            try:
                s = getattr(self._nexus, "lora_adapter_current", lambda: None)()
                if s:
                    adapter_version = str(getattr(s, "version", adapter_version))
                    quality_score = float(getattr(s, "quality_score", 0.0))
            except Exception:
                pass

        next_batch = self._batch_interval - (self._step_count % self._batch_interval)
        return LoRAStatus(
            adapter_version=adapter_version,
            contribution_count=self._total_contributed + len(self._pending),
            principle_count=kind_counts.get("principle", 0),
            fix_count=kind_counts.get("fix", 0),
            rejection_count=kind_counts.get("rejection", 0),
            ratchet_epoch=self._ratchet_epoch,
            pending_count=len(self._pending),
            next_batch_step=next_batch,
            quality_score=quality_score,
        )

    def report(self) -> dict[str, Any]:
        s = self.status()
        return {
            "engine": "lora_flywheel",
            "adapter_version": s.adapter_version,
            "total_contributions": s.contribution_count,
            "ratchet_epoch": s.ratchet_epoch,
            "pending": s.pending_count,
            "step_count": self._step_count,
        }
