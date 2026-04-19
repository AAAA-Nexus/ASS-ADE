# Extracted from C:/!ass-ade/src/ass_ade/workflows.py:234
# Component id: og.source.ass_ade.safe_execute
from __future__ import annotations

__version__ = "0.1.0"

def safe_execute(
    client: NexusClient,
    tool_name: str,
    tool_input: str = "",
    *,
    agent_id: str | None = None,
) -> SafeExecuteResult:
    """AEGIS-wrapped MCP tool execution: shield → scan → proxy → certify.

    Uses the AEGIS MCP proxy for firewalled execution rather than direct invocation.
    """
    result = SafeExecuteResult(tool_name=tool_name)

    # Step 1: Security shield — sanitise payload
    try:
        shield = client.security_shield({"tool": tool_name, "input": tool_input})
        shield_raw = shield.model_dump() if hasattr(shield, "model_dump") else {}
        result.shield_passed = not shield_raw.get("blocked", False)
    except _WORKFLOW_ERRORS:
        _LOG.warning("Security shield failed for tool=%s", tool_name, exc_info=True)
        result.shield_passed = False

    # Step 2: Prompt injection scan
    if tool_input:
        try:
            scan = client.prompt_inject_scan(tool_input)
            scan_raw = scan.model_dump() if hasattr(scan, "model_dump") else {}
            result.prompt_scan_passed = not scan_raw.get("threat_detected", False)
        except _WORKFLOW_ERRORS:
            _LOG.warning("Prompt scan failed for tool=%s", tool_name, exc_info=True)
            result.prompt_scan_passed = False
    else:
        result.prompt_scan_passed = True

    # Step 3: AEGIS MCP proxy execute
    try:
        proxy_result = client.aegis_mcp_proxy(
            tool=tool_name,
            tool_input=tool_input,
            agent_id=agent_id,
        )
        result.invocation_result = proxy_result.model_dump() if hasattr(proxy_result, "model_dump") else {}
    except _WORKFLOW_ERRORS:
        _LOG.warning(
            "AEGIS MCP proxy failed for tool=%s, agent_id=%s",
            tool_name,
            agent_id,
            exc_info=True,
        )
        result.invocation_result = {"error": "proxy_failed"}

    # Step 4: Optional output certification
    output_text = str(result.invocation_result.get("tool_result", result.invocation_result.get("allowed", "")))
    if output_text and result.shield_passed and result.prompt_scan_passed:
        try:
            cert = client.certify_output(output_text, rubric=["tool_safety", "output_integrity"])
            cert_raw = cert.model_dump() if hasattr(cert, "model_dump") else {}
            result.certificate_id = cert_raw.get("certificate_id")
        except _WORKFLOW_ERRORS:
            _LOG.warning("Output certification failed for tool=%s", tool_name, exc_info=True)

    return result
