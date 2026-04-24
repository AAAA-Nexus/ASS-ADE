"""Tier a1 — assimilated function 'extract_nexus_content'

Assimilated from: rebuild/nexus_parse.py:29-54
"""

from __future__ import annotations


# --- assimilated symbol ---
def extract_nexus_content(data: Any) -> str:
    """Pull the assistant text out of a Nexus ``/v1/inference`` response.

    Handles both the flat ``{"response": ...}`` / ``{"output": ...}`` /
    ``{"text": ...}`` shapes and the OpenAI-style
    ``{"choices": [{"message": {"content": ...}}]}`` shape. Surrounding
    markdown fences are stripped.
    """
    if not isinstance(data, dict):
        return ""
    raw: str = ""
    for key in ("response", "output", "text"):
        val = data.get(key)
        if isinstance(val, str) and val.strip():
            raw = val
            break
    if not raw:
        choices = data.get("choices")
        if isinstance(choices, list) and choices:
            first = choices[0] if isinstance(choices[0], dict) else {}
            msg = first.get("message") if isinstance(first, dict) else None
            if isinstance(msg, dict) and isinstance(msg.get("content"), str):
                raw = msg["content"]
            elif isinstance(first, dict) and isinstance(first.get("text"), str):
                raw = first["text"]
    return strip_markdown_fences(raw) if raw else ""

