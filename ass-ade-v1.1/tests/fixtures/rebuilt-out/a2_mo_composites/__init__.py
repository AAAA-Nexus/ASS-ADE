"""Auto-generated tier package.

This package exposes discovery helpers instead of eagerly importing
every emitted module at import time.
"""

from __future__ import annotations

from pathlib import Path
from pkgutil import iter_modules


def available_modules() -> list[str]:
    """Return the emitted module names present in this tier package."""
    package_dir = Path(__file__).resolve().parent
    return sorted(
        module.name
        for module in iter_modules([str(package_dir)])
        if not module.name.startswith("_")
    )


__all__ = ["available_modules"]
