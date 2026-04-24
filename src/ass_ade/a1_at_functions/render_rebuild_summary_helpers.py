"""Tier a1 — assimilated function 'render_rebuild_summary'

Assimilated from: rebuild/orchestrator.py:491-560
"""

from __future__ import annotations


# --- assimilated symbol ---
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

    forge = phases.get("forge", {})
    conflicts = phases.get("conflicts", {})
    import_rw = phases.get("import_rewrite", {})

    lines: list[str] = [
        f"[Phase 1] Ingest     : {ingest.get('files_scanned', 0)} files, "
        f"{ingest.get('symbols', 0)} symbols, {ingest.get('gaps', 0)} gaps",
    ]
    if conflicts:
        n = conflicts.get("conflict_count", 0)
        tag = "clean" if conflicts.get("clean") else f"{n} conflict(s) — last_wins"
        lines.append(f"[Phase 1b] Conflicts : {tag}")
    lines += [
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
        f"[Phase 5] Materialize: {mat.get('written_count', 0)} components "
        f"({mat.get('written_modules', 0)} modules) -> {mat.get('target_root', '')}"
    )
    if import_rw and import_rw.get("files_checked", 0) > 0:
        n_rw = import_rw.get("files_rewritten", 0)
        n_ch = import_rw.get("total_changes", 0)
        tag = f"{n_rw} files, {n_ch} import(s) fixed" if n_rw else "no changes needed"
        lines.append(f"[Phase 5b] ImptRewrite: {tag}")
    if forge and forge.get("tasks", 0) > 0:
        if forge.get("error"):
            lines.append(f"[Phase 5c] Forge     : ERROR — {forge['error']}")
        else:
            lines.append(
                f"[Phase 5c] Forge     : {forge.get('applied', 0)}/{forge.get('tasks', 0)} fixes applied "
                f"({forge.get('files_modified', 0)} files) — model={forge.get('model', '?')}"
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

