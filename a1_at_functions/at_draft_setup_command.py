# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_setup_command.py:5
# Component id: at.source.ass_ade.setup_command
__version__ = "0.1.0"

def setup_command(
    reset: bool = typer.Option(False, help="Re-run setup even if config already exists."),
) -> None:
    """Interactive setup wizard — configure ASS-ADE in 60 seconds.

    Detects your environment, validates your API key, and writes
    .ass-ade/config.json with the right LLM router profile for your setup.

    Run once after install, or again with --reset to reconfigure.
    """
    import json as _json
    import subprocess as _sp

    console.print("\n[bold cyan]Welcome to ASS-ADE![/bold cyan]")
    console.print("[dim]Let's get you set up in 60 seconds.[/dim]\n")

    config_dir = Path.home() / ".ass-ade"
    config_file = config_dir / "config.json"
    if config_file.exists() and not reset:
        console.print(f"[green]✓[/green] Config already exists at {config_file}")
        console.print("[dim]Run with --reset to reconfigure.[/dim]")
        raise typer.Exit(code=0)

    # --- Detect environment ---
    py_ver = sys.version.split()[0]
    console.print(f"[dim]Python {py_ver}[/dim]")

    ollama_available = False
    try:
        r = _sp.run(["ollama", "list"], capture_output=True, timeout=3)
        ollama_available = r.returncode == 0
    except Exception:
        pass
    if ollama_available:
        console.print("[green]✓[/green] Ollama detected — local inference available")
    else:
        console.print("[dim]  Ollama not found — will use cloud/free-tier routing[/dim]")

    git_available = False
    try:
        r = _sp.run(["git", "--version"], capture_output=True, timeout=3)
        git_available = r.returncode == 0
    except Exception:
        pass

    ecosystem_root = os.environ.get("ATOMADIC_ECOSYSTEM_ROOT", "")
    if ecosystem_root and Path(ecosystem_root).exists():
        console.print(f"[green]✓[/green] Atomadic ecosystem root: {ecosystem_root}")
    else:
        console.print(
            "[yellow]![/yellow] ATOMADIC_ECOSYSTEM_ROOT not set.\n"
            "  [dim]Set it to enable the rebuild engine: export ATOMADIC_ECOSYSTEM_ROOT=/path/to/atomadic-ecosystem[/dim]"
        )

    console.print()

    # --- API key ---
    api_key = os.environ.get("AAAA_NEXUS_API_KEY", "")
    if api_key:
        console.print(f"[green]✓[/green] AAAA_NEXUS_API_KEY found in environment")
    else:
        console.print(
            "No AAAA_NEXUS_API_KEY found. You can:\n"
            "  [bold]a)[/bold] Enter a key now\n"
            "  [bold]b)[/bold] Press Enter to use the free tier (3 scans/day)\n"
            "  [bold]c)[/bold] Get a key at [link]https://atomadic.tech[/link]"
        )
        api_key = typer.prompt("API key (or blank for free tier)", default="", hide_input=True)

    # --- Use case ---
    console.print()
    console.print("[bold]What's your main use case?[/bold]")
    console.print("  [bold]1[/bold] Rebuild an existing repo into clean monadic structure")
    console.print("  [bold]2[/bold] Design a new feature or architecture blueprint")
    console.print("  [bold]3[/bold] Enhance and certify an existing project")
    console.print("  [bold]4[/bold] Use as MCP server (attach to Claude, Cursor, etc.)")
    choice = typer.prompt("Choice", default="1")
    use_case_map = {
        "1": "rebuild",
        "2": "design",
        "3": "enhance",
        "4": "mcp",
    }
    use_case = use_case_map.get(choice.strip(), "rebuild")

    # --- LLM profile ---
    profile = "local" if ollama_available else ("premium" if api_key else "free")

    # --- Write config ---
    config_dir.mkdir(parents=True, exist_ok=True)
    cfg: dict = {
        "profile": profile,
        "use_case": use_case,
        "ollama_available": ollama_available,
        "git_available": git_available,
        "ecosystem_root": ecosystem_root or None,
        "setup_complete": True,
    }
    if api_key:
        cfg["api_key_set"] = True
    config_file.write_text(_json.dumps(cfg, indent=2), encoding="utf-8")

    console.print(f"\n[green]✓[/green] Config written to [bold]{config_file}[/bold]")
    console.print(f"[dim]Profile: {profile} | Use case: {use_case}[/dim]")
    console.print()

    # --- Next step hint ---
    hints = {
        "rebuild": "ass-ade rebuild ./your-project ./clean-output",
        "design": "ass-ade design ./your-project",
        "enhance": "ass-ade enhance ./your-project",
        "mcp": "python -m ass_ade  # runs the MCP stdio server",
    }
    console.print(f"[bold]You're ready![/bold] Try: [cyan]{hints[use_case]}[/cyan]")
    console.print("[dim]Or run 'ass-ade tutorial' for an interactive 2-minute demo.[/dim]")
