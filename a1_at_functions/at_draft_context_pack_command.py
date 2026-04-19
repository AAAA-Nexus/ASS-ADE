# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/cli.py:3325
# Component id: at.source.ass_ade.context_pack_command
__version__ = "0.1.0"

def context_pack_command(
    task_description: str = typer.Argument(..., help="Task the context packet should support."),
    file: list[str] = typer.Option([], "--file", help="Repo-relative file to include."),
    source: list[str] = typer.Option([], "--source", help="Official source URL already researched."),
    path: Path = REPO_PATH_OPTION,
    max_files: int = typer.Option(12, help="Maximum files to include."),
    max_bytes_per_file: int = typer.Option(4000, help="Maximum bytes of excerpt per file."),
    json_out: bool = typer.Option(False, "--json", help="Output raw JSON."),
) -> None:
    """Build a compact context packet from repo files and source URLs."""
    from ass_ade.context_memory import build_context_packet

    packet = build_context_packet(
        task_description=task_description,
        working_dir=path,
        file_paths=file or None,
        source_urls=source,
        max_files=max_files,
        max_bytes_per_file=max_bytes_per_file,
    )

    if json_out:
        _print_json(packet.model_dump(), redact=True)
        return

    color = "green" if packet.recon_verdict == "READY_FOR_PHASE_1" else "yellow"
    console.print(f"[{color}]Context Packet: {packet.recon_verdict}[/{color}]")
    console.print(f"Sources: {len(packet.source_urls)}")
    console.print(f"Files: {len(packet.files)}")
    for item in packet.files:
        mark = " truncated" if item.truncated else ""
        console.print(f"  - {item.path} ({item.size_bytes} bytes{mark})")
    if packet.warnings:
        console.print("[bold]Warnings:[/bold]")
        for warning in packet.warnings:
            console.print(f"  - {warning}")
