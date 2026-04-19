# Extracted from C:/!ass-ade/src/ass_ade/agent/bas.py:100
# Component id: at.source.ass_ade.alert
from __future__ import annotations

__version__ = "0.1.0"

def alert(self, kind: str, payload: dict) -> Alert | None:
    now = time.time()
    last_ts = self._last_alert_ts.get(kind)
    if last_ts is not None and (now - last_ts) < self._cooldown_s:
        # On cooldown — return most recent alert of this kind (if any), marked skipped
        for existing in reversed(self._alerts):
            if existing.kind == kind:
                skipped = Alert(
                    kind=existing.kind,
                    severity=existing.severity,
                    payload=existing.payload,
                    ts=existing.ts,
                    cooldown_skipped=True,
                )
                return skipped
        return None

    sev = _SEVERITY.get(kind, "medium")
    a = Alert(
        kind=kind,
        severity=sev,
        payload=payload,
        ts=datetime.now(UTC).isoformat(),
        cooldown_skipped=False,
    )
    self._alerts.append(a)
    self._unflushed.append(a)
    self._last_alert_ts[kind] = now
    self._alerts_total += 1

    # Persist
    self._persist_alert(a)

    # Notify subscribers
    self._notify_subscribers(a)

    # Record to reputation if high severity
    if self._nexus is not None and a.severity == "high":
        try:
            self._nexus.reputation_record(
                agent_id="bas",
                success=False,
                quality=0.0,
                latency_ms=0.0,
            )
        except Exception:
            pass

    return a
