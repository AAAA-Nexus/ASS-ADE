"""Tier a2_mo — evolution gate composite enforcing evidence requirements for REFINE verdicts."""
from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class EvolutionGate:
    """Blocks a REFINE verdict from proceeding unless documented evidence with MCP manifest citation is present."""

    _evidence: list[dict] = field(default_factory=list)

    def record_evidence(self, source: str, mcp_manifest_ref: str, summary: str) -> None:
        self._evidence.append(
            {"source": source, "mcp_manifest_ref": mcp_manifest_ref, "summary": summary}
        )

    def check(self, verdict: str) -> tuple[bool, str]:
        """Return (allowed, reason). REFINE requires at least one evidence entry with an MCP manifest ref."""
        if verdict != "REFINE":
            return True, "non-REFINE verdict passes unconditionally"
        cited = [e for e in self._evidence if e.get("mcp_manifest_ref")]
        if not cited:
            return False, "REFINE requires at least one evidence entry with a non-empty mcp_manifest_ref"
        return True, f"{len(cited)} cited evidence record(s) satisfy gate"

    def allow(self, verdict: str) -> bool:
        ok, _ = self.check(verdict)
        return ok
