# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:69
# Component id: qk.source.ass_ade.pricingmanifest
from __future__ import annotations

__version__ = "0.1.0"

class PricingManifest(NexusModel):
    """/.well-known/pricing.json"""
    tiers: Any = None
