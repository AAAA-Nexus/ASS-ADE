# Extracted from C:/!ass-ade/src/ass_ade/local/linter.py:216
# Component id: at.source.ass_ade.run_linters
from __future__ import annotations

__version__ = "0.1.0"

def run_linters(root: Path, fix: bool = False) -> dict[str, Any]:
    linters = detect_linters(root)
    results: dict[str, Any] = {}

    for linter in linters:
        if linter == "ruff":
            results["ruff"] = run_ruff(root, fix=fix)
        elif linter == "pyright":
            results["pyright"] = run_pyright(root)
        elif linter == "mypy":
            results["mypy"] = _run_generic("mypy", ["mypy", str(root)])
        elif linter == "eslint":
            cmd = ["eslint", str(root), "--format", "json"]
            results["eslint"] = _run_generic("eslint", cmd)
        elif linter == "prettier":
            cmd = ["prettier", "--check", str(root)]
            results["prettier"] = _run_generic("prettier", cmd)
        elif linter == "clippy":
            cmd = ["cargo", "clippy", "--manifest-path", str(root / "Cargo.toml")]
            results["clippy"] = _run_generic("clippy", cmd, timeout=120)
        elif linter == "go-vet":
            cmd = ["go", "vet", "./..."]
            results["go-vet"] = _run_generic("go-vet", cmd)

    total_findings = sum(
        len(r.get("findings") or []) for r in results.values()
    )
    overall_ok = bool(linters) and all(
        r.get("ok") is True for r in results.values()
    )

    return {
        "root": str(root.resolve()),
        "linters_run": list(results.keys()),
        "results": results,
        "overall_ok": overall_ok,
        "total_findings": total_findings,
    }
