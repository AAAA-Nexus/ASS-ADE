# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_cyclereport.py:7
# Component id: mo.source.a2_mo_composites.cyclereport
from __future__ import annotations

__version__ = "0.1.0"

class CycleReport:
    """Full report from one agent step cycle."""
    alerts: list  # list[Alert] — typed at runtime to avoid circular import
    wisdom_score: float = 0.0
    wisdom_passed: int = 0
    wisdom_failed: int = 0
    conviction: float = 0.5
    wisdom_ema: float = 0.5  # Exponential moving average of wisdom scores
    gvu_coefficient: float = 1.0
    synergy: float = 0.0
    synergy_emergent: bool = False
    atlas_subtasks: list = field(default_factory=list)  # list[SubTask]
    principles: list[str] = field(default_factory=list)
    engine_reports: dict[str, dict] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    tca_stale_files: list[str] = field(default_factory=list)
    cie_passes: int = 0
    cie_failures: int = 0
    lora_pending: int = 0
    autopoietic_triggered: bool = False
