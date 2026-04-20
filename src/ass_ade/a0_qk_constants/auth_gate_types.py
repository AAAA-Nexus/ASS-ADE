"""Tier a0 — premium tier constants, feature enum, and pricing for the ASS-ADE CLI gate."""
from __future__ import annotations

from enum import Enum


class PremiumFeature(str, Enum):
    """Identifies a gated premium CLI feature for key validation and usage billing."""

    FORGE_EXECUTION = "rebuild.forge"
    MULTI_REPO_MERGE = "rebuild.multi-repo"
    ENHANCE = "enhance"
    CERTIFY = "certify"
    BLUEPRINT_DESIGN = "blueprint.design"
    BLUEPRINT_BUILD = "blueprint.build"
    EVOLVE = "protocol.evolve"


# Per-call price in USD, mirrors the Stripe metering products in stripe_price_ids.json.
FEATURE_PRICE: dict[str, float] = {
    PremiumFeature.FORGE_EXECUTION.value: 1.00,    # per file processed
    PremiumFeature.MULTI_REPO_MERGE.value: 10.00,  # per merge run
    PremiumFeature.ENHANCE.value: 2.00,            # per analysis
    PremiumFeature.CERTIFY.value: 0.25,            # per certificate signed
    PremiumFeature.BLUEPRINT_DESIGN.value: 2.00,   # per blueprint generated
    PremiumFeature.BLUEPRINT_BUILD.value: 5.00,    # per build run
    PremiumFeature.EVOLVE.value: 1.00,             # per evolution event
}

UPGRADE_URL = "https://atomadic.tech/ass-ade"

TIER_MESSAGE = (
    "This feature requires an Atomadic API key.\n"
    "Get one at: " + UPGRADE_URL + "\n\n"
    "Free:              recon, eco-scan, lint, basic rebuild, doctor, tutorial, setup\n"
    "Starter ($29/mo):  forge, certification, evolution tracking\n"
    "Pro ($99/mo):      multi-repo merge, epiphany engine, blueprints\n"
    "Enterprise ($499/mo): unlimited, IP guard, private LoRA, SLA\n\n"
    "Set your key:  export AAAA_NEXUS_API_KEY=<your-key>\n"
    "Or add to .env: AAAA_NEXUS_API_KEY=<your-key>"
)
