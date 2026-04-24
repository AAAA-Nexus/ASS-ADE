"""a0-grade ASO constants — no I/O, no env reads."""

from __future__ import annotations

from typing import Final, Literal

ASO_ENGINE_IDS: Final[tuple[str, ...]] = ("COE", "SIE", "CCE", "TEE")

SwarmTopology = Literal["parallel", "sequential", "hierarchical", "adaptive"]

DEFAULT_SWARM_TOPOLOGY: SwarmTopology = "adaptive"

# Token / percent claims in marketing copy require local benchmarks — keep budgets numeric only.
MCP_MANIFEST_SOFT_TOKEN_BUDGET: Final[int] = 2000

ASO_LOG_SUBDIRS: Final[tuple[str, ...]] = ("context", "swarm", "codebase", "telemetry")
