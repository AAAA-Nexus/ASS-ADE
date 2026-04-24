"""Tier a1 — assimilated function 'estimate_message_tokens'

Assimilated from: tokens.py:106-124
"""

from __future__ import annotations


# --- assimilated symbol ---
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

