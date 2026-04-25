"""Tier a0 — Semantic CLI theme constants for Atomadic terminal UI.

One accent color (cyan) for structure.
Three status colors (green / yellow / red) for signals.
All styles referenced by semantic name — never hardcoded in rendering code.
"""
from __future__ import annotations

from rich import box as _box
from rich.theme import Theme

# ── Semantic Rich Theme ────────────────────────────────────────────────────────

CLI_THEME = Theme({
    # Status signals
    "ok":               "bold green",
    "warn":             "bold yellow",
    "fail":             "bold red",
    "skip":             "dim",
    # Structure / hierarchy
    "heading":          "bold cyan",
    "muted":            "dim white",
    "path":             "italic dim",
    "version":          "bold white",
    "accent":           "cyan",
    "label":            "bold white",
    # Verdict (reversed for maximum visual weight — one glance)
    "verdict.pass":     "bold green reverse",
    "verdict.warn":     "bold yellow reverse",
    "verdict.fail":     "bold red reverse",
    # Tier identity colors
    "tier.a0":          "cyan",
    "tier.a1":          "green",
    "tier.a2":          "yellow",
    "tier.a3":          "magenta",
    "tier.a4":          "blue",
    # Impact levels (enhance command)
    "impact.high":      "bold red",
    "impact.medium":    "bold yellow",
    "impact.low":       "bold green",
    # Grade / score colors (eco-scan, certify)
    "grade.a":          "bold green",
    "grade.b":          "bold cyan",
    "grade.c":          "bold yellow",
    "grade.d":          "bold magenta",
    "grade.f":          "bold red",
})

# ── Box style guide ────────────────────────────────────────────────────────────
# ROUNDED     → default panels, section containers
# HEAVY_HEAD  → command header panels (authoritative, operator feel)
# DOUBLE      → formal certification / audit output
# MINIMAL     → inner tables (alignment without border weight)

BOX_DEFAULT  = _box.ROUNDED
BOX_HEADER   = _box.HEAVY_HEAD
BOX_FORMAL   = _box.DOUBLE
BOX_MINIMAL  = _box.MINIMAL

# ── Icon system ────────────────────────────────────────────────────────────────
# Status meaning is always carried by icon + label, not color alone.
# Output must be readable in monochrome.

ICON_OK      = "[ok]✓[/ok]"
ICON_WARN    = "[warn]⚠[/warn]"
ICON_FAIL    = "[fail]✗[/fail]"
ICON_SKIP    = "[skip]─[/skip]"
ICON_INFO    = "[accent]·[/accent]"
ICON_RUN     = "[accent]▶[/accent]"
ICON_DOT_OK  = "[ok]●[/ok]"
ICON_DOT_ERR = "[fail]●[/fail]"
ICON_DOT_WRN = "[warn]●[/warn]"

# ── Tier color map ─────────────────────────────────────────────────────────────

TIER_COLORS: dict[str, str] = {
    "a0_qk_constants":     "tier.a0",
    "a1_at_functions":     "tier.a1",
    "a2_mo_composites":    "tier.a2",
    "a3_og_features":      "tier.a3",
    "a4_sy_orchestration": "tier.a4",
}

# ── Grade helpers ──────────────────────────────────────────────────────────────

GRADE_STYLES: dict[str, str] = {
    "A": "grade.a",
    "B": "grade.b",
    "C": "grade.c",
    "D": "grade.d",
    "F": "grade.f",
}

IMPACT_STYLES: dict[str, str] = {
    "high":   "impact.high",
    "medium": "impact.medium",
    "low":    "impact.low",
}


def score_style(score: int) -> str:
    """Return the semantic style name for a 0–100 compliance score."""
    if score >= 90:
        return "grade.a"
    if score >= 75:
        return "grade.b"
    if score >= 60:
        return "grade.c"
    if score >= 40:
        return "grade.d"
    return "grade.f"


def verdict_style(passed: bool, has_warnings: bool = False) -> str:
    """Return the verdict style name for a boolean pass/fail result."""
    if passed and not has_warnings:
        return "verdict.pass"
    if passed and has_warnings:
        return "verdict.warn"
    return "verdict.fail"
