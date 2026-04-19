# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/agent/wisdom.py:38
# Component id: mo.source.ass_ade.wisdomengine
__version__ = "0.1.0"

class WisdomEngine:
    def __init__(self, config: dict, nexus: Any | None = None):
        self._config = config
        self._nexus = nexus
        sde = config.get("sde") or {}
        self._conviction_required = float(sde.get("conviction_required", 0.85))
        self._conviction = 0.5
        self._audits = 0
        self._principles: list[str] = []

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------
    @property
    def conviction(self) -> float:
        return self._conviction

    @property
    def is_confident(self) -> bool:
        return self._conviction >= self._conviction_required

    # ------------------------------------------------------------------
    # Audit logic
    # ------------------------------------------------------------------
    def _answer(self, question: dict, cycle_state: dict) -> bool:
        # Explicit per-question override always wins.
        key = f"q{question['id']}"
        if key in cycle_state:
            return bool(cycle_state[key])

        group = question["group"]
        signals = _GROUP_SIGNALS.get(group, ())
        for sig in signals:
            if sig not in cycle_state:
                continue
            val = cycle_state[sig]
            # Numeric signals (like conviction) pass on > 0.
            if isinstance(val, (int, float)) and not isinstance(val, bool):
                if val > 0:
                    return True
            # Collections pass if non-empty.
            elif isinstance(val, (list, tuple, set, dict)):
                if len(val) > 0:
                    return True
            # Everything else falls back to truthiness.
            elif val:
                return True

        # Default to False when no signal present (audit-report fix).
        return False

    def run_audit(self, cycle_state: dict) -> AuditReport:
        self._audits += 1
        passed = 0
        failed = 0
        per_group: dict[str, dict] = {}
        failures: list[dict] = []
        warnings: list[str] = []

        for q in AUDIT_QUESTIONS:
            ok = self._answer(q, cycle_state)
            g = per_group.setdefault(q["group"], {"passed": 0, "failed": 0})
            if ok:
                passed += 1
                g["passed"] += 1
            else:
                failed += 1
                g["failed"] += 1
                failures.append({"id": q["id"], "group": q["group"], "text": q["text"]})

        total = passed + failed
        score = passed / total if total else 0.0
        # Update conviction EMA.
        self._conviction = 0.5 * self._conviction + 0.5 * score

        # Low-conviction warning after the first audit.
        if score < 0.3 and self._audits > 1:
            warnings.append("low_conviction")

        return AuditReport(
            total=total,
            passed=passed,
            failed=failed,
            score=score,
            conviction=self._conviction,
            per_group=per_group,
            failures=failures,
            warnings=warnings,
            principles=list(self._principles),
        )

    # ------------------------------------------------------------------
    # Principles
    # ------------------------------------------------------------------
    def distill_principles(self, report: AuditReport | None = None) -> list[str]:
        default_principles = [
            "verify before acting",
            "prefer reuse over regeneration",
            "halt on capability gap",
        ]

        if report is None or not report.failures:
            self._principles = list(default_principles)
            return list(self._principles)

        # Count failures per group.
        group_counts: dict[str, int] = {}
        for f in report.failures:
            g = f.get("group", "unknown")
            group_counts[g] = group_counts.get(g, 0) + 1

        group_to_principle = {
            "foundational": "Always classify epistemic tier before acting",
            "operational": "Minimize tool round-trips and track token budget",
            "autonomous": "Consult persistent memory and capture traces for every cycle",
            "meta_cognition": "Certify output and check hallucination signals before delivery",
            "hyperagent": "Invoke MAP=TERRAIN, ATLAS, and LIFR engines for complex tasks",
        }

        # Threshold: a group contributes a principle when it has >= 2 failures
        # (or any failures if there are few overall).
        threshold = 2 if len(report.failures) > 5 else 1
        derived: list[str] = []
        for group, count in sorted(group_counts.items(), key=lambda kv: -kv[1]):
            if count >= threshold and group in group_to_principle:
                derived.append(group_to_principle[group])

        if not derived:
            derived = list(default_principles)

        # Cap at 5 principles total.
        merged: list[str] = []
        for p in derived + default_principles:
            if p not in merged:
                merged.append(p)
            if len(merged) >= 5:
                break

        self._principles = merged
        return list(self._principles)

    def update_principles(self, principles: list[str]) -> list[str]:
        for p in principles:
            if p not in self._principles:
                self._principles.append(p)

    def hydrate_from_memory(self, *, top_k: int = 10, working_dir: str | Any = ".") -> int:
        """Pre-load principles from prior sessions' persisted vector memory.

        Called at orchestrator init so wisdom carries across sessions. Returns
        the number of principles loaded.
        """
        try:
            from ass_ade.context_memory import query_vector_memory

            result = query_vector_memory(
                query="wisdom principle",
                namespace="wisdom_principle",
                top_k=top_k,
                working_dir=working_dir,
            )
            matches = getattr(result, "matches", None) or []
            loaded: list[str] = []
            for m in matches:
                text = getattr(m, "text", None) or (m.get("text") if isinstance(m, dict) else None)
                if text and text not in loaded and text not in self._principles:
                    loaded.append(text)
            if loaded:
                self._principles = (self._principles + loaded)[:20]  # cap at 20
            return len(loaded)
        except Exception as exc:
            _log.debug("WisdomEngine.hydrate_from_memory failed (fail-open): %s", exc)
            return 0

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

    # ------------------------------------------------------------------
    # Gating
    # ------------------------------------------------------------------
    def gate_action(self, action: str, cycle_state: dict) -> tuple[bool, str]:
        self.run_audit(cycle_state)
        if self.is_confident:
            return (True, "conviction_met")
        return (
            False,
            f"conviction {self._conviction:.2f} below required {self._conviction_required:.2f}",
        )

    # ------------------------------------------------------------------
    # Legacy helpers
    # ------------------------------------------------------------------
    def update_conviction(self) -> float:
        return self._conviction

    def run(self, ctx: dict) -> dict:
        report = self.run_audit(ctx.get("cycle_state", {}))
        return {
            "passed": report.passed,
            "failed": report.failed,
            "score": report.score,
            "conviction": report.conviction,
            "failures": report.failures[:5],
            "warnings": list(report.warnings),
        }

    def report(self) -> dict:
        return {
            "engine": "wisdom",
            "audits": self._audits,
            "conviction": self._conviction,
            "conviction_required": self._conviction_required,
            "principles": list(self._principles),
        }
