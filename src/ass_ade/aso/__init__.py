"""Atomadic Swarm Optimizer (ASO) — monadic subsystem skeleton (MAP = TERRAIN).

Tiers (src layout): ``constants`` / ``pure`` / ``plan`` approximate a0→a3;
``ass_ade.commands.aso`` is the a4 Typer surface. Heavy integrations
(MCP compressor proxy, memX, OTel collectors, graph DBs) are explicit
**research / product** slots — ship measured deltas before claiming production savings.
"""

from __future__ import annotations

ASO_SCHEMA_VERSION = "ass-ade.aso.v0"

__all__ = ["ASO_SCHEMA_VERSION"]
