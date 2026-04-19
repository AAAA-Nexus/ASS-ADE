# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_summary.py:7
# Component id: at.source.a1_at_functions.summary
from __future__ import annotations

__version__ = "0.1.0"

def summary(self) -> str:
    s = self.scout
    t = self.test
    d = self.doc
    dep = self.dependency

    parts = [
        f"Repo at `{self.root}` contains {s['total_files']} files"
        f" ({s['source_files']} source, {s['test_files_count']} test-related)"
        f" across {s['max_depth']} directory levels"
        f" ({s['total_size_kb']} KB total).",
    ]
    if dep["has_circular_deps"]:
        parts.append(f"Circular import detected ({len(dep['circular_deps'])} cycle(s)).")
    parts.append(
        f"Test coverage: {t['test_functions']} test functions"
        f" across {t['test_files']} test files"
        f" (ratio {t['coverage_ratio']})."
    )
    if d["doc_coverage"] < 0.5:
        parts.append(f"Documentation coverage is low ({d['doc_coverage']:.0%}).")
    else:
        parts.append(f"Documentation coverage: {d['doc_coverage']:.0%}.")
    dominant = self.tier.get("dominant_tier", "unknown")
    parts.append(f"Dominant tier: `{dominant}`.")
    return " ".join(parts)
