"""Tier a2 — assimilated method 'MCPServer._call_epiphany_breakthrough_cycle'

Assimilated from: server.py:1166-1247
"""

from __future__ import annotations


# --- assimilated symbol ---
def _call_epiphany_breakthrough_cycle(
    self,
    req_id: Any,
    args: dict[str, Any],
    token: Any = None,
    cancellation_context: CancellationContext | None = None,
) -> dict[str, Any]:
    task_description = str(args.get("task_description", "")).strip()
    if not task_description:
        return self._error(req_id, -32602, "task_description is required")

    observations = args.get("observations") or []
    if not isinstance(observations, list):
        return self._error(req_id, -32602, "observations must be an array")
    obs_texts = [str(x) for x in observations if str(x).strip()]

    provided_sources = args.get("provided_sources") or []
    if not isinstance(provided_sources, list):
        return self._error(req_id, -32602, "provided_sources must be an array")

    run_phase0 = bool(args.get("run_phase0", True))
    try:
        max_relevant_files = int(args.get("max_relevant_files", 16))
    except (TypeError, ValueError):
        return self._error(req_id, -32602, "max_relevant_files must be an integer")

    self._emit_progress(
        token, 0.0, message="Composing Epiphany → Breakthrough cycle document..."
    )
    if cancellation_context and cancellation_context.check():
        return self._error(req_id, -32800, "Request cancelled")

    recon_verdict: str | None = None
    recon_files: list[str] = []
    recon_failed = False
    if run_phase0:
        self._emit_progress(token, 0.2, message="Running Phase 0 recon...")
        from ass_ade.recon import phase0_recon

        pr = phase0_recon(
            task_description=task_description,
            working_dir=self._working_dir,
            provided_sources=[str(s) for s in provided_sources],
            max_relevant_files=max_relevant_files,
        )
        recon_verdict = pr.verdict
        recon_files = list(pr.codebase.relevant_files)
        recon_failed = pr.verdict == "RECON_REQUIRED"

    self._emit_progress(token, 0.65, message="Building planner + cycle JSON...")
    from ass_ade.engine.rebuild.epiphany_cycle import (
        build_epiphany_document,
        detect_track_and_steps,
        validate_epiphany_document,
    )

    track, _base = detect_track_and_steps(task_description)
    intro = f"Define success criteria for: {task_description}"
    plan_steps = [intro, *_base]

    doc: dict[str, object] = build_epiphany_document(
        task_description,
        track=track,
        plan_steps=plan_steps,
        recon_verdict=recon_verdict,
        recon_files=recon_files,
        observations=obs_texts,
    )
    val_errs = validate_epiphany_document(doc)
    if val_errs:
        doc["validation_errors"] = val_errs

    self._emit_progress(token, 1.0, message="Epiphany → Breakthrough document ready.")
    text = json.dumps(doc, indent=2)
    is_error = recon_failed or bool(val_errs)
    return self._result(
        req_id,
        {
            "content": [{"type": "text", "text": text}],
            "isError": is_error,
        },
    )

