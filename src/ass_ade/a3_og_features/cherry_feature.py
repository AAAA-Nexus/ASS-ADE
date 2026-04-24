"""Tier a3 — cherry-pick feature: orchestrate scan → rank → select → manifest pipeline."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ass_ade.a0_qk_constants.cherry_types import CherryItemDict, CherryManifestDict
from ass_ade.a2_mo_composites.cherry_session import CherryPickSession


def run_cherry_pick(
    source: str | Path,
    target_root: str | Path,
    *,
    pick: str | None = None,
    actions: set[str] | None = None,
    interactive: bool = True,
    out_path: str | Path | None = None,
    console_print: bool = True,
) -> CherryManifestDict:
    """Full cherry-pick pipeline: load → rank → select → save manifest.

    Args:
        source:       Scout JSON file OR a directory to scan directly.
        target_root:  Where assimilated symbols will land (sets manifest.target_root).
        pick:         Pre-specified selection string ("1,3,5", "all", "assimilate", …).
                      When set, the interactive prompt is skipped.
        actions:      Filter candidates to this action subset before showing the menu.
                      Defaults to {assimilate, rebuild, enhance}.
        interactive:  When True and ``pick`` is None, print the menu and read stdin.
        out_path:     Override the manifest output path.
        console_print: Print status lines to stdout.

    Returns:
        The saved CherryManifestDict.
    """
    session = CherryPickSession(source, target_root)
    candidates = session.load_candidates(actions)

    if not candidates:
        if console_print:
            print("No candidates found. Try widening --action or using a different source.")
        empty: CherryManifestDict = {
            "schema_version": "ass-ade.cherry-pick/v1",
            "source_label": str(source),
            "source_root": "",
            "target_root": str(target_root),
            "selected_count": 0,
            "items": [],
        }
        return empty

    selected: list[CherryItemDict]

    if pick is not None:
        # Non-interactive: resolve from flag
        selected = session.collect_selection(pick)
        if console_print:
            print(f"Cherry-pick: {len(selected)} item(s) selected via --pick {pick!r}")
    elif interactive:
        session.present_menu()
        try:
            raw = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            if console_print:
                print("\nCancelled.")
            raw = ""
        selected = session.collect_selection(raw) if raw else []
        if console_print:
            print(f"Cherry-pick: {len(selected)} item(s) selected.")
    else:
        # Non-interactive, no --pick: default to assimilate-only
        selected = session.collect_selection("assimilate")
        if console_print:
            print(f"Cherry-pick (auto assimilate): {len(selected)} item(s).")

    manifest_path = session.save_manifest(selected, out_path)
    if console_print:
        print(f"Manifest saved: {manifest_path}")

    return {
        "schema_version": "ass-ade.cherry-pick/v1",
        "source_label": str(source),
        "source_root": str(session._report.get("repo", str(session.source)) if session._report else str(session.source)),
        "target_root": str(target_root),
        "selected_count": len(selected),
        "items": selected,
    }


def cherry_pick_summary(manifest: CherryManifestDict) -> dict[str, Any]:
    """Return a compact summary dict suitable for logging or display."""
    items = manifest.get("items", [])
    action_counts: dict[str, int] = {}
    for item in items:
        a = item["action"]
        action_counts[a] = action_counts.get(a, 0) + 1
    return {
        "selected": manifest.get("selected_count", 0),
        "source": manifest.get("source_label", ""),
        "target": manifest.get("target_root", ""),
        "action_counts": action_counts,
    }
