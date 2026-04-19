# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_pipeline_run.py:7
# Component id: at.source.a1_at_functions.pipeline_run
from __future__ import annotations

__version__ = "0.1.0"

def pipeline_run(
    pipeline_type: Annotated[str, typer.Argument(help="Type (trust-gate, certify).")],
    input_value: Annotated[str, typer.Argument(help="Input value.")],
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
    persist: Annotated[bool, typer.Option(help="Persist to .ass-ade/workflows/")] = True,
) -> None:
    from ass_ade.pipeline import trust_gate_pipeline, certify_pipeline, StepStatus

    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)

    persist_dir = ".ass-ade/workflows" if persist else None

    def on_progress(name: str, status: StepStatus, current: int, total: int) -> None:
        color = "green" if status == StepStatus.PASSED else "red"
        if status == StepStatus.RUNNING:
            color = "yellow"
        console.print(f"[{current}/{total}] {name}: [{color}]{status.value}[/{color}]")

    try:
        with NexusClient(
            base_url=settings.nexus_base_url,
            timeout=settings.request_timeout_s,
            api_key=settings.nexus_api_key,
        ) as client:
            if pipeline_type == "trust-gate":
                pipe = trust_gate_pipeline(
                    client, input_value, on_progress=on_progress, persist_dir=persist_dir
                )
            elif pipeline_type == "certify":
                pipe = certify_pipeline(
                    client, input_value, on_progress=on_progress, persist_dir=persist_dir
                )
            else:
                console.print(f"[red]Unknown type:[/red] {pipeline_type}")
                raise typer.Exit(code=1)

            console.print(f"[bold blue]Running pipeline: {pipe.name}[/bold blue]\n")
            result = pipe.run()
            console.print(f"\n[bold]{result.summary}[/bold]")

    except Exception as exc:
        if isinstance(exc, httpx.HTTPError):
            _nexus_err(exc)
        else:
            console.print(f"[red]Error:[/red] {exc}")
            raise typer.Exit(code=1) from exc
