# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_engineorchestrator.py:241
# Component id: mo.source.a2_mo_composites.on_step_start
from __future__ import annotations

__version__ = "0.1.0"

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
