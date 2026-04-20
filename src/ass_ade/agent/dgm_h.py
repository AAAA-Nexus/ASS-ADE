"""v18 pillar 72 — DGM-H meta-editable evolution loop.

Real simulation: runs the golden task set twice (before and after the patch),
derives a weighted quality metric, and validates if the improvement exceeds
the configured threshold AND exceeds the measured noise floor (2σ).

The simulation does NOT apply the patch to live source. Instead patch
metadata influences the "after" run via a prompt suffix — if the diff or
kind hints at a new tool/prompt, the surrogate response is modified
accordingly. Opaque patches fall back to a pure noise-vs-threshold test.
"""
from __future__ import annotations

import hashlib
import json
import math
import random
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


_SIM_STATE_DIR = Path(".ass-ade/state/dgm_h_sims")
_GOLDEN_DEFAULT = Path(".ass-ade/golden/tasks.jsonl")
_BASELINE_SCORE = 0.9


@dataclass
class Patch:
    id: str
    target: str
    diff: str
    kind: str = "code"


@dataclass
class MetaEdit:
    id: str
    procedure: str
    description: str


_VALIDATION_THRESHOLD = 0.05


@dataclass
class SimulationResult:
    """Real DGM-H simulation result with per-cycle telemetry."""

    patch_id: str
    cycles: int
    improvement: float
    weighted_before: float
    weighted_after: float
    noise_sigma: float
    constitutional_violation: bool
    per_cycle_metrics: list[dict[str, Any]] = field(default_factory=list)
    violations: list[str] = field(default_factory=list)
    artifact_path: str | None = None
    threshold: float = _VALIDATION_THRESHOLD

    # ── Back-compat aliases for existing gates code ──────────────────────────
    @property
    def delta(self) -> float:
        return self.improvement

    @property
    def validated(self) -> bool:
        # Require: no violations, improvement >= threshold AND > 2σ of noise.
        return (
            not self.constitutional_violation
            and not self.violations
            and self.improvement >= self.threshold
            and self.improvement > (2.0 * self.noise_sigma)
        )


# Back-compat alias — older code imports SimResult.
SimResult = SimulationResult


def _coerce_patch(patch: Any) -> Patch:
    if isinstance(patch, Patch):
        return patch
    if isinstance(patch, dict):
        pid = str(patch.get("id") or hashlib.sha256(
            json.dumps(patch, sort_keys=True, default=str).encode("utf-8")
        ).hexdigest()[:12])
        return Patch(
            id=pid,
            target=str(patch.get("target", "")),
            diff=str(patch.get("diff", "")),
            kind=str(patch.get("kind", "code")),
        )
    return Patch(
        id=str(getattr(patch, "id", "p0")),
        target=str(getattr(patch, "target", "")),
        diff=str(getattr(patch, "diff", patch)),
        kind=str(getattr(patch, "kind", "code")),
    )


def _patch_prompt_suffix(patch: Patch) -> str:
    """Derive a prompt-level influence string from patch metadata.

    If the diff/kind contains hints about a new tool or prompt template
    they bleed into the surrogate response and change the audit_pass rate.
    Opaque patches produce an empty suffix so the before/after runs
    differ only by noise.
    """
    parts: list[str] = []
    diff = (patch.diff or "").lower()
    kind = (patch.kind or "").lower()
    for token in ("tool:", "prompt:", "system:", "capability:"):
        if token in diff:
            # Extract a short hint after the token.
            idx = diff.index(token)
            tail = diff[idx:idx + 80]
            parts.append(tail)
    if kind and kind not in ("noop", "code"):
        parts.append(f"kind={kind}")
    return " | ".join(parts)


class DGMH:
    def __init__(self, config: dict, nexus: Any | None = None):
        self._config = config
        self._nexus = nexus
        cfg = config.get("dgm_h") or {}
        self._sim_cycles = int(cfg.get("simulation_cycles", 100))
        self._threshold = float(cfg.get("improvement_threshold", 0.05))
        self._meta_enabled = bool(cfg.get("meta_edit_enabled", True))
        self._golden_path = Path(
            cfg.get("golden_task_path", str(_GOLDEN_DEFAULT))
        )
        self._state_dir = Path(
            cfg.get("sim_artifact_dir", str(_SIM_STATE_DIR))
        )
        self._proposals = 0

    # ── Patch / MetaEdit proposal ────────────────────────────────────────────
    def propose_patch(self) -> Patch:
        self._proposals += 1
        pid = hashlib.sha256(f"patch:{self._proposals}".encode()).hexdigest()[:12]
        return Patch(id=pid, target="src/ass_ade/agent/loop.py", diff="# synthesized improvement")

    def propose_meta_edit(self) -> MetaEdit:
        mid = hashlib.sha256(f"meta:{self._proposals}".encode()).hexdigest()[:12]
        return MetaEdit(id=mid, procedure="propose_patch", description="tighten search heuristic")

    # ── Sovereign invariant checks ───────────────────────────────────────────
    def _check_violations(self, patch: Patch) -> list[str]:
        violations: list[str] = []
        low = (patch.diff or "").lower()
        for needle in (
            "eval(", "exec(", "__import__", "pickle.load", "pickle.loads",
            "shell=true", "os.system(", "subprocess.popen", "compile(",
            "yaml.load(", "marshal.load",
        ):
            if needle in low:
                violations.append(f"forbidden:{needle}")
        return violations

    # ── Nexus signal helpers (all graceful) ──────────────────────────────────
    def _halluc_score(self, text: str) -> float:
        if self._nexus is None:
            return 0.0
        fn = getattr(self._nexus, "check_hallucination", None) or getattr(
            self._nexus, "hallucination_oracle", None
        )
        if fn is None:
            return 0.0
        try:
            result = fn(text)
            # Accept dicts or pydantic objects.
            val = None
            if isinstance(result, dict):
                val = result.get("policy_epsilon") or result.get("score")
            else:
                val = getattr(result, "policy_epsilon", None) or getattr(result, "score", None)
            return float(val) if val is not None else 0.0
        except Exception:
            return 0.0

    def _trust_signal(self, agent_id: str = "ass_ade.dgm_h") -> float:
        if self._nexus is None:
            return _BASELINE_SCORE
        fn = getattr(self._nexus, "trust_score", None)
        if fn is None:
            return _BASELINE_SCORE
        try:
            result = fn(agent_id)
            if isinstance(result, dict):
                return float(result.get("score", _BASELINE_SCORE))
            return float(getattr(result, "score", _BASELINE_SCORE))
        except Exception:
            return _BASELINE_SCORE

    # ── Weighted metric assembly ─────────────────────────────────────────────
    def _weighted(self, audit_pass_rate: float, avg_tokens: float,
                  avg_halluc: float, avg_trust: float) -> float:
        return (
            0.4 * audit_pass_rate
            - 0.2 * math.log1p(avg_tokens / 1000.0)
            - 0.2 * avg_halluc
            + 0.2 * avg_trust
        )

    def _run_one(self, patch: Patch, suffix: str, seed: int, cycles: int) -> dict[str, Any]:
        """Run golden task set once with given patch suffix; returns aggregate telemetry."""
        from ass_ade.agent.golden_runner import run_golden

        # Derive tasks_limit / repeats so total == cycles; default layout 10×10.
        tasks_limit = 10
        repeats = max(1, cycles // tasks_limit)
        result = run_golden(
            self._golden_path,
            tasks_limit=tasks_limit,
            repeats=repeats,
            prompt_suffix=suffix,
            seed=seed,
        )
        agg = result.get("aggregate", {})
        pass_rate = float(agg.get("pass_rate", 0.0))
        avg_tokens = float(agg.get("avg_tokens", 0.0))
        noise_sigma = float(agg.get("noise_sigma", 0.05))

        # Sample nexus signals on synthetic response blobs (cheap).
        sample_text = f"dgm_h sim {patch.id} suffix={suffix[:40]}"
        avg_halluc = self._halluc_score(sample_text)
        avg_trust = self._trust_signal()

        weighted = self._weighted(pass_rate, avg_tokens, avg_halluc, avg_trust)
        return {
            "pass_rate": pass_rate,
            "avg_tokens": avg_tokens,
            "avg_halluc": avg_halluc,
            "avg_trust": avg_trust,
            "weighted": weighted,
            "noise_sigma": noise_sigma,
            "per_task": result.get("per_task", []),
        }

    def simulate(self, patch: Any, cycles: int | None = None) -> SimulationResult:
        """Real DGM-H simulation. Accepts Patch or dict (spec-compliant)."""
        p = _coerce_patch(patch)
        n = cycles if cycles is not None else self._sim_cycles

        # Sovereign invariant check first; early halt on violation.
        violations = self._check_violations(p)
        constitutional = bool(violations)

        # Deterministic seeds so the same patch id reproduces.
        seed_before = int(hashlib.sha256((p.id + "|before").encode()).hexdigest()[:8], 16)
        seed_after = int(hashlib.sha256((p.id + "|after").encode()).hexdigest()[:8], 16)

        before = self._run_one(p, suffix="", seed=seed_before, cycles=n)
        suffix = _patch_prompt_suffix(p)
        after = self._run_one(p, suffix=suffix, seed=seed_after, cycles=n)

        weighted_before = before["weighted"]
        weighted_after = after["weighted"]
        denom = abs(weighted_before) if abs(weighted_before) > 1e-9 else 1e-9
        improvement = (weighted_after - weighted_before) / denom

        noise_sigma = max(before["noise_sigma"], after["noise_sigma"], 1e-6)
        # Require improvement to exceed both threshold and 2σ of noise.
        meaningful = improvement >= self._threshold and improvement > (2.0 * noise_sigma)
        if not meaningful and not suffix:
            # Opaque patch: no prompt-level change → treat as no improvement.
            improvement = min(improvement, 0.0)

        per_cycle_metrics: list[dict[str, Any]] = [
            {"phase": "before", **{k: v for k, v in before.items() if k != "per_task"}},
            {"phase": "after", **{k: v for k, v in after.items() if k != "per_task"}},
        ]

        result = SimulationResult(
            patch_id=p.id,
            cycles=n,
            improvement=improvement,
            weighted_before=weighted_before,
            weighted_after=weighted_after,
            noise_sigma=noise_sigma,
            constitutional_violation=constitutional,
            per_cycle_metrics=per_cycle_metrics,
            violations=violations,
            threshold=self._threshold,
        )

        # Persist artifact.
        try:
            self._state_dir.mkdir(parents=True, exist_ok=True)
            ts = datetime.now(UTC).strftime("%Y%m%dT%H%M%S%f")
            artifact = self._state_dir / f"{ts}_{p.id}.json"
            artifact.write_text(
                json.dumps(asdict(result), indent=2, default=str),
                encoding="utf-8",
            )
            result.artifact_path = str(artifact)
        except OSError:
            # Never fail the sim due to disk issues.
            pass
        return result

    # ── Orchestration ────────────────────────────────────────────────────────
    def run(self, ctx: dict) -> dict:
        patch = self.propose_patch()
        sim = self.simulate(patch)
        return {
            "patch_id": patch.id,
            "delta": sim.improvement,
            "improvement": sim.improvement,
            "validated": sim.validated,
            "violations": sim.violations,
            "constitutional_violation": sim.constitutional_violation,
        }

    def report(self) -> dict:
        return {
            "engine": "dgm_h",
            "proposals": self._proposals,
            "sim_cycles": self._sim_cycles,
            "threshold": self._threshold,
            "meta_edit_enabled": self._meta_enabled,
            "golden_path": str(self._golden_path),
        }
