# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a0_qk_constants/qk_draft_estimate_message_tokens.py:7
# Component id: qk.source.a0_qk_constants.estimate_message_tokens
from __future__ import annotations

__version__ = "0.1.0"

def estimate_message_tokens(msg: Message) -> int:
    """Estimate tokens for a single message including role overhead.

    Each message costs ~4 tokens of framing (role, delimiters) plus
    content tokens. Tool calls add their serialized JSON.
    """
    overhead = 4  # role + delimiters
    content_tokens = estimate_tokens(msg.content) if msg.content else 0

    tool_tokens = 0
    if msg.tool_calls:
        for tc in msg.tool_calls:
            tool_tokens += estimate_tokens(tc.name)
            tool_tokens += estimate_tokens(json.dumps(tc.arguments))

    if msg.name:
        overhead += 1  # name field

    return overhead + content_tokens + tool_tokens
