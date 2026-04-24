"""Tier a1 — assimilated function 'register_selfbuild_app'

Assimilated from: selfbuild.py:138-140
"""

from __future__ import annotations


# --- assimilated symbol ---
def register_selfbuild_app(parent: typer.Typer) -> None:
    """Mount ``selfbuild`` under a parent Typer app."""
    parent.add_typer(selfbuild_app, name="selfbuild")

