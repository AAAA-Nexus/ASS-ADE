# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_detect_linters.py:7
# Component id: at.source.a1_at_functions.detect_linters
from __future__ import annotations

__version__ = "0.1.0"

def detect_linters(root: Path) -> list[str]:
    found: list[str] = []

    pyproject = root / "pyproject.toml"
    pyproject_raw = ""
    if pyproject.exists():
        try:
            pyproject_raw = pyproject.read_text(encoding="utf-8")
        except Exception:
            pass

    ruff_toml = root / "ruff.toml"
    if (pyproject_raw and "[tool.ruff]" in pyproject_raw) or ruff_toml.exists():
        if shutil.which("ruff"):
            found.append("ruff")

    mypy_ini = root / "mypy.ini"
    if mypy_ini.exists() or (pyproject_raw and "[tool.mypy]" in pyproject_raw):
        if shutil.which("mypy"):
            found.append("mypy")

    if pyproject_raw and "[tool.pyright]" in pyproject_raw:
        if shutil.which("pyright"):
            found.append("pyright")

    for name in (
        ".eslintrc",
        ".eslintrc.js",
        ".eslintrc.cjs",
        ".eslintrc.mjs",
        ".eslintrc.json",
        ".eslintrc.yaml",
        ".eslintrc.yml",
    ):
        if (root / name).exists():
            if shutil.which("eslint"):
                found.append("eslint")
            break

    for name in (
        ".prettierrc",
        ".prettierrc.js",
        ".prettierrc.cjs",
        ".prettierrc.mjs",
        ".prettierrc.json",
        ".prettierrc.yaml",
        ".prettierrc.yml",
        ".prettierrc.toml",
        "prettier.config.js",
        "prettier.config.cjs",
    ):
        if (root / name).exists():
            if shutil.which("prettier"):
                found.append("prettier")
            break

    if (root / "Cargo.toml").exists() and shutil.which("cargo"):
        found.append("clippy")

    if (root / "go.mod").exists() and shutil.which("go"):
        found.append("go-vet")

    return found
