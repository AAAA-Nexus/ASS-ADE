# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_render_rebuild_summary.py:7
# Component id: at.source.a1_at_functions.render_rebuild_summary
from __future__ import annotations

__version__ = "0.1.0"

def render_rebuild_summary(result: dict[str, Any]) -> str:
    """Return a human-readable rebuild summary for CLI display."""
    phases = result.get("phases", {})
    ingest = phases.get("ingest", {})
    gap = phases.get("gap_fill", {})
    mat = phases.get("materialize", {})
    audit = phases.get("audit", {})
    cert = phases.get("certificate", {})
    pkg = phases.get("package", {})
    cycles = phases.get("cycles", {})
    purity = phases.get("tier_purity", {})

    lines: list[str] = [
        f"[Phase 1] Ingest     : {ingest.get('files_scanned', 0)} files, "
        f"{ingest.get('symbols', 0)} symbols, {ingest.get('gaps', 0)} gaps",
        f"[Phase 2] Gap-Fill   : {gap.get('proposed_components', 0)} proposals",
    ]
    if phases.get("enrich"):
        e = phases["enrich"]
        lines.append(f"[Phase 3] Enrich     : {e.get('bodies_attached', 0)} bodies, "
                     f"{e.get('made_of_edges', 0)} edges")
    if cycles.get("cycle_count"):
        lines.append(f"[Phase 4] Cycles     : {cycles['cycle_count']} detected + broken")
    else:
        lines.append("[Phase 4] Cycles     : none (acyclic)")
    if purity.get("removed_edges"):
        lines.append(f"[Phase 4] Purity     : {purity['removed_edges']} violating edges removed")
    lines.append(
        f"[Phase 5] Materialize: {mat.get('written_count', 0)} components -> {mat.get('target_root', '')}"
    )
    pass_rate = audit.get("pass_rate", 0.0)
    lines.append(
        f"[Phase 6] Audit      : {audit.get('valid', 0)}/{audit.get('total', 0)} clean "
        f"({pass_rate * 100:.1f}%), "
        f"{'conformant' if audit.get('structure_conformant') else 'non-conformant'}"
    )
    if cert.get("certificate_sha256"):
        lines.append(
            f"[Cert]    SHA-256    : {cert['certificate_sha256'][:16]}..."
        )
    if pkg.get("importable"):
        lines.append(f"[Phase 7] Package    : pip install -e {mat.get('target_root', '')}")
    elif pkg.get("error"):
        lines.append(f"[Phase 7] Package    : error — {pkg['error']}")

    return "\n".join(lines)
