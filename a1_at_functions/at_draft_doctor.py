# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/cli.py:353
# Component id: at.source.ass_ade.doctor
__version__ = "0.1.0"

def doctor(
    config: Path | None = CONFIG_OPTION,
    remote: bool | None = REMOTE_PROBE_OPTION,
    json_out: bool = typer.Option(False, "--json", help="Print result as JSON."),
) -> None:
    config_path, settings = _resolve_config(config)
    probe_remote = _should_probe_remote(settings, remote)

    tool_items = collect_tool_status()
    health_data: dict | None = None

    if not json_out:
        summary = Table(title="ASS-ADE Environment")
        summary.add_column("Setting")
        summary.add_column("Value")
        summary.add_row("Config", str(config_path))
        summary.add_row("Profile", settings.profile)
        summary.add_row("Nexus Base URL", settings.nexus_base_url)
        summary.add_row("Remote Probe", "enabled" if probe_remote else "disabled")
        console.print(summary)

        tools = Table(title="Toolchain")
        tools.add_column("Tool")
        tools.add_column("Status")
        tools.add_column("Version / Error")
        for item in tool_items:
            tools.add_row(
                item.name,
                "ok" if item.available else "missing",
                item.version or item.error or "",
            )
        console.print(tools)

    if probe_remote:
        try:
            with NexusClient(
                base_url=settings.nexus_base_url,
                timeout=settings.request_timeout_s,
                api_key=settings.nexus_api_key,
            ) as client:
                health = client.get_health()
                health_data = health.model_dump() if hasattr(health, "model_dump") else dict(health)
        except httpx.HTTPError as exc:
            if not json_out:
                console.print(f"Remote probe failed: {exc}")
            else:
                _print_json({"error": str(exc), "remote_probe": "failed"})
            raise typer.Exit(code=1) from exc

        if not json_out:
            console.print("Remote probe succeeded.")
            _print_json(health_data)

    if json_out:
        payload: dict = {
            "config": str(config_path),
            "profile": settings.profile,
            "nexus_base_url": settings.nexus_base_url,
            "remote_probe": "enabled" if probe_remote else "disabled",
            "tools": [
                {
                    "name": item.name,
                    "available": item.available,
                    "version": item.version,
                    "error": item.error,
                }
                for item in tool_items
            ],
        }
        if health_data is not None:
            payload["remote_health"] = health_data
        print(json.dumps(payload, indent=2))
