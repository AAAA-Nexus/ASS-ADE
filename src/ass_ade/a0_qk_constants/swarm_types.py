"""Tier a0_qk — compressed episode format for swarm handoffs."""
from __future__ import annotations
from typing import TypedDict


class Episode(TypedDict):
    goal: str
    tools_used: list[str]
    key_files: list[str]
    verdict: str  # PASS | FAIL | DEFER
    duration_ms: int
    notes: str
