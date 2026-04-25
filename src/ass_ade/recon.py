"""Recon — Phase 0 task-based gate and parallel codebase reconnaissance.

Never Code Blind means every technical task starts with two artifacts:

1. codebase reconnaissance from the local repository
2. a current technical-document research packet or explicit source targets

The recon gate does not execute the task. It decides whether the task has
enough situational awareness to proceed to MAP = TERRAIN.
"""

from __future__ import annotations

import ast
import concurrent.futures
import json
import os
import re
import time
from collections import defaultdict
from dataclasses import dataclass, field as dc_field
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, Field

from ass_ade.local.repo import DEFAULT_IGNORED_DIRS, summarize_repo

ReconVerdict = Literal["READY_FOR_PHASE_1", "RECON_REQUIRED"]


_TECHNICAL_TERMS = {
    "api",
    "async",
    "auth",
    "cloudflare",
    "code",
    "endpoint",
    "fastmcp",
    "framework",
    "integration",
    "library",
    "mcp",
    "openapi",
    "protocol",
    "sdk",
    "security",
    "server",
    "tool",
    "worker",
    "x402",
}

_DOC_TARGETS = [
    (
        ("mcp", "model context protocol", "fastmcp"),
        "Model Context Protocol official specification",
        "https://modelcontextprotocol.io/specification/2025-11-25",
    ),
    (
        ("openapi", "api", "endpoint"),
        "OpenAPI documentation for the target service",
        "https://spec.openapis.org/oas/latest.html",
    ),
    (
        ("cloudflare", "worker", "workers"),
        "Cloudflare Workers documentation",
        "https://developers.cloudflare.com/workers/",
    ),
    (
        ("typer", "cli"),
        "Typer documentation",
        "https://typer.tiangolo.com/",
    ),
    (
        ("pydantic", "model"),
        "Pydantic documentation",
        "https://docs.pydantic.dev/latest/",
    ),
]

_IMPORTANT_NAMES = {
    "README.md",
    "pyproject.toml",
    "package.json",
    "openapi.json",
    ".mcp.json",
    ".env.example",
}


class ResearchTarget(BaseModel):
    topic: str
    query: str
    suggested_url: str | None = None
    status: str = "required"


class CodebaseRecon(BaseModel):
    root: str
    total_files: int
    total_dirs: int
    file_types: dict[str, int] = Field(default_factory=dict)
    top_level_entries: list[str] = Field(default_factory=list)
    relevant_files: list[str] = Field(default_factory=list)
    test_files: list[str] = Field(default_factory=list)
    docs_files: list[str] = Field(default_factory=list)
    config_files: list[str] = Field(default_factory=list)


class Phase0ReconResult(BaseModel):
    verdict: ReconVerdict
    task_description: str
    codebase: CodebaseRecon
    research_targets: list[ResearchTarget] = Field(default_factory=list)
    provided_sources: list[str] = Field(default_factory=list)
    required_actions: list[str] = Field(default_factory=list)
    next_action: str


def _tokens(text: str) -> set[str]:
    return {
        item
        for item in re.findall(r"[a-zA-Z0-9_]{3,}", text.lower())
        if item not in {"the", "and", "for", "with", "this", "that", "into"}
    }


def _is_technical(task: str) -> bool:
    words = _tokens(task)
    return bool(words & _TECHNICAL_TERMS)


def _walk_files(root: Path, limit: int = 4000) -> list[Path]:
    files: list[Path] = []
    for current, dirs, names in os.walk(root, topdown=True):
        dirs[:] = [name for name in dirs if name not in DEFAULT_IGNORED_DIRS]
        for name in names:
            path = Path(current) / name
            try:
                path.relative_to(root)
            except ValueError:
                continue
            files.append(path)
            if len(files) >= limit:
                return files
    return files


def _score_file(path: Path, task_tokens: set[str]) -> int:
    rel = str(path).replace("\\", "/").lower()
    stem_tokens = _tokens(rel)
    score = len(task_tokens & stem_tokens) * 5
    if path.name in _IMPORTANT_NAMES:
        score += 8
    if path.suffix in {".py", ".ts", ".tsx", ".js", ".json", ".md"}:
        score += 2
    if "test" in rel:
        score += 2
    if "docs/" in rel or rel.endswith("readme.md"):
        score += 2
    return score


def _suggest_research(task: str) -> list[ResearchTarget]:
    normalized = task.lower()
    targets: list[ResearchTarget] = []
    for terms, topic, url in _DOC_TARGETS:
        if any(term in normalized for term in terms):
            targets.append(ResearchTarget(
                topic=topic,
                query=f"latest official {topic}",
                suggested_url=url,
            ))
    if not targets and _is_technical(task):
        targets.append(ResearchTarget(
            topic="Latest official technical documentation for task dependencies",
            query=f"latest official docs for: {task}",
        ))
    return targets


def _rel(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def phase0_recon(
    *,
    task_description: str,
    working_dir: str | Path = ".",
    provided_sources: list[str] | None = None,
    max_relevant_files: int = 20,
) -> Phase0ReconResult:
    """Run Phase 0 recon and return whether later phases may proceed."""
    if not task_description.strip():
        raise ValueError("task_description must not be empty")

    root = Path(working_dir).resolve()
    summary = summarize_repo(root)
    task_tokens = _tokens(task_description)
    files = _walk_files(root)
    scored = sorted(
        ((path, _score_file(path.relative_to(root), task_tokens)) for path in files),
        key=lambda item: (-item[1], str(item[0])),
    )
    relevant = [
        _rel(root, path)
        for path, score in scored
        if score > 0
    ][:max_relevant_files]
    tests = [
        _rel(root, path)
        for path in files
        if "test" in str(path.relative_to(root)).replace("\\", "/").lower()
    ][:max_relevant_files]
    docs = [
        _rel(root, path)
        for path in files
        if path.suffix.lower() == ".md" or "docs" in path.parts
    ][:max_relevant_files]
    configs = [
        _rel(root, path)
        for path in files
        if path.name in _IMPORTANT_NAMES or path.suffix.lower() in {".toml", ".yaml", ".yml"}
    ][:max_relevant_files]

    sources = [source for source in (provided_sources or []) if source.strip()]
    research_targets = _suggest_research(task_description)
    required_actions: list[str] = []
    verdict: ReconVerdict = "READY_FOR_PHASE_1"

    if not relevant:
        verdict = "RECON_REQUIRED"
        required_actions.append("Inspect the repository enough to identify relevant files.")

    if _is_technical(task_description) and research_targets and not sources:
        verdict = "RECON_REQUIRED"
        required_actions.append(
            "Perform latest technical-document research and attach source URLs before coding."
        )

    return Phase0ReconResult(
        verdict=verdict,
        task_description=task_description,
        codebase=CodebaseRecon(
            root=str(root),
            total_files=summary.total_files,
            total_dirs=summary.total_dirs,
            file_types=summary.file_types,
            top_level_entries=summary.top_level_entries,
            relevant_files=relevant,
            test_files=tests,
            docs_files=docs,
            config_files=configs,
        ),
        research_targets=research_targets,
        provided_sources=sources,
        required_actions=required_actions,
        next_action=(
            "Continue to Phase 1 context analysis."
            if verdict == "READY_FOR_PHASE_1"
            else "Complete required recon before MAP = TERRAIN or code changes."
        ),
    )


# ── Parallel Recon System ─────────────────────────────────────────────────────
# 5 agents run concurrently via ThreadPoolExecutor.
# No LLM calls — pure file scanning, AST parsing, and pattern matching.
# Target: < 5 seconds for repos with < 500 files.

_SOURCE_EXTS = {".py", ".ts", ".tsx", ".js", ".jsx", ".rs", ".go", ".java", ".rb", ".cs"}
_DOC_EXTS = {".md", ".rst", ".txt"}
_CONFIG_EXTS = {".toml", ".yaml", ".yml", ".json", ".ini", ".cfg"}
_TIERS = ("qk", "at", "mo", "og", "sy")

_IGNORED_FOR_RECON = DEFAULT_IGNORED_DIRS | {".atomadic", ".ass-ade", ".omc"}


def _iter_files(root: Path, limit: int = 2000) -> list[Path]:
    """Walk root, skipping ignored dirs, up to limit files."""
    files: list[Path] = []
    for current, dirs, names in os.walk(root, topdown=True):
        dirs[:] = [d for d in dirs if d not in _IGNORED_FOR_RECON]
        for name in names:
            files.append(Path(current) / name)
            if len(files) >= limit:
                return files
    return files


# ── ScoutAgent ────────────────────────────────────────────────────────────────

def _scout_agent(root: Path, files: list[Path]) -> dict[str, Any]:
    """File count by language, total size, max depth, top-level layout."""
    lang_map: dict[str, int] = defaultdict(int)
    total_size = 0
    max_depth = 0

    for f in files:
        ext = f.suffix.lower()
        lang_map[ext or "[no_ext]"] += 1
        try:
            total_size += f.stat().st_size
        except OSError:
            pass
        try:
            depth = len(f.relative_to(root).parts) - 1
            if depth > max_depth:
                max_depth = depth
        except ValueError:
            pass

    top_level = sorted(
        item.name for item in root.iterdir() if item.name not in _IGNORED_FOR_RECON
    ) if root.exists() else []

    return {
        "total_files": len(files),
        "total_size_bytes": total_size,
        "total_size_kb": round(total_size / 1024, 1),
        "max_depth": max_depth,
        "top_level": top_level,
        "by_extension": dict(sorted(lang_map.items(), key=lambda x: -x[1])),
        "source_files": sum(lang_map.get(e, 0) for e in _SOURCE_EXTS),
        "test_files_count": sum(
            1 for f in files
            if "test" in f.name.lower() or "test" in str(f.parent).lower()
        ),
    }


# ── DependencyAgent ───────────────────────────────────────────────────────────

def _parse_imports(path: Path) -> list[str]:
    """Return import names from a Python file via AST. Silently skip parse errors."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"))
    except SyntaxError:
        return []
    imports: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module.split(".")[0])
    return imports


def _dependency_agent(root: Path, files: list[Path]) -> dict[str, Any]:
    """Map imports across Python files, detect circular deps, measure max depth."""
    py_files = [f for f in files if f.suffix == ".py"]
    # Build module name → relative path mapping
    mod_to_path: dict[str, str] = {}
    for f in py_files:
        try:
            rel = f.relative_to(root).as_posix()
            mod = f.stem
            mod_to_path[mod] = rel
        except ValueError:
            pass

    graph: dict[str, list[str]] = {}
    unique_deps: set[str] = set()

    for f in py_files:
        try:
            rel = f.relative_to(root).as_posix()
        except ValueError:
            continue
        imports = _parse_imports(f)
        internal = [i for i in imports if i in mod_to_path]
        external = [i for i in imports if i not in mod_to_path]
        graph[rel] = internal
        unique_deps.update(external)

    # Detect circular dependencies (simple DFS)
    cycles: list[str] = []
    visited: set[str] = set()
    rec_stack: set[str] = set()

    def _dfs(node: str, path: list[str]) -> None:
        visited.add(node)
        rec_stack.add(node)
        for nb_mod in graph.get(node, []):
            nb = mod_to_path.get(nb_mod, nb_mod)
            if nb not in visited:
                _dfs(nb, path + [nb])
            elif nb in rec_stack:
                cycle = " → ".join(path + [nb])
                if cycle not in cycles:
                    cycles.append(cycle)
        rec_stack.discard(node)

    for node in list(graph.keys()):
        if node not in visited:
            _dfs(node, [node])

    # Max import depth (BFS from entry-point-like files)
    def _bfs_depth(start: str) -> int:
        seen = {start}
        queue = [(start, 0)]
        max_d = 0
        while queue:
            cur, d = queue.pop(0)
            max_d = max(max_d, d)
            for nb_mod in graph.get(cur, []):
                nb = mod_to_path.get(nb_mod, nb_mod)
                if nb not in seen:
                    seen.add(nb)
                    queue.append((nb, d + 1))
        return max_d

    entry_points = [p for p in graph if any(
        p.endswith(name) for name in ("__main__.py", "cli.py", "main.py", "app.py")
    )]
    max_depth = max((_bfs_depth(e) for e in entry_points), default=0)

    return {
        "python_files": len(py_files),
        "unique_external_deps": len(unique_deps),
        "top_external_deps": sorted(unique_deps)[:20],
        "circular_deps": cycles[:10],
        "has_circular_deps": bool(cycles),
        "max_import_depth": max_depth,
        "internal_modules": len(graph),
    }


# ── TierAgent ─────────────────────────────────────────────────────────────────

def _classify_tier(path: Path) -> str:
    """Classify a Python file into qk/at/mo/og/sy based on AST analysis."""
    try:
        source = path.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(source)
    except (SyntaxError, OSError):
        return "at"

    classes = [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
    # Only top-level (module-level) functions, not class methods
    functions = [n for n in tree.body if isinstance(n, ast.FunctionDef)]
    assigns = [n for n in ast.walk(tree) if isinstance(n, ast.Assign)]
    imports = [n for n in ast.walk(tree) if isinstance(n, (ast.Import, ast.ImportFrom))]

    # sy: orchestration — has a main guard or many imports + multi-class composition
    has_main = any(
        isinstance(n, ast.If) and isinstance(getattr(n, "test", None), ast.Compare)
        and any(
            isinstance(getattr(c, "left", None), ast.Name)
            and getattr(getattr(c, "left", None), "id", "") == "__name__"
            for c in [n.test]
        )
        for n in ast.walk(tree)
    )
    name_lower = path.stem.lower()
    is_orchestrator = any(
        kw in name_lower
        for kw in ("orchestrat", "main", "runner", "loop", "pipeline", "dispatch", "app", "cli")
    )
    if (has_main or is_orchestrator) and (len(imports) >= 3 or len(classes) + len(functions) >= 4):
        return "sy"

    # og: feature modules — has both classes and functions with state
    has_stateful_class = any(
        any(
            isinstance(stmt, ast.FunctionDef) and stmt.name == "__init__"
            and any(
                isinstance(n, ast.Assign)
                and any(
                    isinstance(t, ast.Attribute) and isinstance(t.value, ast.Name) and t.value.id == "self"
                    for t in (n.targets if isinstance(n, ast.Assign) else [])
                )
                for n in ast.walk(stmt)
            )
            for stmt in c.body
        )
        for c in classes
    )
    if classes and functions and has_stateful_class:
        return "og"

    # mo: stateful module — has classes with instance state
    if classes and has_stateful_class:
        return "mo"

    # qk: constants/config — mostly assignments, few or no functions/classes
    if assigns and not functions and not classes:
        return "qk"

    # at: atomic — pure functions, no classes, no side effects at module level
    return "at"


def _tier_agent(root: Path, files: list[Path]) -> dict[str, Any]:
    """Classify each source file into qk/at/mo/og/sy."""
    py_files = [f for f in files if f.suffix == ".py"]
    tier_counts: dict[str, int] = {t: 0 for t in _TIERS}
    tier_examples: dict[str, list[str]] = {t: [] for t in _TIERS}
    unclassifiable: list[str] = []

    for f in py_files:
        try:
            rel = f.relative_to(root).as_posix()
        except ValueError:
            rel = f.name
        tier = _classify_tier(f)
        if tier in tier_counts:
            tier_counts[tier] += 1
            if len(tier_examples[tier]) < 5:
                tier_examples[tier].append(rel)
        else:
            unclassifiable.append(rel)

    violations: list[str] = []
    # Flag files that span tiers (heuristic: very large files in at/qk)
    for f in py_files:
        tier = _classify_tier(f)
        if tier in ("at", "qk"):
            try:
                size = f.stat().st_size
                if size > 20_000:
                    try:
                        rel = f.relative_to(root).as_posix()
                    except ValueError:
                        rel = f.name
                    violations.append(f"{rel} ({tier}, {size // 1024}KB — may span tiers)")
            except OSError:
                pass

    return {
        "total_py_files": len(py_files),
        "tier_distribution": tier_counts,
        "tier_examples": tier_examples,
        "tier_violations": violations[:10],
        "dominant_tier": max(tier_counts, key=lambda k: tier_counts[k]) if py_files else "unknown",
    }


# ── TestAgent ─────────────────────────────────────────────────────────────────

def _count_test_functions(path: Path) -> int:
    """Count test functions in a Python file."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"))
    except SyntaxError:
        return 0
    return sum(
        1
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name.startswith("test_")
    )


def _test_agent(root: Path, files: list[Path]) -> dict[str, Any]:
    """Find test files, count test functions, identify untested modules."""
    test_files = [
        f for f in files
        if f.suffix == ".py" and (
            f.name.startswith("test_") or f.name.endswith("_test.py")
        )
    ]
    source_files = [
        f for f in files
        if f.suffix == ".py"
        and not f.name.startswith("test_")
        and not f.name.endswith("_test.py")
        and f.name != "__init__.py"
    ]

    total_test_fns = sum(_count_test_functions(f) for f in test_files)

    # Check for pytest / unittest markers
    has_pytest = any(
        "pytest" in _parse_imports(f)
        for f in test_files
    )
    has_unittest = any(
        "unittest" in _parse_imports(f)
        for f in test_files
    )

    # Identify untested modules (no matching test file by stem)
    tested_stems = {f.stem.removeprefix("test_").removesuffix("_test") for f in test_files}
    untested = [
        f.relative_to(root).as_posix() if f.is_relative_to(root) else f.name
        for f in source_files
        if f.stem not in tested_stems
    ]

    coverage_ratio = (
        round(len(test_files) / len(source_files), 2)
        if source_files else 0.0
    )

    test_file_paths = []
    for f in test_files[:10]:
        try:
            test_file_paths.append(f.relative_to(root).as_posix())
        except ValueError:
            test_file_paths.append(f.name)

    return {
        "test_files": len(test_files),
        "test_functions": total_test_fns,
        "source_files": len(source_files),
        "untested_modules": untested[:20],
        "untested_count": len(untested),
        "coverage_ratio": coverage_ratio,
        "frameworks": [f for f, ok in [("pytest", has_pytest), ("unittest", has_unittest)] if ok],
        "test_file_paths": test_file_paths,
    }


# ── DocAgent ──────────────────────────────────────────────────────────────────

def _has_docstring(node: ast.AST) -> bool:
    body = getattr(node, "body", [])
    return bool(body) and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant)


def _doc_agent(root: Path, files: list[Path]) -> dict[str, Any]:
    """Check README, docstring coverage, outdated docs, missing docs."""
    readme = next(
        (f for f in files if f.name.lower() == "readme.md"),
        None,
    )
    doc_files = [f for f in files if f.suffix in _DOC_EXTS]

    py_files = [f for f in files if f.suffix == ".py"]
    total_callables = 0
    documented_callables = 0
    undocumented: list[str] = []

    for f in py_files:
        try:
            tree = ast.parse(f.read_text(encoding="utf-8", errors="replace"))
        except (SyntaxError, OSError):
            continue
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                if node.name.startswith("_"):
                    continue
                total_callables += 1
                if _has_docstring(node):
                    documented_callables += 1
                elif len(undocumented) < 10:
                    try:
                        rel = f.relative_to(root).as_posix()
                    except ValueError:
                        rel = f.name
                    undocumented.append(f"{rel}:{node.name}")

    doc_coverage = (
        round(documented_callables / total_callables, 2)
        if total_callables else 1.0
    )

    doc_file_paths = []
    for f in doc_files[:15]:
        try:
            doc_file_paths.append(f.relative_to(root).as_posix())
        except ValueError:
            doc_file_paths.append(f.name)

    return {
        "has_readme": readme is not None,
        "readme_path": str(readme.relative_to(root)) if readme else None,
        "doc_files": len(doc_files),
        "doc_file_paths": doc_file_paths,
        "total_public_callables": total_callables,
        "documented_callables": documented_callables,
        "doc_coverage": doc_coverage,
        "undocumented_samples": undocumented,
    }


# ── WebResearchAgent ──────────────────────────────────────────────────────────

def _web_research_agent(root: Path, files: list[Path]) -> dict[str, Any]:
    """Query AAAA-Nexus inference for external context: best practices, similar projects, dep updates.

    Falls back gracefully when the endpoint is unreachable or API key is missing.
    Results appear in the ## Web Research section of the recon report.
    """
    result: dict[str, Any] = {
        "queried": False,
        "project_name": root.name,
        "best_practices": [],
        "similar_projects": [],
        "dep_updates": [],
        "error": None,
    }

    # Resolve project name from pyproject.toml
    pyproject = root / "pyproject.toml"
    if pyproject.exists():
        try:
            text = pyproject.read_text(encoding="utf-8")
            m = re.search(r'name\s*=\s*["\']([^"\']+)["\']', text)
            if m:
                result["project_name"] = m.group(1)
        except OSError:
            pass

    # Resolve config for endpoint + key
    base_url = "https://atomadic.tech"
    try:
        cfg_path = root / ".ass-ade" / "config.json"
        if cfg_path.exists():
            cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
            base_url = cfg.get("nexus_base_url", base_url).rstrip("/")
    except (OSError, json.JSONDecodeError):
        pass

    api_key = os.environ.get("AAAA_NEXUS_API_KEY", "")
    project_name = result["project_name"]

    # Top 3 external deps for context
    dep_names: list[str] = []
    try:
        pyproject_txt = pyproject.read_text(encoding="utf-8") if pyproject.exists() else ""
        dep_names = re.findall(r'["\']([a-zA-Z][a-zA-Z0-9_\-]{2,})["\']', pyproject_txt)[:5]
    except OSError:
        pass

    queries = [
        f"List 3 best practices for {project_name} Python project in 2025. Be specific and brief.",
        f"Name 3 open-source projects similar to {project_name}. Just names, one per line.",
    ]
    if dep_names:
        queries.append(
            f"Any breaking changes or major updates in {', '.join(dep_names[:3])} in 2024-2025? Be brief."
        )

    try:
        import httpx as _httpx

        headers: dict[str, str] = {"Content-Type": "application/json"}
        if api_key:
            headers["X-API-Key"] = api_key

        responses: list[str] = []
        for query in queries[:3]:
            try:
                resp = _httpx.post(
                    f"{base_url}/v1/inference/chat/completions",
                    headers=headers,
                    json={
                        "model": "falcon3-10B-1.58",
                        "messages": [{"role": "user", "content": query}],
                        "max_tokens": 150,
                        "temperature": 0.3,
                    },
                    timeout=8.0,
                )
                if resp.status_code == 200:
                    content = resp.json()["choices"][0]["message"]["content"].strip()
                    responses.append(content)
            except Exception:
                continue

        if responses:
            result["queried"] = True
            if len(responses) >= 1:
                result["best_practices"] = [
                    line.strip().lstrip("-•*123. ")
                    for line in responses[0].splitlines()
                    if line.strip() and len(line.strip()) > 10
                ][:3]
            if len(responses) >= 2:
                result["similar_projects"] = [
                    line.strip().lstrip("-•*123. ")
                    for line in responses[1].splitlines()
                    if line.strip() and len(line.strip()) > 2
                ][:3]
            if len(responses) >= 3:
                result["dep_updates"] = [
                    line.strip().lstrip("-•*123. ")
                    for line in responses[2].splitlines()
                    if line.strip() and len(line.strip()) > 10
                ][:3]

    except ImportError:
        result["error"] = "httpx not available"
    except Exception as exc:
        result["error"] = str(exc)[:120]

    return result


# ── ReconReport ───────────────────────────────────────────────────────────────

@dataclass
class ReconReport:
    """Consolidated output from all 6 parallel recon agents."""

    root: str
    duration_ms: float
    scout: dict[str, Any]
    dependency: dict[str, Any]
    tier: dict[str, Any]
    test: dict[str, Any]
    doc: dict[str, Any]
    web: dict[str, Any] = dc_field(default_factory=dict)
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

        if self.web:
            lines += ["", "## Web Research", ""]
            if self.web.get("queried"):
                bp = self.web.get("best_practices", [])
                sp = self.web.get("similar_projects", [])
                du = self.web.get("dep_updates", [])
                if bp:
                    lines.append(f"**Best practices for `{self.web.get('project_name', '')}`:**")
                    for item in bp:
                        lines.append(f"  - {item}")
                if sp:
                    lines.append("")
                    lines.append("**Similar projects:**")
                    for item in sp:
                        lines.append(f"  - {item}")
                if du:
                    lines.append("")
                    lines.append("**Dependency updates (2024-2025):**")
                    for item in du:
                        lines.append(f"  - {item}")
            else:
                err = self.web.get("error")
                lines.append(f"*(Web research skipped — {err or 'endpoint unreachable or no API key'})*")

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
            "web": self.web,
            "recommendations": self.recommendations,
            "next_action": self.next_action,
        }


def _build_recommendations(
    scout: dict[str, Any],
    dependency: dict[str, Any],
    tier: dict[str, Any],
    test: dict[str, Any],
    doc: dict[str, Any],
) -> tuple[list[str], str]:
    recs: list[str] = []

    if dependency["has_circular_deps"]:
        recs.append(
            f"Resolve {len(dependency['circular_deps'])} circular import(s) — "
            "introduce an interface layer or inversion-of-control."
        )

    if test["coverage_ratio"] < 0.3:
        recs.append(
            f"Test coverage is low ({test['coverage_ratio']}). "
            f"Add tests for the {test['untested_count']} untested modules."
        )
    elif test["test_functions"] == 0:
        recs.append("No test functions found. Add a pytest suite.")

    if not doc["has_readme"]:
        recs.append("No README.md found. Add one for onboarding context.")

    if doc["doc_coverage"] < 0.4:
        recs.append(
            f"Docstring coverage is {doc['doc_coverage']:.0%}. "
            "Add docstrings to public functions and classes."
        )

    if tier["tier_violations"]:
        recs.append(
            f"{len(tier['tier_violations'])} file(s) may span tier boundaries. "
            "Split into smaller, single-purpose modules."
        )

    if scout["max_depth"] > 6:
        recs.append(
            f"Directory depth is {scout['max_depth']}. "
            "Consider flattening the structure to reduce navigation friction."
        )

    if not recs:
        recs.append("Repo looks healthy. Run `ass-ade certify` to produce a signed certificate.")

    next_action = (
        "Fix circular imports first, then increase test coverage."
        if dependency["has_circular_deps"]
        else "Run `ass-ade lint` for detailed style and security findings."
    )
    return recs, next_action


# ── Public API ────────────────────────────────────────────────────────────────

def run_parallel_recon(path: str | Path = ".") -> ReconReport:
    """Run all 6 recon agents in parallel and return a consolidated ReconReport.

    Agents 1-5 are local (no network). Agent 6 (WebResearch) queries the
    AAAA-Nexus inference endpoint for external context and falls back gracefully.
    """
    root = Path(path).resolve()
    t0 = time.monotonic()

    files = _iter_files(root)

    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        f_scout = pool.submit(_scout_agent, root, files)
        f_dep   = pool.submit(_dependency_agent, root, files)
        f_tier  = pool.submit(_tier_agent, root, files)
        f_test  = pool.submit(_test_agent, root, files)
        f_doc   = pool.submit(_doc_agent, root, files)
        f_web   = pool.submit(_web_research_agent, root, files)

        scout      = f_scout.result()
        dependency = f_dep.result()
        tier       = f_tier.result()
        test       = f_test.result()
        doc        = f_doc.result()
        web        = f_web.result()

    recs, next_action = _build_recommendations(scout, dependency, tier, test, doc)
    duration_ms = (time.monotonic() - t0) * 1000

    return ReconReport(
        root=str(root),
        duration_ms=duration_ms,
        scout=scout,
        dependency=dependency,
        tier=tier,
        test=test,
        doc=doc,
        web=web,
        recommendations=recs,
        next_action=next_action,
    )
