"""Tier a0_qk — agent seed type definitions for behavioral evolution tracking."""
from __future__ import annotations
from typing import TypedDict


class AgentSeed(TypedDict, total=False):
    prompt: str
    tool_policy: dict
    entry_context: dict
    version: str
    parent_seed: str | None
