# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a4_sy_orchestration/sy_draft_mcp_invoke.py:7
# Component id: sy.source.a4_sy_orchestration.mcp_invoke
from __future__ import annotations

__version__ = "0.1.0"

def mcp_invoke(
    identifier: str = typer.Argument(..., help="Tool name or index (1-based)."),
    input_file: Path | None = typer.Option(None, help="Path to JSON file to send as payload."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
    confirm_paid: bool = typer.Option(False, help="Confirm invocation of paid tools."),
    redact: bool = typer.Option(
        True,
        "--redact/--no-redact",
        help="Redact token, key, credential, and payment-proof fields in output.",
    ),
    dry_run: bool = typer.Option(False, "--dry-run",
                                 help="Simulate invocation without network I/O."),
    schema_validate: bool = typer.Option(False, "--schema-validate",
        help="Validate input payload against tool's JSON Schema if provided."),
    json_out: Path | None = typer.Option(None,
        help="Write full response payload as JSON to this path."),
) -> None:
    """Invoke a tool from the MCP manifest. Requires remote access to be enabled.

    Use `--dry-run` to simulate the invocation without performing network I/O.
    """
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    with NexusClient(
        base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key
    ) as client:
        manifest = client.get_mcp_manifest()

    tool = resolve_tool(manifest, identifier)
    if tool is None:
        console.print(f"Tool not found: {identifier}")
        raise typer.Exit(code=2)

    if bool(tool.paid) and not confirm_paid and not dry_run:
        console.print(
            "This tool appears to be paid. Re-run with --confirm-paid to proceed."
        )
        raise typer.Exit(code=3)

    payload = None
    if input_file is not None:
        if not input_file.exists():
            console.print(f"Input file not found: {input_file}")
            raise typer.Exit(code=4)
        try:
            payload = json.loads(input_file.read_text(encoding="utf-8"))
        except Exception as exc:
            console.print(f"Failed to parse input JSON: {exc}")
            raise typer.Exit(code=5)

    # Schema validation (if requested)
    if schema_validate:
        valid, err = validate_payload(getattr(tool, "inputSchema", None), payload)
        if not valid:
            console.print(f"Schema validation failed: {err}")
            raise typer.Exit(code=7)

    if dry_run:
        sim = simulate_invoke(settings.nexus_base_url, tool, payload)
        _print_json(sim)
        if json_out is not None:
            json_out.parent.mkdir(parents=True, exist_ok=True)
            json_out.write_text(f"{json.dumps(sim, indent=2)}\n", encoding="utf-8")
            console.print(f"Wrote simulation to {json_out}")
        return

    try:
        response = invoke_tool(
            settings.nexus_base_url,
            tool,
            payload,
            timeout=settings.request_timeout_s,
            api_key=settings.nexus_api_key,
        )
        response.raise_for_status()
    except httpx.HTTPError as exc:
        console.print(f"Invocation failed: {exc}")
        raise typer.Exit(code=6) from exc

    # Try to pretty-print JSON, otherwise raw text
    try:
        body = response.json()
        rendered_body = _redact_secrets(body) if redact else body
        _print_json(rendered_body)
        if json_out is not None:
            json_out.parent.mkdir(parents=True, exist_ok=True)
            json_out.write_text(f"{json.dumps(rendered_body, indent=2)}\n", encoding="utf-8")
            console.print(f"Wrote response to {json_out}")
    except (json.JSONDecodeError, ValueError):
        console.print(response.text)
