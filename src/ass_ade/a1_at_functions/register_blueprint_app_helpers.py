"""Tier a1 — assimilated function 'register_blueprint_app'

Assimilated from: blueprint.py:225-231
"""

from __future__ import annotations


# --- assimilated symbol ---
def register_blueprint_app(parent: typer.Typer) -> None:
    """Attach the blueprint sub-app to a parent typer.

    Kept as a helper so integration tests and alternative CLI front-ends can
    mount the command without importing the top-level ``ass_ade.cli`` module.
    """
    parent.add_typer(blueprint_app, name="blueprint")

