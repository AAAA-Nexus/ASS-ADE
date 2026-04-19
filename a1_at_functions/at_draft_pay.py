# Extracted from C:/!ass-ade/src/ass_ade/cli.py:3678
# Component id: at.source.ass_ade.pay
from __future__ import annotations

__version__ = "0.1.0"

def pay(
    endpoint: str = typer.Argument(..., help="Endpoint to call (e.g. /v1/trust/score)."),
    body: str = typer.Option("{}", help="JSON body for the request."),
    auto_confirm: bool = typer.Option(False, "--auto-confirm", help="Skip payment consent prompt."),
    config: Path | None = CONFIG_OPTION,
) -> None:
    """Demonstrate x402 autonomous payment flow on Base L2.

    Calls an endpoint, and if it returns 402 Payment Required, parses
    the x402 challenge, shows the cost, and (with consent) submits
    USDC payment on-chain then retries with the payment proof.

    Testnet mode: export ATOMADIC_X402_TESTNET=1
    Wallet key:   export ATOMADIC_WALLET_KEY=<hex-private-key>
    """
    from ass_ade.nexus.x402 import (
        PaymentChallenge,
        format_payment_consent,
        get_chain_config,
        submit_payment,
        build_payment_header,
    )

    _, settings = _resolve_config(config)
    chain = get_chain_config()

    console.print(f"[bold]x402 Payment Demo[/bold] — {chain['network_name']}")
    console.print(f"Calling: {settings.nexus_base_url}{endpoint}")
    console.print()

    try:
        req_body = json.loads(body)
    except json.JSONDecodeError as exc:
        console.print("[red]Invalid JSON body[/red]")
        raise typer.Exit(code=1) from exc

    # Step 1: Make the request
    with NexusClient(
        base_url=settings.nexus_base_url,
        timeout=settings.request_timeout_s,
        api_key=settings.nexus_api_key,
    ) as client:
        post_with_x402 = getattr(client, "_post_with_x402", None) or client.post_with_x402
        result = post_with_x402(endpoint, req_body)

    # Step 2: Check if payment is required
    if not result.get("payment_required"):
        console.print("[green]No payment required — endpoint returned 200[/green]")
        _print_json(result)
        return

    # Step 3: Parse challenge
    challenge = result.get("challenge")
    if not challenge:
        # Fallback: parse from raw for backward compat
        challenge = PaymentChallenge.from_response(result.get("raw", result))
    console.print(format_payment_consent(challenge))
    console.print()

    # Step 4: Get consent
    if not auto_confirm:
        confirm = typer.confirm("Proceed with payment?")
        if not confirm:
            console.print("[yellow]Payment cancelled.[/yellow]")
            raise typer.Exit(code=0)

    # Step 5: Submit payment
    console.print("[bold]Submitting payment...[/bold]")
    payment = submit_payment(challenge)

    if not payment.success:
        console.print(f"[red]Payment failed:[/red] {payment.error}")
        raise typer.Exit(code=1)

    console.print(f"[green]Payment submitted![/green] txid: {payment.txid}")
    if payment.testnet:
        console.print(f"[dim]View on BaseScan: https://sepolia.basescan.org/tx/0x{payment.txid}[/dim]")
    else:
        console.print(f"[dim]View on BaseScan: https://basescan.org/tx/0x{payment.txid}[/dim]")

    # Step 6: Retry with payment proof
    console.print("[bold]Retrying with payment proof...[/bold]")
    headers = build_payment_header(payment)
    try:
        with NexusClient(
            base_url=settings.nexus_base_url,
            timeout=settings.request_timeout_s,
            api_key=settings.nexus_api_key,
        ) as client:
            response = client.request_with_payment_headers(endpoint, req_body, payment_headers=headers)
            if response.status_code == 200:
                console.print("[green]Paid request successful![/green]")
                _print_json(response.json())
            else:
                console.print(f"[red]Retry returned {response.status_code}[/red]")
                console.print(response.text)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
