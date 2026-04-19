# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:289
# Component id: qk.source.ass_ade.get_pricing_manifest
__version__ = "0.1.0"

    def get_pricing_manifest(self) -> PricingManifest:
        """/.well-known/pricing.json — machine-readable tiers, free"""
        return self._get_model("/.well-known/pricing.json", PricingManifest)
