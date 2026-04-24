"""Tier a3 — skill runner: discoverable multi-step workflows for the Atomadic agent."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable


# ── Skill API ─────────────────────────────────────────────────────────────────

@dataclass
class SkillContext:
    """Context object passed into every skill's execute() function."""
    user_input: str
    working_dir: Path
    tone: str
    domain_level: str = "intermediate"
    history: list[Any] = field(default_factory=list)
    extra: dict = field(default_factory=dict)


@dataclass
class Skill:
    """A named, discoverable workflow for the Atomadic agent.

    Skills are prioritised over generic CLI dispatch when their trigger score
    meets the threshold. They can read files, run subprocesses, and return
    formatted Markdown for the interpreter to display.
    """
    name: str
    description: str
    triggers: list[str]
    usage: str
    execute: Callable[[SkillContext], str]

    def match_score(self, user_input: str) -> int:
        """Count how many trigger phrases appear in user_input."""
        lower = user_input.lower()
        return sum(1 for t in self.triggers if t in lower)


# ── Skill registry ────────────────────────────────────────────────────────────

class SkillRunner:
    """Discovers built-in and user-defined skills; dispatches the best match."""

    # Minimum trigger-phrase hits required to prefer a skill over generic dispatch.
    MATCH_THRESHOLD = 2

    def __init__(self, working_dir: Path) -> None:
        self._working_dir = working_dir
        self._skills: dict[str, Skill] = {}
        _register_builtins(self._skills)
        self._discover_user_skills()

    def _discover_user_skills(self) -> None:
        """Load skills from <working_dir>/.ass-ade/skills/*.py."""
        import importlib.util

        skills_dir = self._working_dir / ".ass-ade" / "skills"
        if not skills_dir.is_dir():
            return

        for py_file in sorted(skills_dir.glob("*.py")):
            if py_file.name.startswith("_"):
                continue
            try:
                spec = importlib.util.spec_from_file_location(
                    f"user_skill_{py_file.stem}", py_file
                )
                if not (spec and spec.loader):
                    continue
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)  # type: ignore[union-attr]
                meta = getattr(mod, "SKILL_META", None)
                run_fn = getattr(mod, "run", None)
                if meta and run_fn and isinstance(meta, dict):
                    skill = Skill(
                        name=meta.get("name", py_file.stem),
                        description=meta.get("description", "Custom skill"),
                        triggers=meta.get("triggers", []),
                        usage=meta.get("usage", f"@skill {py_file.stem}"),
                        execute=lambda ctx, fn=run_fn: fn(ctx),
                    )
                    self._skills[skill.name] = skill
            except Exception:
                pass

    def match(self, user_input: str) -> Skill | None:
        """Return the best-matching skill, or None if no skill hits the threshold."""
        best: tuple[int, Skill | None] = (0, None)
        for skill in self._skills.values():
            score = skill.match_score(user_input)
            if score > best[0]:
                best = (score, skill)
        score, skill = best
        return skill if score >= self.MATCH_THRESHOLD else None

    def get(self, name: str) -> Skill | None:
        return self._skills.get(name)

    def list_skills(self) -> list[dict]:
        return [
            {"name": s.name, "description": s.description, "usage": s.usage}
            for s in sorted(self._skills.values(), key=lambda s: s.name)
        ]

    def run(self, skill: Skill, ctx: SkillContext) -> str:
        try:
            return skill.execute(ctx)
        except Exception as exc:
            return f"[skill:{skill.name}] Error — {exc}"


# ── Built-in skill implementations ────────────────────────────────────────────

def _run_git_workflow(ctx: SkillContext) -> str:
    """git status → diff summary → commit message suggestion."""
    wd = str(ctx.working_dir)

    def _run(cmd: list[str]) -> tuple[str, int]:
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, cwd=wd, timeout=15)
            return (r.stdout + r.stderr).strip(), r.returncode
        except Exception as exc:
            return str(exc), -1

    status_out, _ = _run(["git", "status", "--short"])
    if not status_out:
        return "Working tree is clean — nothing to commit."

    lines = [f"**Git status:**\n```\n{status_out}\n```\n"]

    diff_out, _ = _run(["git", "diff", "--stat"])
    if diff_out:
        lines.append(f"**Unstaged changes:**\n```\n{diff_out}\n```\n")

    staged_out, _ = _run(["git", "diff", "--staged", "--stat"])
    if staged_out:
        lines.append(f"**Staged changes:**\n```\n{staged_out}\n```\n")

    changed = [ln.split()[-1] for ln in status_out.splitlines() if ln.strip()][:5]
    if changed:
        if len(changed) == 1 and changed[0].endswith(".py"):
            stem = Path(changed[0]).stem.replace("_", " ")
            suggestion = f"feat: update {stem}"
        else:
            suggestion = f"chore: update {', '.join(changed[:3])}"
        lines.append(f"**Suggested commit message:**\n```\n{suggestion}\n```")
        lines.append("\nRun `git add -A && git commit -m '<message>'` to commit.")

    return "\n".join(lines)


def _run_debug_session(ctx: SkillContext) -> str:
    """Structured debugging: error extraction → hypothesis → fix guidance."""
    text = ctx.user_input
    errors_found: list[str] = []
    for pattern in (
        r"(TypeError[:\s][^\n]+)",
        r"(AttributeError[:\s][^\n]+)",
        r"(ImportError[:\s][^\n]+)",
        r"(ModuleNotFoundError[:\s][^\n]+)",
        r"(KeyError[:\s][^\n]+)",
        r"(ValueError[:\s][^\n]+)",
        r"(RuntimeError[:\s][^\n]+)",
        r"(Exception[:\s][^\n]+)",
        r"(Error: [^\n]+)",
        r"(line \d+[^\n]+)",
    ):
        errors_found.extend(re.findall(pattern, text, re.IGNORECASE)[:1])

    lines: list[str] = ["**Debug Session**\n"]

    if errors_found:
        lines.append("**Detected errors:**")
        for e in errors_found[:3]:
            lines.append(f"  - `{e.strip()}`")
        lines.append("")

    lower = text.lower()
    if "importerror" in lower or "modulenotfounderror" in lower:
        lines.append("**Likely cause:** Package not installed or wrong `PYTHONPATH`.")
        lines.append("**Fix:** `pip install <package>` — or check you're in the right venv.")
    elif "attributeerror" in lower:
        lines.append("**Likely cause:** Wrong type — object doesn't have that attribute.")
        lines.append("**Fix:** Run `type(obj)` and `dir(obj)` to inspect the actual object.")
    elif "typeerror" in lower:
        lines.append("**Likely cause:** Wrong argument type or count.")
        lines.append("**Fix:** Check the function signature and what you're passing in.")
    elif "keyerror" in lower:
        lines.append("**Likely cause:** Key doesn't exist in the dict.")
        lines.append("**Fix:** Use `.get(key, default)` to check safely first.")
    elif "nonetype" in lower:
        lines.append("**Likely cause:** Something returned `None` unexpectedly.")
        lines.append("**Fix:** Add a `None` check before the failing line; trace back where the `None` came from.")
    elif "indentationerror" in lower or "syntaxerror" in lower:
        lines.append("**Likely cause:** Syntax error — often a missing colon, unclosed bracket, or bad indent.")
        lines.append("**Fix:** Look at the line *before* the one the error points to — that's usually the real culprit.")
    else:
        lines.append("**Debugging checklist:**")
        lines.append("1. Find the first traceback line in *your* code (not a library)")
        lines.append("2. Read the exact error message — it usually says exactly what's wrong")
        lines.append("3. Print the variable values at the failing line")
        lines.append("4. Check your assumptions: is the type what you expect?")

    lines.append("\nPaste the full traceback and I'll give you a targeted fix.")
    return "\n".join(lines)


def _run_explain_code(ctx: SkillContext) -> str:
    """Explain a file or code snippet at the right level for the user's domain."""
    text = ctx.user_input
    wd = ctx.working_dir
    domain = ctx.domain_level

    path_match = re.search(r"(?:of|in|for|from)?\s+([\w./\\-]+\.py)", text, re.IGNORECASE)
    lines: list[str] = ["**Code Explanation**\n"]

    if path_match:
        candidate = wd / path_match.group(1).strip()
        if candidate.exists():
            try:
                content = candidate.read_text(encoding="utf-8")[:4000]
                n_lines = content.count("\n")
                import_lines = [l for l in content.splitlines() if l.startswith(("import ", "from "))]
                classes = re.findall(r"^class\s+(\w+)", content, re.MULTILINE)
                funcs = re.findall(r"^def\s+(\w+)", content, re.MULTILINE)
                async_funcs = re.findall(r"^async def\s+(\w+)", content, re.MULTILINE)

                lines.append(f"**`{candidate.name}`** — {n_lines} lines\n")
                lines.append(f"- {len(import_lines)} import(s)")
                if classes:
                    lines.append(f"- Classes: `{'`, `'.join(classes[:6])}`")
                if funcs or async_funcs:
                    all_fns = funcs + [f"async {f}" for f in async_funcs]
                    lines.append(f"- Functions: `{'`, `'.join(all_fns[:10])}`")

                # Docstring extraction
                doc_match = re.search(r'"""(.+?)"""', content, re.DOTALL)
                if doc_match:
                    doc = doc_match.group(1).strip().splitlines()[0][:120]
                    lines.append(f"\n**Module purpose:** {doc}")

                if domain == "novice":
                    lines.append("\nAsk me about any specific function and I'll explain it in plain English.")
                elif domain == "expert":
                    lines.append("\nAsk about specific patterns, edge cases, or architectural decisions.")
                else:
                    lines.append("\nAsk about any part you want me to dig into.")
            except OSError:
                lines.append(f"Could not read `{candidate}`. Is that the right path?")
        else:
            lines.append(f"File `{path_match.group(1)}` not found in `{wd.name}`.")
            lines.append("Check the path, or paste the code directly.")
    else:
        lines.append("Paste the code or function you want explained,")
        lines.append("or tell me a filename like `explain src/mymodule.py`.")
        if domain == "novice":
            lines.append("\nI'll explain in plain English — no assumptions about your background.")
        elif domain == "expert":
            lines.append("\nI'll keep it technical — patterns, tradeoffs, and subtle behaviours.")

    return "\n".join(lines)


def _run_quick_check(ctx: SkillContext) -> str:
    """Fast health check: lint + tests + certificate."""
    wd = str(ctx.working_dir)
    lines: list[str] = ["**Quick Health Check**\n"]

    # Lint
    try:
        r = subprocess.run(
            [sys.executable, "-m", "ass_ade", "lint", wd, "--local-only"],
            capture_output=True, text=True, cwd=wd, timeout=60,
        )
        ok = r.returncode == 0
        lines.append(f"{'✅' if ok else '⚠️'} **Lint:** {'PASS' if ok else 'issues found'}")
        if not ok:
            snippet = (r.stdout + r.stderr)[:300].strip()
            if snippet:
                lines.append(f"```\n{snippet}\n```")
    except Exception as exc:
        lines.append(f"⚠️ **Lint:** could not run ({exc})")

    # Test files
    try:
        test_files = list(ctx.working_dir.rglob("test_*.py"))
        lines.append(f"{'✅' if test_files else '⚠️'} **Tests:** {len(test_files)} test file(s)")
    except Exception:
        pass

    # Certificate
    cert_path = ctx.working_dir / "CERTIFICATE.json"
    if cert_path.exists():
        try:
            cert = json.loads(cert_path.read_text(encoding="utf-8"))
            date = cert.get("date", cert.get("timestamp", ""))[:10]
            lines.append(f"✅ **Certificate:** last certified {date}")
        except Exception:
            lines.append("⚠️ **Certificate:** found but unreadable")
    else:
        lines.append("⚠️ **Certificate:** none — run `ass-ade certify .` to create one")

    return "\n".join(lines)


def _run_test_runner(ctx: SkillContext) -> str:
    """Run pytest with smart filtering and a failure summary."""
    wd = str(ctx.working_dir)
    text = ctx.user_input

    filter_match = re.search(r"(?:for|about|matching|on)\s+(\w[\w_-]*)", text, re.IGNORECASE)
    filter_arg = filter_match.group(1) if filter_match else None

    cmd = [sys.executable, "-m", "pytest", "--tb=short", "-q"]
    if filter_arg:
        cmd += ["-k", filter_arg]

    header = f"**Running tests{f' (filter: `{filter_arg}`)' if filter_arg else ''}**\n"

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=wd, timeout=120)
        output = (result.stdout + result.stderr).strip()

        lines: list[str] = [header]

        summary = re.search(r"(\d+ passed.*)", output)
        if summary:
            lines.append(f"**Result:** {summary.group(1)}")

        failures = re.findall(r"FAILED (.+)", output)
        if failures:
            lines.append(f"\n**Failed ({len(failures)}):**")
            for f in failures[:8]:
                lines.append(f"  - `{f.strip()}`")

        if "short test summary" in output:
            idx = output.find("short test summary")
            lines.append(f"\n```\n{output[idx:idx+600]}\n```")
        elif result.returncode == 0 and not failures:
            lines.append("All tests passed. ✅")
        elif not output:
            lines.append("No test output — are there test files in this directory?")

        return "\n".join(lines)
    except subprocess.TimeoutExpired:
        return f"{header}Tests timed out after 120 s."
    except Exception as exc:
        return f"{header}Error running tests: {exc}"


def _run_dependency_scan(ctx: SkillContext) -> str:
    """Check for outdated or missing dependencies."""
    wd = ctx.working_dir
    lines: list[str] = ["**Dependency Scan**\n"]

    req_files = list(wd.glob("requirements*.txt")) + list(wd.glob("pyproject.toml"))
    if not req_files:
        lines.append("No `requirements*.txt` or `pyproject.toml` found here.")
        return "\n".join(lines)

    for rf in req_files[:3]:
        lines.append(f"Found: `{rf.name}`")
    lines.append("")

    try:
        r = subprocess.run(
            [sys.executable, "-m", "pip", "list", "--outdated", "--format=columns"],
            capture_output=True, text=True, timeout=30,
        )
        out_lines = r.stdout.strip().splitlines()
        if len(out_lines) > 2:
            lines.append(f"**Outdated packages ({len(out_lines) - 2}):**")
            lines.append(f"```\n{chr(10).join(out_lines[:14])}\n```")
            lines.append("Run `pip install --upgrade <package>` to update.")
        else:
            lines.append("All packages are up to date. ✅")
    except Exception as exc:
        lines.append(f"Could not check outdated packages: {exc}")

    return "\n".join(lines)


def _run_scout(ctx: SkillContext) -> str:
    """Scout a repo: static intel, symbol count, benefit mapping, recommendations."""
    from ass_ade.local.scout import scout_repo

    text = ctx.user_input
    wd = ctx.working_dir

    path_match = re.search(r"scout\s+([\w./\\:-]+)", text, re.IGNORECASE)
    if path_match:
        candidate = Path(path_match.group(1).strip())
        if not candidate.is_absolute():
            candidate = wd / candidate
        target = candidate if candidate.exists() else wd
    else:
        target = wd

    use_llm = "--llm" in text or "with llm" in text.lower()
    benefit = wd if target != wd else None

    try:
        report = scout_repo(target, benefit_root=benefit, use_llm=use_llm)
    except Exception as exc:
        return f"Scout failed: {exc}"

    summary = report.get("summary", {})
    symbols = report.get("symbol_summary", {})
    llm_result = report.get("llm", {})
    recs = report.get("static_recommendations", [])

    display_name = target.resolve().name or str(target.resolve())
    lines = [f"**Scout: `{display_name}`**\n"]
    lines.append(
        f"- Files: {summary.get('total_files', 0)} "
        f"| Dirs: {summary.get('total_dirs', 0)}"
    )

    py_files = symbols.get("python_files", 0)
    sym_count = symbols.get("symbols", 0)
    tested = symbols.get("tested_symbols", 0)
    if py_files:
        lines.append(f"- Python: {py_files} files, {sym_count} symbols, {tested} tested")

    file_types = summary.get("file_types", {})
    if file_types:
        top = " | ".join(f"{ext}: {n}" for ext, n in list(file_types.items())[:5])
        lines.append(f"- File types: {top}")

    target_map = report.get("target_map")
    if target_map:
        counts = target_map.get("action_counts", {})
        lines.append(
            f"\n**Benefit mapping:** "
            f"assimilate={counts.get('assimilate', 0)}, "
            f"enhance={counts.get('enhance', 0)}, "
            f"rebuild={counts.get('rebuild', 0)}, "
            f"skip={counts.get('skip', 0)}"
        )

    if recs:
        lines.append("\n**Recommendations:**")
        for rec in recs[:4]:
            lines.append(f"- [{rec.get('priority', '?')}] {rec.get('title', '')}")

    if llm_result.get("status") == "ok":
        analysis = llm_result.get("analysis", {})
        if isinstance(analysis, dict):
            if analysis.get("summary"):
                lines.append(f"\n**LLM:** {analysis['summary']}")
            ops = analysis.get("opportunities", [])
            if ops:
                lines.append("**Opportunities:**")
                for op in ops[:4]:
                    lines.append(f"- {op}")
    elif llm_result.get("status") == "unavailable":
        lines.append(f"\n_LLM unavailable — {llm_result.get('error', '')[:120]}_")

    lines.append(f"\n_Full report: `ass-ade scout {target} --json-out scout.json`_")
    return "\n".join(lines)


def _run_file_reader(ctx: SkillContext) -> str:
    """Read a file from the working directory and return its content."""
    text = ctx.user_input
    wd = ctx.working_dir

    path_match = re.search(
        r"(?:read|open|show|cat|look at|check)\s+([\w./\\-]+(?:\.\w+)?)", text, re.IGNORECASE
    )
    if not path_match:
        path_match = re.search(r"([\w./\\-]+\.\w+)", text)

    if not path_match:
        return "Which file would you like me to read? Give me a path, e.g. `read src/module.py`."

    target = wd / path_match.group(1).strip()
    if not target.exists():
        # Try relative to cwd
        target = Path(path_match.group(1).strip())
    if not target.exists():
        return f"File `{path_match.group(1)}` not found. Check the path and try again."

    try:
        content = target.read_text(encoding="utf-8", errors="replace")
        if len(content) > 6000:
            content = content[:6000] + "\n...(truncated — file is large)"
        return f"**`{target.name}`** ({len(content.splitlines())} lines)\n\n```\n{content}\n```"
    except OSError as exc:
        return f"Could not read `{target}`: {exc}"


# ── Registration ───────────────────────────────────────────────────────────────

def _register_builtins(registry: dict[str, Skill]) -> None:
    skills = [
        Skill(
            name="git",
            description="Git workflow — status, diff, commit message suggestion",
            triggers=["git status", "git diff", "commit", "staged", "what changed",
                      "git changes", "push changes", "uncommitted", "git workflow"],
            usage="show me what changed in git",
            execute=_run_git_workflow,
        ),
        Skill(
            name="debug",
            description="Structured debugging — error analysis, hypothesis, targeted fix",
            triggers=["debug", "error:", "exception", "traceback", "not working",
                      "fails with", "getting an error", "broken", "crash", "crashing",
                      "stack trace", "typeerror", "attributeerror", "importerror"],
            usage="help me debug: <traceback>",
            execute=_run_debug_session,
        ),
        Skill(
            name="explain",
            description="Explain code at the right level for your expertise",
            triggers=["explain", "what does this do", "how does", "walk me through",
                      "understand this", "explain this file", "explain the", "what is this file"],
            usage="explain src/mymodule.py",
            execute=_run_explain_code,
        ),
        Skill(
            name="check",
            description="Quick health check — lint + test count + certificate",
            triggers=["quick check", "health check", "check the code", "code health",
                      "is everything ok", "status check", "quick status"],
            usage="quick check",
            execute=_run_quick_check,
        ),
        Skill(
            name="test",
            description="Run pytest with filtering and a failure summary",
            triggers=["run tests", "run the tests", "pytest", "run unit tests",
                      "run my tests", "test results", "failing tests", "run test"],
            usage="run tests for auth",
            execute=_run_test_runner,
        ),
        Skill(
            name="deps",
            description="Check for outdated or missing dependencies",
            triggers=["dependencies", "outdated packages", "pip list", "requirements",
                      "check deps", "package updates", "update packages", "dep scan"],
            usage="check my dependencies",
            execute=_run_dependency_scan,
        ),
        Skill(
            name="read",
            description="Read and display a file from the working directory",
            triggers=["read the file", "show me the file", "open the file", "cat ",
                      "show file", "read file", "look at the", "check the file"],
            usage="read src/module.py",
            execute=_run_file_reader,
        ),
        Skill(
            name="scout",
            description="Scout a repo — static intel, symbol map, benefit mapping, LLM synthesis",
            triggers=["scout", "survey this repo", "analyze this repo", "repo intel",
                      "what's in this repo", "scout this", "scout the repo",
                      "survey the repo", "scan this repo", "what does this repo contain"],
            usage="scout ../sibling-repo",
            execute=_run_scout,
        ),
    ]
    for s in skills:
        registry[s.name] = s
