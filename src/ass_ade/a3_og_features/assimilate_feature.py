"""Tier a3 — assimilate feature: orchestrate manifest → extract → tier-place → report pipeline."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ass_ade.a0_qk_constants.cherry_types import AssimilateResultDict
from ass_ade.a2_mo_composites.assimilate_runner import AssimilateRunner


def run_assimilate(
    manifest_path: str | Path,
    target_root: str | Path | None = None,
    *,
    dry_run: bool = False,
    tier_override: str | None = None,
    console_print: bool = True,
) -> list[AssimilateResultDict]:
    """Full assimilation pipeline: read manifest → extract symbols → place in tiers → report.

    Args:
        manifest_path: Path to a cherry_pick.json manifest (from ass-ade cherry-pick).
        target_root:   Override the target root from the manifest.
        dry_run:       Compute targets but write nothing to disk.
        tier_override: Force all symbols into this tier (e.g. "a1_at_functions").
        console_print: Print status lines to stdout.

    Returns:
        List of AssimilateResultDicts with status per symbol.
    """
    runner = AssimilateRunner(manifest_path, target_root, tier_override)
    manifest = runner.load()
    items = manifest.get("items", [])

    if console_print:
        mode = "[DRY RUN] " if dry_run else ""
        print(f"{mode}Assimilating {len(items)} item(s) → {runner.target_root}")

    results = runner.run_all(dry_run=dry_run)
    summary = runner.summary(results)

    if console_print:
        _print_summary(summary, dry_run=dry_run)

    return results


def _print_summary(summary: dict[str, Any], *, dry_run: bool) -> None:
    total = summary.get("total", 0)
    by_status = summary.get("by_status", {})
    prefix = "[DRY RUN] " if dry_run else ""
    print(f"\n{prefix}Assimilation complete: {total} item(s)")
    for status, count in sorted(by_status.items()):
        print(f"  {status}: {count}")

    errors = summary.get("errors", [])
    if errors:
        print("\nErrors:")
        for err in errors[:10]:
            print(f"  ✗ {err['qualname']} — {err['error']}")

    written = summary.get("written", [])
    if written:
        verb = "Would write" if dry_run else "Written"
        for item in written[:20]:
            print(f"  → {item['target_file']}  ({item['lines']} LOC, tier={item['tier']})")
        if len(written) > 20:
            print(f"  … and {len(written) - 20} more")


def assimilation_report(results: list[AssimilateResultDict]) -> dict[str, Any]:
    """Build a serialisable report dict from run_assimilate() results."""
    by_status: dict[str, list[dict[str, Any]]] = {}
    for r in results:
        by_status.setdefault(r["status"], []).append(
            {
                "qualname": r["qualname"],
                "target_file": r["target_file"],
                "tier": r["tier"],
                "lines": r["lines"],
                "error": r["error"],
            }
        )
    return {
        "schema_version": "ass-ade.assimilation-report/v1",
        "total": len(results),
        "by_status": {k: len(v) for k, v in by_status.items()},
        "items": by_status,
    }
