# Extracted from C:/!ass-ade/src/ass_ade/cli.py:6696
# Component id: at.source.ass_ade.setup_command
from __future__ import annotations

__version__ = "0.1.0"

def setup_command(
    reset: bool = typer.Option(False, help="Re-run setup even if config already exists."),
    global_config: bool = typer.Option(
        False, "--global", help="Write config to ~/.ass-ade/config.json instead of the project root."
    ),
) -> None:
    """Interactive setup wizard — configure ASS-ADE in under 60 seconds.

    Prompts for API keys, profile, output path, and evolution mode.
    Saves keys to .env and config to .ass-ade/config.json.

    Run once after install, or with --reset to reconfigure.
    """
    import json as _json
    import subprocess as _sp

    # ── Welcome ────────────────────────────────────────────────────────────────
    console.print("\n[bold cyan]Welcome to ASS-ADE[/bold cyan]")
    console.print(
        "[dim]Autonomous Sovereign System: Atomadic Development Environment — "
        "the CLI that rebuilds, documents, and certifies any codebase.[/dim]\n"
    )

    config_path = (Path.home() / ".ass-ade" / "config.json") if global_config else default_config_path()
    env_path = (Path.home() / ".ass-ade" / ".env") if global_config else (Path.cwd() / ".env")

    if config_path.exists() and not reset:
        console.print(f"[green]✓[/green] Config already exists at [bold]{config_path}[/bold]")
        console.print("[dim]Run with --reset to reconfigure.[/dim]")
        raise typer.Exit(code=0)

    # ── Step 1: API Keys ──────────────────────────────────────────────────────
    console.print("[bold]Step 1/5 — API Keys[/bold]")
    console.print(
        "[dim]Optional. ASS-ADE works without keys (3 free calls/day). "
        "Keys unlock remote signing, lint synthesis, and the LoRA flywheel.[/dim]\n"
    )

    # Load existing .env values
    existing_env: dict[str, str] = {}
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                existing_env[k.strip()] = v.strip()

    def _prompt_key(env_var: str, label: str) -> str:
        current = os.getenv(env_var) or existing_env.get(env_var, "")
        if current:
            console.print(f"  [green]✓[/green] {env_var} already set")
            return current
        val = typer.prompt(
            f"  {label}", default="", show_default=False, hide_input=True,
            prompt_suffix=" (Enter to skip): "
        )
        return val.strip()

    nexus_key = _prompt_key("AAAA_NEXUS_API_KEY", "AAAA Nexus API key (remote signing + synthesis)")
    groq_key = _prompt_key("GROQ_API_KEY", "Groq API key (fast LLM for interpreter)")
    gemini_key = _prompt_key("GEMINI_API_KEY", "Gemini API key (fallback LLM)")

    # Write keys to .env (merge with existing, preserve comments)
    new_env_lines: list[str] = []
    existing_raw = env_path.read_text(encoding="utf-8").splitlines() if env_path.exists() else []
    written_keys: set[str] = set()
    for line in existing_raw:
        stripped = line.strip()
        if stripped.startswith("#") or not stripped:
            new_env_lines.append(line)
            continue
        if "=" in stripped:
            k = stripped.split("=", 1)[0].strip()
            if k == "AAAA_NEXUS_API_KEY" and nexus_key:
                new_env_lines.append(f"AAAA_NEXUS_API_KEY={nexus_key}")
                written_keys.add(k)
            elif k == "GROQ_API_KEY" and groq_key:
                new_env_lines.append(f"GROQ_API_KEY={groq_key}")
                written_keys.add(k)
            elif k == "GEMINI_API_KEY" and gemini_key:
                new_env_lines.append(f"GEMINI_API_KEY={gemini_key}")
                written_keys.add(k)
            else:
                new_env_lines.append(line)
        else:
            new_env_lines.append(line)
    # Append any new keys not already in .env
    for key, val in [
        ("AAAA_NEXUS_API_KEY", nexus_key),
        ("GROQ_API_KEY", groq_key),
        ("GEMINI_API_KEY", gemini_key),
    ]:
        if val and key not in written_keys:
            new_env_lines.append(f"{key}={val}")
    if any(k for k in (nexus_key, groq_key, gemini_key)):
        env_path.parent.mkdir(parents=True, exist_ok=True)
        env_path.write_text("\n".join(new_env_lines) + "\n", encoding="utf-8")
        console.print(f"\n  [green]✓[/green] Keys saved to [bold]{env_path}[/bold]")
    else:
        console.print("  [dim]No keys entered — using free tier (3 calls/day per endpoint).[/dim]")

    # ── Step 2: Profile ────────────────────────────────────────────────────────
    console.print("\n[bold]Step 2/5 — Profile[/bold]")
    console.print("  [bold]1[/bold]  Local   — free, all core features, no remote calls")
    console.print("  [bold]2[/bold]  Hybrid  — local + Nexus API for signing & synthesis  [dim](recommended if you have a key)[/dim]")
    console.print("  [bold]3[/bold]  Premium — full cloud pipeline")
    default_profile_num = "2" if nexus_key else "1"
    profile_choice = typer.prompt("  Profile", default=default_profile_num)
    profile_map = {"1": "local", "2": "hybrid", "3": "premium"}
    profile = profile_map.get(profile_choice.strip(), "local")
    console.print(f"  [green]✓[/green] Profile: [bold]{profile}[/bold]")

    # ── Step 3: Default output path ───────────────────────────────────────────
    console.print("\n[bold]Step 3/5 — Default rebuild output location[/bold]")
    console.print("  [bold]1[/bold]  Sibling folder  — ../project-rebuilt-{timestamp}  [dim](default)[/dim]")
    console.print("  [bold]2[/bold]  Custom path     — enter a path below")
    out_choice = typer.prompt("  Output location", default="1")
    rebuild_output_strategy = "sibling"
    rebuild_output_path: str | None = None
    if out_choice.strip() == "2":
        custom = typer.prompt("  Custom path", default="./rebuilt")
        rebuild_output_path = custom.strip()
        rebuild_output_strategy = "custom"
    console.print(f"  [green]✓[/green] Output: [bold]{rebuild_output_path or 'sibling of source'}[/bold]")

    # ── Step 4: Evolution mode ────────────────────────────────────────────────
    console.print("\n[bold]Step 4/5 — Evolution mode[/bold]")
    console.print("  [bold]1[/bold]  Single track  — linear evolution on main branch  [dim](default)[/dim]")
    console.print("  [bold]2[/bold]  Dual track    — parallel branches, merge later  [dim](good for big refactors)[/dim]")
    evo_choice = typer.prompt("  Evolution mode", default="1")
    evolution_mode = "dual" if evo_choice.strip() == "2" else "single"
    console.print(f"  [green]✓[/green] Evolution: [bold]{evolution_mode} track[/bold]")

    # ── Step 5: Write config ───────────────────────────────────────────────────
    console.print("\n[bold]Step 5/5 — Saving configuration[/bold]")
    config_path.parent.mkdir(parents=True, exist_ok=True)
    from ass_ade.config import AssAdeConfig, write_default_config
    write_default_config(config_path)

    import json as _json
    cfg_data = _json.loads(config_path.read_text(encoding="utf-8"))
    cfg_data["profile"] = profile
    cfg_data["evolution_mode"] = evolution_mode
    if rebuild_output_strategy == "custom" and rebuild_output_path:
        cfg_data["rebuild_output_path"] = rebuild_output_path
    config_path.write_text(_json.dumps(cfg_data, indent=2), encoding="utf-8")
    console.print(f"  [green]✓[/green] Config written to [bold]{config_path}[/bold]")

    # ── Summary ────────────────────────────────────────────────────────────────
    console.print("\n[bold]Setup complete![/bold]")
    t = Table(show_header=False, box=None)
    t.add_column(style="dim", width=22)
    t.add_column()
    t.add_row("Profile", f"[bold]{profile}[/bold]")
    t.add_row("Evolution", evolution_mode)
    t.add_row("Output", rebuild_output_path or "sibling of source")
    t.add_row("Nexus key", "[green]set[/green]" if nexus_key else "[dim]not set[/dim]")
    t.add_row("Groq key", "[green]set[/green]" if groq_key else "[dim]not set[/dim]")
    t.add_row("Gemini key", "[green]set[/green]" if gemini_key else "[dim]not set[/dim]")
    console.print(t)

    # ── Auto-run doctor ────────────────────────────────────────────────────────
    console.print("\n[dim]Running environment check (ass-ade doctor)...[/dim]\n")
    try:
        import subprocess as _sp
        _sp.run([sys.executable, "-m", "ass_ade", "doctor"], check=False)
    except Exception as exc:
        console.print(f"[yellow]doctor check skipped:[/yellow] {exc}")

    console.print(
        "\n[dim]Next: run [bold]ass-ade chat[/bold] to start talking to Atomadic, "
        "or [bold]ass-ade enhance .[/bold] to scan this project.[/dim]"
    )
