"""Tier a1 — pure helpers for parsing AAAA-Nexus inference responses.

Stateless functions only. No I/O, no classes, no module-level mutable
state. Shared by ``synthesis.py`` (a3) and ``feature.py`` (a3) so the
two callers cannot drift out of sync on response-shape handling.
"""

from __future__ import annotations

import re
from typing import Any

_FENCE_RE = re.compile(
    r"^\s*```(?:[A-Za-z0-9_+-]*)\s*\n(?P<body>.*?)\n?```\s*$",
    re.DOTALL,
)


def strip_markdown_fences(text: str) -> str:
    """Strip a single surrounding ```lang fenced block if present."""
    if not isinstance(text, str):
        return ""
    m = _FENCE_RE.match(text.strip())
    if m:
        return m.group("body")
    return text


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


def extract_json_array(text: str) -> str:
    """Extract the first top-level JSON array from arbitrary model output.

    Handles fenced ```json blocks, leading prose/headings, and trailing
    commentary. Deterministic: scans for the first ``[`` and tracks
    bracket depth with string-literal awareness.
    """
    s = text.strip()
    fence = re.search(r"```(?:json)?\s*\n(.*?)```", s, re.DOTALL)
    if fence:
        s = fence.group(1).strip()
    start = s.find("[")
    if start == -1:
        return s
    depth = 0
    in_str = False
    escape = False
    for i in range(start, len(s)):
        ch = s[i]
        if in_str:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
        elif ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                return s[start : i + 1]
    return s[start:]


def slugify(text: str) -> str:
    """CamelCase- and punctuation-aware slug: ``TokenBucket`` → ``token_bucket``."""
    spaced = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", text)
    out = re.sub(r"[^a-z0-9]+", "_", spaced.lower()).strip("_")
    return out or "component"
