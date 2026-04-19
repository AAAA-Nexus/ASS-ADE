# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_pipeline_certify.py:7
# Component id: at.source.a1_at_functions.pipeline_certify
from __future__ import annotations

__version__ = "0.1.0"

def pipeline_certify(
    text: str = typer.Argument(..., help="Text to certify."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
    persist: bool = typer.Option(False, help="Persist results to .ass-ade/workflows/"),
    json_out: bool = typer.Option(False, "--json", help="Output raw JSON."),
) -> None:
    """Run the certification pipeline: hallucination → ethics → compliance → certify."""
    from ass_ade.pipeline import certify_pipeline

    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)

    persist_dir = str(Path(".ass-ade/workflows")) if persist else None

    def _progress(name: str, status: Any, current: int, total: int) -> None:
        console.print(f"  [{current}/{total}] {name}: {status.value}")

    with NexusClient(
        base_url=settings.nexus_base_url,
        timeout=settings.request_timeout_s,
        api_key=settings.nexus_api_key,
    ) as client:
        pipe = certify_pipeline(
            client, text, on_progress=_progress, persist_dir=persist_dir
        )
        result = pipe.run()

    if json_out:
        _print_json({
            "name": result.name,
            "passed": result.passed,
            "duration_ms": result.duration_ms,
            "steps": [
                {"name": s.name, "status": s.status.value, "output": s.output, "error": s.error}
                for s in result.steps
            ],
        })
    else:
        verdict = "[green]PASSED[/green]" if result.passed else "[red]FAILED[/red]"
        console.print(f"${verdict} — {result.summary}")
