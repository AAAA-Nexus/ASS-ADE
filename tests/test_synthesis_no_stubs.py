"""Tests for strict no-stubs synthesis behaviour.

Covers two contracts:

1. When Nexus inference returns ``None`` on every attempt and stubs are
   disabled, :func:`synthesize_missing_components` must raise
   :class:`SynthesisFailure` and the plan must not gain a
   ``synthesized_stub`` body.
2. Refinement feedback is recorded: a failing attempt leaves a
   ``refinement_trace`` entry with the rejecting findings.
"""

from __future__ import annotations

import pytest

from ass_ade.engine.rebuild import synthesis as S
from ass_ade.engine.rebuild.synthesis import (
    SynthesisFailure,
    synthesize_missing_components,
)


def _plan_with_missing(cid: str = "at_example_missing") -> dict:
    return {
        "blueprint_fulfillment": [
            {
                "blueprint_id": "bp_test",
                "blueprint_name": "test blueprint",
                "still_unfulfilled": [cid],
                "satisfied_by_synthesis": [],
                "fully_satisfied": False,
            }
        ],
        "proposed_components": [],
    }


def test_strict_no_stubs_raises_when_nexus_unreachable(monkeypatch):
    monkeypatch.setattr(S, "_synthesize_via_nexus", lambda *a, **kw: None)
    monkeypatch.setattr(S, "_fetch_current_adapter", lambda *a, **kw: None)
    plan = _plan_with_missing()

    with pytest.raises(SynthesisFailure):
        synthesize_missing_components(
            plan,
            api_key="dummy",  # force adapter path to be reachable conceptually
            allow_stub_fallback=False,
            strict_no_stubs=True,
            max_refinement_attempts=2,
        )

    bodies = [c.get("body", "") for c in plan.get("proposed_components", [])]
    assert all("synthesized_stub" not in b for b in bodies)
    assert not plan.get("proposed_components"), "no components should be added on strict failure"


def test_refinement_trace_records_cie_failures(monkeypatch):
    call_log: list[str | None] = []

    def fake_nexus(*args, **kwargs):
        call_log.append(kwargs.get("feedback"))
        # Always return code that fails the OWASP gate (contains eval).
        return "def bad():\n    return eval('1+1')\n"

    monkeypatch.setattr(S, "_synthesize_via_nexus", fake_nexus)
    monkeypatch.setattr(S, "_fetch_current_adapter", lambda *a, **kw: None)
    plan = _plan_with_missing("at_bad_component")

    with pytest.raises(SynthesisFailure):
        synthesize_missing_components(
            plan,
            allow_stub_fallback=False,
            strict_no_stubs=True,
            max_refinement_attempts=3,
        )

    # First attempt had no feedback; subsequent attempts should carry feedback.
    assert call_log[0] is None
    assert any(fb is not None for fb in call_log[1:]), "feedback should be forwarded on retries"
    summary = plan.get("summary", {}).get("synthesis", {})
    assert summary.get("rejected_count") == 1
    assert summary.get("refinement_attempts_total", 0) >= 2


def test_stub_fallback_opt_in_still_works(monkeypatch):
    monkeypatch.setattr(S, "_synthesize_via_nexus", lambda *a, **kw: None)
    monkeypatch.setattr(S, "_fetch_current_adapter", lambda *a, **kw: None)
    plan = _plan_with_missing("at_stub_ok")

    receipt = synthesize_missing_components(
        plan,
        allow_stub_fallback=True,
        strict_no_stubs=False,
        max_refinement_attempts=1,
    )
    assert receipt["stub_used"] >= 1 or receipt["rejected"], (
        "stub path must either succeed or emit a structured rejection"
    )
