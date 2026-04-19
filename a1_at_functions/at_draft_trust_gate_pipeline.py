# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_trust_gate_pipeline.py:7
# Component id: at.source.a1_at_functions.trust_gate_pipeline
from __future__ import annotations

__version__ = "0.1.0"

def trust_gate_pipeline(
    client: Any,
    agent_id: str,
    *,
    on_progress: ProgressCallback | None = None,
    persist_dir: str | None = None,
) -> Pipeline:
    """Build a trust-gate pipeline: identity → sybil → trust → reputation → gate.

    Uses NexusClient endpoints, wrapping each as a pipeline step.
    """
    from ass_ade.nexus.validation import validate_agent_id

    aid = validate_agent_id(agent_id)

    def identity_step(ctx: dict[str, Any]) -> StepResult:
        try:
            result = client.identity_verify(aid)
            raw = result.model_dump() if hasattr(result, "model_dump") else {}
            passed = raw.get("decision", "allow") != "deny"
            ctx["identity_passed"] = passed
            return StepResult(name="identity_verify", status=StepStatus.PASSED if passed else StepStatus.FAILED, output=raw)
        except Exception as exc:
            return StepResult(name="identity_verify", status=StepStatus.FAILED, error=str(exc))

    def sybil_step(ctx: dict[str, Any]) -> StepResult:
        try:
            result = client.sybil_check(aid)
            raw = result.model_dump() if hasattr(result, "model_dump") else {}
            risk = raw.get("sybil_risk", "low")
            passed = risk != "high"
            ctx["sybil_passed"] = passed
            return StepResult(name="sybil_check", status=StepStatus.PASSED if passed else StepStatus.FAILED, output=raw)
        except Exception as exc:
            return StepResult(name="sybil_check", status=StepStatus.FAILED, error=str(exc))

    def trust_step(ctx: dict[str, Any]) -> StepResult:
        try:
            result = client.trust_score(aid)
            raw = result.model_dump() if hasattr(result, "model_dump") else {}
            score = raw.get("score", 0)
            passed = score >= 0.5
            ctx["trust_score"] = score
            return StepResult(name="trust_score", status=StepStatus.PASSED if passed else StepStatus.FAILED, output=raw)
        except Exception as exc:
            return StepResult(name="trust_score", status=StepStatus.FAILED, error=str(exc))

    def reputation_step(ctx: dict[str, Any]) -> StepResult:
        try:
            result = client.reputation_score(aid)
            raw = result.model_dump() if hasattr(result, "model_dump") else {}
            ctx["reputation_tier"] = raw.get("tier")
            return StepResult(name="reputation_score", status=StepStatus.PASSED, output=raw)
        except Exception as exc:
            return StepResult(name="reputation_score", status=StepStatus.FAILED, error=str(exc))

    def gate_step(ctx: dict[str, Any]) -> StepResult:
        trust_score = ctx.get("trust_score", 0)
        rep_tier = ctx.get("reputation_tier")
        identity_ok = ctx.get("identity_passed", False)
        sybil_ok = ctx.get("sybil_passed", False)

        if not identity_ok or not sybil_ok:
            verdict = "DENY"
        elif trust_score < 0.5:
            verdict = "DENY"
        elif trust_score < 0.7 and rep_tier not in {"gold", "platinum"}:
            verdict = "WARN"
        else:
            verdict = "ALLOW"

        ctx["verdict"] = verdict
        passed = verdict != "DENY"
        return StepResult(
            name="gate_decision",
            status=StepStatus.PASSED if passed else StepStatus.FAILED,
            output={"verdict": verdict, "trust_score": trust_score, "reputation_tier": rep_tier},
        )

    pipe = Pipeline(
        f"trust-gate-{aid}",
        fail_fast=False,  # run all steps even if some fail
        persist_dir=persist_dir,
        on_progress=on_progress,
    )
    pipe.add("identity_verify", identity_step)
    pipe.add("sybil_check", sybil_step)
    pipe.add("trust_score", trust_step)
    pipe.add("reputation_score", reputation_step)
    pipe.add("gate_decision", gate_step)
    return pipe
