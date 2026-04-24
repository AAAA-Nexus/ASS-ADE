"""Tier a1 — assimilated function 'trust_receipt'

Assimilated from: nexus.py:299-393
"""

from __future__ import annotations


# --- assimilated symbol ---
def trust_receipt(
    outbound_result: Mapping[str, Any],
    *,
    transport: NexusTransport,
    session: Mapping[str, Any] | None = None,
    sleep: Callable[[float], None] = time.sleep,
    now: Callable[[], datetime] | None = None,
) -> TrustReceipt:
    """Run the two §11.3 postflight probes with fail-closed retries.

    Raises :class:`BinderRefused` with
    ``code="hallucination_ceiling_exceeded"`` when the hallucination
    oracle reports the result is above ceiling. Raises
    :class:`NexusUnavailable` after ``_MAX_RETRY_ATTEMPTS`` transport
    failures on either hop.

    ``outbound_result`` is canonicalized and its sha256 is what the
    trust-chain signs over. The returned receipt carries only handles;
    the sovereign ``HALLUCINATION_CEILING`` never crosses the wire.
    """
    if transport is None:
        raise NexusTransportMissing(
            "trust_receipt called without a transport; wire nexus_transport= "
            "on the caller or pass nexus_transport=None to opt out."
        )

    now_fn = now or (lambda: datetime.now(UTC))
    signed_over = _canonical_sha256(outbound_result)

    hallucination = _retry_call(
        "hallucination_check",
        lambda: transport.hallucination_check(outbound_result),
        sleep=sleep,
    )
    h_verdict = str(hallucination.get("verdict", ""))
    ceiling_handle = str(hallucination.get("ceiling", "sovereign:handle:unknown"))
    claims_checked = int(hallucination.get("claims_checked", 0) or 0)
    if h_verdict == "above_ceiling":
        _emit_nexus_event(
            kind="hallucination_check",
            verdict="failure",
            input_payload={"signed_over": signed_over},
            output_payload={
                "verdict": h_verdict,
                "claims_checked": claims_checked,
            },
            escalation_reason="hallucination_ceiling",
            tags=("nexus", "audit", "hallucination_ceiling"),
        )
        raise BinderRefused(
            code="hallucination_ceiling_exceeded",
            message=(
                "Postflight hallucination oracle reports above ceiling; "
                "downgrading bind() to refused per _PROTOCOL.md §11.3."
            ),
        )
    _emit_nexus_event(
        kind="hallucination_check",
        verdict="success",
        input_payload={"signed_over": signed_over},
        output_payload={"verdict": h_verdict, "claims_checked": claims_checked},
        tags=("nexus", "audit"),
    )

    signed = _retry_call(
        "trust_chain_sign",
        lambda: transport.trust_chain_sign(outbound_result, session),
        sleep=sleep,
    )
    ratchet_epoch = int(signed.get("ratchet_epoch", 0) or 0)
    principal = str(signed.get("principal", "ass_ade.engine.binder"))
    _emit_nexus_event(
        kind="trust_chain_sign",
        verdict="success",
        input_payload={"signed_over": signed_over},
        output_payload={
            "ratchet_epoch": ratchet_epoch,
            "principal": principal,
        },
        tags=("nexus", "audit"),
    )

    return TrustReceipt(
        hallucination_receipt_id=str(
            hallucination.get("receipt_id") or uuid.uuid4()
        ),
        hallucination_verdict=h_verdict,
        ceiling_handle=ceiling_handle,
        claims_checked=claims_checked,
        trust_chain_receipt_id=str(signed.get("receipt_id") or uuid.uuid4()),
        signed_over=signed_over,
        ratchet_epoch=ratchet_epoch,
        principal=principal,
        ts=_iso(now_fn()),
    )

