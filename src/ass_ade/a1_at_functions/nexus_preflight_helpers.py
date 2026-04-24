"""Tier a1 — assimilated function 'nexus_preflight'

Assimilated from: nexus.py:195-291
"""

from __future__ import annotations


# --- assimilated symbol ---
def nexus_preflight(
    inbound_envelope: Mapping[str, Any],
    *,
    transport: NexusTransport,
    sleep: Callable[[float], None] = time.sleep,
    now: Callable[[], datetime] | None = None,
) -> PreflightResult:
    """Run the two §11.1 preflight probes with fail-closed retries.

    Raises :class:`BinderRefused` with ``code`` in
    ``{"nexus_injection_blocked", "nexus_drift_stale"}`` when a probe
    returns a non-clean verdict. Raises :class:`NexusUnavailable`
    after ``_MAX_RETRY_ATTEMPTS`` transport failures.

    The envelope is bound into the Aegis response via
    ``sha256(canonical(inputs))``. Callers assemble the envelope with
    at minimum: ``{"manifest_fingerprint": ..., "session_id": ...,
    "rules_hash": ..., "context_pack_ref": ...}``. Anything else in
    the envelope is passed through.
    """
    if transport is None:
        raise NexusTransportMissing(
            "nexus_preflight called without a transport; provide nexus_transport= "
            "on bind() or pass nexus_transport=None explicitly to opt out of §11."
        )

    now_fn = now or (lambda: datetime.now(UTC))
    bound_to = _canonical_sha256(inbound_envelope)

    aegis = _retry_call(
        "aegis_scan",
        lambda: transport.aegis_scan(inbound_envelope),
        sleep=sleep,
    )
    aegis_verdict = str(aegis.get("verdict", ""))
    if aegis_verdict != "clean":
        _emit_nexus_event(
            kind="aegis_scan",
            verdict="failure",
            input_payload={"bound_to": bound_to},
            output_payload={"verdict": aegis_verdict},
            escalation_reason="injection_detected",
            tags=("nexus", "audit", "injection_blocked"),
        )
        raise BinderRefused(
            code="nexus_injection_blocked",
            message=(
                f"Aegis-Edge verdict {aegis_verdict!r} - refusing to bind. "
                "Review the inputs and refresh the session."
            ),
        )
    _emit_nexus_event(
        kind="aegis_scan",
        verdict="success",
        input_payload={"bound_to": bound_to},
        output_payload={"verdict": aegis_verdict},
        tags=("nexus", "audit"),
    )

    drift = _retry_call(
        "drift_check",
        lambda: transport.drift_check(inbound_envelope),
        sleep=sleep,
    )
    drift_verdict = str(drift.get("verdict", ""))
    if drift_verdict != "fresh":
        _emit_nexus_event(
            kind="drift_check",
            verdict="failure",
            input_payload={"bound_to": bound_to},
            output_payload={"verdict": drift_verdict},
            escalation_reason="drift_detected",
            tags=("nexus", "audit", "drift_stale"),
        )
        raise BinderRefused(
            code="nexus_drift_stale",
            message=(
                f"UEP-govern drift verdict {drift_verdict!r} - refusing to "
                "bind. Refresh RULES.md, CONTEXT_PACK, and TASK-INDEX."
            ),
        )
    _emit_nexus_event(
        kind="drift_check",
        verdict="success",
        input_payload={"bound_to": bound_to},
        output_payload={"verdict": drift_verdict},
        tags=("nexus", "audit"),
    )

    return PreflightResult(
        aegis_receipt_id=str(aegis.get("receipt_id") or uuid.uuid4()),
        aegis_verdict=aegis_verdict,
        drift_receipt_id=str(drift.get("receipt_id") or uuid.uuid4()),
        drift_verdict=drift_verdict,
        bound_to=bound_to,
        ts=_iso(now_fn()),
    )

