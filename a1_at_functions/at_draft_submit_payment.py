# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_submit_payment.py:7
# Component id: at.source.a1_at_functions.submit_payment
from __future__ import annotations

__version__ = "0.1.0"

def submit_payment(challenge: PaymentChallenge) -> PaymentResult:
    """Submit a USDC payment on Base to fulfill an x402 challenge.

    Requires ATOMADIC_WALLET_KEY environment variable with the sender's
    private key (hex, without 0x prefix).

    For testnet: set ATOMADIC_X402_TESTNET=1

    Returns PaymentResult with txid and signature header on success.
    """
    wallet_key = os.environ.get("ATOMADIC_WALLET_KEY", "").strip()
    if not wallet_key:
        return PaymentResult(
            success=False,
            error="ATOMADIC_WALLET_KEY not set. Export your Base wallet private key.",
        )

    if challenge.is_expired:
        return PaymentResult(success=False, error="Payment challenge has expired.")

    if challenge.amount_micro_usdc <= 0 or challenge.amount_micro_usdc > MAX_CHALLENGE_MICRO_USDC:
        return PaymentResult(
            success=False,
            error=f"Payment aborted: amount {challenge.amount_micro_usdc} outside valid range (1\u2013{MAX_CHALLENGE_MICRO_USDC})",
        )

    config = get_chain_config()

    if challenge.chain_id and challenge.chain_id != config["chain_id"]:
        return PaymentResult(
            success=False,
            error=(
                f"Payment aborted: challenge chain_id {challenge.chain_id} "
                f"does not match active chain {config['chain_id']}"
            ),
        )

    if challenge.token_address:
        try:
            challenge_token = challenge.token_address.lower()
            expected_token = config["usdc_address"].lower()
        except AttributeError:
            return PaymentResult(success=False, error="Payment aborted: invalid token address in challenge")
        if challenge_token != expected_token:
            return PaymentResult(
                success=False,
                error=(
                    f"Payment aborted: challenge token {challenge.token_address} "
                    f"does not match expected USDC token {config['usdc_address']}"
                ),
            )

    try:
        from eth_account import Account
        from web3 import Web3
    except ImportError:
        return PaymentResult(
            success=False,
            error="web3 and eth-account packages required. Install: pip install web3 eth-account",
        )

    try:
        w3 = Web3(Web3.HTTPProvider(config["rpc_url"]))
        if not w3.is_connected():
            return PaymentResult(success=False, error=f"Cannot connect to {config['rpc_url']}")

        account = Account.from_key(wallet_key)

        # USDC ERC-20 transfer ABI
        usdc_abi = [
            {
                "name": "transfer",
                "type": "function",
                "inputs": [
                    {"name": "to", "type": "address"},
                    {"name": "amount", "type": "uint256"},
                ],
                "outputs": [{"name": "", "type": "bool"}],
            }
        ]

        usdc = w3.eth.contract(
            address=Web3.to_checksum_address(config["usdc_address"]),
            abi=usdc_abi,
        )

        # Build transfer transaction
        recipient = Web3.to_checksum_address(challenge.recipient)
        expected = Web3.to_checksum_address(ATOMADIC_TREASURY)
        if recipient != expected:
            return PaymentResult(
                success=False,
                error=f"Payment aborted: server proposed recipient {recipient} does not match expected treasury {expected}",
            )
        nonce = w3.eth.get_transaction_count(account.address)

        gas_price = w3.eth.gas_price
        max_gas_wei = MAX_GAS_PRICE_GWEI * 10**9
        if gas_price > max_gas_wei:
            return PaymentResult(
                success=False,
                error=f"Gas price {gas_price / 10**9:.1f} Gwei exceeds limit {MAX_GAS_PRICE_GWEI} Gwei. Retry when network is less congested.",
            )

        tx = usdc.functions.transfer(
            recipient, challenge.amount_micro_usdc
        ).build_transaction({
            "from": account.address,
            "nonce": nonce,
            "gas": 100_000,
            "gasPrice": gas_price,
            "chainId": config["chain_id"],
        })

        # Sign and send
        signed = account.sign_transaction(tx)
        tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
        txid = tx_hash.hex()

        # Build the payment proof header
        # Format: <sig_hex>;<wallet_addr>;<txid>;<amount_micro>
        sig_hex = signed.signature.hex()
        if sig_hex.startswith("0x"):
            sig_hex = sig_hex[2:]
        wallet_addr = account.address[2:]  # Remove 0x prefix — wallet address, not public key
        header = f"{sig_hex};{wallet_addr};{txid};{challenge.amount_micro_usdc}"

        return PaymentResult(
            success=True,
            txid=txid,
            signature_header=header,
            testnet=config["testnet"],
        )

    except (ValueError, TypeError, OSError, RuntimeError):
        import logging
        logging.getLogger(__name__).exception("Payment submission failed")
        return PaymentResult(success=False, error="Payment submission failed. Check logs for details.")
