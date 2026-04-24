"""Tier a2 — assimilated class 'ExtractedBody'

Assimilated from: rebuild/body_extractor.py:20-28
"""

from __future__ import annotations


# --- assimilated symbol ---
class ExtractedBody:
    source_path: str
    source_line: int
    symbol_name: str
    language: str
    body: str
    imports: list[str]
    callers_of: list[str]
    exceptions_raised: list[str]

