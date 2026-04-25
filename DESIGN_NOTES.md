# Atomadic CLI TUI Design Notes

## What Makes Premium Developer CLIs Feel Legendary

Researched tools: lazygit, k9s, btop, gitui, Charm.sh (gum/bubbletea), Speakeasy CLI.

### Core Principles Extracted

**1. Verdict-first hierarchy**
Every command output opens with a single scannable verdict: PASS / WARN / FAIL.
Eyes land on this first. Users should never have to read the full output to know if
something worked. Current state: none of Atomadic's commands had this. Fixed in Phase 2.

**2. Spatial containment via panels**
Panels (Rich `box.ROUNDED`) act as visual containers that group related information.
Border labels replace separate heading rows. `box.HEAVY_HEAD` signals "this is the
command header." `box.DOUBLE` signals "formal output, audit quality." Never use the
same box style for everything — box style carries semantic meaning.

**3. Semantic color, not palette decoration**
One accent color for structure (cyan). Three status colors (green/yellow/red) for signals.
Colors defined in a `Theme` object, referenced by semantic names (`ok`, `warn`, `fail`,
`heading`, `muted`, `path`). Never hardcode `[red]` for structure or `[cyan]` for status.
The research rule: if the output reads in monochrome, you built it right — status should
be carried by icon + label, not color alone.

**4. Three-column grid for health checks**
```
✓  Python           3.12.3
⚠  Rich             MISSING
✓  Nexus client     connected
```
Icon (3 chars) | Label (20 chars fixed) | Value (dim/italic). This column alignment
is what creates the "engineered" optical impression. btop and k9s both use this.

**5. `Rule` dividers replace blank lines**
`console.print(Rule("[heading]Workspace[/heading]", style="dim cyan"))` adds structure
without weight. Blank lines alone create visual ambiguity — a Rule names the boundary.

**6. Path de-emphasis**
Paths compete with status signals if rendered at normal weight. Always render paths
as `[path]` (dim italic). Users who need the full path run `--verbose`.

**7. Width-responsive layout**
`console.width` determines whether to use the full 3-column layout or a compact fallback
at <80 columns. Terminal pane splitting is common; don't break at narrow widths.

**8. Spinner for any operation > 100ms**
`console.status("[muted]Scanning...[/muted]", spinner="dots")` eliminates "is this hung?"
anxiety. Remote checks, linting, recon — all should use spinners.

**9. Footer as context menu**
Show only the actionable next step, not a dump of all options. If lint passes:
`[muted]All clean — run ass-ade certify . to record a snapshot[/muted]`
If lint fails: `[warn]Run: ass-ade enhance . to see improvement recommendations[/warn]`

**10. The screenshot test**
After rendering, ask: "Would someone screenshot this and share it on Twitter?" If no,
iterate. The answer should be yes for doctor, eco-scan, enhance, and the chat greeting.

---

## Atomadic Design Decisions

### Color Palette (semantic)
| Name | Style | Use |
|------|-------|-----|
| `ok` | bold green | Passed checks, success |
| `warn` | bold yellow | Degraded but usable, warnings |
| `fail` | bold red | Failed checks, errors |
| `skip` | dim | Not applicable, skipped |
| `heading` | bold cyan | Section titles, command names |
| `muted` | dim white | Hints, paths (long), contextual info |
| `path` | italic dim | File paths, always de-emphasized |
| `version` | bold white | Version strings, key values |
| `accent` | cyan | Borders, rules, structural color |

### Box Style Guide
| Box | Use |
|-----|-----|
| `ROUNDED` | Default panels, section containers |
| `HEAVY_HEAD` | Command header panels (doctor, eco-scan) |
| `DOUBLE` | Certification / audit output (certify) |
| `MINIMAL` | Inner tables (no border, just alignment) |

### Icon System
```
✓  OK / passed
⚠  Warning / degraded
✗  Failed / error
─  Skipped / n/a
●  Status dot (green=ok, red=fail, yellow=warn)
▶  Running / dispatching
·  Info / neutral
```

### Tier Colors
```
a0_qk_constants    cyan
a1_at_functions    green
a2_mo_composites   yellow
a3_og_features     magenta
a4_sy_orchestration blue
```

---

## What Changed (Phase 1 → Phase 2)

**Phase 1** (functional):
- doctor: ASCII art header, colored status dots, JSON panel
- chat greeting: Rich Panel with tier colors

**Phase 2** (legendary):
- Semantic `Theme` applied to all console output
- eco-scan: verdict header + score panel + tier table in Panel + issues panel
- recon: wrapped in command header Panel + structured sections
- enhance: summary header Panel + findings table in Panel + score bar
- lint: summary Panel with per-linter grid + PASS/FAIL verdict
- certify: DOUBLE box Panel with signature status
- All errors: standardized red Panel instead of plain `[red]text[/red]`
- App help banner: branded Panel on `ass-ade` bare invocation
- interpreter greeting: refined with episodic memory hints in structured layout
