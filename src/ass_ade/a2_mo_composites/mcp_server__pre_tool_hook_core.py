"""Tier a2 — assimilated method 'MCPServer._pre_tool_hook'

Assimilated from: server.py:592-609
"""

from __future__ import annotations


# --- assimilated symbol ---
def _pre_tool_hook(self, name: str, arguments: dict[str, Any]) -> tuple[bool, str]:
    """Run pre-execution gates. Returns (allow, reason).

    - write_file / edit_file: enforce NCB contract (file must have been read)
    """
    if name in ("write_file", "edit_file"):
        path = arguments.get("path") or arguments.get("file_path") or ""
        if path and not self.tca.ncb_contract(path):
            report = self.tca.check_freshness(path)
            msg = (
                f"NCB violation: {path} was not read within the last "
                f"{int(report.threshold_hours)}h. Call read_file first."
            )
            if self._ncb_mode == "block":
                return False, msg
            # warn mode: log + let through
            _LOG.warning("NCB warn: %s", msg)
    return True, ""

