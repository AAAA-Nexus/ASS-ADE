"""Tier a3 — write ``API_INVENTORY.md`` into a materialized rebuild root."""

from __future__ import annotations

from pathlib import Path

from ass_ade.a1_at_functions.api_inventory_emit import (
    build_api_inventory_markdown,
    collect_public_python_symbols,
)

API_INVENTORY_REPORT_NAME = "API_INVENTORY.md"


def emit_api_inventory(target_root: Path, out_path: Path | None = None) -> Path:
    """Emit ``API_INVENTORY.md`` for ``target_root``; returns the written path.

    When ``out_path`` is None, writes to ``target_root / API_INVENTORY.md``.
    """
    symbols = collect_public_python_symbols(target_root)
    text = build_api_inventory_markdown(symbols)
    destination = out_path if out_path is not None else (target_root / API_INVENTORY_REPORT_NAME)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(text, encoding="utf-8")
    return destination
