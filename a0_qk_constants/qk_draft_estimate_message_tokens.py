# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/engine/tokens.py:106
# Component id: qk.source.ass_ade.estimate_message_tokens
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
