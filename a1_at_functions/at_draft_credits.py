# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/cli.py:428
# Component id: at.source.ass_ade.credits
__version__ = "0.1.0"

def credits(
    config: Path | None = CONFIG_OPTION,
) -> None:
    """Show your API credit balance and usage, with quick buy links."""
    _, settings = _resolve_config(config)

    if not settings.nexus_api_key:
        console.print("[bold yellow]No API key configured.[/bold yellow]\n")
        console.print(_CREDITS_BUY_MESSAGE)
        raise typer.Exit(code=0)

    try:
        with NexusClient(
            base_url=settings.nexus_base_url,
            timeout=settings.request_timeout_s,
            api_key=settings.nexus_api_key,
        ) as client:
            result = client._client.get("/v1/credits/balance")
            result.raise_for_status()
            data = result.json()
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code in (401, 402):
            console.print("[red]Authentication failed.[/red]\n")
            console.print(_CREDITS_BUY_MESSAGE)
        else:
            console.print(f"[red]Error checking balance:[/red] {exc}")
        raise typer.Exit(code=1) from exc
    except Exception as exc:
        console.print(f"[red]Error checking balance:[/red] {exc}")
        raise typer.Exit(code=1) from exc

    t = Table(title="API Credits")
    t.add_column("Field")
    t.add_column("Value")
    balance_keys = {"balance", "balance_usdc", "balance_micro_usdc", "plan", "calls_remaining"}
    for k, v in data.items():
        if str(k).lower() in balance_keys or not balance_keys.isdisjoint({str(k).lower()}):
            t.add_row(str(k), str(v))
        else:
            t.add_row(str(k), str(v))
    console.print(t)

    # Rewards section
    accepted = data.get("lora_contributions_accepted", data.get("contributions_accepted"))
    quality = data.get("quality_score", data.get("trust_score"))
    next_tier = data.get("next_reward_tier")
    if accepted is not None or quality is not None:
        r = Table(title="LoRA Contribution Rewards")
        r.add_column("Metric")
        r.add_column("Value")
        if accepted is not None:
            earned = int(accepted) * 2
            r.add_row("Contributions accepted", f"{accepted} (earned {earned} bonus credits)")
        if quality is not None:
            r.add_row("Quality score", f"{quality} (trust gate: ≥ τ_trust)")
        if next_tier is not None:
            r.add_row("Next reward tier", f"{next_tier} more accepted contributions")
        console.print(r)
        console.print("[dim]Top contributors with consistently high quality get unlimited access.[/dim]")

    console.print("\nTop up at [cyan]https://atomadic.tech/pay[/cyan]")
