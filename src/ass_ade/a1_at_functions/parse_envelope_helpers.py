"""Tier a1 — assimilated function 'parse_envelope'

Assimilated from: protocol.py:100-166
"""

from __future__ import annotations


# --- assimilated symbol ---
def parse_envelope(text: str) -> SignalEnvelope:
    """Parse the on-disk signal format back into an envelope.

    Raises ``MalformedSignalError`` with a specific message for each failure.
    """
    m = _FRONT_MATTER_RE.match(text)
    if not m:
        raise MalformedSignalError("missing YAML front matter")

    head = m.group(1)
    body = text[m.end():].strip()

    meta: dict = {}
    routes: list[str] = []
    current_list_key: str | None = None
    for raw in head.splitlines():
        line = raw.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if current_list_key == "routes" and line.lstrip().startswith("- "):
            routes.append(line.lstrip()[2:].strip().strip('"\''))
            continue
        current_list_key = None
        if ":" not in line:
            raise MalformedSignalError(f"expected 'key: value' line, got {line!r}")
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.strip().strip('"\'')
        if key == "routes" and val == "":
            current_list_key = "routes"
            continue
        meta[key] = val

    required = ("signal_id", "priority", "issued_by", "issued_at",
                "subject", "ack_required", "digest")
    missing = [k for k in required if k not in meta]
    if missing:
        raise MalformedSignalError(f"missing required fields: {missing}")

    try:
        priority = Priority.parse(meta["priority"])
    except ValueError as e:
        raise MalformedSignalError(str(e)) from e

    ack_required = meta["ack_required"].lower() in ("true", "yes", "1")

    envelope = SignalEnvelope(
        signal_id=meta["signal_id"],
        priority=priority,
        issued_by=meta["issued_by"],
        issued_at=meta["issued_at"],
        subject=meta["subject"],
        body=body,
        routes=tuple(routes) if routes else ("*",),
        ack_required=ack_required,
        expires_at=meta.get("expires_at", ""),
        digest=meta["digest"],
    )

    expected = _digest(envelope.signal_id, envelope.subject, envelope.body,
                       envelope.issued_by)
    if expected != envelope.digest:
        raise MalformedSignalError(
            f"digest mismatch: file claims {envelope.digest}, "
            f"content hashes to {expected}"
        )
    return envelope

