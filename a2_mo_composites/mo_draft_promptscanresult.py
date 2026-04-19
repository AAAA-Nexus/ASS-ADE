# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:420
# Component id: mo.source.ass_ade.promptscanresult
from __future__ import annotations

__version__ = "0.1.0"

class PromptScanResult(NexusModel):
    """/v1/prompts/inject-scan and /v1/security/prompt-scan"""
    threat_detected: bool | None = None
    threat_level: str | None = None  # "none" | "low" | "medium" | "high"
    confidence: float | None = None
    threat_report: dict | None = None
