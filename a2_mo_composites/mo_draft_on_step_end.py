# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_engineorchestrator.py:334
# Component id: mo.source.a2_mo_composites.on_step_end
from __future__ import annotations

__version__ = "0.1.0"

def on_step_end(
    self,
    response: str,
    cycle_state: dict,
    agent_traces: dict | None = None,
) -> CycleReport:
    """Called after final response. Runs full cycle analysis."""
    report = CycleReport(alerts=[])

    # Wisdom: 50-question audit
    try:
        # Augment cycle_state with step metrics
        cs = dict(cycle_state)
        cs.setdefault("tool_calls", list(self._step_tool_counts.keys()))
        cs.setdefault("budget_ok", True)
        wisdom_report = self.wisdom.run_audit(cs)
        report.wisdom_score = wisdom_report.score
        report.wisdom_passed = wisdom_report.passed
        report.wisdom_failed = wisdom_report.failed
        report.conviction = wisdom_report.conviction
        report.principles = self.wisdom.distill_principles(wisdom_report)
        report.warnings = list(wisdom_report.warnings) if hasattr(wisdom_report, "warnings") else []
        # Wisdom EMA (Phase 4): track session quality trend
        self._wisdom_ema = 0.85 * self._wisdom_ema + 0.15 * wisdom_report.score
        report.wisdom_ema = self._wisdom_ema
        # Persist EMA so next session's conviction pre-gate is meaningful
        self._persist_wisdom_ema(wisdom_report)
        # Consecutive low wisdom tracking (for autopoietic trigger)
        if wisdom_report.score < 0.3:
            self._consecutive_low_wisdom += 1
        else:
            self._consecutive_low_wisdom = 0
        # Principle persistence (Phase 4)
        try:
            self.wisdom.persist_principles(lora_flywheel=self._lora_flywheel)
        except Exception:
            pass
    except Exception as exc:
        _LOG.debug("wisdom.on_step_end failed: %s", exc)

    # TDMI: compute synergy from agent traces
    try:
        traces = agent_traces or {
            tool: [float(i) for i in range(count)]
            for tool, count in self._step_tool_counts.items()
            if count > 1
        }
        if len(traces) >= 2:
            synergy = self.tdmi.compute_synergy(traces)
            report.synergy = synergy
            report.synergy_emergent = synergy > self.tdmi._threshold
        else:
            report.synergy = 0.0
    except Exception as exc:
        _LOG.debug("tdmi.on_step_end failed: %s", exc)

    # GVU: update coefficient from wisdom score improvement
    try:
        if report.wisdom_score > 0:
            coef = self.gvu.update([report.wisdom_score - 0.5])
            report.gvu_coefficient = coef
        else:
            report.gvu_coefficient = self.gvu.compute_coefficient()
    except Exception as exc:
        _LOG.debug("gvu.on_step_end failed: %s", exc)

    # BAS: full monitor with all available metrics
    try:
        metrics = {
            "synergy": report.synergy,
            "novelty": report.wisdom_score,
            "gvu_delta": max(0.0, report.gvu_coefficient - 1.0),
            "trust_score": cycle_state.get("trust_score", 1.0),
            "budget_pct": cycle_state.get("budget_pct", 0.0),
            "score_delta": report.wisdom_score - cycle_state.get("last_wisdom_score", report.wisdom_score),
            "tool_repeat_count": max(self._step_tool_counts.values()) if self._step_tool_counts else 0,
            "missing_capabilities": cycle_state.get("missing_capabilities", []),
        }
        new_alerts = self.bas.monitor_all(metrics)
        unflushed = self.bas.flush_alerts()
        report.alerts = list(new_alerts) + [a for a in unflushed if a not in new_alerts]
    except Exception as exc:
        _LOG.debug("bas.on_step_end failed: %s", exc)

    # EDEE: capture experience trace
    try:
        self.edee.capture_trace("step_end", {
            "summary": response[:200] if response else "",
            "wisdom_score": report.wisdom_score,
            "alerts": len(report.alerts),
            "tool_calls": list(self._step_tool_counts.keys()),
        })
    except Exception as exc:
        _LOG.debug("edee.on_step_end failed: %s", exc)

    # Collect all engine reports
    for name, getter in [
        ("atlas", lambda: self._atlas),
        ("bas", lambda: self._bas),
        ("wisdom", lambda: self._wisdom),
        ("gvu", lambda: self._gvu),
        ("tdmi", lambda: self._tdmi),
        ("edee", lambda: self._edee),
        ("lifr", lambda: self._lifr),
        ("puppeteer", lambda: self._puppeteer),
        ("lse", lambda: self._lse),
        ("tca", lambda: self._tca),
        ("cie", lambda: self._cie),
        ("lora_flywheel", lambda: self._lora_flywheel),
    ]:
        try:
            engine = getter()
            if engine is not None:
                report.engine_reports[name] = engine.report()
        except Exception:
            pass

    # Atlas subtasks from step start
    report.atlas_subtasks = [s for s in report.engine_reports.get("atlas", {}).get("subtasks", [])]

    # TCA stale files (Phase 2)
    try:
        stale = self.tca.get_stale_files()
        report.tca_stale_files = [r.path for r in stale[:10]]
    except Exception as exc:
        _LOG.debug("tca.on_step_end failed: %s", exc)

    # LoRA Flywheel tick (Phase 5) — batch every RG_LOOP=47 steps
    try:
        batch_result = self.lora_flywheel.tick()
        report.lora_pending = len(self._lora_flywheel._pending) if self._lora_flywheel else 0
        if batch_result and batch_result.submitted > 0:
            _LOG.info("LoRA batch submitted: %d contributions", batch_result.submitted)
    except Exception as exc:
        _LOG.debug("lora_flywheel.on_step_end failed: %s", exc)

    # Autopoietic trigger check (Phase 5)
    try:
        if self._consecutive_low_wisdom >= 5 or self._consecutive_refine_failures >= 3:
            report.autopoietic_triggered = True
            try:
                self.bas.alert("autopoietic_trigger", {
                    "consecutive_low_wisdom": self._consecutive_low_wisdom,
                    "consecutive_refine_failures": self._consecutive_refine_failures,
                })
            except Exception:
                pass
            report.warnings.append(
                f"autopoietic_trigger:low_wisdom={self._consecutive_low_wisdom}"
            )
    except Exception as exc:
        _LOG.debug("autopoietic trigger check failed: %s", exc)

    # CIE stats from engine (Phase 3)
    try:
        if self._cie:
            cie_rep = self._cie.report()
            report.cie_passes = cie_rep.get("passes", 0)
            report.cie_failures = cie_rep.get("failures", 0)
    except Exception:
        pass

    return report
