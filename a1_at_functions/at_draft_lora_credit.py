# Extracted from C:/!ass-ade/src/ass_ade/cli.py:6588
# Component id: at.source.ass_ade.lora_credit
from __future__ import annotations

__version__ = "0.1.0"

def lora_credit(
    config: Path | None = CONFIG_OPTION,
) -> None:
    """Show accrued Nexus credit balance (auto-applied on paid calls)."""
    _, settings = _resolve_config(config)
    if settings.profile == "local":
        console.print("[yellow]Local profile — credit is earned/applied in hybrid or premium mode.[/yellow]")
        return
    try:
        with NexusClient(
            base_url=settings.nexus_base_url,
            timeout=settings.request_timeout_s,
            api_key=settings.nexus_api_key,
            agent_id=settings.agent_id,
        ) as client:
            balance = client.lora_credit_balance(agent_id=settings.agent_id)
            claim = client.lora_reward_claim(agent_id=settings.agent_id)
    except Exception as exc:
        console.print(f"[red]Error:[/red] {exc}")
        return
    t = Table(title=f"Nexus Credit — {settings.agent_id}")
    t.add_column("Metric")
    t.add_column("Value")
    t.add_row("Accepted contributions", str(claim.get("accepted_contributions", 0)))
    t.add_row("Reputation earned", str(claim.get("reputation_earned", 0)))
    t.add_row(
        "Credit balance",
        f"${balance.get('balance_usdc', '0.000000')} "
        f"({balance.get('balance_micro_usdc', 0)} micro-USDC)",
    )
    t.add_row("Reward model", str(balance.get("reward_model", "nexus_api_credit")))
    console.print(t)
    console.print(
        "\n[dim]Balance is auto-deducted on paid calls when X-Agent-Id is set (handled by ass-ade automatically).[/dim]"
    )
