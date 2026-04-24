"""Tier a1 — assimilated function 'classify_tier'

Assimilated from: rebuild/project_parser.py:205-261
"""

from __future__ import annotations


# --- assimilated symbol ---
def classify_tier(symbol: Symbol) -> str:
    classifier_path = _classification_path(symbol.path)
    tokens = _keyword_tokens(classifier_path, symbol.name, symbol.kind)
    name_tokens = _keyword_tokens(symbol.name)
    contract_tokens = {
        "constant", "const", "schema", "manifest", "token", "invariant", "proof"
    }
    atom_tokens = {
        "button", "textarea", "input", "validator", "validate", "format", "parse", "atom"
    }
    composite_tokens = {
        "engine", "service", "client", "manager", "store", "hook", "calculator", "molecule"
    }
    feature_tokens = {
        "registry", "gateway", "vault", "module", "feature", "workflow", "page", "screen", "organism"
    }
    orchestration_tokens = {
        "server", "router", "orchestrator", "bridge", "runtime", "system", "main", "mcp"
    }
    orchestration_function_tokens = {"main", "entrypoint", "bootstrap"}

    if symbol.kind == "function":
        if name_tokens.intersection(orchestration_function_tokens):
            return "a4_sy_orchestration"
        return "a1_at_functions"

    if symbol.kind == "variable":
        if tokens.intersection(contract_tokens):
            return "a0_qk_constants"
        return "a1_at_functions"

    if symbol.kind in {"class", "type"} and tokens.intersection(composite_tokens):
        return "a2_mo_composites"
    # Pure contract/data carriers intentionally stay in a0 when their names
    # advertise manifest/schema/token-style semantics, unless a stronger
    # stateful composite hint already matched above.
    if symbol.kind in {"class", "type"} and tokens.intersection(contract_tokens):
        return "a0_qk_constants"
    if symbol.kind in {"class", "type"} and tokens.intersection(feature_tokens):
        return "a3_og_features"
    if symbol.kind in {"class", "type"} and tokens.intersection(orchestration_tokens):
        return "a4_sy_orchestration"
    if tokens.intersection(contract_tokens):
        return "a0_qk_constants"
    if tokens.intersection(atom_tokens):
        return "a1_at_functions"
    if tokens.intersection(composite_tokens):
        return "a2_mo_composites"
    if tokens.intersection(feature_tokens):
        return "a3_og_features"
    if tokens.intersection(orchestration_tokens):
        return "a4_sy_orchestration"
    if symbol.kind == "function":
        return "a1_at_functions"
    if symbol.kind in {"class", "type"}:
        return "a2_mo_composites"
    return "a1_at_functions"

