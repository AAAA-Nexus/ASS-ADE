"""Forge phase — Epiphany-driven, parallel LLM code improvement.

Architecture (as directed by Thomas):
  1. EpiphanyEngine  — analyzes materialized files, generates a structured plan
                       (one experiment per issue per node).
  2. ForgeLoop       — takes the plan, executes each task as a focused LLM call,
                       runs tasks in parallel via ThreadPoolExecutor.

Entry point for the rebuild orchestrator: `run_forge_phase(target_root, model)`.
"""
from __future__ import annotations

import ast
import logging
import os
import re
import textwrap
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import httpx

log = logging.getLogger(__name__)

_OLLAMA_BASE = os.getenv("OLLAMA_HOST", "http://localhost:11434") + "/v1"
_FORGE_MODEL = os.getenv("ASS_ADE_FORGE_MODEL", "helix7b:latest")
_MAX_WORKERS = int(os.getenv("ASS_ADE_FORGE_WORKERS", "2"))  # conservative for cloud rate limits

# Module-level provider cache so we don't rebuild on every LLM call.
_provider: Any = None


def _hydrate_env_from_project() -> None:
    """Load .env into os.environ from project root or global config dir.

    Search order:
      1. cwd → parent → grandparent  (project-local .env)
      2. ~/.ass-ade/.env             (global, written by `ass-ade setup --global`)
    Process env always wins — existing values are never overwritten.
    """
    def _load_env_file(path: Path) -> bool:
        if not path.exists():
            return False
        try:
            for line in path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                key = key.strip()
                if key and key not in os.environ:
                    os.environ[key] = value.strip()
            log.debug("Hydrated .env from %s", path)
            return True
        except OSError:
            return False

    # 1. Walk up from cwd
    cwd = Path.cwd()
    for candidate in [cwd, cwd.parent, cwd.parent.parent]:
        if _load_env_file(candidate / ".env"):
            return

    # 2. Global fallback (~/.ass-ade/.env)
    _load_env_file(Path.home() / ".ass-ade" / ".env")


_PROVIDER_SPECS: list[tuple[str, str, str]] = [
    ("GROQ_API_KEY",       "https://api.groq.com/openai/v1",         "llama-3.3-70b-versatile"),
    ("CEREBRAS_API_KEY",   "https://api.cerebras.ai/v1",              "llama3.3-70b"),
    ("MISTRAL_API_KEY",    "https://api.mistral.ai/v1",               "mistral-large-latest"),
    ("TOGETHER_API_KEY",   "https://api.together.xyz/v1",             "meta-llama/Llama-3-70b-chat-hf"),
    ("OPENROUTER_API_KEY", "https://openrouter.ai/api/v1",            "meta-llama/llama-3.3-70b-instruct"),
]


def _build_cloud_provider(env_key: str, base_url: str, model: str) -> Any:
    from ass_ade.engine.provider import OpenAICompatibleProvider
    return OpenAICompatibleProvider(base_url=base_url, api_key=os.environ[env_key],
                                    model=model, timeout=60.0)


def _get_all_providers() -> list[Any]:
    """Return one provider per available API key — used for multi-provider parallel.

    Each file group in execute_plan is assigned to a different provider so that
    e.g. Groq handles app.py while Cerebras handles models.py simultaneously.
    """
    _hydrate_env_from_project()
    providers = []
    for env_key, base_url, model in _PROVIDER_SPECS:
        if os.getenv(env_key):
            providers.append(_build_cloud_provider(env_key, base_url, model))
            log.debug("Forge pool: added %s", env_key.split("_API_KEY")[0].split("_TOKEN")[0])
    if not providers:
        providers.append(_get_provider())
    return providers


def _get_provider() -> Any:
    """Return a single cached provider — used when only one provider is needed.

    Priority: Groq → Cerebras → Mistral → Together → OpenRouter → Ollama fallback.
    """
    global _provider
    if _provider is not None:
        return _provider

    _hydrate_env_from_project()

    for env_key, base_url, model in _PROVIDER_SPECS:
        if os.getenv(env_key):
            _provider = _build_cloud_provider(env_key, base_url, model)
            log.info("Forge provider: %s @ %s", env_key.split("_API_KEY")[0], base_url)
            return _provider

    # Nexus API key
    nexus_key = os.getenv("AAAA_NEXUS_API_KEY")
    if nexus_key:
        try:
            from ass_ade.config import load_config
            from ass_ade.engine.router import build_provider
            config = load_config()
            _provider = build_provider(config)
            log.info("Forge provider: MultiProvider via Nexus")
            return _provider
        except Exception as exc:
            log.warning("Nexus provider build failed: %s", exc)

    # Final fallback: Ollama local
    from ass_ade.engine.provider import OpenAICompatibleProvider
    log.info("Forge provider: Ollama fallback @ %s", _OLLAMA_BASE)
    _provider = OpenAICompatibleProvider(
        base_url=_OLLAMA_BASE, api_key="ollama", model=_FORGE_MODEL, timeout=120.0,
    )
    return _provider


# ── Data types ────────────────────────────────────────────────────────────────

@dataclass
class ForgeTask:
    """A single focused improvement task — one LLM call."""

    task_id: str
    file: str          # relative to target_root
    abs_path: str      # absolute path for file writes
    node: str          # function/class name
    node_type: str     # "function" | "class" | "module"
    start_line: int    # 1-indexed, inclusive
    end_line: int      # 1-indexed, inclusive
    code: str          # current source of the node
    issue: str         # "missing_docstring" | "todo_comment" | "debug_hardcoded" | "missing_404"
    instruction: str   # human-readable fix instruction for the LLM


@dataclass
class TaskResult:
    """Result of executing one ForgeTask."""

    task_id: str
    file: str
    node: str
    issue: str
    fixed_code: str | None
    verified: bool
    error: str | None = None
    diff_summary: str = ""


@dataclass
class EpiphanyPlan:
    """Structured plan produced by the Epiphany analysis pass."""

    schema: str = "atomadic.epiphany-plan.v1"
    idea: str = "Improve materialized codebase"
    experiments: list[ForgeTask] = field(default_factory=list)
    vetted_sources: list[str] = field(default_factory=list)
    promoted: bool = False


@dataclass
class ForgeResult:
    """Aggregate result of the full forge phase."""

    plan_tasks: int = 0
    applied: int = 0
    skipped: int = 0
    files_modified: set[str] = field(default_factory=set)
    results: list[TaskResult] = field(default_factory=list)
    model_used: str = ""


# ── Helpers ───────────────────────────────────────────────────────────────────

def _strip_thinking(text: str) -> str:
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()


def _strip_fences(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        newline = text.find("\n")
        if newline != -1:
            text = text[newline + 1:]
    last_fence = text.rfind("```")
    if last_fence != -1:
        text = text[:last_fence].rstrip()
    return text.strip()


def _validate_python(source: str) -> tuple[bool, str]:
    try:
        ast.parse(source)
        return True, ""
    except SyntaxError as exc:
        return False, f"SyntaxError line {exc.lineno}: {exc.msg}"


def _get_node_source(source_lines: list[str], node: ast.AST) -> tuple[int, int, str]:
    """Return (start_line, end_line, code) for a function or class node.

    Lines are 1-indexed inclusive. end_line is node.end_lineno.
    """
    start = node.lineno  # 1-indexed
    end = node.end_lineno  # 1-indexed
    code = "".join(source_lines[start - 1 : end])
    return start, end, code


def _node_has_docstring(node: ast.AST) -> bool:
    body = getattr(node, "body", [])
    return (
        body
        and isinstance(body[0], ast.Expr)
        and isinstance(body[0].value, (ast.Constant, ast.Str))
    )


def _body_has_todo(source_lines: list[str], start: int, end: int) -> bool:
    return any(
        "# TODO" in line or "# todo" in line or "# FIXME" in line
        for line in source_lines[start - 1 : end]
    )


def _is_trivial_init(path: Path) -> bool:
    if path.name != "__init__.py":
        return False
    text = path.read_text(encoding="utf-8").strip()
    non_comment = [l for l in text.splitlines() if l.strip() and not l.strip().startswith("#")]
    return len(non_comment) <= 5


# ── Phase 1: Epiphany — analyze, generate plan ────────────────────────────────

def _analyze_file(path: Path, target_root: Path) -> list[ForgeTask]:
    """Parse one Python file and return a list of improvement tasks."""
    tasks: list[ForgeTask] = []
    try:
        source = path.read_text(encoding="utf-8")
    except Exception:
        return tasks

    source_lines = source.splitlines(keepends=True)
    rel = path.relative_to(target_root).as_posix()
    task_counter = [0]

    def _tid(issue: str) -> str:
        task_counter[0] += 1
        return f"{rel}:{issue}:{task_counter[0]}"

    # Module-level: debug=True in app.run()
    if "debug=True" in source:
        for lineno, line in enumerate(source_lines, 1):
            if "app.run(" in line and "debug=True" in line:
                tasks.append(ForgeTask(
                    task_id=_tid("debug_hardcoded"),
                    file=rel,
                    abs_path=str(path),
                    node="app.run",
                    node_type="module",
                    start_line=lineno,
                    end_line=lineno,
                    code=line.rstrip(),
                    issue="debug_hardcoded",
                    instruction=(
                        "Replace `app.run(debug=True)` with "
                        "`app.run(debug=os.getenv('FLASK_DEBUG', '0') == '1')`. "
                        "Add `import os` at the top of the file if not already present. "
                        "Return ONLY the complete fixed file."
                    ),
                ))

    # Parse AST for function/class level issues
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return tasks

    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            continue
        if not hasattr(node, "end_lineno"):
            continue

        start, end, code = _get_node_source(source_lines, node)
        node_type = "function" if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) else "class"

        # Missing docstring
        if not _node_has_docstring(node):
            if node_type == "function":
                instr = (
                    f"Add a concise Google-style docstring to the function `{node.name}`. "
                    "Include Args and Returns sections if the function has parameters or a return value. "
                    "Return ONLY the complete fixed function, preserving all existing code."
                )
            else:
                instr = (
                    f"Add a concise one-line docstring to the class `{node.name}`. "
                    "Return ONLY the complete fixed class, preserving all existing code."
                )
            tasks.append(ForgeTask(
                task_id=_tid("missing_docstring"),
                file=rel,
                abs_path=str(path),
                node=node.name,
                node_type=node_type,
                start_line=start,
                end_line=end,
                code=code,
                issue="missing_docstring",
                instruction=instr,
            ))

        # TODO / FIXME comments
        if _body_has_todo(source_lines, start, end):
            tasks.append(ForgeTask(
                task_id=_tid("todo_comment"),
                file=rel,
                abs_path=str(path),
                node=node.name,
                node_type=node_type,
                start_line=start,
                end_line=end,
                code=code,
                issue="todo_comment",
                instruction=(
                    f"Resolve all `# TODO` comments in `{node.name}` by implementing the described changes. "
                    "For SQLAlchemy models, add the missing `db.Column(...)` fields with appropriate types. "
                    "Import any new modules (datetime, etc.) at the top of the file. "
                    "Return ONLY the complete fixed class/function, preserving existing code."
                ),
            ))

        # Missing 404 handling in Flask route handlers
        if (
            node_type == "function"
            and any(
                isinstance(dec, ast.Call) and (
                    (hasattr(dec.func, "attr") and dec.func.attr == "route") or
                    (hasattr(dec.func, "id") and dec.func.id == "route")
                )
                for dec in getattr(node, "decorator_list", [])
            )
            and ".query.get(" in code
            and "404" not in code
            and "abort" not in code
        ):
            tasks.append(ForgeTask(
                task_id=_tid("missing_404"),
                file=rel,
                abs_path=str(path),
                node=node.name,
                node_type="function",
                start_line=start,
                end_line=end,
                code=code,
                issue="missing_404",
                instruction=(
                    f"Add 404 error handling to Flask route `{node.name}`. "
                    "After calling `.query.get(id)`, check if the result is None and return "
                    "`jsonify({{'error': 'Not found'}}), 404`. "
                    "Return ONLY the complete fixed function."
                ),
            ))

    return tasks


def generate_plan(target_root: Path) -> EpiphanyPlan:
    """Epiphany pass — scan materialized output and build improvement plan."""
    plan = EpiphanyPlan(
        idea=f"Improve materialized codebase at {target_root.name}",
        vetted_sources=[str(target_root)],
    )

    py_files = sorted(target_root.rglob("*.py"))
    for path in py_files:
        if _is_trivial_init(path):
            continue
        if path.parent == target_root and path.name == "__init__.py":
            continue
        tasks = _analyze_file(path, target_root)
        plan.experiments.extend(tasks)

    plan.promoted = len(plan.experiments) > 0
    log.info(
        "Epiphany plan: %d improvement tasks across %d files",
        len(plan.experiments),
        len({t.file for t in plan.experiments}),
    )
    return plan


# ── Phase 2: Forge — execute plan in parallel ─────────────────────────────────

def _call_llm(system: str, user: str, model: str, provider: Any = None) -> str | None:  # noqa: ARG001
    """Single focused LLM call via the provider's raw HTTP client.

    Bypasses pydantic CompletionResponse to avoid float-usage issues with
    Groq's non-standard response fields. Retries once on 429.
    """
    if provider is None:
        provider = _get_provider()

    # Extract base_url and api_key from the provider instance
    client = getattr(provider, "_client", None)
    if client is None:
        log.warning("LLM call failed: provider has no _client")
        return None

    body = {
        "model": getattr(provider, "_default_model", model),
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": 0.0,
        "max_tokens": 2048,
    }

    for attempt in range(2):
        try:
            resp = client.post("/chat/completions", json=body)
            if resp.status_code == 429:
                import time
                wait = float(resp.headers.get("retry-after", "5"))
                log.warning("Rate limited by %s — waiting %.0fs", type(provider).__name__, wait)
                time.sleep(wait)
                continue
            resp.raise_for_status()
            raw = resp.json()["choices"][0]["message"]["content"]
            return _strip_fences(_strip_thinking(raw))
        except Exception as exc:
            log.warning("LLM call failed (attempt %d): %s", attempt + 1, exc)
            if attempt == 0:
                import time; time.sleep(2)

    return None


def _execute_task(task: ForgeTask, model: str, provider: Any = None) -> TaskResult:
    """Execute one ForgeTask — one focused LLM call."""
    path = Path(task.abs_path)

    # For module-level tasks (debug=True), send the whole file
    if task.node_type == "module":
        source = path.read_text(encoding="utf-8")
        system = (
            "You are a Python code improver. "
            "Return ONLY the complete fixed Python file. "
            "No explanation, no markdown fences."
        )
        user = f"{task.instruction}\n\nFile to fix:\n\n{source}"
        fixed = _call_llm(system, user, model, provider=provider)
        if fixed is None:
            return TaskResult(task_id=task.task_id, file=task.file, node=task.node,
                              issue=task.issue, fixed_code=None, verified=False,
                              error="LLM call failed")
        valid, err = _validate_python(fixed)
        if not valid:
            return TaskResult(task_id=task.task_id, file=task.file, node=task.node,
                              issue=task.issue, fixed_code=fixed, verified=False,
                              error=f"syntax error: {err}")
        path.write_text(fixed, encoding="utf-8")
        return TaskResult(task_id=task.task_id, file=task.file, node=task.node,
                          issue=task.issue, fixed_code=fixed, verified=True,
                          diff_summary="debug=True removed")

    # For function/class tasks, read current file, extract current node, replace
    try:
        current_source = path.read_text(encoding="utf-8")
    except Exception as exc:
        return TaskResult(task_id=task.task_id, file=task.file, node=task.node,
                          issue=task.issue, fixed_code=None, verified=False,
                          error=f"read failed: {exc}")

    system = (
        "You are a Python code improver. "
        "Return ONLY the fixed Python code block (function or class). "
        "Preserve the original indentation exactly. "
        "No explanation, no markdown fences, no extra blank lines at start/end."
    )
    user = (
        f"{task.instruction}\n\n"
        f"Code to fix:\n\n{task.code}\n\n"
        "Return ONLY the complete fixed function/class. Same indentation as input."
    )

    fixed_node = _call_llm(system, user, model, provider=provider)
    if fixed_node is None:
        return TaskResult(task_id=task.task_id, file=task.file, node=task.node,
                          issue=task.issue, fixed_code=None, verified=False,
                          error="LLM call failed")

    # Validate the fixed node parses on its own
    valid, err = _validate_python(textwrap.dedent(fixed_node))
    if not valid:
        return TaskResult(task_id=task.task_id, file=task.file, node=task.node,
                          issue=task.issue, fixed_code=fixed_node, verified=False,
                          error=f"syntax error: {err}")

    # Re-read the file (may have changed from a parallel task on same file)
    current_source = path.read_text(encoding="utf-8")
    current_lines = current_source.splitlines(keepends=True)

    # Re-locate the node in the current file (line numbers may have shifted)
    try:
        tree = ast.parse(current_source)
    except SyntaxError:
        return TaskResult(task_id=task.task_id, file=task.file, node=task.node,
                          issue=task.issue, fixed_code=fixed_node, verified=False,
                          error="current file has syntax error (parallel task collision?)")

    target_node = None
    for n in ast.walk(tree):
        if (
            isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
            and n.name == task.node
            and hasattr(n, "end_lineno")
        ):
            target_node = n
            break

    if target_node is None:
        return TaskResult(task_id=task.task_id, file=task.file, node=task.node,
                          issue=task.issue, fixed_code=fixed_node, verified=False,
                          error=f"node '{task.node}' not found in current file")

    cur_start, cur_end = target_node.lineno, target_node.end_lineno

    # Build new file: lines before + fixed node + lines after
    fixed_lines_list = fixed_node.splitlines(keepends=True)
    if fixed_lines_list and not fixed_lines_list[-1].endswith("\n"):
        fixed_lines_list[-1] += "\n"

    new_lines = (
        current_lines[: cur_start - 1]
        + fixed_lines_list
        + current_lines[cur_end:]
    )
    new_source = "".join(new_lines)

    # Final full-file validation
    valid_full, err_full = _validate_python(new_source)
    if not valid_full:
        return TaskResult(task_id=task.task_id, file=task.file, node=task.node,
                          issue=task.issue, fixed_code=fixed_node, verified=False,
                          error=f"full-file validation failed: {err_full}")

    path.write_text(new_source, encoding="utf-8")

    diff_parts: list[str] = []
    if task.issue == "missing_docstring":
        diff_parts.append("docstring added")
    elif task.issue == "todo_comment":
        diff_parts.append("TODOs resolved")
    elif task.issue == "missing_404":
        diff_parts.append("404 handling added")
    else:
        diff_parts.append("code improved")

    return TaskResult(
        task_id=task.task_id, file=task.file, node=task.node,
        issue=task.issue, fixed_code=fixed_node, verified=True,
        diff_summary=", ".join(diff_parts),
    )


def execute_plan(
    plan: EpiphanyPlan,
    model: str = _FORGE_MODEL,
    max_workers: int = _MAX_WORKERS,
) -> ForgeResult:
    """ForgeLoop — execute all tasks in the Epiphany plan using a thread pool.

    Tasks on the same file run sequentially (same-file serialization) to avoid
    line-number drift from concurrent writes. Tasks on different files run in
    parallel.
    """
    result = ForgeResult(plan_tasks=len(plan.experiments), model_used=model)

    # Build provider pool — one provider per available API key for true parallel
    provider_pool = _get_all_providers()
    n_providers = len(provider_pool)
    if n_providers > 1:
        log.info(
            "Forge multi-provider: %d providers available for %d file group(s)",
            n_providers, len({t.file for t in plan.experiments}),
        )

    # Group tasks by file to serialize per-file execution
    from collections import defaultdict
    by_file: dict[str, list[ForgeTask]] = defaultdict(list)
    for task in plan.experiments:
        by_file[task.file].append(task)

    def _run_file_tasks(tasks: list[ForgeTask], provider: Any) -> list[TaskResult]:
        # Module-level tasks (debug fix) must run FIRST since they rewrite the whole file
        ordered = sorted(tasks, key=lambda t: (0 if t.node_type == "module" else 1, t.start_line))
        return [_execute_task(t, model, provider=provider) for t in ordered]

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {
            pool.submit(_run_file_tasks, tasks, provider_pool[i % n_providers]): file
            for i, (file, tasks) in enumerate(by_file.items())
        }
        for future in as_completed(futures):
            file_path = futures[future]
            try:
                task_results = future.result()
            except Exception as exc:
                log.error("Forge task group failed for %s: %s", file_path, exc)
                continue
            for tr in task_results:
                result.results.append(tr)
                if tr.verified:
                    result.applied += 1
                    result.files_modified.add(tr.file)
                else:
                    result.skipped += 1
                    log.warning("Task %s skipped: %s", tr.task_id, tr.error)

    log.info(
        "Forge complete: %d/%d tasks applied, %d files modified",
        result.applied, result.plan_tasks, len(result.files_modified),
    )
    return result


# ── Orchestrator entry point ──────────────────────────────────────────────────

def run_forge_phase(
    target_root: Path,
    model: str = _FORGE_MODEL,
    max_workers: int = _MAX_WORKERS,
) -> dict[str, Any]:
    """Full forge phase: Epiphany analysis → ForgeLoop execution.

    Returns a summary dict compatible with the orchestrator phases dict.
    """
    log.info("Phase 5b [Epiphany]: Analyzing %s …", target_root.name)
    plan = generate_plan(target_root)

    if not plan.promoted:
        log.info("Epiphany: no improvement tasks found — skipping forge")
        return {"tasks": 0, "applied": 0, "skipped": 0, "files_modified": 0}

    log.info(
        "Phase 5b [Forge]: Executing %d tasks across %d files (model=%s, workers=%d) …",
        len(plan.experiments),
        len({t.file for t in plan.experiments}),
        model,
        max_workers,
    )
    forge = execute_plan(plan, model=model, max_workers=max_workers)

    summary: dict[str, Any] = {
        "tasks": forge.plan_tasks,
        "applied": forge.applied,
        "skipped": forge.skipped,
        "files_modified": len(forge.files_modified),
        "model": forge.model_used,
        "changes": [
            {
                "file": r.file,
                "node": r.node,
                "issue": r.issue,
                "verified": r.verified,
                "summary": r.diff_summary,
                "error": r.error,
            }
            for r in forge.results
        ],
    }
    return summary
