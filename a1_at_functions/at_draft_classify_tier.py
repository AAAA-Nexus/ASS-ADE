# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_classify_tier.py:7
# Component id: at.source.a1_at_functions.classify_tier
from __future__ import annotations

__version__ = "0.1.0"

def classify_tier(symbol: Symbol) -> str:
    haystack = f"{symbol.path} {symbol.name} {symbol.kind}".lower()
    if any(term in haystack for term in (
        "constant", "const", "schema", "manifest", "token", "invariant", "proof"
    )):
        return "a0_qk_constants"
    if any(term in haystack for term in (
        "button", "textarea", "input", "validator", "validate", "format", "parse", "atom"
    )):
        return "a1_at_functions"
    if any(term in haystack for term in (
        "engine", "service", "client", "manager", "store", "hook", "calculator", "molecule"
    )):
        return "a2_mo_composites"
    if any(term in haystack for term in (
        "registry", "gateway", "vault", "module", "feature", "workflow", "page", "screen", "organism"
    )):
        return "a3_og_features"
    if any(term in haystack for term in (
        "server", "router", "orchestrator", "bridge", "runtime", "system", "main", "mcp"
    )):
        return "a4_sy_orchestration"
    if symbol.kind == "function":
        return "a1_at_functions"
    if symbol.kind == "class":
        return "a2_mo_composites"
    return "a1_at_functions"
