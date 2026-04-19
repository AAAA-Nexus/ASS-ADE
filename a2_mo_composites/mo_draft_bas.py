# Extracted from C:/!ass-ade/src/ass_ade/agent/bas.py:47
# Component id: mo.source.ass_ade.bas
from __future__ import annotations

__version__ = "0.1.0"

class BAS:
    def __init__(self, config: dict, nexus: Any | None = None):
        self._config = config
        self._nexus = nexus
        self._alerts: list[Alert] = []
        self._unflushed: list[Alert] = []
        self._subscribers: list[Callable[[Alert], None]] = []
        self._last_alert_ts: dict[str, float] = {}
        self._cooldown_s: float = float(config.get("bas_cooldown_s", 60.0))

        syn = config.get("synergy") or {}
        self._synergy_threshold = float(syn.get("threshold", 0.6))
        self._novelty_threshold = float((config.get("sde") or {}).get("novelty_threshold", 0.75))

        # Persistence path
        path_override = config.get("bas_state_path")
        self._persist_path: Path = Path(path_override) if path_override else _DEFAULT_STATE_PATH

        # Count existing persisted alerts
        self._alerts_total: int = self._load_alert_count()

    def _load_alert_count(self) -> int:
        """Count existing alert lines in the persist file without loading all content."""
        try:
            if not self._persist_path.exists():
                return 0
            count = 0
            with self._persist_path.open("r", encoding="utf-8") as f:
                for _ in f:
                    count += 1
            return count
        except OSError:
            return 0

    def _persist_alert(self, a: Alert) -> None:
        """Append an alert to the JSONL file, creating directories as needed."""
        try:
            self._persist_path.parent.mkdir(parents=True, exist_ok=True)
            with self._persist_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(a.__dict__) + "\n")
        except OSError:
            pass

    def subscribe(self, callback: Callable[[Alert], None]) -> None:
        self._subscribers.append(callback)

    def _notify_subscribers(self, a: Alert) -> None:
        for cb in self._subscribers:
            try:
                cb(a)
            except Exception:
                pass

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

    def monitor(self, metrics: dict) -> Alert | None:
        synergy = float(metrics.get("synergy", 0.0))
        novelty = float(metrics.get("novelty", 0.0))
        gvu = float(metrics.get("gvu_delta", 0.0))
        if synergy > self._synergy_threshold:
            return self.alert("emergent_synergy", {"synergy": synergy})
        if novelty > self._novelty_threshold:
            return self.alert("novelty_spike", {"novelty": novelty})
        if gvu > 0.1:
            return self.alert("gvu_jump", {"gvu_delta": gvu})
        return None

    def monitor_all(self, metrics: dict) -> list[Alert]:
        """Check all thresholds and return all alerts fired."""
        fired: list[Alert] = []

        synergy = float(metrics.get("synergy", 0.0))
        if synergy > self._synergy_threshold:
            a = self.alert("emergent_synergy", {"synergy": synergy})
            if a is not None:
                fired.append(a)

        novelty = float(metrics.get("novelty", 0.0))
        if novelty > self._novelty_threshold:
            a = self.alert("novelty_spike", {"novelty": novelty})
            if a is not None:
                fired.append(a)

        gvu = float(metrics.get("gvu_delta", 0.0))
        if gvu > 0.1:
            a = self.alert("gvu_jump", {"gvu_delta": gvu})
            if a is not None:
                fired.append(a)

        missing_caps = metrics.get("missing_capabilities")
        if isinstance(missing_caps, list) and len(missing_caps) > 0:
            a = self.alert("capability_gap", {"missing_capabilities": list(missing_caps)})
            if a is not None:
                fired.append(a)

        trust_score = float(metrics.get("trust_score", 1.0))
        if trust_score < 0.3:
            a = self.alert("trust_violation", {"trust_score": trust_score})
            if a is not None:
                fired.append(a)

        budget_pct = float(metrics.get("budget_pct", 0.0))
        if budget_pct > 0.9:
            a = self.alert("budget_exhaustion", {"budget_pct": budget_pct})
            if a is not None:
                fired.append(a)

        score_delta = float(metrics.get("score_delta", 0.0))
        if score_delta < -0.2:
            a = self.alert("quality_regression", {"score_delta": score_delta})
            if a is not None:
                fired.append(a)

        tool_repeat = int(metrics.get("tool_repeat_count", 0))
        if tool_repeat > 3:
            a = self.alert("loop_detected", {"tool_repeat_count": tool_repeat})
            if a is not None:
                fired.append(a)

        return fired

    def flush_alerts(self) -> list[Alert]:
        """Drain and return the unflushed alerts buffer."""
        drained = list(self._unflushed)
        self._unflushed.clear()
        return drained

    def run(self, ctx: dict) -> dict:
        alert = self.monitor(ctx.get("metrics", {}))
        return {"alert": alert.__dict__ if alert else None}

    def report(self) -> dict:
        return {
            "engine": "bas",
            "alerts_total": self._alerts_total,
            "alerts_session": len(self._alerts),
            "unflushed": len(self._unflushed),
            "subscribers": len(self._subscribers),
            "last": self._alerts[-1].__dict__ if self._alerts else None,
            "cooldown_s": self._cooldown_s,
        }
