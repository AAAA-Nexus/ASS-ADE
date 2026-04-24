"""Tier a3 — assimilation statistics.

Rolls up scout reports, cherry-pick manifests, and assimilation reports into
dashboard-ready summaries. The Assimilate tab uses this to power:
  - Stats strip: total repos scouted, symbols indexed, cherry-picks applied
  - Cherry-pick candidate table with filter/sort
  - Action distribution chart (assimilate/enhance/rebuild/skip)
  - Opportunity highlights from LLM scout synthesis
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any


_STATS_DIRNAME = ".ass-ade"


def _read_json(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def collect_scout_reports(root: Path) -> list[dict]:
    """Return all scout-*.json files under <root>/.ass-ade/, newest first."""
    stats_dir = root / _STATS_DIRNAME
    if not stats_dir.is_dir():
        return []
    reports: list[dict] = []
    for p in sorted(stats_dir.glob("scout*.json")):
        data = _read_json(p)
        if data is None:
            continue
        data["_file"] = str(p)
        data["_filename"] = p.name
        try:
            data["_mtime"] = p.stat().st_mtime
        except OSError:
            data["_mtime"] = 0.0
        reports.append(data)
    return sorted(reports, key=lambda r: r.get("_mtime", 0.0), reverse=True)


def collect_cherry_manifests(root: Path) -> list[dict]:
    """Return cherry_pick*.json manifests under <root>/.ass-ade/."""
    stats_dir = root / _STATS_DIRNAME
    if not stats_dir.is_dir():
        return []
    manifests: list[dict] = []
    for p in sorted(stats_dir.glob("cherry_pick*.json")):
        data = _read_json(p)
        if data is None:
            continue
        data["_file"] = str(p)
        try:
            data["_mtime"] = p.stat().st_mtime
        except OSError:
            data["_mtime"] = 0.0
        manifests.append(data)
    return manifests


def collect_assimilation_reports(root: Path) -> list[dict]:
    """Return assimilation report JSONs (*.report.json or assimilate-*.json)."""
    stats_dir = root / _STATS_DIRNAME
    if not stats_dir.is_dir():
        return []
    found: list[dict] = []
    for pattern in ("assimilate*.json", "*.report.json"):
        for p in sorted(stats_dir.glob(pattern)):
            data = _read_json(p)
            if data is None:
                continue
            data["_file"] = str(p)
            try:
                data["_mtime"] = p.stat().st_mtime
            except OSError:
                data["_mtime"] = 0.0
            found.append(data)
    return found


def aggregate_assimilation_stats(
    scout_reports: list[dict],
    cherry_manifests: list[dict] | None = None,
    assimilation_reports: list[dict] | None = None,
) -> dict[str, Any]:
    """Roll every kind of artifact into one dashboard-friendly dict."""
    cherry_manifests = cherry_manifests or []
    assimilation_reports = assimilation_reports or []

    action_totals: Counter[str] = Counter()
    total_symbols = 0
    total_tested = 0
    repos_scouted = len(scout_reports)
    opportunities: list[str] = []
    risks: list[str] = []

    for report in scout_reports:
        tm = report.get("target_map") or {}
        for action, n in (tm.get("action_counts") or {}).items():
            try:
                action_totals[str(action)] += int(n)
            except (TypeError, ValueError):
                pass
        sym = report.get("symbol_summary") or {}
        try:
            total_symbols += int(sym.get("symbols") or 0)
            total_tested += int(sym.get("tested_symbols") or 0)
        except (TypeError, ValueError):
            pass
        llm = report.get("llm") or {}
        analysis = llm.get("analysis") if isinstance(llm.get("analysis"), dict) else {}
        for op in (analysis.get("opportunities") or [])[:4]:
            opportunities.append(str(op)[:160])
        for r in (analysis.get("risks") or [])[:3]:
            risks.append(str(r)[:160])

    cherry_picked = 0
    for manifest in cherry_manifests:
        items = manifest.get("items") or manifest.get("picks") or manifest.get("selections") or []
        if isinstance(items, list):
            cherry_picked += len(items)

    assimilated_count = 0
    assimilation_errors = 0
    tier_distribution: Counter[str] = Counter()
    for report in assimilation_reports:
        results = report.get("results") or report.get("written") or []
        if isinstance(results, list):
            assimilated_count += len(results)
            for r in results:
                if isinstance(r, dict):
                    tier = r.get("tier") or r.get("landed_tier")
                    if tier:
                        tier_distribution[str(tier)] += 1
        errors = report.get("errors") or []
        if isinstance(errors, list):
            assimilation_errors += len(errors)

    return {
        "repos_scouted": repos_scouted,
        "total_symbols": total_symbols,
        "total_tested_symbols": total_tested,
        "cherry_picked": cherry_picked,
        "assimilated": assimilated_count,
        "assimilation_errors": assimilation_errors,
        "action_totals": dict(action_totals),
        "tier_distribution": dict(tier_distribution),
        "opportunities_highlight": opportunities[:12],
        "risks_highlight": risks[:8],
    }


def cherry_pick_candidates(
    scout_reports: list[dict],
    action: str | None = None,
    min_confidence: float = 0.0,
    limit: int = 200,
) -> list[dict]:
    """Flatten target-map targets across reports, filterable by action + confidence.

    Used by the dashboard Assimilate tab to show a checkbox-pickable table.
    """
    out: list[dict] = []
    for report in scout_reports:
        tm = report.get("target_map") or {}
        for target in (tm.get("targets") or []):
            if not isinstance(target, dict):
                continue
            target_action = str(target.get("action") or "")
            if action and target_action != action:
                continue
            try:
                conf = float(target.get("confidence") or 0.0)
            except (TypeError, ValueError):
                conf = 0.0
            if conf < min_confidence:
                continue
            symbol = target.get("symbol") or {}
            if not isinstance(symbol, dict):
                symbol = {}
            out.append({
                "qualname": symbol.get("qualname") or target.get("qualname") or "?",
                "module": symbol.get("module") or "?",
                "rel_path": symbol.get("rel_path") or "",
                "kind": symbol.get("kind") or "",
                "action": target_action,
                "confidence": conf,
                "reasons": list(target.get("reasons") or []),
                "recommended_path": target.get("recommended_path") or "",
                "source_repo": report.get("repo"),
                "source_report": report.get("_filename") or Path(report.get("_file", "")).name,
            })
    out.sort(key=lambda t: (-t["confidence"], t["qualname"]))
    return out[:limit]


def summarize_for_dashboard(root: Path) -> dict[str, Any]:
    """One-shot call that gives the Assimilate tab everything it needs."""
    scouts = collect_scout_reports(root)
    cherries = collect_cherry_manifests(root)
    assimilations = collect_assimilation_reports(root)
    return {
        "stats": aggregate_assimilation_stats(scouts, cherries, assimilations),
        "scout_reports": [
            {
                "file": r.get("_filename"),
                "repo": r.get("repo"),
                "mtime": r.get("_mtime"),
                "counts": (r.get("target_map") or {}).get("action_counts"),
                "llm_status": (r.get("llm") or {}).get("status"),
            }
            for r in scouts
        ],
        "cherry_manifests": [
            {"file": Path(m.get("_file", "")).name, "mtime": m.get("_mtime"),
             "items": len((m.get("items") or m.get("picks") or m.get("selections") or []) or [])}
            for m in cherries
        ],
    }
