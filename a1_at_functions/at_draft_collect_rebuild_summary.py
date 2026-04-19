# Extracted from C:/!ass-ade/src/ass_ade/protocol/evolution.py:258
# Component id: at.source.ass_ade.collect_rebuild_summary
from __future__ import annotations

__version__ = "0.1.0"

def collect_rebuild_summary(rebuild_path: Path | None) -> dict[str, Any]:
    if rebuild_path is None:
        return {}
    root = rebuild_path.resolve()
    if not root.exists():
        return {"path": str(root), "exists": False}

    summary: dict[str, Any] = {"path": str(root), "exists": True}
    version_file = root / "VERSION"
    if version_file.exists():
        lines = version_file.read_text(encoding="utf-8").splitlines()
        if lines:
            summary["version"] = lines[0].strip()
    manifest = _read_json(root / "MANIFEST.json")
    if manifest:
        components = manifest.get("components")
        if isinstance(components, list):
            summary["component_count"] = len(components)
        tier_distribution = manifest.get("tier_distribution")
        if isinstance(tier_distribution, dict):
            summary["tier_distribution"] = tier_distribution
    cert = _certificate_summary(root / "CERTIFICATE.json")
    if cert:
        summary["certificate"] = cert
    report_path = root / "REBUILD_REPORT.md"
    if report_path.exists():
        summary["report"] = str(report_path)
    return summary
