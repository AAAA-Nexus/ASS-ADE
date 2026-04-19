"""v18 EngineOrchestrator — lifecycle coordinator for all standalone engines.

Holds and coordinates all v18 pillar engines. Called by AgentLoop at:
  - on_step_start(): ATLAS decompose, Puppeteer select next, LIFR query
  - on_tool_event(): BAS monitor per tool call, SAM validate
  - on_step_end(): Wisdom audit, TDMI synergy, GVU update, EDEE trace, IDE search

The orchestrator never blocks the agent loop — all methods are fail-open.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

_LOG = logging.getLogger(__name__)


def _infer_required_capabilities(user_message: str, step_start: dict[str, Any]) -> list[str]:
    """Heuristic inference of required capabilities from a user message.

    Looks for explicit hints (ATLAS subtasks, routing.capabilities) and falls
    back to keyword matching on common verbs. Conservative: empty list means
    "no required caps known" and MAP=TERRAIN is skipped.
    """
    caps: list[str] = []
    # 1. Explicit caps from routing
    explicit = step_start.get("required_capabilities")
    if isinstance(explicit, (list, tuple)):
        caps.extend(str(c).strip() for c in explicit if str(c).strip())
    # 2. Pull verbs from ATLAS subtasks
    for sub in step_start.get("atlas_subtasks") or []:
        action = sub.get("action") if isinstance(sub, dict) else None
        if action:
            caps.append(str(action).strip().lower())
    # 3. Keyword hints from user message
    lower = (user_message or "").lower()
    keyword_map = {
        "certify": "certify_output",
        "trust gate": "trust_gate",
        "safe execute": "safe_execute",
        "a2a": "a2a_validate",
        "map terrain": "map_terrain",
    }
    for kw, cap in keyword_map.items():
        if kw in lower:
            caps.append(cap)
    # Dedupe while preserving order
    seen: set[str] = set()
    out: list[str] = []
    for c in caps:
        if c and c not in seen:
            seen.add(c)
            out.append(c)
    return out


@dataclass
class CycleReport:
    """Full report from one agent step cycle."""
    alerts: list  # list[Alert] — typed at runtime to avoid circular import
    wisdom_score: float = 0.0
    wisdom_passed: int = 0
    wisdom_failed: int = 0
    conviction: float = 0.5
    wisdom_ema: float = 0.5  # Exponential moving average of wisdom scores
    gvu_coefficient: float = 1.0
    synergy: float = 0.0
    synergy_emergent: bool = False
    atlas_subtasks: list = field(default_factory=list)  # list[SubTask]
    principles: list[str] = field(default_factory=list)
    engine_reports: dict[str, dict] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    tca_stale_files: list[str] = field(default_factory=list)
    cie_passes: int = 0
    cie_failures: int = 0
    lora_pending: int = 0
    autopoietic_triggered: bool = False


class EngineOrchestrator:
    def __init__(
        self,
        config: dict,
        nexus: Any | None = None,
        working_dir: str = ".",
    ) -> None:
        self._config = config
        self._nexus = nexus
        self._working_dir = working_dir
        # Instantiate all engines — lazy init on first use
        self._atlas = None
        self._bas = None
        self._wisdom = None
        self._gvu = None
        self._tdmi = None
        self._edee = None
        self._severa = None
        self._ide = None
        self._lifr = None
        self._puppeteer = None
        self._sam = None
        # Phase 1-5 engines
        self._lse = None
        self._tca = None
        self._cie = None
        self._lora_flywheel = None
        # Cross-session state: loaded on first access via _hydrate_state
        self._state_hydrated: bool = False
        # Metrics accumulated across tool calls within one step
        self._step_tool_counts: dict[str, int] = {}
        self._step_tool_results: list[str] = []
        # Wisdom EMA and autopoietic tracking (Phase 4-5)
        self._wisdom_ema: float = 0.5
        self._consecutive_low_wisdom: int = 0
        self._consecutive_refine_failures: int = 0
        # Conviction threshold for pre-gate (below this → warn)
        self._conviction_threshold: float = float(
            (config.get("sde") or {}).get("conviction_required", 0.4)
        )
        # Destructive tool names that require conviction pre-gate
        self._destructive_tools: frozenset[str] = frozenset({
            "write_file", "edit_file", "run_command", "safe_execute",
        })

    # ── Engine accessors (lazy init) ──────────────────────────────────────────

    @property
    def atlas(self):
        if self._atlas is None:
            from ass_ade.agent.atlas import Atlas
            self._atlas = Atlas(self._config, self._nexus)
        return self._atlas

    @property
    def bas(self):
        if self._bas is None:
            from ass_ade.agent.bas import BAS
            self._bas = BAS(self._config, self._nexus)
        return self._bas

    @property
    def wisdom(self):
        if self._wisdom is None:
            from ass_ade.agent.wisdom import WisdomEngine
            self._wisdom = WisdomEngine(self._config, self._nexus)
            # Hydrate principles + conviction from prior sessions (Phase 4)
            self._hydrate_wisdom(self._wisdom)
        return self._wisdom

    def _persist_wisdom_ema(self, wisdom_report: Any) -> None:
        """Write current conviction/EMA to disk so next session starts informed."""
        try:
            from pathlib import Path as _P
            import json as _json
            state_dir = _P(self._working_dir) / ".ass-ade" / "state"
            state_dir.mkdir(parents=True, exist_ok=True)
            (state_dir / "wisdom_ema.json").write_text(
                _json.dumps({
                    "ema": self._wisdom_ema,
                    "conviction": getattr(wisdom_report, "conviction", 0.5),
                    "audits": getattr(self._wisdom, "_audits", 0) if self._wisdom else 0,
                    "last_score": getattr(wisdom_report, "score", 0.0),
                }, indent=2),
                encoding="utf-8",
            )
        except Exception:
            pass

    def _hydrate_wisdom(self, engine: Any) -> None:
        """Pre-load principles + last conviction EMA from persisted memory.

        Called once when WisdomEngine is first materialized. Makes the
        conviction pre-gate meaningful on turn 1 of a new session (instead
        of no-op because `_audits == 0`), and carries distilled principles
        forward from previous sessions.
        """
        try:
            # 1. Hydrate principles from vector store
            loaded = engine.hydrate_from_memory(top_k=10, working_dir=self._working_dir)
            if loaded:
                _LOG.info("WisdomEngine hydrated with %d prior principles", loaded)

            # 2. Load last session's conviction EMA so the pre-gate works
            #    on turn 1 (instead of being no-op for fresh sessions).
            from pathlib import Path as _P
            ema_path = _P(self._working_dir) / ".ass-ade" / "state" / "wisdom_ema.json"
            if ema_path.exists():
                import json as _json
                data = _json.loads(ema_path.read_text(encoding="utf-8"))
                ema = float(data.get("ema", 0.5))
                prior_audits = int(data.get("audits", 0))
                engine._conviction = ema
                engine._audits = prior_audits  # keeps pre-gate active on turn 1
                self._wisdom_ema = ema
        except Exception as exc:
            _LOG.debug("_hydrate_wisdom failed (fail-open): %s", exc)

    @property
    def gvu(self):
        if self._gvu is None:
            from ass_ade.agent.gvu import GVU
            cfg = dict(self._config)
            cfg.setdefault("gvu_state_path", f"{self._working_dir}/.ass-ade/state/gvu.json")
            self._gvu = GVU(cfg, self._nexus)
        return self._gvu

    @property
    def tdmi(self):
        if self._tdmi is None:
            from ass_ade.agent.tdmi import TDMI
            self._tdmi = TDMI(self._config, self._nexus)
        return self._tdmi

    @property
    def edee(self):
        if self._edee is None:
            from ass_ade.agent.edee import EDEE
            cfg = dict(self._config)
            cfg.setdefault("working_dir", self._working_dir)
            self._edee = EDEE(cfg, self._nexus)
        return self._edee

    @property
    def lifr(self):
        if self._lifr is None:
            from ass_ade.agent.lifr_graph import LIFRGraph
            cfg = dict(self._config)
            cfg.setdefault("working_dir", self._working_dir)
            self._lifr = LIFRGraph(cfg, self._nexus)
        return self._lifr

    @property
    def puppeteer(self):
        if self._puppeteer is None:
            from ass_ade.agent.puppeteer import Puppeteer
            self._puppeteer = Puppeteer(self._config, self._nexus)
        return self._puppeteer

    @property
    def sam(self):
        if self._sam is None:
            from ass_ade.agent.sam import SAM
            self._sam = SAM(self._config, self._nexus)
        return self._sam

    @property
    def ide(self):
        if self._ide is None:
            from ass_ade.agent.ide import IDE
            self._ide = IDE(self._config, self._nexus)
        return self._ide

    @property
    def severa(self):
        if self._severa is None:
            from ass_ade.agent.severa import Severa
            self._severa = Severa(self._config, self._nexus)
        return self._severa

    @property
    def lse(self):
        if self._lse is None:
            from ass_ade.agent.lse import LSEEngine
            self._lse = LSEEngine(self._config, self._nexus)
        return self._lse

    @property
    def tca(self):
        if self._tca is None:
            from ass_ade.agent.tca import TCAEngine
            cfg = dict(self._config)
            cfg.setdefault("working_dir", self._working_dir)
            self._tca = TCAEngine(cfg, self._nexus)
        return self._tca

    @property
    def cie(self):
        if self._cie is None:
            from ass_ade.agent.cie import CIEPipeline
            self._cie = CIEPipeline(self._config, self._nexus)
        return self._cie

    @property
    def lora_flywheel(self):
        if self._lora_flywheel is None:
            from ass_ade.agent.lora_flywheel import LoRAFlywheel
            self._lora_flywheel = LoRAFlywheel(self._config, self._nexus)
        return self._lora_flywheel

    # ── Conviction pre-gate (Phase 4) ─────────────────────────────────────────

    def check_conviction_gate(self, tool_name: str, args: dict) -> bool:
        """Return True if the tool call should be BLOCKED due to low conviction.

        Only blocks destructive tools when conviction is below threshold.
        Fail-open: returns False (don't block) on any error.
        """
        if tool_name not in self._destructive_tools:
            return False
        try:
            conviction = self.wisdom.conviction if self._wisdom else 0.5
            if conviction < self._conviction_threshold and self.wisdom._audits > 0:
                _LOG.warning(
                    "Conviction gate: %s blocked (conviction=%.2f < %.2f)",
                    tool_name, conviction, self._conviction_threshold,
                )
                return True
        except Exception as exc:
            _LOG.debug("conviction gate check failed (fail-open): %s", exc)
        return False

    # ── Lifecycle hooks ───────────────────────────────────────────────────────

    def on_step_start(self, user_message: str, routing: Any = None) -> dict:
        """Called before model is invoked. Returns pre-step analysis."""
        # Reset per-step metrics
        self._step_tool_counts = {}
        self._step_tool_results = []

        result: dict[str, Any] = {}

        # ATLAS: decompose if complex
        try:
            complexity = float(getattr(routing, "complexity", 0.0) or 0.0)
            subs = self.atlas.decompose(user_message, complexity if complexity > 0 else None)
            result["atlas_subtasks"] = [s.__dict__ for s in subs]
            result["atlas_complexity"] = self.atlas.complexity_score(user_message)
        except Exception as exc:
            _LOG.debug("atlas.on_step_start failed: %s", exc)

        # LIFR: query knowledge graph for relevant patterns
        try:
            matches = self.lifr.query(user_message[:500], top_k=3)
            result["lifr_matches"] = len(matches)
            result["lifr_patterns"] = [m.spec[:100] for m in matches]
        except Exception as exc:
            _LOG.debug("lifr.on_step_start failed: %s", exc)

        # Puppeteer: get next engine recommendation
        try:
            state = {"visited": list(result.keys())}
            agent_ref = self.puppeteer.select_next_agent(state)
            result["puppeteer_next"] = agent_ref.name
            result["puppeteer_reason"] = agent_ref.reason
        except Exception as exc:
            _LOG.debug("puppeteer.on_step_start failed: %s", exc)

        # TCA: freshness pre-check (Phase 2)
        try:
            stale = self.tca.get_stale_files()
            result["tca_stale_count"] = len(stale)
            result["tca_stale_paths"] = [r.path for r in stale[:5]]
        except Exception as exc:
            _LOG.debug("tca.on_step_start failed: %s", exc)

        # MAP=TERRAIN: active capability gate pre-synthesis (Phase 2)
        # Infer required capabilities from ATLAS subtask verbs and from
        # explicit per-step hints in routing. If any are missing, emit a BAS
        # alert + surface the verdict — agent loop can decide to halt.
        try:
            from ass_ade.map_terrain import active_terrain_gate

            required = _infer_required_capabilities(user_message, result)
            if required:
                terrain = active_terrain_gate(
                    required,
                    context={"task_description": user_message[:200]},
                    working_dir=self._working_dir,
                    write_stubs=False,  # never write stubs from the pre-synthesis gate
                )
                result["terrain_verdict"] = terrain.verdict
                result["terrain_missing"] = list(terrain.capabilities_missing)
                if terrain.verdict == "HALT_AND_INVENT":
                    try:
                        self.bas.alert("capability_gap", {
                            "missing": terrain.capabilities_missing[:5],
                            "task": user_message[:120],
                        })
                    except Exception:
                        pass
        except Exception as exc:
            _LOG.debug("map_terrain.on_step_start failed: %s", exc)

        return result

    def on_tool_event(self, tool_name: str, args: dict, result_content: str) -> list:
        """Called after each tool execution. Returns list of BAS alerts fired."""
        self._step_tool_counts[tool_name] = self._step_tool_counts.get(tool_name, 0) + 1
        self._step_tool_results.append(f"{tool_name}:{result_content[:50]}")

        alerts = []
        try:
            max_repeat = max(self._step_tool_counts.values()) if self._step_tool_counts else 0
            metrics = {
                "tool_repeat_count": max_repeat,
                "synergy": 0.0,
                "novelty": 0.0,
                "gvu_delta": 0.0,
            }
            new_alerts = self.bas.monitor_all(metrics)
            alerts.extend(new_alerts)
        except Exception as exc:
            _LOG.debug("bas.on_tool_event failed: %s", exc)

        return alerts

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

    def engine_report(self) -> dict:
        """Combined report from all initialized engines."""
        reports: dict[str, Any] = {}
        for name, getter in [
            ("atlas", lambda: self._atlas),
            ("bas", lambda: self._bas),
            ("wisdom", lambda: self._wisdom),
            ("gvu", lambda: self._gvu),
            ("tdmi", lambda: self._tdmi),
            ("edee", lambda: self._edee),
            ("severa", lambda: self._severa),
            ("ide", lambda: self._ide),
            ("lifr", lambda: self._lifr),
            ("puppeteer", lambda: self._puppeteer),
            ("sam", lambda: self._sam),
            ("lse", lambda: self._lse),
            ("tca", lambda: self._tca),
            ("cie", lambda: self._cie),
            ("lora_flywheel", lambda: self._lora_flywheel),
        ]:
            engine = getter()
            if engine is not None:
                try:
                    reports[name] = engine.report()
                except Exception:
                    pass
        return reports
