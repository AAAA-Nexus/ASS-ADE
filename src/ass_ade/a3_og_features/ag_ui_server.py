"""Tier a3 — FastAPI AG-UI server.

Bridges the Atomadic Python agent to any AG-UI-compatible frontend (Tauri shell,
SvelteKit/React SPA, CopilotKit widgets, etc.) over:
  - GET  /events       — Server-Sent Events stream (AG-UI protocol)
  - GET  /state        — current state snapshot
  - GET  /commands     — introspected CLI command schemas (for ⌘K palette)
  - POST /commands/{name}/run — execute a CLI command with JSON args
  - POST /chat         — send a turn to the interpreter
  - GET  /scout/reports, /scout/report/{name}
  - GET  /assimilation/summary, /assimilation/candidates
  - GET  /memory/personality, /memory/episodes, /memory/anchors
  - POST /memory/anchors, DELETE /memory/anchors/{key}
  - POST /personality/persona
  - GET  /skills, POST /skills/{name}/run

FastAPI and uvicorn are optional — install with: pip install 'ass-ade[ui]'.
"""

from __future__ import annotations

import traceback
from pathlib import Path
from typing import Any


def build_app(working_dir: Path | None = None):
    """Build the FastAPI app. Imports FastAPI lazily so the module imports
    cleanly even when the 'ui' extra is not installed."""
    try:
        from fastapi import Body, FastAPI, HTTPException
        from fastapi.middleware.cors import CORSMiddleware
        from fastapi.responses import StreamingResponse
        from pydantic import BaseModel
    except ImportError as exc:  # pragma: no cover - exercised by install check
        raise RuntimeError(
            "FastAPI is not installed. Install the UI extras: pip install 'ass-ade[ui]'"
        ) from exc

    from ass_ade.a2_mo_composites.ag_ui_bus import (
        AGUIEventType,
        get_bus,
    )

    app = FastAPI(title="ASS-ADE Dashboard", version="1.0.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    bus = get_bus()
    wdir = (working_dir or Path.cwd()).resolve()

    # ── Health / meta ───────────────────────────────────────────────────────

    @app.get("/health")
    def health() -> dict:
        return {
            "status": "ok",
            "working_dir": str(wdir),
            "subscribers": bus.subscriber_count(),
            "buffered_events": len(bus.history(500)),
        }

    # ── AG-UI event stream ──────────────────────────────────────────────────

    @app.get("/events")
    async def events(replay: int = 0) -> StreamingResponse:
        async def stream():
            # AG-UI SSE: emit a snapshot first so late joiners get the state
            bus.emit_snapshot()
            async for event in bus.subscribe(replay=replay):
                yield event.to_sse()
        return StreamingResponse(stream(), media_type="text/event-stream")

    @app.get("/state")
    def state() -> dict:
        return bus.snapshot()

    @app.get("/history")
    def history(limit: int = 100) -> list[dict]:
        return bus.history(limit=limit)

    # ── CLI command palette ─────────────────────────────────────────────────

    @app.get("/commands")
    def commands() -> dict:
        from ass_ade.a2_mo_composites.cli_introspector import (
            categorize_commands,
            introspect_typer_app,
        )
        from ass_ade.cli import app as typer_app

        cmds = introspect_typer_app(typer_app)
        return {
            "total": len(cmds),
            "commands": cmds,
            "categories": categorize_commands(cmds),
        }

    class CommandInvocation(BaseModel):
        args: list[str] = []

    @app.post("/commands/{name}/run")
    def run_command(name: str, body: CommandInvocation) -> dict:
        """Run a CLI command with stringified args (as you'd type on the shell)."""
        from click.testing import CliRunner

        from ass_ade.cli import app as typer_app

        run_id = bus.new_run_id()
        bus.emit(AGUIEventType.TOOL_CALL_START,
                 {"tool": "cli", "command": name, "args": body.args}, run_id=run_id)
        try:
            runner = CliRunner(mix_stderr=False)
            result = runner.invoke(typer_app, [name, *body.args])
            bus.emit(AGUIEventType.TOOL_CALL_RESULT,
                     {"tool": "cli", "command": name, "exit_code": result.exit_code,
                      "stdout": result.stdout[:20_000], "stderr": (result.stderr or "")[:20_000]},
                     run_id=run_id)
            bus.emit(AGUIEventType.TOOL_CALL_END, {"tool": "cli"}, run_id=run_id)
            return {
                "run_id": run_id,
                "exit_code": result.exit_code,
                "stdout": result.stdout,
                "stderr": result.stderr or "",
            }
        except Exception as exc:
            bus.emit(AGUIEventType.RUN_ERROR,
                     {"error": str(exc), "traceback": traceback.format_exc()}, run_id=run_id)
            raise HTTPException(status_code=500, detail=str(exc))

    # ── Chat / interpreter ──────────────────────────────────────────────────

    class ChatMessage(BaseModel):
        text: str
        working_dir: str | None = None

    @app.post("/chat")
    def chat(msg: ChatMessage) -> dict:
        from ass_ade.interpreter import Atomadic

        run_id = bus.new_run_id()
        bus.emit(AGUIEventType.RUN_STARTED, {"input": msg.text}, run_id=run_id)
        try:
            target_wd = Path(msg.working_dir).resolve() if msg.working_dir else wdir
            agent = Atomadic(working_dir=target_wd)
            bus.emit(AGUIEventType.TEXT_MESSAGE_START, {"role": "assistant"}, run_id=run_id)
            response = agent.process(msg.text)
            bus.emit(AGUIEventType.TEXT_MESSAGE_CONTENT, {"delta": response}, run_id=run_id)
            bus.emit(AGUIEventType.TEXT_MESSAGE_END, {}, run_id=run_id)
            bus.emit(AGUIEventType.RUN_FINISHED, {}, run_id=run_id)
            return {"run_id": run_id, "response": response}
        except Exception as exc:
            bus.emit(AGUIEventType.RUN_ERROR,
                     {"error": str(exc), "traceback": traceback.format_exc()}, run_id=run_id)
            raise HTTPException(status_code=500, detail=str(exc))

    # ── Scout tab ──────────────────────────────────────────────────────────

    @app.get("/scout/reports")
    def scout_reports() -> list[dict]:
        from ass_ade.a3_og_features.assimilation_stats import collect_scout_reports

        return [
            {
                "file": r.get("_filename"),
                "path": r.get("_file"),
                "repo": r.get("repo"),
                "mtime": r.get("_mtime"),
                "summary": r.get("summary"),
                "symbol_summary": r.get("symbol_summary"),
                "counts": (r.get("target_map") or {}).get("action_counts"),
                "llm_status": (r.get("llm") or {}).get("status"),
                "recommendations": r.get("static_recommendations"),
            }
            for r in collect_scout_reports(wdir)
        ]

    @app.get("/scout/report/{name}")
    def scout_report(name: str) -> dict:
        from ass_ade.a3_og_features.assimilation_stats import collect_scout_reports

        for r in collect_scout_reports(wdir):
            if r.get("_filename") == name:
                return r
        raise HTTPException(status_code=404, detail="Report not found")

    class ScoutRequest(BaseModel):
        path: str
        use_llm: bool = False
        benefit_root: str | None = None

    @app.post("/scout/run")
    def scout_run(req: ScoutRequest) -> dict:
        from ass_ade.local.scout import scout_repo

        run_id = bus.new_run_id()
        bus.emit(AGUIEventType.TOOL_CALL_START,
                 {"tool": "scout", "path": req.path, "use_llm": req.use_llm}, run_id=run_id)
        try:
            target = Path(req.path).resolve()
            benefit = Path(req.benefit_root).resolve() if req.benefit_root else None
            report = scout_repo(target, benefit_root=benefit, use_llm=req.use_llm)
            bus.emit_widget("scout_report", {
                "repo": report.get("repo"),
                "counts": (report.get("target_map") or {}).get("action_counts"),
                "llm_status": (report.get("llm") or {}).get("status"),
            }, run_id=run_id)
            bus.emit(AGUIEventType.TOOL_CALL_RESULT, {"tool": "scout", "ok": True}, run_id=run_id)
            bus.emit(AGUIEventType.TOOL_CALL_END, {"tool": "scout"}, run_id=run_id)
            return report
        except Exception as exc:
            bus.emit(AGUIEventType.RUN_ERROR, {"error": str(exc)}, run_id=run_id)
            raise HTTPException(status_code=500, detail=str(exc))

    # ── Assimilate tab ─────────────────────────────────────────────────────

    @app.get("/assimilation/summary")
    def assimilation_summary() -> dict:
        from ass_ade.a3_og_features.assimilation_stats import summarize_for_dashboard

        return summarize_for_dashboard(wdir)

    @app.get("/assimilation/candidates")
    def assimilation_candidates(
        action: str | None = None,
        min_confidence: float = 0.0,
        limit: int = 200,
    ) -> list[dict]:
        from ass_ade.a3_og_features.assimilation_stats import (
            cherry_pick_candidates,
            collect_scout_reports,
        )

        return cherry_pick_candidates(
            collect_scout_reports(wdir),
            action=action,
            min_confidence=min_confidence,
            limit=limit,
        )

    @app.post("/assimilation/cherry-preview")
    def assimilation_cherry_preview(req: dict = Body(default={})) -> dict:  # noqa: B008
        """Preview ranked cherry-pick candidates for a scout report or source directory."""
        from ass_ade.a3_og_features.cherry_feature import preview_cherry_pick

        source = Path(str(req.get("source") or wdir)).resolve()
        target = Path(str(req.get("target") or wdir)).resolve()
        action = req.get("action")
        actions = None if not action or action == "all" else {str(action)}
        min_confidence = float(req.get("min_confidence") or 0.0)
        limit = int(req.get("limit") or 200)
        preview = preview_cherry_pick(
            source=source,
            target_root=target,
            actions=actions,
            min_confidence=min_confidence,
            limit=limit,
        )
        bus.emit_widget("assimilation_table", {
            "rows": preview.get("candidates", []),
            "action_filter": str(action or "all"),
            "min_confidence": min_confidence,
            "total_candidates": (preview.get("summary") or {}).get("total", 0),
        })
        return preview

    @app.post("/assimilation/cherry-pick")
    def assimilation_cherry_pick(req: dict = Body(default={})) -> dict:  # noqa: B008
        """Create/refresh a cherry_pick manifest from selected candidates."""
        from ass_ade.a3_og_features.cherry_feature import run_cherry_pick

        source = Path(str(req.get("source") or wdir)).resolve()
        target = Path(str(req.get("target") or wdir)).resolve()
        action = req.get("action")
        actions = None if not action or action == "all" else {str(action)}
        pick = str(req.get("pick") or "assimilate")
        out = req.get("out")
        out_path = Path(str(out)).resolve() if out else None
        manifest = run_cherry_pick(
            source=source,
            target_root=target,
            pick=pick,
            actions=actions,
            interactive=False,
            out_path=out_path,
            console_print=False,
            min_confidence=float(req.get("min_confidence") or 0.0),
            limit=int(req.get("limit") or 200),
        )
        actions_total: dict[str, int] = {}
        for item in manifest.get("items") or []:
            item_action = str(item.get("action") or "?")
            actions_total[item_action] = actions_total.get(item_action, 0) + 1
        bus.emit_widget("cherry_manifest", {
            "source_label": manifest.get("source_label", ""),
            "target_root": manifest.get("target_root", ""),
            "selected_count": manifest.get("selected_count", 0),
            "actions": actions_total,
        })
        return manifest

    # ── Wire tab ───────────────────────────────────────────────────────────

    def _resolve_source_dir(raw: str | None) -> Path:
        if raw:
            return Path(raw).resolve()
        src_dir = wdir / "src"
        if src_dir.is_dir():
            subdirs = [p for p in src_dir.iterdir() if p.is_dir() and p.name.isidentifier()]
            if len(subdirs) == 1:
                return subdirs[0]
        return wdir

    @app.post("/wire/scan")
    def wire_scan(req: dict = Body(default={})) -> dict:
        """Dry-run wire scan: returns violations and proposed patches without writing."""
        from ass_ade.a2_mo_composites.context_loader_wiring_specialist_core import (
            ContextLoaderWiringSpecialist,
        )

        run_id = bus.new_run_id()
        source = _resolve_source_dir(req.get("source") if isinstance(req, dict) else None)
        bus.emit(AGUIEventType.TOOL_CALL_START,
                 {"tool": "wire.scan", "source": str(source)}, run_id=run_id)
        specialist = ContextLoaderWiringSpecialist(
            package_name=req.get("package") if isinstance(req, dict) else None
        )
        records = specialist.rewire_imports(source)
        fixable = [r for r in records if r.auto_fixable]
        not_fixable = [r for r in records if not r.auto_fixable]
        by_file: dict[str, list[dict[str, str]]] = {}
        for r in fixable:
            by_file.setdefault(r.file, []).append({"old": r.old_import, "new": r.new_import or ""})

        report = {
            "source_dir": str(source),
            "violations_found": len(records),
            "would_fix": len(fixable),
            "not_fixable": len(not_fixable),
            "files_to_change": len(by_file),
            "changes": by_file,
            "manual_review": [
                {"file": r.file, "file_tier": r.file_tier, "import": r.old_import,
                 "imported_tier": r.imported_tier, "reason": r.reason}
                for r in not_fixable
            ],
            "dry_run": True,
            "verdict": "PASS" if not records else ("REFINE" if not_fixable else "DRY_RUN"),
        }

        bus.emit_widget("wiring_report", {
            "source_dir": report["source_dir"],
            "violations_found": report["violations_found"],
            "would_fix": report["would_fix"],
            "not_fixable": report["not_fixable"],
            "files_to_change": report["files_to_change"],
            "verdict": report["verdict"],
            "dry_run": True,
            "auto_fixed": 0,
            "files_changed": 0,
            "manual_review_count": len(not_fixable),
        }, run_id=run_id)
        bus.emit(AGUIEventType.TOOL_CALL_RESULT,
                 {"tool": "wire.scan", "ok": True}, run_id=run_id)
        bus.emit(AGUIEventType.TOOL_CALL_END, {"tool": "wire.scan"}, run_id=run_id)
        return report

    @app.post("/wire/apply")
    def wire_apply(req: dict = Body(default={})) -> dict:
        """Live wire: actually patches files on disk. Use with caution."""
        from ass_ade.a2_mo_composites.context_loader_wiring_specialist_core import (
            ContextLoaderWiringSpecialist,
        )

        run_id = bus.new_run_id()
        source = _resolve_source_dir(req.get("source") if isinstance(req, dict) else None)
        bus.emit(AGUIEventType.TOOL_CALL_START,
                 {"tool": "wire.apply", "source": str(source)}, run_id=run_id)
        specialist = ContextLoaderWiringSpecialist(
            package_name=req.get("package") if isinstance(req, dict) else None
        )
        report = specialist.wire(source)

        bus.emit_widget("wiring_report", {
            "source_dir": report["source_dir"],
            "violations_found": report["violations_found"],
            "auto_fixed": report["auto_fixed"],
            "files_changed": report["files_changed"],
            "not_fixable": report["not_fixable"],
            "verdict": report["verdict"],
            "dry_run": False,
            "manual_review_count": len(report.get("manual_review") or []),
        }, run_id=run_id)
        bus.emit(AGUIEventType.TOOL_CALL_RESULT,
                 {"tool": "wire.apply", "verdict": report["verdict"]}, run_id=run_id)
        bus.emit(AGUIEventType.TOOL_CALL_END, {"tool": "wire.apply"}, run_id=run_id)
        return report

    # ── Cherry-pick manifest (read-only view of .ass-ade/cherry_pick.json) ─

    @app.get("/assimilation/manifest")
    def assimilation_manifest() -> dict:
        """Return the current cherry_pick.json manifest, or {} if none."""
        manifest_path = wdir / ".ass-ade" / "cherry_pick.json"
        if not manifest_path.is_file():
            return {"present": False}
        try:
            import json as _json
            data = _json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            raise HTTPException(status_code=500, detail=f"Could not read manifest: {exc}")
        actions: dict[str, int] = {}
        for item in data.get("items") or []:
            a = str(item.get("action") or "?")
            actions[a] = actions.get(a, 0) + 1
        data["_path"] = str(manifest_path)
        data["_action_totals"] = actions
        data["present"] = True
        return data

    # ── Playground tab ─────────────────────────────────────────────────────

    def _playground_source_dir() -> Path:
        src = wdir / "src"
        if src.is_dir():
            subdirs = [p for p in src.iterdir() if p.is_dir() and p.name.isidentifier()]
            if len(subdirs) == 1:
                return subdirs[0]
        return wdir

    # Lazy singleton so scans are cached across requests
    _registry_cache: dict[str, Any] = {"registry": None, "mtime": 0.0}

    def _get_registry(force: bool = False):
        from ass_ade.a2_mo_composites.block_registry import BlockRegistry

        src = _playground_source_dir()
        if _registry_cache["registry"] is None or force:
            reg = BlockRegistry(src)
            reg.scan()
            _registry_cache["registry"] = reg
            bus.emit_widget("block_registry_snapshot", reg.stats())
        return _registry_cache["registry"]

    @app.get("/playground/blocks")
    def playground_blocks(
        query: str | None = None,
        tier: str | None = None,
        kind: str | None = None,
        has_test: bool | None = None,
        limit: int = 200,
        rescan: bool = False,
    ) -> dict:
        reg = _get_registry(force=rescan)
        results = reg.search(
            query=query, tier=tier, kind=kind, has_test=has_test, limit=limit
        )
        return {
            "stats": reg.stats(),
            "blocks": [b.to_dict() for b in results],
        }

    @app.get("/playground/block/{block_id}")
    def playground_block(block_id: str) -> dict:
        reg = _get_registry()
        block = reg.get(block_id)
        if block is None:
            raise HTTPException(status_code=404, detail="Block not found")
        return block.to_dict()

    @app.post("/playground/compile")
    def playground_compile(plan: dict = Body(default={})) -> dict:
        """Compile a CompositionPlan; does NOT write to disk."""
        from ass_ade.a3_og_features.composition_engine import (
            CompositionEngine,
            CompositionPlan,
        )

        run_id = bus.new_run_id()
        try:
            parsed = CompositionPlan.from_dict(plan)
        except Exception as exc:
            raise HTTPException(status_code=400, detail=f"Invalid plan: {exc}")

        bus.emit_widget("composition_plan", {
            "name": parsed.name,
            "target_tier": parsed.target_tier,
            "node_count": len(parsed.nodes),
            "edge_count": len(parsed.edges),
            "gap_count": len(parsed.gaps),
            "description": parsed.description,
        }, run_id=run_id)

        reg = _get_registry()
        engine = CompositionEngine(reg)
        result = engine.compile(parsed)

        bus.emit_widget("composition_result", {
            "name": parsed.name,
            "target_path": result.target_path,
            "verdict": result.verdict,
            "tier_violations": len(result.tier_violations),
            "detected_gaps": len(result.detected_gaps),
            "wrote_to_disk": False,
        }, run_id=run_id)
        return result.to_dict()

    class MaterializeRequest(BaseModel):
        plan: dict
        target_root: str | None = None

    @app.post("/playground/materialize")
    def playground_materialize(body: dict = Body(default={})) -> dict:
        """Compile AND write to disk. target_root defaults to the working dir."""
        from ass_ade.a3_og_features.composition_engine import (
            CompositionEngine,
            CompositionPlan,
        )

        plan_dict = body.get("plan") if isinstance(body, dict) else None
        if not isinstance(plan_dict, dict):
            raise HTTPException(status_code=400, detail="Missing 'plan' in request body")
        target_root_raw = body.get("target_root") if isinstance(body, dict) else None
        target_root = Path(target_root_raw).resolve() if target_root_raw else _playground_source_dir()

        parsed = CompositionPlan.from_dict(plan_dict)
        reg = _get_registry()
        engine = CompositionEngine(reg)
        result = engine.compile(parsed)
        if result.verdict == "REJECT":
            return result.to_dict()
        result = engine.materialize(result, target_root)
        bus.emit_widget("composition_result", {
            "name": parsed.name,
            "target_path": result.target_path,
            "verdict": result.verdict,
            "tier_violations": len(result.tier_violations),
            "detected_gaps": len(result.detected_gaps),
            "wrote_to_disk": result.wrote_to_disk,
        })
        return result.to_dict()

    # ── Gap-fill + hot-patch ───────────────────────────────────────────────

    @app.post("/playground/synthesize")
    def playground_synthesize(body: dict = Body(default={})) -> dict:
        """Fill every gap in a plan, materialize the feature, wire imports.

        Body:
          {"plan": {...}, "target_root": "<optional path>",
           "allow_stub_fallback": true, "use_llm": true}
        """
        from ass_ade.a3_og_features.composition_engine import CompositionPlan
        from ass_ade.a3_og_features.gap_fill_pipeline import GapFillPipeline

        plan_dict = body.get("plan") if isinstance(body, dict) else None
        if not isinstance(plan_dict, dict):
            raise HTTPException(status_code=400, detail="Missing 'plan' in request body")

        target_root_raw = body.get("target_root") if isinstance(body, dict) else None
        target_root = Path(target_root_raw).resolve() if target_root_raw else _playground_source_dir()
        allow_stub = bool(body.get("allow_stub_fallback", True))
        use_llm = bool(body.get("use_llm", True))

        run_id = bus.new_run_id()
        bus.emit(AGUIEventType.TOOL_CALL_START,
                 {"tool": "playground.synthesize", "plan": plan_dict.get("name")},
                 run_id=run_id)

        plan = CompositionPlan.from_dict(plan_dict)
        reg = _get_registry(force=True)
        pipeline = GapFillPipeline(reg, allow_stub_fallback=allow_stub, use_llm=use_llm)
        report = pipeline.run(plan, target_root=target_root)

        bus.emit_widget("gap_fill_report", {
            "plan_name": report.plan_name,
            "gaps_total": report.gaps_total,
            "gaps_filled": report.gaps_filled,
            "gaps_stubbed": report.gaps_stubbed,
            "gaps_failed": report.gaps_failed,
            "materialized_path": report.materialized_path,
            "wire_verdict": report.wire_verdict,
            "final_verdict": report.final_verdict,
        }, run_id=run_id)
        bus.emit(AGUIEventType.TOOL_CALL_RESULT,
                 {"tool": "playground.synthesize", "verdict": report.final_verdict},
                 run_id=run_id)
        bus.emit(AGUIEventType.TOOL_CALL_END, {"tool": "playground.synthesize"}, run_id=run_id)
        _registry_cache["registry"] = None
        return report.to_dict()

    @app.post("/playground/hot-patch")
    def playground_hot_patch(body: dict = Body(default={})) -> dict:
        """Reload newly-materialized modules into the live Python process.

        Body:
          {"paths": ["a3_og_features/foo_feature.py", ...],
           "root": "<optional root; defaults to playground source dir>"}
        """
        from ass_ade.a3_og_features.hot_patch_runtime import hot_patch

        paths_raw = body.get("paths") if isinstance(body, dict) else None
        if not isinstance(paths_raw, list) or not paths_raw:
            raise HTTPException(status_code=400, detail="Missing 'paths' list in request body")
        root_raw = body.get("root") if isinstance(body, dict) else None
        root = Path(root_raw).resolve() if root_raw else _playground_source_dir()

        run_id = bus.new_run_id()
        bus.emit(AGUIEventType.TOOL_CALL_START,
                 {"tool": "playground.hot_patch", "paths": paths_raw}, run_id=run_id)

        report = hot_patch([Path(p) for p in paths_raw], root=root)

        counts = {"reloaded": 0, "imported": 0, "skipped_blocked": 0, "error": 0, "not_found": 0}
        for r in report.results:
            counts[r.status] = counts.get(r.status, 0) + 1

        bus.emit_widget("hot_patch_report", {
            "root": report.root,
            "requested_paths": list(report.requested_paths),
            "reloaded": counts["reloaded"],
            "imported": counts["imported"],
            "blocked": counts["skipped_blocked"],
            "errored": counts["error"] + counts["not_found"],
            "verdict": report.verdict,
        }, run_id=run_id)
        bus.emit(AGUIEventType.TOOL_CALL_RESULT,
                 {"tool": "playground.hot_patch", "verdict": report.verdict},
                 run_id=run_id)
        bus.emit(AGUIEventType.TOOL_CALL_END, {"tool": "playground.hot_patch"}, run_id=run_id)
        return report.to_dict()

    # ── Atomadic Copilot ───────────────────────────────────────────────────

    _copilot_cache: dict[str, Any] = {"copilot": None}

    def _get_copilot():
        from ass_ade.a3_og_features.atomadic_copilot import AtomadicCopilot

        if _copilot_cache["copilot"] is None:
            _copilot_cache["copilot"] = AtomadicCopilot(_get_registry())
        return _copilot_cache["copilot"]

    @app.post("/copilot/chat")
    def copilot_chat(body: dict = Body(default={})) -> dict:
        text = body.get("text") if isinstance(body, dict) else None
        if not isinstance(text, str) or not text.strip():
            raise HTTPException(status_code=400, detail="Missing 'text' in request body")

        run_id = bus.new_run_id()
        bus.emit_widget("copilot_message", {
            "role": "user", "text": text[:500], "mode": "input", "has_plan": False,
        }, run_id=run_id)

        copilot = _get_copilot()
        response = copilot.ask(text)

        bus.emit_widget("copilot_message", {
            "role": "assistant",
            "text": response.text[:2000],
            "mode": response.mode,
            "has_plan": response.suggested_plan is not None,
        }, run_id=run_id)
        return response.to_dict()

    @app.post("/copilot/critique")
    def copilot_critique(body: dict = Body(default={})) -> dict:
        plan = body.get("plan") if isinstance(body, dict) else None
        if not isinstance(plan, dict):
            raise HTTPException(status_code=400, detail="Missing 'plan' in request body")
        copilot = _get_copilot()
        response = copilot.critique_plan(plan)
        return response.to_dict()

    @app.post("/copilot/reset")
    def copilot_reset() -> dict:
        copilot = _get_copilot()
        copilot.reset()
        return {"ok": True}

    # ── Memory tab ─────────────────────────────────────────────────────────

    @app.get("/memory/personality")
    def memory_personality() -> dict:
        from ass_ade.a2_mo_composites.personality_engine import PersonalityEngine

        eng = PersonalityEngine.load()
        return {
            "persona": eng.persona,
            "verbosity": eng.verbosity,
            "use_emoji": eng.use_emoji,
            "domain_level": eng.domain_level,
        }

    class PersonaUpdate(BaseModel):
        persona: str

    @app.post("/memory/personality")
    def set_personality(body: PersonaUpdate) -> dict:
        from ass_ade.a2_mo_composites.personality_engine import PersonalityEngine

        eng = PersonalityEngine.load()
        ok = eng.set_persona(body.persona)
        bus.set_state("personality.persona", eng.persona)
        return {"ok": ok, "persona": eng.persona}

    @app.get("/memory/episodes")
    def memory_episodes() -> dict:
        from ass_ade.a2_mo_composites.episodic_memory import EpisodicStore

        store = EpisodicStore.load()
        return {
            "anchors": store.get_anchors(),
            "episodes": store._episodes[-60:],
        }

    class AnchorBody(BaseModel):
        key: str
        value: str

    @app.post("/memory/anchors")
    def add_anchor(body: AnchorBody) -> dict:
        from ass_ade.a2_mo_composites.episodic_memory import EpisodicStore

        store = EpisodicStore.load()
        store.add_anchor(body.key, body.value)
        bus.set_state(f"memory.anchors.{body.key}", body.value)
        return {"ok": True, "anchors": store.get_anchors()}

    @app.delete("/memory/anchors/{key}")
    def remove_anchor(key: str) -> dict:
        from ass_ade.a2_mo_composites.episodic_memory import EpisodicStore

        store = EpisodicStore.load()
        removed = store.remove_anchor(key)
        return {"ok": removed, "anchors": store.get_anchors()}

    # ── Skills tab ─────────────────────────────────────────────────────────

    @app.get("/skills")
    def skills() -> list[dict]:
        from ass_ade.a3_og_features.skill_runner import SkillRunner

        runner = SkillRunner(wdir)
        return runner.list_skills()

    class SkillInvocation(BaseModel):
        user_input: str

    @app.post("/skills/{name}/run")
    def run_skill(name: str, body: SkillInvocation) -> dict:
        from ass_ade.a3_og_features.skill_runner import SkillContext, SkillRunner

        runner = SkillRunner(wdir)
        skill = runner.get(name)
        if skill is None:
            raise HTTPException(status_code=404, detail=f"Skill '{name}' not found")

        run_id = bus.new_run_id()
        bus.emit(AGUIEventType.TOOL_CALL_START,
                 {"tool": f"skill:{name}", "input": body.user_input}, run_id=run_id)
        ctx = SkillContext(
            user_input=body.user_input,
            working_dir=wdir,
            tone="casual",
            domain_level="intermediate",
        )
        out = runner.run(skill, ctx)
        bus.emit(AGUIEventType.TOOL_CALL_RESULT,
                 {"tool": f"skill:{name}", "output": out[:20_000]}, run_id=run_id)
        bus.emit(AGUIEventType.TOOL_CALL_END, {"tool": f"skill:{name}"}, run_id=run_id)
        return {"run_id": run_id, "name": name, "output": out}

    return app
