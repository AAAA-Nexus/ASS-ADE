# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_reconreport.py:5
# Component id: mo.source.ass_ade.reconreport
__version__ = "0.1.0"

class ReconReport:
    """Consolidated output from all 5 parallel recon agents."""

    root: str
    duration_ms: float
    scout: dict[str, Any]
    dependency: dict[str, Any]
    tier: dict[str, Any]
    test: dict[str, Any]
    doc: dict[str, Any]
    recommendations: list[str] = dc_field(default_factory=list)
    next_action: str = ""

    @property
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

    def to_markdown(self) -> str:
        lines = [
            f"# RECON_REPORT",
            f"",
            f"**Path:** `{self.root}`  ",
            f"**Duration:** {self.duration_ms:.0f} ms",
            f"",
            f"## Summary",
            f"",
            self.summary,
            f"",
            f"## Scout",
            f"",
            f"- Files: {self.scout['total_files']} ({self.scout['total_size_kb']} KB)",
            f"- Source files: {self.scout['source_files']}",
            f"- Max depth: {self.scout['max_depth']}",
            f"- Top-level: {', '.join(self.scout['top_level'][:10])}",
            f"",
            "**By extension:**",
        ]
        for ext, count in list(self.scout["by_extension"].items())[:8]:
            lines.append(f"  - `{ext}`: {count}")

        lines += [
            f"",
            f"## Dependencies",
            f"",
            f"- Python files: {self.dependency['python_files']}",
            f"- Unique external deps: {self.dependency['unique_external_deps']}",
            f"- Max import depth: {self.dependency['max_import_depth']}",
            f"- Circular deps: {'YES — ' + str(self.dependency['circular_deps'][:3]) if self.dependency['has_circular_deps'] else 'none'}",
            f"",
            f"## Tier Distribution",
            f"",
        ]
        for t, count in self.tier["tier_distribution"].items():
            examples = ", ".join(self.tier["tier_examples"].get(t, [])[:2])
            lines.append(f"- `{t}`: {count}" + (f" — e.g. {examples}" if examples else ""))

        if self.tier["tier_violations"]:
            lines += ["", "**Violations:**"]
            for v in self.tier["tier_violations"]:
                lines.append(f"  - {v}")

        lines += [
            f"",
            f"## Tests",
            f"",
            f"- Test files: {self.test['test_files']}",
            f"- Test functions: {self.test['test_functions']}",
            f"- Coverage ratio: {self.test['coverage_ratio']}",
            f"- Frameworks: {', '.join(self.test['frameworks']) or 'none detected'}",
            f"- Untested modules: {self.test['untested_count']}",
        ]
        if self.test["untested_modules"]:
            lines.append("")
            lines.append("**Untested (sample):**")
            for m in self.test["untested_modules"][:8]:
                lines.append(f"  - `{m}`")

        lines += [
            f"",
            f"## Documentation",
            f"",
            f"- README: {'yes' if self.doc['has_readme'] else 'MISSING'}",
            f"- Doc files: {self.doc['doc_files']}",
            f"- Public callables: {self.doc['total_public_callables']}",
            f"- Documented: {self.doc['documented_callables']} ({self.doc['doc_coverage']:.0%})",
        ]
        if self.doc["undocumented_samples"]:
            lines.append("")
            lines.append("**Missing docstrings (sample):**")
            for u in self.doc["undocumented_samples"]:
                lines.append(f"  - `{u}`")

        if self.recommendations:
            lines += ["", "## Recommendations", ""]
            for i, rec in enumerate(self.recommendations, 1):
                lines.append(f"{i}. {rec}")

        if self.next_action:
            lines += ["", f"**Next action:** {self.next_action}"]

        return "\n".join(lines) + "\n"

    def to_dict(self) -> dict[str, Any]:
        return {
            "root": self.root,
            "duration_ms": self.duration_ms,
            "summary": self.summary,
            "scout": self.scout,
            "dependency": self.dependency,
            "tier": self.tier,
            "test": self.test,
            "doc": self.doc,
            "recommendations": self.recommendations,
            "next_action": self.next_action,
        }
