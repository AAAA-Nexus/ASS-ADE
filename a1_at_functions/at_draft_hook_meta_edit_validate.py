# Extracted from C:/!ass-ade/src/ass_ade/agent/gates.py:349
# Component id: at.source.ass_ade.hook_meta_edit_validate
from __future__ import annotations

__version__ = "0.1.0"

def hook_meta_edit_validate(self, meta_edit: Any) -> dict[str, Any] | None:
    """Validate a meta-edit by running N=5 sample tasks before and after.

    Passes iff audit_pass_rate_delta >= 0.05. Results are persisted to
    .ass-ade/state/meta_edit_audits/{timestamp}.json.
    """
    import json
    from datetime import UTC, datetime
    from pathlib import Path

    try:
        from ass_ade.agent.golden_runner import run_golden

        cfg = getattr(self, "_v18_config", {}) or {}
        golden_path = Path(
            (cfg.get("dgm_h") or {}).get("golden_task_path", ".ass-ade/golden/tasks.jsonl")
        )
        audits_dir = Path(
            (cfg.get("dgm_h") or {}).get("meta_audit_dir", ".ass-ade/state/meta_edit_audits")
        )

        me_id = str(getattr(meta_edit, "id", "meta_edit"))
        me_desc = str(getattr(meta_edit, "description", "") or getattr(meta_edit, "procedure", ""))

        before = run_golden(golden_path, tasks_limit=5, repeats=1, prompt_suffix="", seed=11)
        after = run_golden(
            golden_path,
            tasks_limit=5,
            repeats=1,
            prompt_suffix=f"meta_edit:{me_id}:{me_desc[:80]}",
            seed=13,
        )
        before_rate = float(before.get("aggregate", {}).get("pass_rate", 0.0))
        after_rate = float(after.get("aggregate", {}).get("pass_rate", 0.0))
        delta = after_rate - before_rate
        ok = delta >= 0.05

        artifact: dict[str, Any] = {
            "meta_edit_id": me_id,
            "description": me_desc,
            "before_rate": before_rate,
            "after_rate": after_rate,
            "delta": delta,
            "validated": ok,
            "before_per_task": before.get("per_task", []),
            "after_per_task": after.get("per_task", []),
            "ts": datetime.now(UTC).isoformat(),
        }
        try:
            audits_dir.mkdir(parents=True, exist_ok=True)
            ts = datetime.now(UTC).strftime("%Y%m%dT%H%M%S%f")
            (audits_dir / f"{ts}_{me_id}.json").write_text(
                json.dumps(artifact, indent=2), encoding="utf-8"
            )
        except OSError:
            pass

        self._gate_log.append(GateResult(
            gate="meta_edit_validate",
            passed=ok,
            confidence=max(0.0, min(1.0, 0.5 + delta)),
            details={"before_rate": before_rate, "after_rate": after_rate, "delta": delta},
        ))
        return {
            "before_rate": before_rate,
            "after_rate": after_rate,
            "delta": delta,
            "validated": ok,
        }
    except Exception as exc:
        logging.getLogger(__name__).warning("hook_meta_edit_validate failed: %s", exc)
        return None
