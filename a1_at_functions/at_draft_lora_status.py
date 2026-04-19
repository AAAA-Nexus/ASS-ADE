# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_lora_status.py:5
# Component id: at.source.ass_ade.lora_status
__version__ = "0.1.0"

def lora_status(
    config: Path | None = CONFIG_OPTION,
) -> None:
    """Show LoRA flywheel contribution status and adapter health."""
    from ass_ade.agent.lora_flywheel import LoRAFlywheel, RG_LOOP

    _, settings = _resolve_config(config)
    nexus = None
    if settings.profile != "local":
        try:
            nexus = NexusClient(
                base_url=settings.nexus_base_url,
                timeout=settings.request_timeout_s,
                api_key=settings.nexus_api_key,
            ).__enter__()
        except Exception:
            pass

    flywheel = LoRAFlywheel(nexus=nexus)
    status = flywheel.status()

    t = Table(title="LoRA Flywheel Status")
    t.add_column("Metric")
    t.add_column("Value")
    t.add_row("Adapter version", status.adapter_version)
    t.add_row("Total contributions", str(status.contribution_count))
    t.add_row("  Fixes captured", str(status.fix_count))
    t.add_row("  Principles captured", str(status.principle_count))
    t.add_row("  Rejections captured", str(status.rejection_count))
    t.add_row("Ratchet epoch", f"{status.ratchet_epoch} / 7")
    t.add_row("Pending contributions", str(status.pending_count))
    t.add_row(f"Next batch (every {RG_LOOP} steps)", f"in {status.next_batch_step} steps")
    if status.quality_score > 0:
        t.add_row("Adapter quality", f"{status.quality_score:.2%}")

    # Fetch live reputation + Nexus credit balance (non-blocking)
    reputation: int | None = None
    credit_micro: int | None = None
    accepted_contributions: int | None = None
    if nexus is not None:
        try:
            claim = nexus.lora_reward_claim(agent_id=settings.agent_id)
            if isinstance(claim, dict):
                reputation = int(claim.get("reputation_earned", 0))
                credit_micro = int(claim.get("usdc_micro_payout", 0))  # legacy field = credit balance
                accepted_contributions = int(claim.get("accepted_contributions", 0))
        except Exception:
            pass

    if accepted_contributions is not None:
        t.add_row("Accepted by Nexus", str(accepted_contributions))
    if reputation is not None:
        t.add_row("Reputation earned", str(reputation))
    if credit_micro is not None:
        t.add_row("Nexus credit accrued", f"${credit_micro / 1_000_000:.6f} (discount against future API calls)")

    console.print(t)

    if credit_micro is not None and credit_micro > 0:
        console.print(
            "\n[green]✓[/green] Credit will auto-discount your next metered Nexus calls.\n"
            "[dim]Reward model: Nexus API-call credits today; on-chain USDC once Nexus is cash-positive.[/dim]"
        )
    elif status.ratchet_epoch == 0:
        console.print("\n[dim]Contribute fixes to earn Nexus API credit + advance the ratchet epoch.[/dim]")
    elif status.ratchet_epoch >= 7:
        console.print("\n[green]✓ Sovereign contributor status achieved.[/green]")
