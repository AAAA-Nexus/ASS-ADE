"""Tier a2 — assimilated method 'MCPServer._call_a2a_negotiate'

Assimilated from: server.py:1570-1622
"""

from __future__ import annotations


# --- assimilated symbol ---
def _call_a2a_negotiate(self, req_id: Any, args: dict[str, Any]) -> dict[str, Any]:
    remote_url = args.get("remote_url", "")
    if not remote_url:
        return self._error(req_id, -32602, "remote_url is required")
    from ass_ade.nexus.validation import validate_url

    try:
        validate_url(remote_url)
    except ValueError as e:
        return self._result(
            req_id,
            {
                "content": [{"type": "text", "text": f"Blocked: {e}"}],
                "isError": True,
            },
        )
    from ass_ade.a2a import fetch_agent_card, local_agent_card, negotiate

    local = local_agent_card(self._working_dir)
    report = fetch_agent_card(remote_url)
    if not report.valid or not report.card:
        messages = [issue.message for issue in report.errors]
        return self._result(
            req_id,
            {
                "content": [
                    {
                        "type": "text",
                        "text": f"Remote agent card is invalid: {messages}",
                    }
                ],
                "isError": True,
            },
        )
    result = negotiate(local, report.card)
    out = json.dumps(
        {
            "compatible": result.compatible,
            "shared_skills": result.shared_skills,
            "local_only": result.local_only,
            "remote_only": result.remote_only,
            "auth_compatible": result.auth_compatible,
            "notes": result.notes,
        },
        indent=2,
    )
    return self._result(
        req_id,
        {
            "content": [{"type": "text", "text": out}],
            "isError": not result.compatible,
        },
    )

