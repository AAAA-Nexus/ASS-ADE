# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a0_qk_constants/qk_draft_get_pricing_manifest.py:7
# Component id: qk.source.a0_qk_constants.get_pricing_manifest
from __future__ import annotations

__version__ = "0.1.0"

def get_pricing_manifest(self) -> PricingManifest:
    """/.well-known/pricing.json — machine-readable tiers, free"""
    return self._get_model("/.well-known/pricing.json", PricingManifest)
