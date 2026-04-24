"""Repository scout: static intel plus optional LLM synthesis."""

from __future__ import annotations

import ast
import json
from collections import Counter
from pathlib import Path
from typing import Any

from ass_ade.a1_at_functions.assimilation_target_map import (
    build_assimilation_target_map,
    scan_symbols,
)
from ass_ade.config import AssAdeConfig
from ass_ade.engine.router import build_provider
from ass_ade.engine.types import CompletionRequest, Message
from ass_ade.local.enhancer import build_enhancement_report
from ass_ade.local.repo import summarize_repo

_PACKAGE_FILES = (
    "pyproject.toml",
    "package.json",
    "Cargo.toml",
    "go.mod",
    "requirements.txt",
    "setup.py",
    "uv.lock",
    "poetry.lock",
)
_DOC_FILES = ("README.md", "README.rst", "docs", "mkdocs.yml")
_ENTRY_HINTS = ("cli.py", "__main__.py", "main.py", "app.py", "server.py")
_MAX_SAMPLE_FILES = 18


def _read_text(path: Path, max_chars: int = 80_000) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")[:max_chars]
    except OSError:
        return ""


def _walk_files(root: Path) -> list[Path]:
    ignored = {
        ".git",
        ".hg",
        ".svn",
        ".venv",
        "__pycache__",
        "node_modules",
        "dist",
        "build",
        ".pytest_cache",
        ".ruff_cache",
        ".ass-ade",
    }
    files: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(root)
        if any(part in ignored for part in rel.parts):
            continue
        files.append(path)
    return sorted(files)


def _detect_repo_traits(root: Path, files: list[Path]) -> dict[str, Any]:
    rel_names = {path.relative_to(root).as_posix() for path in files}
    top_names = {path.name for path in files}
    package_files = sorted(name for name in _PACKAGE_FILES if name in top_names)
    docs = sorted(name for name in _DOC_FILES if (root / name).exists())
    entrypoints = sorted(
        path.relative_to(root).as_posix()
        for path in files
        if path.name in _ENTRY_HINTS or path.name.startswith("manage.")
    )[:20]
    test_files = sorted(
        path.relative_to(root).as_posix()
        for path in files
        if path.name.startswith("test_")
        or path.name.endswith("_test.py")
        or "tests/" in path.relative_to(root).as_posix()
    )[:30]
    ci_files = sorted(
        name
        for name in rel_names
        if name.startswith(".github/workflows/")
        or name in {".gitlab-ci.yml", "azure-pipelines.yml", "tox.ini", "noxfile.py"}
    )
    return {
        "package_files": package_files,
        "docs": docs,
        "entrypoints": entrypoints,
        "test_files_sample": test_files,
        "ci_files": ci_files,
    }


def _dependency_hints(root: Path) -> dict[str, list[str]]:
    hints: dict[str, list[str]] = {}
    req = root / "requirements.txt"
    if req.is_file():
        hints["requirements.txt"] = [
            line.strip()
            for line in _read_text(req).splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        ][:40]
    pyproject = root / "pyproject.toml"
    if pyproject.is_file():
        lines = []
        for line in _read_text(pyproject).splitlines():
            stripped = line.strip()
            if stripped.startswith('"') or stripped.startswith("'") or "dependencies" in stripped:
                lines.append(stripped)
        hints["pyproject.toml"] = lines[:60]
    package = root / "package.json"
    if package.is_file():
        try:
            data = json.loads(_read_text(package))
            deps = sorted((data.get("dependencies") or {}).keys())
            dev = sorted((data.get("devDependencies") or {}).keys())
            hints["package.json"] = deps[:30] + [f"dev:{name}" for name in dev[:20]]
        except json.JSONDecodeError:
            hints["package.json"] = ["unparseable package.json"]
    return hints


def _sample_python_modules(root: Path, files: list[Path]) -> list[dict[str, Any]]:
    samples: list[dict[str, Any]] = []
    for path in [p for p in files if p.suffix == ".py"][:_MAX_SAMPLE_FILES]:
        text = _read_text(path)
        try:
            tree = ast.parse(text)
        except SyntaxError:
            continue
        funcs = [
            node.name
            for node in ast.walk(tree)
            if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
            and not node.name.startswith("_")
        ][:12]
        classes = [
            node.name
            for node in ast.walk(tree)
            if isinstance(node, ast.ClassDef) and not node.name.startswith("_")
        ][:12]
        if funcs or classes:
            samples.append(
                {
                    "path": path.relative_to(root).as_posix(),
                    "classes": classes,
                    "functions": funcs,
                }
            )
    return samples


def _static_recommendations(
    *,
    repo_root: Path,
    benefit_root: Path | None,
    target_map: dict[str, Any] | None,
    enhancement: dict[str, Any],
) -> list[dict[str, Any]]:
    recs: list[dict[str, Any]] = []
    if target_map:
        counts = target_map.get("action_counts") or {}
        if counts.get("assimilate", 0):
            recs.append(
                {
                    "priority": "high",
                    "type": "assimilate",
                    "title": "Low-risk symbols are ready for policy-scoped assimilation",
                    "evidence": counts,
                }
            )
        if counts.get("enhance", 0):
            recs.append(
                {
                    "priority": "high",
                    "type": "enhance",
                    "title": "Sibling has related symbols that can harden existing ASS-ADE features",
                    "evidence": counts,
                }
            )
        if counts.get("rebuild", 0):
            recs.append(
                {
                    "priority": "medium",
                    "type": "rebuild",
                    "title": "Some candidates need tier-safe rebuild before adoption",
                    "evidence": counts,
                }
            )
    if enhancement.get("total_findings", 0):
        recs.append(
            {
                "priority": "medium",
                "type": "quality",
                "title": "Scout found quality/security findings to review before trusting this repo",
                "evidence": {
                    "total_findings": enhancement.get("total_findings"),
                    "by_category": enhancement.get("by_category"),
                },
            }
        )
    if not recs:
        recs.append(
            {
                "priority": "low",
                "type": "observe",
                "title": "No obvious adoption target found from static evidence",
                "evidence": {"repo": str(repo_root), "benefit_root": str(benefit_root) if benefit_root else None},
            }
        )
    return recs


def _build_llm_prompt(report: dict[str, Any]) -> str:
    compact = {
        "repo": report["repo"],
        "summary": report["summary"],
        "traits": report["traits"],
        "dependencies": report["dependencies"],
        "symbol_summary": report["symbol_summary"],
        "target_map": {
            "action_counts": (report.get("target_map") or {}).get("action_counts"),
            "top_targets": (report.get("target_map") or {}).get("targets", [])[:20],
        },
        "enhancement": {
            "total_findings": report["enhancement"].get("total_findings"),
            "by_category": report["enhancement"].get("by_category"),
            "findings": report["enhancement"].get("findings", [])[:12],
        },
        "static_recommendations": report["static_recommendations"],
    }
    return (
        "You are ASS-ADE's repository scout. Use only the evidence below. "
        "Identify what this repo contains, what can benefit ASS-ADE, what should be "
        "assimilated/rebuilt/enhanced/skipped, and what risks must be checked first. "
        "Return strict JSON with keys: summary, benefit_thesis, opportunities, risks, "
        "recommended_next_actions. Each opportunity must include action, target, reason, "
        "confidence, and evidence.\n\n"
        f"EVIDENCE_JSON:\n{json.dumps(compact, indent=2, default=str)}"
    )


def _analysis_to_text(analysis: Any) -> str:
    if isinstance(analysis, str):
        return analysis
    return json.dumps(analysis, indent=2, sort_keys=True, default=str)


def _opportunity_action_counts(analysis: Any) -> dict[str, int]:
    counts = {action: 0 for action in ("assimilate", "rebuild", "enhance", "skip")}
    if not isinstance(analysis, dict):
        return counts
    opportunities = analysis.get("opportunities")
    if not isinstance(opportunities, list):
        return counts
    for item in opportunities:
        if not isinstance(item, dict):
            continue
        action = str(item.get("action", "")).lower()
        if action in counts:
            counts[action] += 1
    return counts


def _local_grounding_guard(report: dict[str, Any], analysis: Any) -> dict[str, Any]:
    """Check that LLM opportunities are shaped and evidence-backed."""
    allowed_actions = {"assimilate", "rebuild", "enhance", "skip", "observe", "quality"}
    evidence_blob = json.dumps(
        {
            "traits": report.get("traits"),
            "dependencies": report.get("dependencies"),
            "target_map": report.get("target_map"),
            "enhancement": report.get("enhancement"),
            "symbol_summary": report.get("symbol_summary"),
        },
        default=str,
    ).lower()
    unsupported: list[dict[str, Any]] = []
    checked = 0
    if isinstance(analysis, dict) and isinstance(analysis.get("opportunities"), list):
        for item in analysis["opportunities"]:
            if not isinstance(item, dict):
                unsupported.append({"reason": "opportunity is not an object", "item": str(item)[:160]})
                continue
            checked += 1
            action = str(item.get("action", "")).lower()
            target = str(item.get("target", "")).strip()
            evidence = item.get("evidence")
            if action not in allowed_actions:
                unsupported.append({"target": target, "reason": f"unknown action: {action}"})
            if not target:
                unsupported.append({"reason": "missing target", "action": action})
            elif target.lower() not in evidence_blob and action not in {"observe", "quality"}:
                unsupported.append({"target": target, "reason": "target not found in scout evidence"})
            if evidence in (None, "", [], {}):
                unsupported.append({"target": target, "reason": "missing evidence"})
    return {
        "status": "passed" if not unsupported else "caution",
        "opportunities_checked": checked,
        "unsupported": unsupported[:20],
    }


def _nexus_client_for_guards(settings: AssAdeConfig) -> Any:
    from ass_ade.nexus.client import NexusClient

    return NexusClient(
        base_url=settings.nexus_base_url,
        timeout=settings.request_timeout_s,
        api_key=settings.nexus_api_key,
        agent_id=settings.agent_id,
    )


def _nexus_guard_synthesis(
    *,
    report: dict[str, Any],
    analysis: Any,
    settings: AssAdeConfig,
    model_id: str,
) -> dict[str, Any]:
    """Run AAAA-Nexus trust, hallucination, certification, and drift guards."""
    text = _analysis_to_text(analysis)
    guard: dict[str, Any] = {
        "status": "unavailable",
        "passed": None,
        "checks": {},
        "errors": [],
    }
    client = _nexus_client_for_guards(settings)
    try:
        passed = True

        try:
            trust = client.trust_score(settings.agent_id)
            trust_doc = trust.model_dump() if hasattr(trust, "model_dump") else dict(trust)
            guard["checks"]["trust_score"] = trust_doc
            score = trust_doc.get("score")
            if score is not None and float(score) < 0.5:
                passed = False
        except Exception as exc:  # noqa: BLE001
            guard["errors"].append(f"trust_score:{type(exc).__name__}:{str(exc)[:160]}")

        try:
            hallucination = client.hallucination_oracle(text)
            hallucination_doc = (
                hallucination.model_dump()
                if hasattr(hallucination, "model_dump")
                else dict(hallucination)
            )
            guard["checks"]["hallucination"] = hallucination_doc
            if str(hallucination_doc.get("verdict", "")).lower() == "unsafe":
                passed = False
        except Exception as exc:  # noqa: BLE001
            guard["errors"].append(f"hallucination:{type(exc).__name__}:{str(exc)[:160]}")

        try:
            certified = client.certify_output(
                output=text,
                rubric=[
                    "grounded in provided scout evidence",
                    "no unsupported feature claims",
                    "clear risk and next-action separation",
                ],
            )
            certified_doc = (
                certified.model_dump() if hasattr(certified, "model_dump") else dict(certified)
            )
            guard["checks"]["certification"] = certified_doc
            if certified_doc.get("rubric_passed") is False:
                passed = False
        except Exception as exc:  # noqa: BLE001
            guard["errors"].append(f"certify:{type(exc).__name__}:{str(exc)[:160]}")

        try:
            target_map = report.get("target_map") if isinstance(report.get("target_map"), dict) else {}
            drift = client.drift_check(
                model_id=model_id,
                reference_data={
                    "static_action_counts": (target_map or {}).get("action_counts"),
                    "static_recommendations": report.get("static_recommendations"),
                },
                current_data={
                    "llm_action_counts": _opportunity_action_counts(analysis),
                    "llm_summary": analysis.get("summary") if isinstance(analysis, dict) else None,
                },
            )
            drift_doc = drift.model_dump() if hasattr(drift, "model_dump") else dict(drift)
            guard["checks"]["drift"] = drift_doc
            if drift_doc.get("drift_detected") is True:
                passed = False
        except Exception as exc:  # noqa: BLE001
            guard["errors"].append(f"drift:{type(exc).__name__}:{str(exc)[:160]}")

        guard["passed"] = passed
        guard["status"] = "ok" if guard["checks"] else "unavailable"
        return guard
    finally:
        client.close()


def _llm_synthesis(
    report: dict[str, Any],
    *,
    config_path: Path | None,
    model: str | None,
    nexus_guards: bool,
) -> dict[str, Any]:
    from ass_ade.agent.lse import LSEEngine
    from ass_ade.config import load_config

    settings = load_config(config_path)
    provider = build_provider(settings)
    settings_dict = settings.model_dump(exclude={"nexus_api_key"})
    decision = LSEEngine(settings_dict).select(
        trs_score=0.72,
        complexity="complex",
        budget_remaining=12_000,
        user_model_override=model or settings.agent_model or None,
    )
    prompt = _build_llm_prompt(report)
    try:
        response = provider.complete(
            CompletionRequest(
                messages=[
                    Message(
                        role="system",
                        content="Return strict JSON only. Do not invent facts beyond provided evidence.",
                    ),
                    Message(role="user", content=prompt),
                ],
                model=decision.model,
                temperature=0.1,
                max_tokens=1800,
            )
        )
        text = response.message.content.strip()
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError:
            parsed = {"raw_text": text}
        local_guard = _local_grounding_guard(report, parsed)
        nexus_guard = {"status": "skipped"}
        if nexus_guards:
            nexus_guard = _nexus_guard_synthesis(
                report=report,
                analysis=parsed,
                settings=settings,
                model_id=response.model or decision.model,
            )
        return {
            "status": "ok",
            "provider": decision.provider,
            "model": response.model or decision.model,
            "tier": decision.tier,
            "analysis": parsed,
            "grounding_guard": local_guard,
            "nexus_guards": nexus_guard,
        }
    finally:
        close = getattr(provider, "close", None)
        if callable(close):
            close()


def scout_repo(
    repo_root: str | Path,
    *,
    benefit_root: str | Path | None = None,
    use_llm: bool = True,
    nexus_guards: bool = True,
    config_path: str | Path | None = None,
    model: str | None = None,
) -> dict[str, Any]:
    """Gather repo intel and optionally synthesize it with the configured LLM."""
    root = Path(repo_root).resolve()
    benefit = Path(benefit_root).resolve() if benefit_root is not None else None
    files = _walk_files(root)
    suffixes = Counter(path.suffix.lower().lstrip(".") or "[no_ext]" for path in files)
    repo_summary = summarize_repo(root)
    symbol_summary, symbols = scan_symbols(root)
    enhancement = build_enhancement_report(root)
    target_map = None
    if benefit is not None and benefit.exists() and benefit != root:
        target_map = build_assimilation_target_map(
            primary_root=benefit,
            sibling_roots=[root],
        ).to_dict()

    report: dict[str, Any] = {
        "schema_version": "ass-ade.scout/v1",
        "repo": str(root),
        "benefit_root": str(benefit) if benefit else None,
        "summary": {
            "total_files": repo_summary.total_files,
            "total_dirs": repo_summary.total_dirs,
            "file_types": dict(suffixes.most_common(20)),
            "top_level_entries": repo_summary.top_level_entries[:40],
        },
        "traits": _detect_repo_traits(root, files),
        "dependencies": _dependency_hints(root),
        "symbol_summary": {
            "python_files": symbol_summary.python_files,
            "symbols": symbol_summary.symbols,
            "tested_symbols": symbol_summary.tested_symbols,
            "sample_modules": _sample_python_modules(root, files),
            "top_symbol_names": [symbol.qualname for symbol in symbols[:40]],
        },
        "enhancement": enhancement,
        "target_map": target_map,
        "static_recommendations": [],
        "llm": {"status": "skipped"},
    }
    report["static_recommendations"] = _static_recommendations(
        repo_root=root,
        benefit_root=benefit,
        target_map=target_map,
        enhancement=enhancement,
    )

    if use_llm:
        try:
            report["llm"] = _llm_synthesis(
                report,
                config_path=Path(config_path).resolve() if config_path else None,
                model=model,
                nexus_guards=nexus_guards,
            )
        except Exception as exc:  # noqa: BLE001
            report["llm"] = {
                "status": "unavailable",
                "error": f"{type(exc).__name__}: {str(exc)[:240]}",
            }

    return report
