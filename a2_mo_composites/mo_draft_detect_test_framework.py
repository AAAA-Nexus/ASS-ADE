# Extracted from C:/!ass-ade/src/ass_ade/local/docs_engine.py:177
# Component id: mo.source.ass_ade.detect_test_framework
from __future__ import annotations

__version__ = "0.1.0"

def detect_test_framework(root: Path) -> str | None:
    if (root / "pytest.ini").exists():
        return "pytest"

    pyproject = root / "pyproject.toml"
    if pyproject.exists():
        try:
            raw = pyproject.read_text(encoding="utf-8")
            if "[tool.pytest" in raw:
                return "pytest"
        except Exception:
            pass

    for name in ("jest.config.js", "jest.config.ts", "jest.config.mjs", "jest.config.cjs"):
        if (root / name).exists():
            return "jest"

    cargo = root / "Cargo.toml"
    if cargo.exists():
        try:
            raw = cargo.read_text(encoding="utf-8")
            if "[dev-dependencies]" in raw:
                return "cargo-test"
        except Exception:
            pass

    if (root / "go.mod").exists():
        return "go-test"

    return None
