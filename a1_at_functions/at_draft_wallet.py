# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/cli.py:3778
# Component id: at.source.ass_ade.wallet
__version__ = "0.1.0"

def wallet(
    config: Path | None = CONFIG_OPTION,
) -> None:
    """Show x402 wallet status and chain configuration."""
    import os
    from ass_ade.nexus.x402 import get_chain_config

    _resolve_config(config)
    chain = get_chain_config()
    wallet_key = os.environ.get("ATOMADIC_WALLET_KEY", "")
    has_wallet = bool(wallet_key)

    table = Table(title="x402 Wallet Status")
    table.add_row("Network", chain["network_name"])
    table.add_row("Chain ID", str(chain["chain_id"]))
    table.add_row("RPC", chain["rpc_url"])
    table.add_row("USDC Contract", chain["usdc_address"])
    table.add_row("Treasury", chain["treasury"])
    table.add_row("Wallet Key", "[green]Set[/green]" if has_wallet else "[red]Not set (export ATOMADIC_WALLET_KEY)[/red]")
    table.add_row("Testnet Mode", "[green]ON[/green]" if chain["testnet"] else "[yellow]OFF (mainnet)[/yellow]")

    if has_wallet:
        try:
            account_module = importlib.import_module("eth_account")
            Account = account_module.Account
            acct = Account.from_key(wallet_key)
            table.add_row("Wallet Address", acct.address)
        except ImportError:
            table.add_row("Wallet Address", "[dim]Install web3: pip install web3 eth-account[/dim]")
        except Exception as e:
            table.add_row("Wallet Address", f"[red]Error: {e}[/red]")

    console.print(table)
