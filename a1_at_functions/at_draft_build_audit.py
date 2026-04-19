# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_build_audit.py:7
# Component id: at.source.a1_at_functions.build_audit
from __future__ import annotations

__version__ = "0.1.0"

def build_audit(root: Path, settings: AssAdeConfig) -> list[ProtocolAuditCheck]:
    checks: list[ProtocolAuditCheck] = []

    required_files = [
        root / "README.md",
        root / "docs" / "architecture.md",
        root / "docs" / "dev-stack.md",
        root / ".github" / "copilot-instructions.md",
        root / "pyproject.toml",
        root / "src" / "ass_ade" / "cli.py",
        root / "src" / "ass_ade" / "nexus" / "models.py",
        root / "src" / "ass_ade" / "local" / "repo.py",
        root / "tests" / "test_cli.py",
    ]
    checks.append(
        ProtocolAuditCheck(
            name="Public shell scaffold present",
            passed=all(path.exists() for path in required_files),
            detail="Checks that docs, package config, CLI, typed contracts, local utility, and tests exist.",
        )
    )

    checks.append(
        ProtocolAuditCheck(
            name="Local mode is the default",
            passed=settings.profile == "local",
            detail=f"Current profile is '{settings.profile}'. Public-safe default should remain local.",
        )
    )

    checks.append(
        ProtocolAuditCheck(
            name="Remote contract boundary preserved",
            passed=(root / "src" / "ass_ade" / "nexus" / "models.py").exists(),
            detail="Typed public-contract models should exist instead of raw backend logic in the repo.",
        )
    )

    checks.append(
        ProtocolAuditCheck(
            name="Standalone local value exists",
            passed=(root / "src" / "ass_ade" / "local" / "repo.py").exists(),
            detail="The repo should ship at least one genuinely useful local capability with no premium dependency.",
        )
    )

    checks.append(
        ProtocolAuditCheck(
            name="Protocol docs are public-safe",
            passed=(root / "docs" / "protocol.md").exists(),
            detail="The sanitized protocol should be documented without embedding private backend internals.",
        )
    )

    return checks
