# Extracted from C:/!ass-ade/src/ass_ade/cli.py:6265
# Component id: at.source.ass_ade.certify_command
from __future__ import annotations

__version__ = "0.1.0"

def certify_command(
    path: Path = typer.Argument(Path("."), help="Folder to certify."),
    config: Path | None = CONFIG_OPTION,
    version: str | None = typer.Option(None, help="Version string to embed in the certificate."),
    out: Path | None = typer.Option(None, help="Write CERTIFICATE.json to this path."),
    local_only: bool = typer.Option(
        False,
        help="Generate a local-only unsigned certificate (not verifiable by third parties).",
    ),
    allow_remote: bool = typer.Option(
        False,
        help="Force remote signing even in local profile.",
    ),
    json_out: bool = typer.Option(False, "--json", help="Print certificate as JSON."),
) -> None:
    """Generate a tamper-evident certificate for any codebase.

    Local step: walks the codebase, computes SHA-256 digests of all source
    files, bundles them into a CERTIFICATE.json payload.

    Remote step: sends the local digest to atomadic.tech for PQC signing.
    A certificate is only third-party verifiable when server-signed. Free tier:
    3 calls/day. Paid: x402 USDC or API key.

    Every certification result is captured by the LoRA flywheel.

    Examples:
        ass-ade certify .
        ass-ade certify . --version 1.2.0 --allow-remote
        ass-ade certify ~/myproject --local-only --out CERTIFICATE.json
    """
    import datetime as _dt
    from ass_ade.local.certifier import build_local_certificate, render_certificate_text

    _, settings = _resolve_config(config)
    target = path.resolve()
    if not target.exists():
        console.print(f"[red]Path does not exist:[/red] {target}")
        raise typer.Exit(code=1)

    console.print(f"[bold]Certifying[/bold] {target}")
    cert = build_local_certificate(target, version=version)

    use_remote = not local_only and _should_probe_remote(settings, allow_remote if allow_remote else None)

    if use_remote:
        try:
            with NexusClient(
                base_url=settings.nexus_base_url,
                api_key=settings.nexus_api_key,
                agent_id=str(settings.agent_id) if settings.agent_id else None,
                timeout=60.0,
            ) as nx:
                console.print("[dim]Sending to atomadic.tech for PQC signing…[/dim]")
                result = nx.certify_codebase(
                    local_certificate=cert,
                    agent_id=str(settings.agent_id) if settings.agent_id else None,
                )
                if result.ok and result.signature:
                    cert["signed_by"] = result.signed_by
                    cert["signature"] = result.signature
                    cert["valid"] = result.valid
                    cert["issued_at"] = result.issued_at
                    console.print("[green][OK][/green] Certificate signed by atomadic.tech")
                    if result.lora_captured:
                        console.print("[dim]LoRA flywheel: sample captured.[/dim]")
        except Exception as exc:
            exc_str = str(exc)
            if "402" in exc_str:
                console.print("[yellow]Remote signing requires credits.[/yellow]")
                console.print(
                    "[dim]Get credits at [bold]https://atomadic.tech/pay[/bold] "
                    "then set [bold]AAAA_NEXUS_API_KEY[/bold] in your .env file.[/dim]"
                )
            elif "401" in exc_str or "403" in exc_str:
                console.print(
                    "[yellow]Remote signing failed — API key invalid or missing.[/yellow]"
                )
                console.print(
                    "[dim]Set [bold]AAAA_NEXUS_API_KEY=your_key[/bold] in your project .env file "
                    "([bold]C:\\!ass-ade\\.env[/bold]).[/dim]"
                )
            else:
                console.print(f"[yellow]Remote signing unavailable:[/yellow] {exc}")
            console.print("[dim]Certificate written as local-only (not third-party verifiable).[/dim]")

    cert_path = out or (target / "CERTIFICATE.json")
    import json as _json
    cert_path.write_text(_json.dumps(cert, indent=2, default=str), encoding="utf-8")
    console.print(f"\n[green][OK][/green] Certificate written: {cert_path}")

    if json_out:
        _print_json(cert)
        return

    console.print()
    console.print(render_certificate_text(cert))

    if not cert.get("valid"):
        console.print(
            "\n[yellow]Note:[/yellow] Certificate is not server-signed. "
            "Use --allow-remote or set profile=hybrid/premium for a verifiable certificate."
        )
