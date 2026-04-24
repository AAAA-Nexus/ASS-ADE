"""Tier a2 — assimilated method 'MCPServer._call_a2a_validate'

Assimilated from: server.py:1531-1568
"""

from __future__ import annotations


# --- assimilated symbol ---
def _call_a2a_validate(self, req_id: Any, args: dict[str, Any]) -> dict[str, Any]:
    url = args.get("url", "")
    if not url:
        return self._error(req_id, -32602, "url is required")
    from ass_ade.nexus.validation import validate_url

    try:
        validate_url(url)
    except ValueError as e:
        return self._result(
            req_id,
            {
                "content": [{"type": "text", "text": f"Blocked: {e}"}],
                "isError": True,
            },
        )
    from ass_ade.a2a import fetch_agent_card

    report = fetch_agent_card(url)
    issues = [
        {"severity": i.severity, "field": i.field, "message": i.message}
        for i in report.issues
    ]
    out = json.dumps(
        {
            "valid": report.valid,
            "issues": issues,
            "card": report.card.model_dump() if report.card else None,
        },
        indent=2,
    )
    return self._result(
        req_id,
        {
            "content": [{"type": "text", "text": out}],
            "isError": not report.valid,
        },
    )

