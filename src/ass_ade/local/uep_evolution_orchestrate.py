"""Governance-aligned evolution handoff: research hops, tech-doc pointers, epiphany, panel charter.

This module is intentionally **stdio- and filesystem-first** so it runs in CI and on
air-gapped runners. It does **not** call LLM APIs. It emits structured artifacts that
human operators or external agents (Cursor teams, Nexus, OMC) complete:

- Multi-hop **web research** is represented as ``queries[]`` plus optional ``sources[]``
  (fill with verified URLs after browsing).
- **Technical documentation** hops point at repository Markdown and config surfaces.
- **Epiphany** output is produced by invoking ``scripts/epiphany_breakthrough_local.py``
  with ``--provided-source`` entries so phase-0 recon clears for technical tasks.
- **Panel** markdown lists specialist roles for a round-table plan before auto-evolve.
- Optional **third-party formal specification JSON** (local bundle paths only) may supply
  *metadata* such as epistemic status codes and document identity for labeling handoffs.
  Content of that JSON is **not** treated as runtime truth for ASS-ADE / AAAA-Nexus.

See also: ``ass_ade.local.planner.draft_epiphany_breakthrough_plan`` and
``ass_ade.engine.rebuild.epiphany_cycle`` for the epiphany envelope.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "ass-ade.evolution-handoff.v1.2"

EVOLUTION_HANDOFF_JSON = "evolution_handoff.json"

GOVERNANCE_PHASES: list[dict[str, str]] = [
    {"id": "P0", "name": "MAP = TERRAIN", "gate": "Repo paths, tier-map, and MCP manifest are the authority map."},
    {
        "id": "P1",
        "name": "Epistemic grounding",
        "gate": (
            "No production claim without verificationEvidence or DEFER. "
            "External or partner specification prose used for intuition must carry epistemic tags "
            "([A]/[D]/[L]/[S]/[X]); only [L] with artifact pointers may gate shipping code."
        ),
    },
    {"id": "P2", "name": "Public / private boundary", "gate": "Secrets and org policy live outside the public tree."},
    {"id": "P3", "name": "Research hops", "gate": "Web + vendor docs captured as sources, not chat prose."},
    {"id": "P4", "name": "Epiphany → experiment", "gate": "Hypotheses tie to observations; one smallest experiment."},
    {"id": "P5", "name": "Panel consensus", "gate": "Specialists disagree in writing; chair records decision."},
    {"id": "P6", "name": "Enhancement promotion", "gate": "Only green tests + CLI smoke feed auto-evolve / PR."},
]


def _tokens(text: str) -> set[str]:
    return {t.lower() for t in re.findall(r"[A-Za-z0-9][A-Za-z0-9_+\.-]*", text)}


def _score_path(rel: str, tokens: set[str]) -> int:
    parts = rel.replace("\\", "/").lower()
    stem = set(re.findall(r"[a-z0-9]{3,}", parts))
    return len(tokens & stem) * 3 + (5 if "docs/" in parts else 0)


def discover_tech_doc_paths(root: Path, task: str, *, limit: int = 12) -> list[str]:
    """Rank repo markdown / docs likely relevant to *task* (offline heuristic)."""
    tok = _tokens(task)
    scored: list[tuple[int, str]] = []
    for path in root.rglob("*.md"):
        try:
            rel = path.relative_to(root).as_posix()
        except ValueError:
            continue
        if any(p in rel.split("/") for p in (".git", ".venv", "node_modules", ".ass-ade/builds")):
            continue
        sc = _score_path(rel, tok)
        if sc > 0 or rel.upper().startswith("README") or rel.startswith("docs/"):
            scored.append((sc + (2 if rel.startswith("docs/") else 0), rel))
    scored.sort(key=lambda x: (-x[0], x[1]))
    out = []
    for _, rel in scored:
        if rel not in out:
            out.append(rel)
        if len(out) >= limit:
            break
    if not out and (root / "README.md").is_file():
        out.append("README.md")
    return out


def github_blob_urls(repo: str, paths: list[str], ref: str = "main") -> list[str]:
    owner, _, name = repo.partition("/")
    if not owner or not name:
        return []
    base = f"https://github.com/{owner}/{name}/blob/{ref}/"
    return [base + p.replace("\\", "/") for p in paths]


def default_formal_codex_json_candidates() -> list[Path]:
    """Resolve optional formal-spec JSON candidates from env and well-known roots.

    The actual catalog path is an opaque local artifact (see AN-TH-CODEX-CATALOG).
    Callers can override the lookup entirely via ``FORMAL_CODEX_JSON`` or
    ``ASS_ADE_FORMAL_CODEX_JSON``. No catalog filename is embedded in this
    public module - we only return whatever the caller points us at.
    """
    out: list[Path] = []
    for env_var in ("FORMAL_CODEX_JSON", "ASS_ADE_FORMAL_CODEX_JSON"):
        v = os.environ.get(env_var, "").strip()
        if v:
            out.append(Path(v))
    # No hard-coded private paths or filenames: the private catalog lives in
    # the upstream sovereign archive and is fetched via the AAAA-Nexus oracle,
    # not from a local filesystem layout.
    dedup: list[Path] = []
    for p in out:
        if p not in dedup:
            dedup.append(p)
    return dedup


def discover_formal_codex_json_path(explicit: Path | None) -> Path | None:
    if explicit is not None:
        return explicit if explicit.is_file() else None
    for p in default_formal_codex_json_candidates():
        if p.is_file():
            return p
    return None


def load_formal_codex_context(path: Path, *, max_bytes: int = 2_000_000) -> dict[str, Any] | None:
    """Return a small, whitelisted JSON view for evolution labeling (no numeric 'truth' in code paths)."""
    try:
        sz = path.stat().st_size
    except OSError:
        return None
    if sz > max_bytes:
        return None
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return None
    if not isinstance(raw, dict):
        return None
    codes_in = raw.get("epistemic_status_codes")
    codes_out: list[dict[str, str]] = []
    if isinstance(codes_in, list):
        for row in codes_in[:12]:
            if not isinstance(row, dict):
                continue
            code = str(row.get("code", "")).strip()
            meaning = str(row.get("meaning", "")).strip()
            notes = str(row.get("notes", "")).strip()
            if code:
                codes_out.append({"code": code, "meaning": meaning, "notes": notes})
    lean = raw.get("lean4_verification")
    lean_out: dict[str, Any] | None = None
    if isinstance(lean, dict):
        lean_out = {
            "status": str(lean.get("status", "")).strip(),
            "totalTheorems": lean.get("total_theorems"),
            "totalSorry": lean.get("total_sorry"),
            "asOf": str(lean.get("as_of", "")).strip(),
        }
    return {
        "sourcePath": str(path.resolve()),
        "documentId": str(raw.get("document_id", "")).strip(),
        "title": str(raw.get("title", "")).strip(),
        "version": str(raw.get("version", "")).strip(),
        "epistemicStatusProse": str(raw.get("epistemic_status", "")).strip(),
        "epistemicStatusCodes": codes_out,
        "lean4Summary": lean_out,
        "operatorNote": (
            "Metadata for human/agent labeling only. Do not treat third-party JSON prose or "
            "structured fields as verified runtime facts in ASS-ADE; pair [L] claims with "
            "machine-checked artifact pointers, or mark narrative as [S]/[X]."
        ),
    }


def render_evolution_audit_checklist(*, task: str, formal_codex_context: dict[str, Any] | None) -> str:
    """Slim pre-merge governance questions (not a full extended audit questionnaire)."""
    codex_line = (
        "_No optional formal-spec JSON was discovered; skip external-spec rows or set `FORMAL_CODEX_JSON`._"
    )
    if formal_codex_context and formal_codex_context.get("documentId"):
        codex_line = (
            f"_External spec document:_ `{formal_codex_context.get('documentId')}` "
            f"({formal_codex_context.get('version', '')}) — map codes [A][D][L][S][X] using "
            f"`research_pack.json` → `extensions.formalCodexContext`."
        )
    return "\n".join(
        [
            "# Evolution audit checklist (ASS-ADE)",
            "",
            f"**Task:** {task.strip()[:800]}",
            "",
            codex_line,
            "",
            "## Trust and evidence",
            "",
            "1. For each user-facing or security claim in the proposed change, what is the **verificationEvidence** (path, test name, CI job, or DEFER)?",
            "2. **Trust-before-memory:** would `trust_gate` / policy allow storing this narrative in vector memory unchanged? If not, what redaction or label applies?",
            "3. List **rollback** steps if the enhancement ships and regresses (feature flag, revert commit, MCP disable).",
            "",
            "## Repository law",
            "",
            "4. Does the diff respect **monadic tier direction** and avoid upward imports?",
            "5. Are generated trees (e.g. `.ass-ade/builds/`, large selfbuild outputs) excluded from auto-evolve commits?",
            "",
            "## Research and boundaries",
            "",
            "6. Which **webResearch** hops were completed with primary URLs (not search result pages only)?",
            "7. **Public / private:** any secrets, tokens, or org-only hostnames in the diff or logs?",
            "",
            "## Panel and promotion",
            "",
            "8. Did **specialists disagree in writing** and did the chair record a single verdict (PASS|REFINE|QUARANTINE|REJECT)?",
            "9. What is the **smallest experiment** (one test or one CLI smoke) that proves the hypothesis?",
            "10. Are **MCP / tool** surfaces reviewed for injection and over-broad filesystem access?",
            "",
            "## External formal specification (when used)",
            "",
            "11. Any constant or identity borrowed from optional third-party formal JSON: is it labeled **[L]** "
            "with a machine-checked pointer, or **[S]/[X]** with explicit non-proof scope?",
            "12. If the handoff uses informal metaphors (loops, ratios, envelopes), map each to **concrete repo checks** "
            "(tests, limits, validators) — not prose alone.",
            "",
            "_Chair sign-off:_ ",
            "",
        ]
    )


def build_research_pack(
    *,
    task: str,
    root: Path,
    repo: str,
    formal_codex_context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Assemble webResearch + techDocs JSON (context-pack compatible subset)."""
    now = datetime.now(timezone.utc).isoformat()
    doc_paths = discover_tech_doc_paths(root, task)
    hops: list[dict[str, Any]] = [
        {
            "id": "H1-ecosystem",
            "queries": [
                f"MCP ecosystem governance patterns for: {task[:120]}",
                "Model Context Protocol server security checklist",
            ],
            "findingSummary": "",
            "verificationEvidence": {"kind": "pending", "ref": "", "note": "Fill after browse; cite primary sources."},
        },
        {
            "id": "H2-official-docs",
            "queries": [f"Official documentation for dominant libraries named in: {task[:120]}"],
            "findingSummary": "",
            "verificationEvidence": {"kind": "pending", "ref": "", "note": "Prefer vendor docs + release notes."},
        },
        {
            "id": "H3-repo-terrain",
            "queries": [f"Repository hot paths for: {task[:120]}"],
            "findingSummary": "Ranked markdown/config paths under this repo root.",
            "verificationEvidence": {"kind": "path", "ref": doc_paths[0] if doc_paths else "README.md", "note": "Heuristic discover_tech_doc_paths."},
        },
        {
            "id": "H4-formal-codex-boundary",
            "queries": [
                "Where do machine-checked artifacts (tests, provers, CI) bound this task vs narrative-only specs?",
                "If partner or internal specification prose is used, which sentences stay [S]/[X] vs [L] with pointers?",
            ],
            "findingSummary": (
                "Formal context attached under research_pack.extensions when a JSON file is found; else fill manually."
                if formal_codex_context
                else "Optional: set FORMAL_CODEX_JSON to a local formal-spec bundle, or mark DEFER."
            ),
            "verificationEvidence": (
                {
                    "kind": "path",
                    "ref": formal_codex_context["sourcePath"],
                    "note": "Whitelisted metadata slice from load_formal_codex_context; not a proof artifact.",
                }
                if formal_codex_context
                else {"kind": "pending", "ref": "", "note": "Attach formal JSON path or mark DEFER."}
            ),
        },
    ]
    sources = []
    for url in github_blob_urls(repo, doc_paths[:6]):
        sources.append({"url": url, "retrievedAt": now, "supports": ["H3-repo-terrain"]})
    out: dict[str, Any] = {
        "schemaVersion": "atomadic.context-pack.v1",
        "generatedAt": now,
        "intent": {
            "summary": task.strip()[:500],
            "deliverables": [EVOLUTION_HANDOFF_JSON, "panel_charter.md", "epiphany.json"],
        },
        "paths": {"repoRoot": str(root.resolve()), "packDir": ""},
        "webResearch": {"hops": hops, "sources": sources},
        "techDocs": {
            "stackFingerprint": {"tierMap": ".ass-ade/tier-map.json", "mcpManifest": "mcp/server.json"},
            "deliverableScopes": [{"path": p, "note": "Skim for constraints touching the task."} for p in doc_paths[:8]],
        },
        "governancePhases": GOVERNANCE_PHASES,
    }
    if formal_codex_context:
        out["extensions"] = {"formalCodexContext": formal_codex_context}
    return out


def render_panel_charter(
    *,
    task: str,
    research_path: str,
    epiphany_path: str,
    formal_codex_context: dict[str, Any] | None = None,
) -> str:
    roles = [
        ("Chair / MAP=TERRAIN", "Keeps scope bounded; records verdict PASS|REFINE|QUARANTINE|REJECT."),
        ("Research lead (web + vendor docs)", "Owns H1–H2 hops; pastes URLs + one-line why each source matters."),
        ("Security + red-team", "OWASP LLM / tool injection / secret exfil; blocks unsafe automation."),
        ("Monadic + economics", "Tier law direction, MCP metering, rollback story for shipped changes."),
    ]
    if formal_codex_context and formal_codex_context.get("documentId"):
        roles.append(
            (
                "Formal / external-spec boundary",
                "Maps epistemic labels ([A][D][L][S][X]) to repo evidence; blocks shipping on [S]/[X] alone.",
            )
        )
    lines = [
        "# Evolution panel charter",
        "",
        f"**Task:** {task.strip()}",
        "",
        f"- Research pack: `{research_path}`",
        f"- Epiphany JSON: `{epiphany_path}`",
        "",
        "## Governance phase checklist (complete before coding)",
        "",
    ]
    for ph in GOVERNANCE_PHASES:
        lines.append(f"- **{ph['id']} — {ph['name']}:** {ph['gate']}")
    lines.extend(["", "## Round table (paste specialist notes below)", ""])
    for title, brief in roles:
        lines.extend([f"### {title}", f"_{brief}_", "", "_Notes:_", "", "---", ""])
    if formal_codex_context and formal_codex_context.get("documentId"):
        lines.extend(
            [
                "## External formal specification (read-only context)",
                "",
                f"- **Document:** `{formal_codex_context.get('documentId')}` — "
                f"{formal_codex_context.get('title', '')} ({formal_codex_context.get('version', '')})",
                f"- **Source file:** `{formal_codex_context.get('sourcePath', '')}`",
                "- Treat third-party JSON narrative fields as **non-runtime** unless backed by this repo's tests "
                "or cited machine-checked modules.",
                "- Prefer `research_pack.json` hop **H4-formal-codex-boundary** for where formal vs narrative split lands for this task.",
                "",
            ]
        )
    lines.extend(
        [
            "## Consensus output (chair fills)",
            "",
            "_Top 3 enhancement candidates (each one sentence, testable):_",
            "",
            "1. ",
            "2. ",
            "3. ",
            "",
            "_Chair verdict:_ ",
            "",
        ]
    )
    return "\n".join(lines)


@dataclass(frozen=True)
class OrchestrateResult:
    out_dir: Path
    research_json: Path
    panel_md: Path
    epiphany_json: Path
    audit_md: Path


def run_epiphany_cli(
    *,
    root: Path,
    task_file: Path,
    out_json: Path,
    provided_sources: list[str],
) -> None:
    script = root / "scripts" / "epiphany_breakthrough_local.py"
    if not script.is_file():
        raise FileNotFoundError(f"missing {script}")
    cmd = [
        sys.executable,
        str(script),
        "--task-file",
        str(task_file),
        "--max-relevant-files",
        "24",
    ]
    for src in provided_sources:
        cmd.extend(["--provided-source", src])
    proc = subprocess.run(cmd, cwd=str(root), capture_output=True, text=True, check=False)
    out_json.write_text(proc.stdout or "{}", encoding="utf-8")
    if proc.returncode != 0:
        err = (proc.stderr or "").strip()
        raise RuntimeError(f"epiphany_breakthrough_local exit {proc.returncode}: {err[:800]}")


def orchestrate(
    *,
    root: Path,
    task: str,
    out_dir: Path,
    repo: str,
    formal_codex_json: Path | None = None,
) -> OrchestrateResult:
    """Write research JSON, panel charter, epiphany JSON, and audit checklist under *out_dir*."""
    if not task.strip():
        raise ValueError("task must be non-empty")
    out_dir.mkdir(parents=True, exist_ok=True)
    codex_path = discover_formal_codex_json_path(formal_codex_json)
    formal_ctx = load_formal_codex_context(codex_path) if codex_path else None
    pack = build_research_pack(task=task, root=root, repo=repo, formal_codex_context=formal_ctx)
    research_path = out_dir / "research_pack.json"
    research_path.write_text(json.dumps(pack, indent=2), encoding="utf-8")

    doc_paths = discover_tech_doc_paths(root, task)
    provided = github_blob_urls(repo, doc_paths[:8])
    if not provided and (root / "README.md").is_file():
        provided = github_blob_urls(repo, ["README.md"])

    task_file = out_dir / "task.md"
    task_file.write_text(task.strip() + "\n", encoding="utf-8")

    epiphany_path = out_dir / "epiphany.json"
    run_epiphany_cli(root=root, task_file=task_file, out_json=epiphany_path, provided_sources=provided)

    audit_md = out_dir / "evolution_audit_checklist.md"
    audit_md.write_text(
        render_evolution_audit_checklist(task=task, formal_codex_context=formal_ctx),
        encoding="utf-8",
    )

    handoff = {
        "schemaVersion": SCHEMA_VERSION,
        "generatedAt": pack["generatedAt"],
        "taskFile": str(task_file.as_posix()),
        "researchPack": str(research_path.as_posix()),
        "epiphany": str(epiphany_path.as_posix()),
        "panelCharter": str((out_dir / "panel_charter.md").as_posix()),
        "evolutionAuditChecklist": str(audit_md.as_posix()),
        "formalCodexContext": formal_ctx,
        "providedSourcesUsed": provided,
        "suggestedNextSteps": [
            "Run multi-agent panel against panel_charter.md (Cursor team or OMC).",
            "Complete evolution_audit_checklist.md before opening an auto-evolve PR.",
            "Fill webResearch.hops[].findingSummary + verificationEvidence in research_pack.json.",
            "Trust-before-memory: run trust_gate (or equivalent policy) before ingesting handoff prose into vector memory.",
            "Feed consensus enhancement list into auto-evolve task input or enhancer findings.",
        ],
    }
    (out_dir / EVOLUTION_HANDOFF_JSON).write_text(json.dumps(handoff, indent=2), encoding="utf-8")

    panel_md = out_dir / "panel_charter.md"
    panel_md.write_text(
        render_panel_charter(
            task=task,
            research_path=str(research_path.relative_to(root)),
            epiphany_path=str(epiphany_path.relative_to(root)),
            formal_codex_context=formal_ctx,
        ),
        encoding="utf-8",
    )
    return OrchestrateResult(
        out_dir=out_dir,
        research_json=research_path,
        panel_md=panel_md,
        epiphany_json=epiphany_path,
        audit_md=audit_md,
    )
