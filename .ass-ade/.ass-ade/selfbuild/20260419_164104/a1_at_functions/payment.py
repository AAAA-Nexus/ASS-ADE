"""Payment command group — stub for future payment operations.

Currently a placeholder for modularization. Payment functionality
will be added in a future phase when x402 payment UX is implemented.
"""

from __future__ import annotations

import typer


def register(app: typer.Typer) -> None:
    """Register payment commands on the provided app (stub)."""
    # Placeholder for future payment commands:
    # - payment request
    # - payment status
    # - payment history
    pass
