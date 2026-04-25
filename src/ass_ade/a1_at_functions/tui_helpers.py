"""Tier a1 — Reusable Rich rendering helpers for Atomadic CLI.

All helpers return Rich renderables (Panel, Table, Rule, Text).
They never print directly — callers control when to render.

Design contract:
- command_header()  → consistent top-of-command banner
- verdict_panel()   → PASS / WARN / FAIL one-glance summary
- check_grid()      → 3-column icon|label|value table (doctor, recon, launch)
- section_rule()    → named horizontal divider between sections
- error_panel()     → standardised red error container
- findings_table()  → enhance findings with impact color + file column
- score_panel()     → eco-scan grade + score + issue count
- path_fmt()        → dim-italic path string for inline use
"""
from __future__ import annotations

from pathlib import Path
from typing import Sequence

from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table
from rich.text import Text

from ass_ade.a0_qk_constants.cli_theme import (
    BOX_DEFAULT,
    BOX_FORMAL,
    BOX_HEADER,
    BOX_MINIMAL,
    CLI_THEME,
    GRADE_STYLES,
    ICON_FAIL,
    ICON_INFO,
    ICON_OK,
    ICON_RUN,
    ICON_SKIP,
    ICON_WARN,
    IMPACT_STYLES,
    TIER_COLORS,
    score_style,
    verdict_style,
)


# ── Console factory ────────────────────────────────────────────────────────────

def make_themed_console(**kwargs) -> Console:
    """Return a Console wired to the Atomadic CLI_THEME."""
    return Console(theme=CLI_THEME, **kwargs)


# ── Command header panel ───────────────────────────────────────────────────────

def command_header(
    title: str,
    subtitle: str = "",
    ascii_art: str = "",
    version: str = "v1.0.0",
) -> Panel:
    """Top-of-command banner panel (HEAVY_HEAD box, cyan border).

    Used at the start of doctor, eco-scan, certify, etc.
    """
    lines: list[str] = []
    if ascii_art:
        lines.append(f"[heading]{ascii_art}[/heading]\n")
    lines.append(f"[heading]{title}[/heading]")
    if subtitle:
        lines.append(f"[muted]{subtitle}[/muted]")
    content = "\n".join(lines)
    return Panel(
        content,
        box=BOX_HEADER,
        border_style="accent",
        padding=(1, 2),
        subtitle=f"[muted]{version}[/muted]",
    )


# ── Verdict panel ──────────────────────────────────────────────────────────────

def verdict_panel(
    verdict: str,
    detail: str = "",
    *,
    passed: bool = True,
    has_warnings: bool = False,
) -> Panel:
    """One-glance PASS / WARN / FAIL panel — eyes land here first.

    Args:
        verdict:      Short label, e.g. "All systems operational"
        detail:       Optional secondary line (muted)
        passed:       Whether the overall result is passing
        has_warnings: Degrades a pass to a warn verdict
    """
    style_name = verdict_style(passed, has_warnings)
    icon = ICON_OK if passed and not has_warnings else (ICON_WARN if passed else ICON_FAIL)
    label = "PASS" if passed and not has_warnings else ("WARN" if passed else "FAIL")

    text = Text()
    text.append(f"  {label}  ", style=style_name)
    text.append(f"  {verdict}", style="label")
    if detail:
        text.append(f"\n  [muted]{detail}[/muted]")

    border = "green" if passed and not has_warnings else ("yellow" if passed else "red")
    return Panel(
        Align.left(text),
        box=BOX_DEFAULT,
        border_style=border,
        padding=(0, 1),
    )


# ── Check grid (health-check rows) ────────────────────────────────────────────

def check_grid(
    rows: Sequence[tuple[str, str, str]],
    *,
    col_widths: tuple[int, int] = (22, 0),
) -> Table:
    """Three-column alignment grid: icon | label | value.

    Each row is (status, label, value) where status is one of:
      "ok" | "warn" | "fail" | "skip" | "info" | "run"

    Returns a Table (no border) suitable for embedding in a Panel.
    """
    icon_map = {
        "ok":   ICON_OK,
        "warn": ICON_WARN,
        "fail": ICON_FAIL,
        "skip": ICON_SKIP,
        "info": ICON_INFO,
        "run":  ICON_RUN,
    }
    grid = Table.grid(padding=(0, 1))
    grid.add_column(width=3, no_wrap=True)
    grid.add_column(width=col_widths[0], no_wrap=True)
    grid.add_column(style="muted" if col_widths[1] == 0 else "")
    for status, label, value in rows:
        icon = icon_map.get(status, ICON_INFO)
        grid.add_row(icon, f"[label]{label}[/label]", value)
    return grid


# ── Section rule ───────────────────────────────────────────────────────────────

def section_rule(title: str = "", *, style: str = "dim accent") -> Rule:
    """Horizontal Rule with an optional section heading label."""
    if title:
        return Rule(f"[heading]{title}[/heading]", style=style)
    return Rule(style=style)


# ── Error panel ───────────────────────────────────────────────────────────────

def error_panel(message: str, title: str = "Error") -> Panel:
    """Standardised error container — red border, clear message."""
    return Panel(
        f"[fail]{message}[/fail]",
        title=f"[fail]{title}[/fail]",
        border_style="red",
        box=BOX_DEFAULT,
        padding=(0, 1),
    )


def warn_panel(message: str, title: str = "Warning") -> Panel:
    """Standardised warning container — yellow border."""
    return Panel(
        f"[warn]{message}[/warn]",
        title=f"[warn]{title}[/warn]",
        border_style="yellow",
        box=BOX_DEFAULT,
        padding=(0, 1),
    )


# ── Score / grade display ──────────────────────────────────────────────────────

def score_panel(
    score: int,
    grade: str,
    label: str = "Monadic Compliance",
    issues: int = 0,
) -> Panel:
    """Score + grade display for eco-scan output.

    Renders as: [GRADE A]  label  score/100  — N issues
    """
    grade_style = GRADE_STYLES.get(grade, "version")
    s_style = score_style(score)

    text = Text()
    text.append(f"  {grade}  ", style=grade_style + " reverse")
    text.append("  ")
    text.append(f"{label}", style="label")
    text.append("  ")
    text.append(f"{score}/100", style=s_style)
    if issues:
        text.append(f"  ·  {issues} issue{'s' if issues != 1 else ''}", style="muted")

    border_color = (
        "green" if score >= 75
        else "yellow" if score >= 50
        else "red"
    )
    return Panel(
        Align.left(text),
        box=BOX_DEFAULT,
        border_style=border_color,
        padding=(0, 1),
    )


# ── Findings table (enhance) ──────────────────────────────────────────────────

def findings_table(
    findings: list[dict],
    *,
    total: int = 0,
    shown: int = 0,
) -> Panel:
    """Enhancement findings rendered as a Panel-wrapped table.

    Each finding dict must have: id, impact, effort, category, title, file (opt), line (opt).
    """
    title_str = f"Enhancement Opportunities  [muted]{shown or len(findings)} shown"
    if total and total > (shown or len(findings)):
        title_str += f" of {total}[/muted]"
    else:
        title_str += "[/muted]"

    t = Table(box=BOX_MINIMAL, show_header=True, header_style="heading", expand=True)
    t.add_column("ID",       width=4,  justify="right", style="muted")
    t.add_column("Impact",   width=8)
    t.add_column("Effort",   width=8,  style="muted")
    t.add_column("Category", width=18, style="muted")
    t.add_column("Title",    ratio=3)
    t.add_column("File",     ratio=2,  style="path")

    for f in findings:
        impact    = f.get("impact", "low")
        imp_style = IMPACT_STYLES.get(impact, "version")
        line      = f.get("line")
        loc       = f.get("file", "")
        if line:
            loc = f"{loc}:{line}"
        t.add_row(
            str(f.get("id", "")),
            f"[{imp_style}]{impact}[/{imp_style}]",
            f.get("effort", ""),
            f.get("category", ""),
            f.get("title", ""),
            loc,
        )

    high_count = sum(1 for f in findings if f.get("impact") == "high")
    border = "red" if high_count > 0 else "yellow"
    return Panel(t, title=f"[heading]{title_str}", border_style=border, box=BOX_DEFAULT)


# ── Tier distribution table ────────────────────────────────────────────────────

def tier_table(tier_dist: dict[str, int]) -> Panel:
    """Tier distribution table for eco-scan output."""
    t = Table(box=BOX_MINIMAL, show_header=True, header_style="heading")
    t.add_column("Tier",  style="label")
    t.add_column("Files", justify="right", style="version")
    t.add_column("",      width=20)

    total_files = sum(tier_dist.values()) or 1
    for tier_name in sorted(tier_dist):
        count = tier_dist[tier_name]
        pct   = count / total_files
        bar   = "█" * int(pct * 15)
        color = TIER_COLORS.get(tier_name, "accent")
        t.add_row(
            f"[{color}]{tier_name}[/{color}]",
            str(count),
            f"[{color}]{bar}[/{color}]",
        )
    return Panel(t, title="[heading]Tier Distribution[/heading]", border_style="accent", box=BOX_DEFAULT)


# ── Issues list panel ─────────────────────────────────────────────────────────

def issues_panel(issues: list[str], title: str = "Findings") -> Panel:
    """Bulleted issues list inside a yellow panel."""
    lines = "\n".join(f"  {ICON_WARN}  {issue}" for issue in issues)
    return Panel(
        lines or f"  {ICON_OK}  No issues found.",
        title=f"[heading]{title}[/heading]",
        border_style="green" if not issues else "yellow",
        box=BOX_DEFAULT,
        padding=(0, 1),
    )


# ── Certificate panel ─────────────────────────────────────────────────────────

def certificate_panel(cert: dict) -> Panel:
    """Formal certificate summary (DOUBLE box for gravitas)."""
    rows: list[tuple[str, str, str]] = []
    if root := cert.get("root"):
        rows.append(("info", "Root", f"[path]{root}[/path]"))
    if version := cert.get("version"):
        rows.append(("info", "Version", f"[version]{version}[/version]"))
    if file_count := cert.get("file_count"):
        rows.append(("info", "Files hashed", str(file_count)))
    if signed_by := cert.get("signed_by"):
        rows.append(("ok", "Signed by", signed_by))
    elif cert.get("valid") is False:
        rows.append(("warn", "Signature", "Local-only (not third-party verifiable)"))
    if issued_at := cert.get("issued_at") or cert.get("created_at"):
        rows.append(("info", "Issued at", str(issued_at)[:19]))
    if conformance := cert.get("conformance"):
        rows.append(("info", "Conformance", str(conformance)))

    grid = check_grid(rows)
    signed = bool(cert.get("signed_by"))
    return Panel(
        grid,
        title="[heading]CERTIFICATE[/heading]",
        border_style="green" if signed else "yellow",
        box=BOX_FORMAL,
        padding=(1, 2),
    )


# ── Linter results grid ────────────────────────────────────────────────────────

def linter_grid(results: dict) -> Panel:
    """Per-linter status grid for lint command."""
    rows: list[tuple[str, str, str]] = []
    for linter_name, res in results.items():
        ok      = res.get("ok", False)
        errors  = res.get("error_count", 0)
        warns   = res.get("warning_count", 0)
        count   = errors + warns
        status  = "ok" if ok else "fail"
        detail  = (
            f"[version]{count}[/version] finding{'s' if count != 1 else ''}"
            if count else "[ok]clean[/ok]"
        )
        rows.append((status, linter_name, detail))
    grid = check_grid(rows, col_widths=(18, 0))
    total = sum(r.get("error_count", 0) + r.get("warning_count", 0) for r in results.values())
    border = "red" if total > 0 else "green"
    return Panel(grid, title="[heading]Linter Results[/heading]", border_style=border, box=BOX_DEFAULT)


# ── Path formatting ────────────────────────────────────────────────────────────

def path_fmt(p: str | Path, *, stem_only: bool = False) -> str:
    """Return a dim-italic markup string for a path."""
    display = Path(p).name if stem_only else str(p)
    return f"[path]{display}[/path]"


# ── Recon report panel ────────────────────────────────────────────────────────

def recon_summary_panel(report_md: str, duration_ms: float) -> Panel:
    """Wrap a recon markdown report in a command panel."""
    from rich.markdown import Markdown
    content = Markdown(report_md)
    return Panel(
        content,
        title="[heading]Reconnaissance Report[/heading]",
        subtitle=f"[muted]{duration_ms:.0f} ms  ·  5 agents[/muted]",
        border_style="accent",
        box=BOX_DEFAULT,
        padding=(1, 2),
    )
