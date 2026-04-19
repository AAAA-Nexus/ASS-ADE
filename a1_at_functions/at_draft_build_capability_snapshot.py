# Extracted from C:/!ass-ade/src/ass_ade/agent/capabilities.py:183
# Component id: at.source.ass_ade.build_capability_snapshot
from __future__ import annotations

__version__ = "0.1.0"

def build_capability_snapshot(working_dir: str | Path = ".") -> CapabilitySnapshot:
    cwd = str(Path(working_dir).resolve())
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    if now.endswith("+00:00"):
        now = f"{now[:-6]}Z"
    return CapabilitySnapshot(
        generated_at_utc=now,
        working_dir=cwd,
        cli_commands=collect_cli_commands(),
        local_tools=collect_local_tools(cwd),
        mcp_tools=collect_mcp_tools(cwd),
        agents=collect_agents(cwd),
        hooks=collect_hooks(cwd),
    )
