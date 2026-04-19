# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_eco_scan.py:7
# Component id: at.source.a1_at_functions.eco_scan
from __future__ import annotations

__version__ = "0.1.0"

def eco_scan(
    path: Path = typer.Argument(Path("."), help="Folder to scan."),
    json_out: bool = typer.Option(False, "--json", help="Print result as JSON."),
    out: Path | None = typer.Option(None, "--out", "-o", help="Write ECO_SCAN_REPORT.md here."),
) -> None:
    """Run a monadic compliance check on any codebase.

    Evaluates the codebase against the Atomadic 5-tier monadic architecture
    (qk → at → mo → og → sy). Reports tier distribution, boundary violations,
    circular dependencies, test coverage, and documentation gaps.

    Produces a compliance score (0-100) and actionable recommendations.
    """
    import json as _json
    import subprocess as _sp
    import sys as _sys
    from ass_ade.recon import run_parallel_recon
    from ass_ade.local.linter import run_linters

    target = path.resolve()
    if not target.exists():
        console.print(f"[red]Path does not exist:[/red] {target}")
        raise typer.Exit(code=1)

    # ── External script path (when atomadic-ecosystem is installed) ───────────
    _eco_root = os.environ.get("ATOMADIC_ECOSYSTEM_ROOT", "")
    if _eco_root:
        _eco_script = Path(_eco_root) / "sy_manifold" / "sy_eco_scan.py"
        if _eco_script.exists():
            cmd: list[str] = [_sys.executable, str(_eco_script), str(target)]
            if json_out:
                cmd.append("--json")
            if out:
                cmd += ["--out", str(out)]
            _result = _sp.run(cmd)
            raise typer.Exit(code=_result.returncode)
        else:
            console.print(
                f"[dim]ATOMADIC_ECOSYSTEM_ROOT set but sy_eco_scan.py not found at {_eco_script} — using built-in.[/dim]"
            )

    # ── Built-in fallback ─────────────────────────────────────────────────────
    console.print(f"[bold]Eco-scanning[/bold] {target}")
    console.print("[dim]Running 5 parallel recon agents…[/dim]")

    report = run_parallel_recon(target)

    # ── Compliance scoring (0–100) ────────────────────────────────────────────
    score = 100
    issues: list[str] = []

    # Tier violations: -5 each, cap at -30
    violations = report.tier.get("tier_violations", [])
    tier_penalty = min(5 * len(violations), 30)
    score -= tier_penalty
    for v in violations:
        issues.append(f"Tier boundary violation: {v}")

    # Circular dependencies: -10 per cycle, cap at -20
    if report.dependency.get("has_circular_deps"):
        n_cycles = len(report.dependency.get("circular_deps", []))
        score -= min(10 * n_cycles, 20)
        issues.append(f"Circular imports detected ({n_cycles} cycle(s))")

    # Test coverage: -15 if below 0.15
    cov = float(report.test.get("coverage_ratio", 0))
    if cov < 0.15:
        score -= 15
        issues.append(f"Test coverage critically low ({cov:.0%})")
    elif cov < 0.30:
        score -= 7
        issues.append(f"Test coverage below 30% ({cov:.0%})")

    # Doc coverage: -10 if below 30%
    doc_cov = report.doc.get("doc_coverage", 0.0)
    if doc_cov < 0.30:
        score -= 10
        issues.append(f"Documentation coverage low ({doc_cov:.0%})")

    # Linter: run ruff; -5 if it finds any errors
    console.print("[dim]Running linter checks…[/dim]")
    lint_result = run_linters(target)
    total_lint = lint_result.get("total_findings", 0)
    if total_lint > 0:
        score -= min(total_lint // 10, 10)
        issues.append(f"Linter: {total_lint} finding(s)")

    # ── Standalone naming + cross-tier import checks (no external tools needed) ─
    import ast as _ast

    _TIER_ORDER_ECO: dict[str, int] = {"qk": 0, "at": 1, "mo": 2, "og": 3, "sy": 4}
    _IGNORE_DIRS_ECO = {".venv", "venv", "__pycache__", ".git", ".tox", "node_modules", "dist", "build"}
    _SKIP_STEMS_ECO = {"__init__", "__main__", "conftest"}

    def _iter_py_eco(root: Path) -> list[Path]:
        result: list[Path] = []
        for f in root.rglob("*.py"):
            if not any(part in _IGNORE_DIRS_ECO for part in f.parts):
                result.append(f)
        return result

    def _parse_imports_eco(f: Path) -> list[str]:
        try:
            tree = _ast.parse(f.read_text(encoding="utf-8", errors="replace"))
        except SyntaxError:
            return []
        names: list[str] = []
        for node in _ast.walk(tree):
            if isinstance(node, _ast.Import):
                for alias in node.names:
                    names.append(alias.name.split(".")[0])
            elif isinstance(node, _ast.ImportFrom):
                if node.module:
                    names.append(node.module.split(".")[0])
        return names

    py_files_eco = _iter_py_eco(target)
    unnamed_eco: list[str] = []
    stem_to_tier_eco: dict[str, str] = {}
    for _f in py_files_eco:
        _stem = _f.stem.lower()
        if _stem in _SKIP_STEMS_ECO or _f.name.startswith("test_") or _f.name.endswith("_test.py"):
            continue
        _matched = next((t for t in _TIER_ORDER_ECO if _stem.startswith(t + "_")), None)
        if _matched:
            stem_to_tier_eco[_f.stem] = _matched
        else:
            try:
                unnamed_eco.append(_f.relative_to(target).as_posix())
            except ValueError:
                unnamed_eco.append(_f.name)

    _named_count = len(stem_to_tier_eco)
    _total_scannable = _named_count + len(unnamed_eco)
    if _total_scannable > 0 and _named_count > 0:
        _naming_pct = _named_count / _total_scannable
        if _naming_pct < 0.5:
            score -= 5
            issues.append(
                f"Naming: {len(unnamed_eco)} file(s) lack tier prefix (qk_/at_/mo_/og_/sy_) "
                f"— only {_naming_pct:.0%} follow the convention"
            )

    cross_tier: list[str] = []
    for _f in py_files_eco:
        _tier = stem_to_tier_eco.get(_f.stem)
        if _tier is None:
            continue
        for _imp in _parse_imports_eco(_f):
            _imported_tier = stem_to_tier_eco.get(_imp)
            if _imported_tier and _TIER_ORDER_ECO.get(_imported_tier, 0) > _TIER_ORDER_ECO.get(_tier, 0):
                try:
                    _rel = _f.relative_to(target).as_posix()
                except ValueError:
                    _rel = _f.name
                cross_tier.append(f"{_rel} ({_tier}) imports {_imp} ({_imported_tier})")
    if cross_tier:
        score -= min(5 * len(cross_tier), 15)
        for _ct in cross_tier[:5]:
            issues.append(f"Cross-tier import: {_ct}")
        if len(cross_tier) > 5:
            issues.append(f"… and {len(cross_tier) - 5} more cross-tier import(s)")
    else:
        cross_tier = []

    score = max(score, 0)
    grade = (
        "A" if score >= 90 else
        "B" if score >= 75 else
        "C" if score >= 60 else
        "D" if score >= 40 else
        "F"
    )

    tier_dist = report.tier.get("tier_distribution", {})

    if json_out:
        payload = {
            "root": str(target),
            "score": score,
            "grade": grade,
            "tier_distribution": tier_dist,
            "violations": violations,
            "cross_tier_imports": cross_tier,
            "naming_unnamed": unnamed_eco[:20],
            "circular_deps": report.dependency.get("circular_deps", []),
            "test_coverage": cov,
            "doc_coverage": doc_cov,
            "lint_findings": total_lint,
            "issues": issues,
            "recommendations": report.recommendations,
        }
        _print_json(payload)
        return

    # ── Markdown report ───────────────────────────────────────────────────────
    score_color = "green" if score >= 75 else "yellow" if score >= 50 else "red"
    console.print(f"\n[bold]Monadic Compliance Score:[/bold] [{score_color}]{score}/100 (Grade {grade})[/{score_color}]")

    # Tier table
    if tier_dist:
        t = Table(title="Tier Distribution", show_header=True)
        t.add_column("Tier", style="bold")
        t.add_column("Files", justify="right")
        for tier_name, count in sorted(tier_dist.items()):
            t.add_row(tier_name, str(count))
        console.print(t)

    if violations:
        console.print(f"\n[yellow]Tier Violations ({len(violations)})[/yellow]")
        for v in violations[:10]:
            console.print(f"  • {v}")
        if len(violations) > 10:
            console.print(f"  … and {len(violations) - 10} more")

    if cross_tier:
        console.print(f"\n[yellow]Cross-Tier Imports ({len(cross_tier)})[/yellow]")
        for ct in cross_tier[:5]:
            console.print(f"  • {ct}")
        if len(cross_tier) > 5:
            console.print(f"  … and {len(cross_tier) - 5} more")

    if issues:
        console.print(f"\n[bold]Findings[/bold]")
        for issue in issues:
            console.print(f"  [yellow]⚠[/yellow]  {issue}")
    else:
        console.print("\n[green]No compliance issues found.[/green]")

    if report.recommendations:
        console.print(f"\n[bold]Recommendations[/bold]")
        for rec in report.recommendations:
            console.print(f"  {rec}")

    # Write to file if requested
    if out:
        md_lines = [
            f"# ECO-SCAN REPORT",
            f"",
            f"**Path:** `{target}`  ",
            f"**Score:** {score}/100 (Grade {grade})",
            f"",
            f"## Tier Distribution",
            "",
        ]
        for tier_name, count in sorted(tier_dist.items()):
            md_lines.append(f"- `{tier_name}`: {count}")
        if violations:
            md_lines += ["", f"## Tier Violations", ""]
            for v in violations:
                md_lines.append(f"- {v}")
        if cross_tier:
            md_lines += ["", f"## Cross-Tier Imports", ""]
            for ct in cross_tier:
                md_lines.append(f"- {ct}")
        if issues:
            md_lines += ["", f"## Findings", ""]
            for issue in issues:
                md_lines.append(f"- {issue}")
        if report.recommendations:
            md_lines += ["", f"## Recommendations", ""]
            for rec in report.recommendations:
                md_lines.append(f"- {rec}")
        out.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
        console.print(f"\n[dim]Report written to {out}[/dim]")

    raise typer.Exit(code=0 if score >= 60 else 1)
