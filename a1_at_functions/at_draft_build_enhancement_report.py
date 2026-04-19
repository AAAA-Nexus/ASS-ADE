# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/local/enhancer.py:333
# Component id: at.source.ass_ade.build_enhancement_report
__version__ = "0.1.0"

def build_enhancement_report(root: Path) -> dict[str, Any]:
    scanners = [
        scan_missing_tests,
        scan_long_functions,
        scan_missing_docs,
        scan_security_patterns,
        scan_bare_except,
        scan_missing_type_hints,
        scan_todo_fixme,
    ]
    all_findings: list[dict[str, Any]] = []
    for scanner in scanners:
        try:
            all_findings.extend(scanner(root))
        except Exception:
            pass

    ranked = rank_findings(all_findings)

    by_impact: dict[str, int] = {"high": 0, "medium": 0, "low": 0}
    by_category: dict[str, int] = {}
    for f in ranked:
        impact = f.get("impact", "low")
        by_impact[impact] = by_impact.get(impact, 0) + 1
        cat = f.get("category", "unknown")
        by_category[cat] = by_category.get(cat, 0) + 1

    scanned = len(_walk_python_files(root))

    return {
        "root": str(root.resolve()),
        "total_findings": len(ranked),
        "by_impact": by_impact,
        "by_category": by_category,
        "findings": ranked,
        "scanned_files": scanned,
    }
