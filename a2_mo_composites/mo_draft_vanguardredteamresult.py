# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_vanguardredteamresult.py:7
# Component id: mo.source.a2_mo_composites.vanguardredteamresult
from __future__ import annotations

__version__ = "0.1.0"

class VanguardRedTeamResult(NexusModel):
    """POST /v1/vanguard/continuous-redteam"""
    run_id: str | None = None
    agent_id: str | None = None
    vulnerabilities_found: int | None = None
    severity: str | None = None
    findings: list[dict] = Field(default_factory=list)
    next_run_at: int | None = None
