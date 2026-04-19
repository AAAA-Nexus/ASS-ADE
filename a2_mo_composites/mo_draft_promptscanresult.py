# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_promptscanresult.py:7
# Component id: mo.source.a2_mo_composites.promptscanresult
from __future__ import annotations

__version__ = "0.1.0"

class PromptScanResult(NexusModel):
    """/v1/prompts/inject-scan and /v1/security/prompt-scan"""
    threat_detected: bool | None = None
    threat_level: str | None = None  # "none" | "low" | "medium" | "high"
    confidence: float | None = None
    threat_report: dict | None = None
