# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_trust_gate_pipeline.py:63
# Component id: at.source.a1_at_functions.gate_step
from __future__ import annotations

__version__ = "0.1.0"

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
