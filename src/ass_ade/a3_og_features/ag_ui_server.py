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

import asyncio
import io
import sys
import traceback
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from typing import Any


def build_app(working_dir: Path | None = None):
    """Build the FastAPI app. Imports FastAPI lazily so the module imports
    cleanly even when the 'ui' extra is not installed."""
    try:
        from fastapi import FastAPI, HTTPException
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
