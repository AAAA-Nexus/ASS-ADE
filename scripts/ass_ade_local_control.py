"""Local control tooling for ASS-ADE evolution and rebuild outputs.

This script keeps local split-evolution work from turning into ambiguous
sibling folders. It creates a dedicated control tree, inventories ASS-ADE
siblings, stamps rebuild outputs with metadata, validates those outputs, and
compares candidates against a baseline for measurable feature gain.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


CONTROL_SCHEMA = "ass-ade.local-control.v1"
OUTPUT_SCHEMA = "ass-ade.rebuild-output.v1"
CAPABILITY_SCHEMA = "ass-ade.capability-registry.v1"

LANES = (
    "quality",
    "security",
    "performance",
    "features",
    "docs",
    "memory",
    "coordination",
    "release",
    "scratch",
)

OUTPUT_CLASSES = ("experiment", "candidate", "release", "archive")
STATUS_RANK = {
    "deprecated": -1,
    "missing": 0,
    "planned": 1,
    "partial": 2,
    "complete": 3,
}

SKIP_DIRS_FOR_SIZE = {
    ".git",
    ".venv",
    "venv",
    "env",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    "node_modules",
    "dist",
    "build",
    ".mypy_cache",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def default_parent() -> Path:
    raw = os.environ.get("ASS_ADE_PARENT")
    if raw:
        return Path(raw).expanduser().resolve()
    if os.name == "nt":
        return Path(r"C:\!aaaa-nexus").resolve()
    return Path.cwd().resolve()


def default_control_root(parent: Path | None = None) -> Path:
    raw = os.environ.get("ASS_ADE_CONTROL_ROOT")
    if raw:
        return Path(raw).expanduser().resolve()
    base = parent or default_parent()
    return (base / "!ass-ade-control").resolve()


def slugify(value: str, fallback: str = "local") -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return slug or fallback


def run(cmd: list[str], cwd: Path | None = None, timeout: int = 30) -> tuple[int, str, str]:
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(cwd) if cwd else None,
            text=True,
            capture_output=True,
            timeout=timeout,
            check=False,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return 127, "", str(exc)
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def sha256_file(path: Path) -> str | None:
    if not path.exists() or not path.is_file():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def git_info(path: Path) -> dict[str, Any]:
    code, inside, _ = run(["git", "-C", str(path), "rev-parse", "--is-inside-work-tree"])
    if code != 0 or inside.lower() != "true":
        return {"is_git": False}

    _, branch, _ = run(["git", "-C", str(path), "branch", "--show-current"])
    _, head, _ = run(["git", "-C", str(path), "rev-parse", "--short=12", "HEAD"])
    _, full_head, _ = run(["git", "-C", str(path), "rev-parse", "HEAD"])
    _, origin, _ = run(["git", "-C", str(path), "remote", "get-url", "origin"])
    _, status, _ = run(["git", "-C", str(path), "status", "--short"], timeout=60)
    dirty_items = len([line for line in status.splitlines() if line.strip()])

    ahead = None
    behind = None
    code, upstream_counts, _ = run(
        ["git", "-C", str(path), "rev-list", "--left-right", "--count", "HEAD...@{upstream}"]
    )
    if code == 0 and upstream_counts:
        parts = upstream_counts.split()
        if len(parts) == 2 and all(part.isdigit() for part in parts):
            ahead = int(parts[0])
            behind = int(parts[1])

    return {
        "is_git": True,
        "branch": branch or None,
        "head": head or None,
        "sha": full_head or head or None,
        "origin": origin or None,
        "dirty": dirty_items > 0,
        "dirty_items": dirty_items,
        "ahead_upstream": ahead,
        "behind_upstream": behind,
    }


def directory_stats(path: Path) -> dict[str, Any]:
    total = 0
    files = 0
    dirs = 0
    for root, dirnames, filenames in os.walk(path):
        dirnames[:] = [name for name in dirnames if name not in SKIP_DIRS_FOR_SIZE]
        dirs += len(dirnames)
        for filename in filenames:
            files += 1
            candidate = Path(root) / filename
            try:
                total += candidate.stat().st_size
            except OSError:
                continue
    return {
        "files": files,
        "directories": dirs,
        "size_bytes": total,
        "size_mb": round(total / (1024 * 1024), 2),
    }


def parse_version_surfaces(root: Path) -> dict[str, str | None]:
    pyproject = read_text(root / "pyproject.toml")
    init_py = read_text(root / "src" / "ass_ade" / "__init__.py")
    pyproject_version = None
    init_version = None
    match = re.search(r'^version\s*=\s*"([^"]+)"', pyproject, re.MULTILINE)
    if match:
        pyproject_version = match.group(1)
    match = re.search(r'__version__\s*=\s*"([^"]+)"', init_py)
    if match:
        init_version = match.group(1)
    version_file = None
    if (root / "VERSION").exists():
        version_file = read_text(root / "VERSION").splitlines()[0].strip() or None
    return {
        "pyproject": pyproject_version,
        "version_file": version_file,
        "package_init": init_version,
    }


def versions_synced(versions: dict[str, str | None]) -> bool:
    present = [value for value in versions.values() if value]
    return bool(present) and len(set(present)) == 1


def parse_rebuild_report(output: Path) -> dict[str, Any]:
    report_path = output / "REBUILD_REPORT.md"
    text = read_text(report_path)
    if not text:
        return {}

    def one(pattern: str) -> str | None:
        match = re.search(pattern, text, re.MULTILINE)
        return match.group(1).strip() if match else None

    components = one(r"\|\s*Components written\s*\|\s*([0-9]+)\s*\|")
    valid = re.search(r"\*\*Valid components\*\*:\s*([0-9]+)\s*/\s*([0-9]+)", text)
    tier_counts: dict[str, int] = {}
    for tier, count in re.findall(r"\|\s*`(a[0-4]_[^`]+)`\s*\|\s*([0-9]+)\s*\|", text):
        tier_counts[tier] = int(count)

    parsed: dict[str, Any] = {
        "rebuild_tag": one(r"\*\*Rebuild tag\*\*:\s*`?([^`\n]+)`?"),
        "issued": one(r"\*\*Issued\*\*:\s*([^`\n]+)"),
        "components_written": int(components) if components else None,
        "pass_rate": one(r"\*\*Pass rate\*\*:\s*([0-9.]+%)"),
        "certificate_sha256": one(r"\*\*SHA-256\*\*:\s*`?([a-fA-F0-9]{64})`?"),
        "tier_counts": tier_counts,
    }
    if valid:
        parsed["valid_components"] = {
            "valid": int(valid.group(1)),
            "total": int(valid.group(2)),
        }
    return parsed


def file_artifact(root: Path, filename: str) -> dict[str, Any]:
    path = root / filename
    return {
        "present": path.exists(),
        "path": filename if path.exists() else None,
        "sha256": sha256_file(path),
        "size_bytes": path.stat().st_size if path.exists() and path.is_file() else None,
    }


def retention_for(output_class: str, pin: bool) -> dict[str, Any]:
    if pin or output_class in {"release", "archive"}:
        return {
            "pin": True,
            "expires": None,
            "reason": "pinned release/archive" if output_class != "experiment" else "explicitly pinned",
        }
    days = 30 if output_class == "candidate" else 14
    expires = (datetime.now(timezone.utc).date() + timedelta(days=days)).isoformat()
    return {
        "pin": False,
        "expires": expires,
        "reason": f"{output_class} retention window",
    }


def build_output_metadata(
    output: Path,
    *,
    output_class: str,
    lane: str,
    source: Path | None,
    branch: str | None,
    slug: str,
    parent_output_id: str | None,
    pin: bool,
) -> dict[str, Any]:
    output = output.resolve()
    source_info = git_info(source) if source else git_info(output)
    parsed_report = parse_rebuild_report(output)
    source_sha = source_info.get("sha") or source_info.get("head") or "0000000"
    short_sha = str(source_sha)[:12] if source_sha else "0000000"
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output_id = f"rb_{timestamp}__{slugify(lane)}__{short_sha}__{slugify(slug, output.name)}"

    version_map = parse_version_surfaces(source or output)
    metadata = {
        "schema": OUTPUT_SCHEMA,
        "output_id": output_id,
        "class": output_class,
        "created_at": utc_now(),
        "path": str(output),
        "source": {
            "repo": source_info.get("origin"),
            "path": str(source.resolve()) if source else None,
            "ref": source_info.get("branch"),
            "sha": source_info.get("sha") or source_info.get("head"),
            "dirty": bool(source_info.get("dirty", False)),
            "dirty_items": int(source_info.get("dirty_items", 0) or 0),
        },
        "lineage": {
            "lane": slugify(lane),
            "branch": branch or source_info.get("branch"),
            "parent_output_id": parent_output_id,
            "merge_sibling_ids": [],
            "pr": None,
        },
        "artifacts": {
            "manifest": file_artifact(output, "MANIFEST.json"),
            "certificate": file_artifact(output, "CERTIFICATE.json"),
            "rebuild_report": file_artifact(output, "REBUILD_REPORT.md"),
            "components_written": parsed_report.get("components_written"),
            "tier_counts": parsed_report.get("tier_counts", {}),
            "pass_rate": parsed_report.get("pass_rate"),
            "certificate_sha256": parsed_report.get("certificate_sha256"),
        },
        "gates": {
            "pytest": "unknown",
            "certify": "passed" if (output / "CERTIFICATE.json").exists() else "unknown",
            "lint": "unknown",
            "docs_synced": "unknown",
            "version_synced": versions_synced(version_map),
            "stress_gain": None,
        },
        "retention": retention_for(output_class, pin),
        "notes": [
            "Generated by scripts/ass_ade_local_control.py.",
            "Move or delete this output only through the local control workflow.",
        ],
    }
    return metadata


def ensure_control_tree(root: Path) -> dict[str, Any]:
    root = root.resolve()
    directories = [
        "evo/worktrees",
        "evo/merge-siblings",
        "evo/retired",
        "outputs/experiments",
        "outputs/candidates",
        "outputs/releases",
        "outputs/stress",
        "archive",
        "scratch",
        "logs",
        "inventory",
    ]
    for lane in LANES:
        directories.append(f"evo/lanes/{lane}")
    for relative in directories:
        (root / relative).mkdir(parents=True, exist_ok=True)

    control_doc = {
        "schema": CONTROL_SCHEMA,
        "updated_at": utc_now(),
        "root": str(root),
        "lanes": list(LANES),
        "directories": directories,
        "naming": {
            "worktree": "wt_<YYYYMMDD>_<lane>_<slug>_<shortsha>",
            "output": "rb_<YYYYMMDDTHHMMSSZ>__<lane>__<shortsha>__<slug>",
            "branch": "evo/<lane>/<YYYYMMDD>-<slug>",
            "merge": "merge/<YYYYMMDD>/<version>-rc<N>",
        },
    }
    write_json(root / "CONTROL_ROOT.json", control_doc)

    readme = root / "README.md"
    if not readme.exists():
        readme.write_text(
            "# ASS-ADE Local Control Root\n\n"
            "This folder separates active evolution work, rebuild outputs, archives, "
            "scratch work, logs, and inventories.\n\n"
            "Use the repo script to update it:\n\n"
            "```powershell\n"
            "python C:/!aaaa-nexus/ass-ade-github-latest/scripts/ass_ade_local_control.py inventory\n"
            "```\n",
            encoding="utf-8",
        )
    return control_doc


def classify_sibling(path: Path, info: dict[str, Any]) -> str:
    name = path.name.lower()
    if name == "!ass-ade-control":
        return "control-root"
    if name.endswith("github-latest"):
        return "canonical-mirror"
    if info.get("is_git") and info.get("dirty"):
        return "git-working-copy-dirty"
    if info.get("is_git"):
        return "git-working-copy-clean"
    if (path / "REBUILD_REPORT.md").exists() or (path / "ASS_ADE_OUTPUT.json").exists():
        return "rebuild-output"
    if "legacy" in name:
        return "legacy-copy"
    if "merged" in name or "unified" in name or "rebuilt" in name:
        return "unstamped-rebuild-output"
    if name == "!ass-ade":
        return "mixed-source-dump"
    return "unclassified"


def inventory_siblings(parent: Path, control_root: Path, pattern: str = "*ass-ade*") -> dict[str, Any]:
    parent = parent.resolve()
    control_root = control_root.resolve()
    siblings = []
    if parent.exists():
        for child in sorted(parent.glob(pattern), key=lambda p: p.name.lower()):
            if not child.is_dir():
                continue
            if child.resolve() == control_root:
                continue
            info = git_info(child)
            stats = directory_stats(child)
            artifact = parse_rebuild_report(child)
            siblings.append(
                {
                    "name": child.name,
                    "path": str(child.resolve()),
                    "role": classify_sibling(child, info),
                    "git": info,
                    "stats": stats,
                    "artifact": artifact,
                    "has_output_metadata": (child / "ASS_ADE_OUTPUT.json").exists(),
                    "last_write": datetime.fromtimestamp(child.stat().st_mtime, timezone.utc)
                    .replace(microsecond=0)
                    .isoformat()
                    .replace("+00:00", "Z"),
                }
            )
    return {
        "schema": "ass-ade.local-inventory.v1",
        "created_at": utc_now(),
        "parent": str(parent),
        "control_root": str(control_root),
        "siblings": siblings,
    }


def load_capability_registry(root: Path) -> dict[str, Any]:
    path = root / "capabilities" / "registry.json"
    if not path.exists():
        return {"schema": CAPABILITY_SCHEMA, "capabilities": []}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {"schema": CAPABILITY_SCHEMA, "capabilities": []}
    if not isinstance(data, dict):
        return {"schema": CAPABILITY_SCHEMA, "capabilities": []}
    if not isinstance(data.get("capabilities", []), list):
        data["capabilities"] = []
    return data


def collect_cli_commands(root: Path) -> list[str]:
    cli = root / "src" / "ass_ade" / "cli.py"
    text = read_text(cli)
    if not text:
        return []

    app_names = {"app": ""}
    for variable, name in re.findall(r"app\.add_typer\((\w+),\s*name=[\"']([^\"']+)[\"']", text):
        app_names[variable] = name

    commands: list[str] = []
    pending: list[tuple[str, str | None]] = []
    decorator_re = re.compile(r"@(?P<app>\w+)\.command\((?P<args>[^)]*)\)")
    def_re = re.compile(r"def\s+(?P<name>[a-zA-Z_][a-zA-Z0-9_]*)\s*\(")
    for line in text.splitlines():
        decorator = decorator_re.search(line.strip())
        if decorator:
            raw_args = decorator.group("args")
            name_match = re.search(r"[\"']([^\"']+)[\"']", raw_args)
            pending.append((decorator.group("app"), name_match.group(1) if name_match else None))
            continue
        function = def_re.search(line.strip())
        if function and pending:
            func_name = function.group("name").replace("_", "-")
            for app_variable, explicit in pending:
                prefix = app_names.get(app_variable, app_variable.removesuffix("_app"))
                command_name = explicit or func_name
                commands.append(f"{prefix} {command_name}".strip())
            pending = []
    return sorted(set(commands))


def collect_public_python_api(root: Path) -> list[str]:
    src = root / "src" / "ass_ade"
    symbols: list[str] = []
    if not src.exists():
        return symbols
    for path in src.rglob("*.py"):
        if "__pycache__" in path.parts:
            continue
        module = path.relative_to(src).with_suffix("").as_posix().replace("/", ".")
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except (SyntaxError, UnicodeDecodeError, OSError):
            continue
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                if not node.name.startswith("_"):
                    symbols.append(f"{module}:{node.name}")
    return sorted(set(symbols))


def count_files(root: Path, pattern: str) -> int:
    if not root.exists():
        return 0
    return sum(1 for path in root.rglob(pattern) if path.is_file() and "__pycache__" not in path.parts)


def collect_pytest_count(root: Path, timeout: int = 180) -> dict[str, Any]:
    code, stdout, stderr = run(
        [sys.executable, "-m", "pytest", "--collect-only", "-q"],
        cwd=root,
        timeout=timeout,
    )
    count = None
    combined = "\n".join([stdout, stderr])
    match = re.search(r"([0-9]+)\s+tests?\s+collected", combined)
    if match:
        count = int(match.group(1))
    return {
        "exit_code": code,
        "collected": count,
    }


def feature_snapshot(root: Path, *, collect_pytest: bool = False) -> dict[str, Any]:
    root = root.resolve()
    registry = load_capability_registry(root)
    capabilities = {
        str(cap.get("id")): str(cap.get("status", "missing"))
        for cap in registry.get("capabilities", [])
        if isinstance(cap, dict) and cap.get("id")
    }
    status_counts: dict[str, int] = {}
    for status in capabilities.values():
        status_counts[status] = status_counts.get(status, 0) + 1

    version_map = parse_version_surfaces(root)
    report = parse_rebuild_report(root)
    snapshot = {
        "schema": "ass-ade.feature-snapshot.v1",
        "created_at": utc_now(),
        "root": str(root),
        "git": git_info(root),
        "versions": version_map,
        "version_synced": versions_synced(version_map),
        "capability_count": len(capabilities),
        "capability_status_counts": status_counts,
        "capabilities": capabilities,
        "cli_commands": collect_cli_commands(root),
        "public_python_api": collect_public_python_api(root),
        "source_files": count_files(root / "src", "*.py"),
        "test_files": count_files(root / "tests", "test_*.py"),
        "doc_files": count_files(root / "docs", "*.md"),
        "rebuild_components": report.get("components_written"),
        "rebuild_tiers": report.get("tier_counts", {}),
    }
    if collect_pytest:
        snapshot["pytest_collect"] = collect_pytest_count(root)
    return snapshot


def compare_snapshots(base: dict[str, Any], candidate: dict[str, Any]) -> dict[str, Any]:
    base_caps = base.get("capabilities", {})
    cand_caps = candidate.get("capabilities", {})
    cap_added = sorted(set(cand_caps) - set(base_caps))
    cap_removed = sorted(set(base_caps) - set(cand_caps))

    cap_improved = []
    cap_regressed = []
    for cap_id in sorted(set(base_caps) & set(cand_caps)):
        old = STATUS_RANK.get(str(base_caps[cap_id]), 0)
        new = STATUS_RANK.get(str(cand_caps[cap_id]), 0)
        if new > old:
            cap_improved.append({"id": cap_id, "from": base_caps[cap_id], "to": cand_caps[cap_id]})
        elif new < old:
            cap_regressed.append({"id": cap_id, "from": base_caps[cap_id], "to": cand_caps[cap_id]})

    base_cli = set(base.get("cli_commands", []))
    cand_cli = set(candidate.get("cli_commands", []))
    base_api = set(base.get("public_python_api", []))
    cand_api = set(candidate.get("public_python_api", []))

    pytest_base = (base.get("pytest_collect") or {}).get("collected")
    pytest_cand = (candidate.get("pytest_collect") or {}).get("collected")
    pytest_delta = None
    if isinstance(pytest_base, int) and isinstance(pytest_cand, int):
        pytest_delta = pytest_cand - pytest_base

    components_base = base.get("rebuild_components")
    components_cand = candidate.get("rebuild_components")
    components_delta = None
    if isinstance(components_base, int) and isinstance(components_cand, int):
        components_delta = components_cand - components_base

    growth_signals = {
        "capabilities_added": len(cap_added),
        "capabilities_improved": len(cap_improved),
        "cli_commands_added": len(cand_cli - base_cli),
        "public_api_added": len(cand_api - base_api),
        "test_files_delta": int(candidate.get("test_files", 0)) - int(base.get("test_files", 0)),
        "pytest_collected_delta": pytest_delta,
        "rebuild_components_delta": components_delta,
    }

    regressions = {
        "capabilities_removed": cap_removed,
        "capabilities_regressed": cap_regressed,
        "cli_commands_removed": sorted(base_cli - cand_cli),
        "public_api_removed": sorted(base_api - cand_api),
        "version_synced": bool(candidate.get("version_synced", False)),
    }

    severe_regression = bool(
        cap_removed
        or cap_regressed
        or regressions["cli_commands_removed"]
        or (pytest_delta is not None and pytest_delta < 0)
        or not candidate.get("version_synced", False)
    )
    gained = any(
        value and value > 0
        for value in (
            growth_signals["capabilities_added"],
            growth_signals["capabilities_improved"],
            growth_signals["cli_commands_added"],
            growth_signals["public_api_added"],
            growth_signals["test_files_delta"],
            growth_signals["pytest_collected_delta"],
            growth_signals["rebuild_components_delta"],
        )
        if value is not None
    )

    return {
        "schema": "ass-ade.feature-gain-report.v1",
        "created_at": utc_now(),
        "base": base.get("root"),
        "candidate": candidate.get("root"),
        "passed": bool(gained and not severe_regression),
        "growth_signals": growth_signals,
        "regressions": regressions,
        "added": {
            "capabilities": cap_added,
            "cli_commands": sorted(cand_cli - base_cli),
            "public_api": sorted(cand_api - base_api),
        },
        "improved_capabilities": cap_improved,
    }


def validate_output(output: Path) -> dict[str, Any]:
    output = output.resolve()
    metadata_path = output / "ASS_ADE_OUTPUT.json"
    errors: list[str] = []
    warnings: list[str] = []
    metadata: dict[str, Any] = {}

    if not metadata_path.exists():
        errors.append("missing ASS_ADE_OUTPUT.json")
    else:
        try:
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"invalid ASS_ADE_OUTPUT.json: {exc}")

    if metadata:
        if metadata.get("schema") != OUTPUT_SCHEMA:
            errors.append(f"schema must be {OUTPUT_SCHEMA}")
        if metadata.get("class") not in OUTPUT_CLASSES:
            errors.append(f"class must be one of {', '.join(OUTPUT_CLASSES)}")
        output_id = str(metadata.get("output_id", ""))
        if not output_id.startswith("rb_"):
            errors.append("output_id must start with rb_")
        source = metadata.get("source") or {}
        if source.get("dirty"):
            warnings.append("source was dirty when output was stamped")
        gates = metadata.get("gates") or {}
        if gates.get("version_synced") is False:
            warnings.append("version surfaces were not synced when output was stamped")

    for filename in ("MANIFEST.json", "CERTIFICATE.json"):
        if not (output / filename).exists():
            errors.append(f"missing {filename}")
    if not (output / "REBUILD_REPORT.md").exists():
        warnings.append("missing REBUILD_REPORT.md")

    return {
        "schema": "ass-ade.output-validation.v1",
        "created_at": utc_now(),
        "output": str(output),
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "metadata": metadata,
    }


def validate_registry(repo: Path) -> dict[str, Any]:
    repo = repo.resolve()
    registry = load_capability_registry(repo)
    errors: list[str] = []
    warnings: list[str] = []
    seen: set[str] = set()
    areas: dict[str, int] = {}
    statuses: dict[str, int] = {}

    if registry.get("schema") != CAPABILITY_SCHEMA:
        errors.append(f"registry schema must be {CAPABILITY_SCHEMA}")

    caps = registry.get("capabilities", [])
    if not isinstance(caps, list):
        errors.append("capabilities must be a list")
        caps = []

    for index, cap in enumerate(caps):
        if not isinstance(cap, dict):
            errors.append(f"capability #{index} must be an object")
            continue
        cap_id = str(cap.get("id") or "").strip()
        status = str(cap.get("status") or "").strip()
        area = str(cap.get("area") or "").strip()
        evidence = cap.get("evidence", [])
        if not cap_id:
            errors.append(f"capability #{index} missing id")
        elif cap_id in seen:
            errors.append(f"duplicate capability id: {cap_id}")
        else:
            seen.add(cap_id)
        if not str(cap.get("name") or "").strip():
            errors.append(f"{cap_id or index}: missing name")
        if not area:
            errors.append(f"{cap_id or index}: missing area")
        else:
            areas[area] = areas.get(area, 0) + 1
        if status not in STATUS_RANK:
            errors.append(f"{cap_id or index}: invalid status {status!r}")
        else:
            statuses[status] = statuses.get(status, 0) + 1
        if not isinstance(evidence, list):
            errors.append(f"{cap_id or index}: evidence must be a list")
            continue
        if status in {"complete", "partial"} and not evidence:
            warnings.append(f"{cap_id}: {status} capability has no evidence paths")
        for raw_path in evidence:
            if not isinstance(raw_path, str):
                errors.append(f"{cap_id}: evidence entries must be strings")
                continue
            if raw_path.startswith(("http://", "https://")):
                continue
            if not (repo / raw_path).exists():
                warnings.append(f"{cap_id}: evidence path missing: {raw_path}")

    return {
        "schema": "ass-ade.capability-registry-validation.v1",
        "created_at": utc_now(),
        "repo": str(repo),
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "capability_count": len(caps),
        "areas": dict(sorted(areas.items())),
        "statuses": dict(sorted(statuses.items())),
    }


def status_icon(status: str) -> str:
    return {
        "complete": "OK",
        "partial": "PARTIAL",
        "planned": "PLANNED",
        "missing": "MISSING",
        "deprecated": "DEPRECATED",
    }.get(status, status.upper() or "UNKNOWN")


_AREA_TITLE_OVERRIDES: dict[str, str] = {
    "a2a": "A2A",
    "mcp": "MCP",
    "ide": "IDE",
    "api": "API",
}

_LEGEND_DESCRIPTIONS: dict[str, str] = {
    "complete": "`OK`: implemented and covered by local evidence.",
    "partial": "`PARTIAL`: usable, but with known product or integration gaps.",
    "planned": "`PLANNED`: accepted direction, not yet built.",
    "missing": "`MISSING`: known gap.",
    "deprecated": "`DEPRECATED`: intentionally retired.",
}


def _area_title(area: str) -> str:
    key = area.lower().replace("_", "").replace("-", "")
    if key in _AREA_TITLE_OVERRIDES:
        return _AREA_TITLE_OVERRIDES[key]
    return area.replace("_", " ").replace("-", " ").title()


def render_capability_matrix(repo: Path) -> str:
    registry = load_capability_registry(repo)
    caps = [cap for cap in registry.get("capabilities", []) if isinstance(cap, dict)]
    grouped: dict[str, list[dict[str, Any]]] = {}
    for cap in caps:
        grouped.setdefault(str(cap.get("area") or "uncategorized"), []).append(cap)

    status_counts: dict[str, int] = {}
    for cap in caps:
        status = str(cap.get("status") or "missing")
        status_counts[status] = status_counts.get(status, 0) + 1

    # Sort areas: surface missing/partial first within each area by sorting caps
    lines = [
        "# Capability Matrix",
        "",
        f"> Generated: {utc_now()}  |  source: `capabilities/registry.json`",
        "",
        "## Summary",
        "",
        "| Status | Count |",
        "| --- | ---: |",
    ]
    for status in ("complete", "partial", "planned", "missing", "deprecated"):
        count = status_counts.get(status, 0)
        if count:
            lines.append(f"| {status_icon(status)} | {count} |")

    # Legend: only show statuses that actually appear
    present_statuses = [s for s in ("complete", "partial", "planned", "missing", "deprecated") if status_counts.get(s, 0)]
    lines.extend(["", "## Legend", ""])
    for status in present_statuses:
        lines.append(f"- {_LEGEND_DESCRIPTIONS[status]}")

    # Gaps section: missing and partial capabilities upfront
    gap_caps = [c for c in caps if str(c.get("status") or "missing") in ("missing", "partial")]
    if gap_caps:
        lines.extend(["", "## Gaps (action required)", ""])
        for cap in sorted(gap_caps, key=lambda c: (str(c.get("status") or ""), str(c.get("id") or ""))):
            icon = status_icon(str(cap.get("status") or "missing"))
            lines.append(f"- `{cap.get('id', '')}` — {cap.get('name', '')} [{icon}]")

    _STATUS_PRIORITY = {"missing": 0, "partial": 1, "planned": 2, "complete": 3, "deprecated": 4}

    has_notes = any(cap.get("notes") for cap in caps)
    header = "| ID | Capability | Status | Evidence |" + (" Notes |" if has_notes else "")
    sep = "| --- | --- | :---: | --- |" + (" --- |" if has_notes else "")

    for area in sorted(grouped):
        title = _area_title(area)
        lines.extend(["", f"## {title}", "", header, sep])
        sorted_caps = sorted(
            grouped[area],
            key=lambda c: (_STATUS_PRIORITY.get(str(c.get("status") or "missing"), 99), str(c.get("id") or "")),
        )
        for cap in sorted_caps:
            evidence_items = cap.get("evidence", [])
            if isinstance(evidence_items, list):
                ev_links = [f"[`{e}`]({e})" if not e.startswith("http") else f"[{e}]({e})" for e in evidence_items[:3]]
                evidence = ", ".join(ev_links)
                if len(evidence_items) > 3:
                    evidence += f" (+{len(evidence_items) - 3} more)"
            else:
                evidence = ""
            row = (
                f"| `{cap.get('id', '')}` | {cap.get('name', '')} | "
                f"{status_icon(str(cap.get('status') or 'missing'))} | {evidence} |"
            )
            if has_notes:
                row += f" {cap.get('notes') or ''} |"
            lines.append(row)
    lines.append("")
    return "\n".join(lines)


def render_control_status(control_root: Path) -> str:
    control_root = control_root.resolve()
    inventory_path = control_root / "inventory" / "latest.json"
    index_path = control_root / "CONTROL_INDEX.json"
    inventory: dict[str, Any] = {}
    index: dict[str, Any] = {}
    if inventory_path.exists():
        try:
            inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            inventory = {}
    if index_path.exists():
        try:
            index = json.loads(index_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            index = {}

    siblings = [item for item in inventory.get("siblings", []) if isinstance(item, dict)]
    role_counts: dict[str, int] = {}
    for item in siblings:
        role = str(item.get("role") or "unknown")
        role_counts[role] = role_counts.get(role, 0) + 1

    # Audit chain state
    chain_result = verify_chain(control_root)
    chain_entries = chain_result.get("entries", 0)
    chain_head_val = str(chain_result.get("head") or "genesis")
    chain_head_short = chain_head_val[:24] if chain_head_val != "genesis" else "genesis (empty)"
    chain_valid = "valid" if chain_result.get("valid") else "INVALID"

    # Registry gaps from index
    registry_info = index.get("registry") or {}
    reg_statuses = registry_info.get("statuses") or {}
    missing_count = reg_statuses.get("missing", 0)
    partial_count = reg_statuses.get("partial", 0)

    lines = [
        "# Local Control Status",
        "",
        f"> Generated: {utc_now()}",
        "",
        f"- Control root: `{control_root}`",
        f"- Inventory: `{inventory_path}`",
        f"- Index: `{index_path}`",
        "",
        "## Audit Chain",
        "",
        f"| Entries | Head (24 chars) | Valid |",
        "| ---: | --- | --- |",
        f"| {chain_entries} | `{chain_head_short}` | {chain_valid} |",
        "",
        "## Registry",
        "",
        f"| Capabilities | Complete | Partial | Missing |",
        "| ---: | ---: | ---: | ---: |",
        f"| {registry_info.get('capability_count', 0)} | {reg_statuses.get('complete', 0)} | {partial_count} | {missing_count} |",
        "",
        "## Sibling Roles",
        "",
        "| Role | Count |",
        "| --- | ---: |",
    ]
    for role, count in sorted(role_counts.items()):
        lines.append(f"| `{role}` | {count} |")

    lines.extend([
        "",
        "## Siblings",
        "",
        "| Name | Role | Branch | SHA | Dirty | Metadata | Components | Size MB | Last Write |",
        "| --- | --- | --- | --- | ---: | --- | ---: | ---: | --- |",
    ])
    for item in siblings:
        git = item.get("git") or {}
        if git.get("is_git"):
            branch = git.get("branch") or "—"
            sha = str(git.get("head") or "")[:8] or "—"
            dirty_items = git.get("dirty_items", 0) or 0
            dirty_cell = str(dirty_items) if dirty_items else "—"
        else:
            branch = "—"
            sha = "—"
            dirty_cell = "—"
        artifact = item.get("artifact") or {}
        components = artifact.get("components_written")
        components_text = str(components) if isinstance(components, int) else "—"
        stats = item.get("stats") or {}
        last_write = str(item.get("last_write") or "")[:16].replace("T", " ")
        lines.append(
            f"| `{item.get('name', '')}` | `{item.get('role', '')}` | {branch} | `{sha}` | "
            f"{dirty_cell} | {'yes' if item.get('has_output_metadata') else 'no'} | "
            f"{components_text} | {stats.get('size_mb', '—')} | {last_write} |"
        )

    outputs = index.get("outputs", []) if isinstance(index.get("outputs"), list) else []
    stress = index.get("stress", []) if isinstance(index.get("stress"), list) else []
    lines.extend(["", "## Ingested JSON", "", f"- Stamped outputs: {len(outputs)}", f"- Stress/snapshot reports: {len(stress)}", ""])
    return "\n".join(lines)


def mermaid_label(value: Any) -> str:
    text = str(value)
    text = text.replace("\\", "/").replace('"', "'").replace("\r", " ").replace("\n", " ")
    return text


def mermaid_id(prefix: str, value: Any) -> str:
    slug = re.sub(r"[^a-zA-Z0-9_]+", "_", str(value)).strip("_")
    if not slug:
        slug = "item"
    if slug[0].isdigit():
        slug = f"n_{slug}"
    return f"{prefix}_{slug[:48]}"


def load_control_index(control_root: Path) -> dict[str, Any]:
    index_path = control_root.resolve() / "CONTROL_INDEX.json"
    if not index_path.exists():
        return {}
    try:
        data = json.loads(index_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def load_latest_inventory(control_root: Path) -> dict[str, Any]:
    inventory_path = control_root.resolve() / "inventory" / "latest.json"
    if not inventory_path.exists():
        return {}
    try:
        data = json.loads(inventory_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def render_local_control_mermaid(control_root: Path) -> str:
    control_root = control_root.resolve()
    inventory = load_latest_inventory(control_root)
    siblings = [item for item in inventory.get("siblings", []) if isinstance(item, dict)]
    lines = [
        "flowchart TD",
        '  parent["C:/!aaaa-nexus"]',
        '  control["!ass-ade-control"]',
        '  inventory["inventory/latest.json"]',
        '  index["CONTROL_INDEX.json"]',
        '  stress["outputs/stress"]',
        '  docs["generated docs"]',
        "  parent --> control",
        "  control --> inventory",
        "  control --> index",
        "  control --> stress",
        "  index --> docs",
        "",
        "  subgraph Local_Siblings[Local siblings]",
    ]
    for idx, item in enumerate(siblings):
        node = f"sibling_{idx}"
        name = mermaid_label(item.get("name", "unknown"))
        role = mermaid_label(item.get("role", "unknown"))
        metadata = "stamped" if item.get("has_output_metadata") else "unstamped"
        lines.append(f'    {node}["{name}<br/>{role}<br/>{metadata}"]')
    lines.append("  end")
    for idx, item in enumerate(siblings):
        node = f"sibling_{idx}"
        role = str(item.get("role") or "")
        if role == "rebuild-output":
            lines.append(f"  {node} --> index")
        elif role == "canonical-mirror":
            lines.append(f"  {node} --> stress")
        else:
            lines.append(f"  parent --> {node}")
    lines.append("")
    return "\n".join(lines)


def render_capability_status_mermaid(repo: Path) -> str:
    """Area-grouped capability status diagram.

    Each area is a subgraph node showing complete/partial/missing counts.
    Avoids the flat fan-out hairball of connecting every node to registry.
    """
    registry = load_capability_registry(repo)
    caps = [cap for cap in registry.get("capabilities", []) if isinstance(cap, dict)]

    # Build per-area status breakdown
    area_status: dict[str, dict[str, int]] = {}
    overall: dict[str, int] = {}
    for cap in caps:
        status = str(cap.get("status") or "missing")
        area = str(cap.get("area") or "uncategorized")
        area_status.setdefault(area, {})
        area_status[area][status] = area_status[area].get(status, 0) + 1
        overall[status] = overall.get(status, 0) + 1

    lines = [
        "flowchart TD",
        f'  registry["capabilities/registry.json\\n{len(caps)} total"]',
        "",
        "  subgraph Overall[Overall status]",
    ]
    for status in ("complete", "partial", "missing", "planned", "deprecated"):
        count = overall.get(status, 0)
        if count:
            node = mermaid_id("ov", status)
            icon = {"complete": "OK", "partial": "~", "missing": "GAP", "planned": "→", "deprecated": "X"}.get(status, status)
            lines.append(f'    {node}["{icon} {status}: {count}"]')
    lines.append("  end")
    lines.append("  registry --> Overall")
    lines.append("")

    # One node per area showing counts inline
    lines.append("  subgraph Areas[By area]")
    for area in sorted(area_status):
        node = mermaid_id("area", area)
        counts = area_status[area]
        parts = []
        for st in ("complete", "partial", "missing"):
            if counts.get(st):
                parts.append(f"{st[0].upper()}:{counts[st]}")
        label = f"{_area_title(area)} [{' '.join(parts)}]"
        lines.append(f'    {node}["{mermaid_label(label)}"]')
    lines.append("  end")
    lines.append("  registry --> Areas")
    lines.append("")
    return "\n".join(lines)


def render_json_lifecycle_mermaid() -> str:
    return "\n".join(
        [
            "flowchart LR",
            '  refresh["refresh --collect-pytest --docs"]',
            '  inventory["inventory/latest.json"]',
            '  outputs["ASS_ADE_OUTPUT.json files"]',
            '  stress["outputs/stress/*.json"]',
            '  registry["capabilities/registry.json"]',
            '  index["CONTROL_INDEX.json"]',
            '  matrix["docs/capability-matrix.md"]',
            '  status["docs/local-control-status.md"]',
            '  diagrams["docs/diagrams/*.mmd"]',
            "  refresh --> inventory",
            "  refresh --> stress",
            "  refresh --> registry",
            "  inventory --> index",
            "  outputs --> index",
            "  stress --> index",
            "  registry --> index",
            "  registry --> matrix",
            "  index --> status",
            "  index --> diagrams",
            "  registry --> diagrams",
            "",
        ]
    )


def render_mermaid_docs(repo: Path, control_root: Path) -> str:
    local = render_local_control_mermaid(control_root)
    capability = render_capability_status_mermaid(repo)
    lifecycle = render_json_lifecycle_mermaid()
    return "\n".join(
        [
            "# Generated Mermaid Diagrams",
            "",
            "Generated from local control JSON ledgers and `capabilities/registry.json`.",
            "",
            "## JSON Lifecycle",
            "",
            "```mermaid",
            lifecycle.rstrip(),
            "```",
            "",
            "## Local Control",
            "",
            "```mermaid",
            local.rstrip(),
            "```",
            "",
            "## Capability Status",
            "",
            "```mermaid",
            capability.rstrip(),
            "```",
            "",
            "Standalone Mermaid files are written under `docs/diagrams/`.",
            "",
        ]
    )


def generate_docs(repo: Path, control_root: Path) -> dict[str, Any]:
    repo = repo.resolve()
    control_root = control_root.resolve()
    diagrams_dir = repo / "docs" / "diagrams"
    diagrams_dir.mkdir(parents=True, exist_ok=True)
    outputs = {
        "capability_matrix": repo / "docs" / "capability-matrix.md",
        "local_control_status": repo / "docs" / "local-control-status.md",
        "mermaid_diagrams": repo / "docs" / "mermaid-diagrams.md",
        "diagram_json_lifecycle": diagrams_dir / "json-lifecycle.mmd",
        "diagram_local_control": diagrams_dir / "local-control.mmd",
        "diagram_capability_status": diagrams_dir / "capability-status.mmd",
    }
    outputs["capability_matrix"].write_text(render_capability_matrix(repo), encoding="utf-8")
    outputs["local_control_status"].write_text(render_control_status(control_root), encoding="utf-8")
    outputs["diagram_json_lifecycle"].write_text(render_json_lifecycle_mermaid(), encoding="utf-8")
    outputs["diagram_local_control"].write_text(render_local_control_mermaid(control_root), encoding="utf-8")
    outputs["diagram_capability_status"].write_text(render_capability_status_mermaid(repo), encoding="utf-8")
    outputs["mermaid_diagrams"].write_text(render_mermaid_docs(repo, control_root), encoding="utf-8")
    return {
        "schema": "ass-ade.docs-generation.v1",
        "created_at": utc_now(),
        "repo": str(repo),
        "control_root": str(control_root),
        "outputs": {key: str(path) for key, path in outputs.items()},
    }


def generic_json_diff(before: Any, after: Any, path: str = "$", *, limit: int = 200) -> list[dict[str, Any]]:
    changes: list[dict[str, Any]] = []
    if len(changes) >= limit:
        return changes
    if isinstance(before, dict) and isinstance(after, dict):
        for key in sorted(set(before) - set(after)):
            changes.append({"kind": "removed", "path": f"{path}.{key}", "before": before[key]})
            if len(changes) >= limit:
                return changes
        for key in sorted(set(after) - set(before)):
            changes.append({"kind": "added", "path": f"{path}.{key}", "after": after[key]})
            if len(changes) >= limit:
                return changes
        for key in sorted(set(before) & set(after)):
            changes.extend(generic_json_diff(before[key], after[key], f"{path}.{key}", limit=limit - len(changes)))
            if len(changes) >= limit:
                return changes
        return changes
    if isinstance(before, list) and isinstance(after, list):
        if before != after:
            changes.append({"kind": "changed", "path": path, "before_count": len(before), "after_count": len(after)})
        return changes
    if before != after:
        changes.append({"kind": "changed", "path": path, "before": before, "after": after})
    return changes


def diff_inventories(before: dict[str, Any], after: dict[str, Any]) -> dict[str, Any]:
    before_items = {str(item.get("path") or item.get("name")): item for item in before.get("siblings", []) if isinstance(item, dict)}
    after_items = {str(item.get("path") or item.get("name")): item for item in after.get("siblings", []) if isinstance(item, dict)}
    role_changes = []
    dirty_changes = []
    metadata_changes = []
    for key in sorted(set(before_items) & set(after_items)):
        old = before_items[key]
        new = after_items[key]
        if old.get("role") != new.get("role"):
            role_changes.append({"path": key, "from": old.get("role"), "to": new.get("role")})
        old_dirty = (old.get("git") or {}).get("dirty_items")
        new_dirty = (new.get("git") or {}).get("dirty_items")
        if old_dirty != new_dirty:
            dirty_changes.append({"path": key, "from": old_dirty, "to": new_dirty})
        if old.get("has_output_metadata") != new.get("has_output_metadata"):
            metadata_changes.append({"path": key, "from": old.get("has_output_metadata"), "to": new.get("has_output_metadata")})
    return {
        "added": sorted(set(after_items) - set(before_items)),
        "removed": sorted(set(before_items) - set(after_items)),
        "role_changes": role_changes,
        "dirty_changes": dirty_changes,
        "metadata_changes": metadata_changes,
    }


def diff_json_files(before_path: Path, after_path: Path) -> dict[str, Any]:
    before = json.loads(before_path.read_text(encoding="utf-8"))
    after = json.loads(after_path.read_text(encoding="utf-8"))
    before_schema = before.get("schema") if isinstance(before, dict) else None
    after_schema = after.get("schema") if isinstance(after, dict) else None
    specialized: dict[str, Any] | None = None
    if before_schema == after_schema == "ass-ade.local-inventory.v1":
        specialized = diff_inventories(before, after)
    elif before_schema == after_schema == "ass-ade.feature-snapshot.v1":
        specialized = compare_snapshots(before, after)
    return {
        "schema": "ass-ade.json-diff.v1",
        "created_at": utc_now(),
        "before": str(before_path.resolve()),
        "after": str(after_path.resolve()),
        "before_schema": before_schema,
        "after_schema": after_schema,
        "specialized": specialized,
        "generic_changes": generic_json_diff(before, after),
    }


def ingest_control_json(repo: Path, control_root: Path, parent: Path) -> dict[str, Any]:
    repo = repo.resolve()
    control_root = control_root.resolve()
    parent = parent.resolve()
    output_docs: list[dict[str, Any]] = []
    stress_docs: list[dict[str, Any]] = []

    for metadata_path in sorted(parent.glob("*ass-ade*/ASS_ADE_OUTPUT.json")):
        try:
            payload = json.loads(metadata_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        output_docs.append({
            "path": str(metadata_path),
            "output_id": payload.get("output_id"),
            "class": payload.get("class"),
            "lane": (payload.get("lineage") or {}).get("lane"),
            "components_written": (payload.get("artifacts") or {}).get("components_written"),
            "valid": validate_output(metadata_path.parent)["valid"],
        })

    stress_root = control_root / "outputs" / "stress"
    if stress_root.exists():
        for json_path in sorted(stress_root.glob("*.json")):
            try:
                payload = json.loads(json_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                continue
            stress_docs.append({
                "path": str(json_path),
                "schema": payload.get("schema"),
                "passed": payload.get("passed"),
                "created_at": payload.get("created_at"),
            })

    inventory_path = control_root / "inventory" / "latest.json"
    inventory = None
    if inventory_path.exists():
        try:
            inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            inventory = None

    registry_validation = validate_registry(repo)
    index = {
        "schema": "ass-ade.control-index.v1",
        "created_at": utc_now(),
        "repo": str(repo),
        "control_root": str(control_root),
        "parent": str(parent),
        "inventory": {
            "path": str(inventory_path),
            "created_at": inventory.get("created_at") if isinstance(inventory, dict) else None,
            "siblings": len(inventory.get("siblings", [])) if isinstance(inventory, dict) else 0,
        },
        "registry": {
            "valid": registry_validation["valid"],
            "capability_count": registry_validation["capability_count"],
            "statuses": registry_validation["statuses"],
            "warnings": len(registry_validation["warnings"]),
            "errors": len(registry_validation["errors"]),
        },
        "outputs": output_docs,
        "stress": stress_docs,
    }
    write_json(control_root / "CONTROL_INDEX.json", index)
    return index


def cmd_init(args: argparse.Namespace) -> int:
    root = Path(args.root).expanduser().resolve()
    doc = ensure_control_tree(root)
    print(json.dumps(doc, indent=2, sort_keys=True))
    return 0


def cmd_inventory(args: argparse.Namespace) -> int:
    parent = Path(args.parent).expanduser().resolve()
    control_root = Path(args.root).expanduser().resolve()
    ensure_control_tree(control_root)
    payload = inventory_siblings(parent, control_root, args.pattern)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    inventory_dir = control_root / "inventory"
    write_json(inventory_dir / f"local-inventory-{timestamp}.json", payload)
    write_json(inventory_dir / "latest.json", payload)
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(f"Inventoried {len(payload['siblings'])} sibling(s).")
        print(f"Latest inventory: {inventory_dir / 'latest.json'}")
    return 0


def cmd_stamp_output(args: argparse.Namespace) -> int:
    output = Path(args.output).expanduser().resolve()
    if not output.exists():
        raise SystemExit(f"output does not exist: {output}")
    if args.output_class not in OUTPUT_CLASSES:
        raise SystemExit(f"--class must be one of: {', '.join(OUTPUT_CLASSES)}")
    source = Path(args.source).expanduser().resolve() if args.source else None
    metadata = build_output_metadata(
        output,
        output_class=args.output_class,
        lane=args.lane,
        source=source,
        branch=args.branch,
        slug=args.slug or output.name,
        parent_output_id=args.parent_output_id,
        pin=args.pin,
    )
    write_json(output / "ASS_ADE_OUTPUT.json", metadata)
    print(json.dumps(metadata, indent=2, sort_keys=True))
    return 0


def cmd_validate_output(args: argparse.Namespace) -> int:
    result = validate_output(Path(args.output).expanduser().resolve())
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["valid"] else 1


def cmd_snapshot(args: argparse.Namespace) -> int:
    snap = feature_snapshot(Path(args.path).expanduser().resolve(), collect_pytest=args.collect_pytest)
    if args.out:
        write_json(Path(args.out).expanduser().resolve(), snap)
    print(json.dumps(snap, indent=2, sort_keys=True))
    return 0


def cmd_stress_gain(args: argparse.Namespace) -> int:
    base = feature_snapshot(Path(args.base).expanduser().resolve(), collect_pytest=args.collect_pytest)
    candidate = feature_snapshot(Path(args.candidate).expanduser().resolve(), collect_pytest=args.collect_pytest)
    report = compare_snapshots(base, candidate)
    if args.out:
        write_json(Path(args.out).expanduser().resolve(), report)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["passed"] or args.no_fail else 1


def cmd_validate_registry(args: argparse.Namespace) -> int:
    result = validate_registry(Path(args.repo).expanduser().resolve())
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["valid"] else 1


def cmd_docs_generate(args: argparse.Namespace) -> int:
    result = generate_docs(
        Path(args.repo).expanduser().resolve(),
        Path(args.root).expanduser().resolve(),
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


def cmd_diff_json(args: argparse.Namespace) -> int:
    result = diff_json_files(
        Path(args.before).expanduser().resolve(),
        Path(args.after).expanduser().resolve(),
    )
    if args.out:
        write_json(Path(args.out).expanduser().resolve(), result)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


def cmd_ingest_json(args: argparse.Namespace) -> int:
    result = ingest_control_json(
        Path(args.repo).expanduser().resolve(),
        Path(args.root).expanduser().resolve(),
        Path(args.parent).expanduser().resolve(),
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["registry"]["valid"] else 1


def cmd_refresh(args: argparse.Namespace) -> int:
    repo = Path(args.repo).expanduser().resolve()
    parent = Path(args.parent).expanduser().resolve()
    control_root = Path(args.root).expanduser().resolve()
    ensure_control_tree(control_root)

    inventory_payload = inventory_siblings(parent, control_root, args.pattern)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    inventory_dir = control_root / "inventory"
    inventory_path = inventory_dir / f"local-inventory-{timestamp}.json"
    write_json(inventory_path, inventory_payload)
    write_json(inventory_dir / "latest.json", inventory_payload)

    snapshot_path = control_root / "outputs" / "stress" / "baseline-main-pytest-snapshot.json"
    snapshot = feature_snapshot(repo, collect_pytest=args.collect_pytest)
    write_json(snapshot_path, snapshot)

    registry_validation = validate_registry(repo)
    write_json(control_root / "logs" / "registry-validation-latest.json", registry_validation)

    index = ingest_control_json(repo, control_root, parent)
    docs = generate_docs(repo, control_root) if args.docs else None

    result = {
        "schema": "ass-ade.local-refresh.v1",
        "created_at": utc_now(),
        "repo": str(repo),
        "control_root": str(control_root),
        "inventory": str(inventory_path),
        "snapshot": str(snapshot_path),
        "registry_valid": registry_validation["valid"],
        "index": str(control_root / "CONTROL_INDEX.json"),
        "docs": docs,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if registry_validation["valid"] else 1


CHAIN_SCHEMA = "ass-ade.control-chain-entry.v1"
CHAIN_GENESIS = "sha256:0000000000000000000000000000000000000000000000000000000000000000"


def _sha256_bytes(payload: bytes) -> str:
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def _canonical_json(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")


def chain_path(control_root: Path) -> Path:
    return control_root.resolve() / "logs" / "control-chain.jsonl"


def chain_head(control_root: Path) -> str:
    path = chain_path(control_root)
    if not path.exists():
        return CHAIN_GENESIS
    last = None
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                last = line
    if not last:
        return CHAIN_GENESIS
    try:
        return str(json.loads(last).get("hash") or CHAIN_GENESIS)
    except json.JSONDecodeError:
        return CHAIN_GENESIS


def chain_next_seq(control_root: Path) -> int:
    path = chain_path(control_root)
    if not path.exists():
        return 0
    count = 0
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                count += 1
    return count


def append_chain(
    control_root: Path,
    *,
    command: str,
    args: dict[str, Any],
    payload: dict[str, Any],
    nexus_audit_id: str | None = None,
) -> dict[str, Any]:
    control_root = control_root.resolve()
    (control_root / "logs").mkdir(parents=True, exist_ok=True)
    prev = chain_head(control_root)
    seq = chain_next_seq(control_root)
    ts = utc_now()
    args_hash = _sha256_bytes(_canonical_json(args))
    payload_hash = _sha256_bytes(_canonical_json(payload))
    material = "|".join([prev, str(seq), ts, command, args_hash, payload_hash]).encode("utf-8")
    entry = {
        "schema": CHAIN_SCHEMA,
        "seq": seq,
        "ts": ts,
        "command": command,
        "args_hash": args_hash,
        "payload_hash": payload_hash,
        "prev_hash": prev,
        "hash": _sha256_bytes(material),
        "nexus_audit_id": nexus_audit_id,
    }
    with chain_path(control_root).open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, sort_keys=True) + "\n")
    return entry


def verify_chain(control_root: Path) -> dict[str, Any]:
    path = chain_path(control_root)
    if not path.exists():
        return {"schema": "ass-ade.control-chain-verify.v1", "valid": True, "entries": 0, "head": CHAIN_GENESIS, "errors": []}
    errors: list[str] = []
    prev = CHAIN_GENESIS
    count = 0
    head = CHAIN_GENESIS
    with path.open("r", encoding="utf-8") as handle:
        for lineno, raw in enumerate(handle, start=1):
            raw = raw.strip()
            if not raw:
                continue
            try:
                entry = json.loads(raw)
            except json.JSONDecodeError as exc:
                errors.append(f"line {lineno}: invalid json: {exc}")
                continue
            if entry.get("prev_hash") != prev:
                errors.append(f"line {lineno}: prev_hash mismatch (expected {prev})")
            if entry.get("seq") != count:
                errors.append(f"line {lineno}: seq mismatch (expected {count})")
            material = "|".join([
                str(entry.get("prev_hash") or ""),
                str(entry.get("seq") if entry.get("seq") is not None else ""),
                str(entry.get("ts") or ""),
                str(entry.get("command") or ""),
                str(entry.get("args_hash") or ""),
                str(entry.get("payload_hash") or ""),
            ]).encode("utf-8")
            expected = _sha256_bytes(material)
            if entry.get("hash") != expected:
                errors.append(f"line {lineno}: hash mismatch (expected {expected})")
            prev = str(entry.get("hash") or prev)
            head = prev
            count += 1
    return {
        "schema": "ass-ade.control-chain-verify.v1",
        "valid": not errors,
        "entries": count,
        "head": head,
        "errors": errors,
    }


CLASS_PROMOTION_TARGETS = {
    "experiment": ("candidate", "outputs/candidates"),
    "candidate": ("release", "outputs/releases"),
}


def _latest_release_snapshot(control_root: Path) -> Path | None:
    releases_dir = control_root / "outputs" / "releases"
    if not releases_dir.exists():
        return None
    snaps: list[Path] = []
    for child in releases_dir.iterdir():
        if child.is_dir():
            candidate = child / "feature-snapshot.json"
            if candidate.exists():
                snaps.append(candidate)
    if not snaps:
        return None
    return max(snaps, key=lambda p: p.stat().st_mtime)


def _registry_status_for(repo: Path, capability_id: str) -> str | None:
    registry = load_capability_registry(repo)
    for cap in registry.get("capabilities", []):
        if isinstance(cap, dict) and str(cap.get("id")) == capability_id:
            return str(cap.get("status") or "missing")
    return None


def promote_output(
    *,
    source: Path,
    repo: Path,
    control_root: Path,
    target_class: str,
    capability_id: str | None,
    pin: bool,
    skip_stress: bool = False,
) -> dict[str, Any]:
    source = source.resolve()
    repo = repo.resolve()
    control_root = control_root.resolve()

    gate_trace: list[dict[str, Any]] = []

    def _record(name: str, status: str, detail: Any = None) -> None:
        gate_trace.append({"gate": name, "status": status, "detail": detail})

    # Gate 1: source must be under ass-ade-github-latest (canonical-mirror) lineage
    metadata_path = source / "ASS_ADE_OUTPUT.json"
    if not metadata_path.exists():
        _record("source_present", "DENY", "missing ASS_ADE_OUTPUT.json")
        return {"verdict": "REJECT", "gates": gate_trace, "source": str(source)}
    try:
        source_meta = json.loads(metadata_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        _record("source_parseable", "DENY", str(exc))
        return {"verdict": "REJECT", "gates": gate_trace, "source": str(source)}
    source_repo = str(((source_meta.get("source") or {}).get("path")) or "")
    if source_repo and Path(source_repo).resolve() != repo:
        _record("source_from_canonical_mirror", "DENY", source_repo)
        return {"verdict": "REJECT", "gates": gate_trace, "source": str(source)}
    _record("source_from_canonical_mirror", "PASS", source_repo)

    # Gate 2: validate-output
    validation = validate_output(source)
    if not validation["valid"]:
        _record("validate_output", "DENY", validation["errors"])
        return {"verdict": "REJECT", "gates": gate_trace, "source": str(source), "validation": validation}
    _record("validate_output", "PASS", validation.get("warnings", []))

    # Gate 3: target must be a valid promotion
    current_class = str(source_meta.get("class") or "")
    expected_next, target_subdir = CLASS_PROMOTION_TARGETS.get(current_class, (None, None))
    if target_class != expected_next:
        _record("valid_promotion_path", "DENY", f"{current_class} -> {target_class} not allowed")
        return {"verdict": "REJECT", "gates": gate_trace, "source": str(source)}
    _record("valid_promotion_path", "PASS", f"{current_class} -> {target_class}")

    # Gate 4: stress-gain vs last release (skipped for first release baseline)
    baseline_snapshot = _latest_release_snapshot(control_root)
    if baseline_snapshot is None and not skip_stress:
        _record("stress_gain", "SKIP", "no prior release snapshot (first release)")
    elif skip_stress:
        _record("stress_gain", "SKIP", "skip_stress=true")
    else:
        candidate_snapshot = feature_snapshot(repo, collect_pytest=False)
        baseline = json.loads(baseline_snapshot.read_text(encoding="utf-8"))
        report = compare_snapshots(baseline, candidate_snapshot)
        if not report["passed"]:
            _record("stress_gain", "DENY", report["growth_signals"])
            return {"verdict": "REJECT", "gates": gate_trace, "source": str(source), "stress_report": report}
        _record("stress_gain", "PASS", report["growth_signals"])

    # Gate 5: capability status rank must have improved if declared
    if capability_id:
        current_status = _registry_status_for(repo, capability_id)
        if current_status is None:
            _record("capability_declared", "DENY", f"capability_id {capability_id} not in registry")
            return {"verdict": "REJECT", "gates": gate_trace, "source": str(source)}
        # baseline rank: status from registry at last release (best-effort — use current for first release)
        if baseline_snapshot is not None:
            baseline = json.loads(baseline_snapshot.read_text(encoding="utf-8"))
            baseline_rank = STATUS_RANK.get(str((baseline.get("capabilities") or {}).get(capability_id) or "missing"), 0)
            current_rank = STATUS_RANK.get(current_status, 0)
            if current_rank <= baseline_rank:
                _record("capability_rank_improved", "DENY", f"{capability_id}: {baseline_rank} -> {current_rank}")
                return {"verdict": "REJECT", "gates": gate_trace, "source": str(source)}
            _record("capability_rank_improved", "PASS", f"{capability_id}: {baseline_rank} -> {current_rank}")
        else:
            _record("capability_rank_improved", "SKIP", "first release baseline")

    # Gate 6/7: Nexus drift/hallucination — offline skipped, recorded for audit
    _record("nexus_drift_check", "SKIP", "offline: call via atomadic_uep nexus_gates at runtime")
    _record("nexus_hallucination_oracle", "SKIP", "offline: call via atomadic_uep nexus_gates at runtime")
    if target_class == "release":
        _record("nexus_certify_output", "SKIP", "offline: stamp certificate hash post-install")

    # Perform the move
    target_dir = control_root / target_subdir / source.name
    if target_dir.exists():
        _record("target_collision", "DENY", str(target_dir))
        return {"verdict": "REJECT", "gates": gate_trace, "source": str(source)}
    target_dir.parent.mkdir(parents=True, exist_ok=True)
    source.rename(target_dir)

    # Update metadata on the moved output
    new_meta = dict(source_meta)
    new_meta["class"] = target_class
    new_meta["path"] = str(target_dir)
    new_meta["retention"] = retention_for(target_class, pin)
    new_meta["promoted_from"] = source_meta.get("path")
    new_meta["promoted_at"] = utc_now()
    if capability_id:
        lineage = dict(new_meta.get("lineage") or {})
        lineage["capability_id"] = capability_id
        new_meta["lineage"] = lineage
    # Also write a feature-snapshot alongside for future releases
    if target_class == "release":
        snap = feature_snapshot(repo, collect_pytest=False)
        write_json(target_dir / "feature-snapshot.json", snap)
    write_json(target_dir / "ASS_ADE_OUTPUT.json", new_meta)
    _record("move_and_restamp", "PASS", str(target_dir))

    entry = append_chain(
        control_root,
        command="promote",
        args={"source": str(source), "target_class": target_class, "capability_id": capability_id, "pin": pin},
        payload={"gates": gate_trace, "new_output_path": str(target_dir)},
    )

    return {
        "schema": "ass-ade.promote-result.v1",
        "verdict": "PASS",
        "gates": gate_trace,
        "source": str(source),
        "target": str(target_dir),
        "target_class": target_class,
        "capability_id": capability_id,
        "chain_entry": entry,
    }


def retire_outputs(
    control_root: Path,
    *,
    lane: str | None = None,
    output_class: str | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    control_root = control_root.resolve()
    today = datetime.now(timezone.utc).date()
    archive_root = control_root / "archive" / today.strftime("%Y")
    retired: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []

    search_dirs = []
    if output_class in (None, "experiment"):
        search_dirs.append(control_root / "outputs" / "experiments")
    if output_class in (None, "candidate"):
        search_dirs.append(control_root / "outputs" / "candidates")

    for search_dir in search_dirs:
        if not search_dir.exists():
            continue
        for child in sorted(search_dir.iterdir()):
            if not child.is_dir():
                continue
            metadata_path = child / "ASS_ADE_OUTPUT.json"
            if not metadata_path.exists():
                skipped.append({"path": str(child), "reason": "no metadata"})
                continue
            try:
                meta = json.loads(metadata_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                skipped.append({"path": str(child), "reason": "invalid metadata"})
                continue
            retention = meta.get("retention") or {}
            if retention.get("pin"):
                skipped.append({"path": str(child), "reason": "pinned"})
                continue
            expires = retention.get("expires")
            if not expires:
                skipped.append({"path": str(child), "reason": "no expiry"})
                continue
            try:
                expiry_date = datetime.fromisoformat(expires).date()
            except ValueError:
                skipped.append({"path": str(child), "reason": f"invalid expires: {expires}"})
                continue
            if expiry_date > today:
                skipped.append({"path": str(child), "reason": f"expires {expires}"})
                continue
            lane_lineage = (meta.get("lineage") or {}).get("lane")
            if lane and lane_lineage != slugify(lane):
                skipped.append({"path": str(child), "reason": f"lane {lane_lineage} != {lane}"})
                continue
            destination = archive_root / child.name
            retired.append({"path": str(child), "archive": str(destination), "expires": expires})
            if not dry_run:
                destination.parent.mkdir(parents=True, exist_ok=True)
                child.rename(destination)

    result = {
        "schema": "ass-ade.retire-result.v1",
        "created_at": utc_now(),
        "dry_run": dry_run,
        "retired": retired,
        "skipped": skipped,
    }
    if not dry_run and retired:
        append_chain(
            control_root,
            command="retire",
            args={"lane": lane, "class": output_class, "dry_run": dry_run},
            payload={"retired_count": len(retired), "paths": [r["path"] for r in retired]},
        )
    return result


def cmd_promote(args: argparse.Namespace) -> int:
    result = promote_output(
        source=Path(args.source).expanduser().resolve(),
        repo=Path(args.repo).expanduser().resolve(),
        control_root=Path(args.root).expanduser().resolve(),
        target_class=args.target_class,
        capability_id=args.capability_id,
        pin=args.pin,
        skip_stress=args.skip_stress,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result.get("verdict") == "PASS" else 1


def cmd_retire(args: argparse.Namespace) -> int:
    result = retire_outputs(
        Path(args.root).expanduser().resolve(),
        lane=args.lane,
        output_class=args.output_class,
        dry_run=args.dry_run,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


def cmd_verify_chain(args: argparse.Namespace) -> int:
    result = verify_chain(Path(args.root).expanduser().resolve())
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["valid"] else 1


def build_parser() -> argparse.ArgumentParser:
    parent = default_parent()
    control = default_control_root(parent)
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="Create the local control directory tree.")
    p_init.add_argument("--root", default=str(control), help="Control root to create.")
    p_init.set_defaults(func=cmd_init)

    p_inventory = sub.add_parser("inventory", help="Inventory local ASS-ADE sibling folders.")
    p_inventory.add_argument("--parent", default=str(parent), help="Parent directory containing ASS-ADE siblings.")
    p_inventory.add_argument("--root", default=str(control), help="Control root.")
    p_inventory.add_argument("--pattern", default="*ass-ade*", help="Sibling glob pattern.")
    p_inventory.add_argument("--json", action="store_true", help="Print full JSON inventory.")
    p_inventory.set_defaults(func=cmd_inventory)

    p_stamp = sub.add_parser("stamp-output", help="Write ASS_ADE_OUTPUT.json into a rebuild output.")
    p_stamp.add_argument("output", help="Rebuild output directory.")
    p_stamp.add_argument("--source", help="Source git checkout used for the rebuild.")
    p_stamp.add_argument("--class", dest="output_class", default="experiment", help="Output class.")
    p_stamp.add_argument("--lane", default="scratch", help="Evolution lane.")
    p_stamp.add_argument("--branch", help="Associated branch name.")
    p_stamp.add_argument("--slug", help="Output slug.")
    p_stamp.add_argument("--parent-output-id", help="Parent rebuild output id.")
    p_stamp.add_argument("--pin", action="store_true", help="Pin output for retention.")
    p_stamp.set_defaults(func=cmd_stamp_output)

    p_validate = sub.add_parser("validate-output", help="Validate a stamped rebuild output.")
    p_validate.add_argument("output", help="Rebuild output directory.")
    p_validate.set_defaults(func=cmd_validate_output)

    p_snapshot = sub.add_parser("snapshot", help="Write a feature snapshot for a repo or output.")
    p_snapshot.add_argument("path", help="Repo or rebuild output path.")
    p_snapshot.add_argument("--collect-pytest", action="store_true", help="Run pytest collection.")
    p_snapshot.add_argument("--out", help="Write snapshot JSON to this path.")
    p_snapshot.set_defaults(func=cmd_snapshot)

    p_stress = sub.add_parser("stress-gain", help="Compare baseline and candidate for measurable feature gain.")
    p_stress.add_argument("base", help="Baseline repo or output path.")
    p_stress.add_argument("candidate", help="Candidate repo or output path.")
    p_stress.add_argument("--collect-pytest", action="store_true", help="Run pytest collection on both paths.")
    p_stress.add_argument("--out", help="Write report JSON to this path.")
    p_stress.add_argument("--no-fail", action="store_true", help="Always exit zero after writing the report.")
    p_stress.set_defaults(func=cmd_stress_gain)

    p_registry = sub.add_parser("validate-registry", help="Validate capabilities/registry.json.")
    p_registry.add_argument("--repo", default=str(Path.cwd()), help="Repository root.")
    p_registry.set_defaults(func=cmd_validate_registry)

    p_docs = sub.add_parser("docs-generate", help="Regenerate docs from JSON ledgers.")
    p_docs.add_argument("--repo", default=str(Path.cwd()), help="Repository root.")
    p_docs.add_argument("--root", default=str(control), help="Control root.")
    p_docs.set_defaults(func=cmd_docs_generate)

    p_diff = sub.add_parser("diff-json", help="Diff two JSON ledger files.")
    p_diff.add_argument("before", help="Earlier JSON file.")
    p_diff.add_argument("after", help="Later JSON file.")
    p_diff.add_argument("--out", help="Write diff JSON to this path.")
    p_diff.set_defaults(func=cmd_diff_json)

    p_ingest = sub.add_parser("ingest-json", help="Build CONTROL_INDEX.json from local JSON ledgers.")
    p_ingest.add_argument("--repo", default=str(Path.cwd()), help="Repository root.")
    p_ingest.add_argument("--parent", default=str(parent), help="Parent directory containing ASS-ADE siblings.")
    p_ingest.add_argument("--root", default=str(control), help="Control root.")
    p_ingest.set_defaults(func=cmd_ingest_json)

    p_refresh = sub.add_parser("refresh", help="Update inventory, baseline snapshot, index, and generated docs.")
    p_refresh.add_argument("--repo", default=str(Path.cwd()), help="Repository root.")
    p_refresh.add_argument("--parent", default=str(parent), help="Parent directory containing ASS-ADE siblings.")
    p_refresh.add_argument("--root", default=str(control), help="Control root.")
    p_refresh.add_argument("--pattern", default="*ass-ade*", help="Sibling glob pattern.")
    p_refresh.add_argument("--collect-pytest", action="store_true", help="Run pytest collection for baseline snapshot.")
    p_refresh.add_argument("--docs", action="store_true", help="Regenerate generated docs.")
    p_refresh.set_defaults(func=cmd_refresh)

    p_promote = sub.add_parser(
        "promote",
        help="Promote an experiment to candidate or candidate to release through fail-closed gates.",
    )
    p_promote.add_argument("source", help="Source rebuild output directory to promote.")
    p_promote.add_argument(
        "--target-class",
        required=True,
        choices=["candidate", "release"],
        help="Target output class.",
    )
    p_promote.add_argument("--repo", default=str(Path.cwd()), help="Canonical repo root (canonical-mirror).")
    p_promote.add_argument("--root", default=str(control), help="Control root.")
    p_promote.add_argument("--capability-id", help="Capability id being advanced by this promotion.")
    p_promote.add_argument("--pin", action="store_true", help="Pin the promoted output for retention.")
    p_promote.add_argument(
        "--skip-stress",
        action="store_true",
        help="Skip stress-gain (only for emergency rollbacks; recorded in chain).",
    )
    p_promote.set_defaults(func=cmd_promote)

    p_retire = sub.add_parser("retire", help="Archive expired experiments and candidates honoring pin + expires.")
    p_retire.add_argument("--root", default=str(control), help="Control root.")
    p_retire.add_argument("--lane", help="Only retire outputs on this lane slug.")
    p_retire.add_argument(
        "--class",
        dest="output_class",
        choices=["experiment", "candidate"],
        help="Restrict to one output class.",
    )
    p_retire.add_argument("--dry-run", action="store_true", help="Report what would be retired without moving.")
    p_retire.set_defaults(func=cmd_retire)

    p_chain = sub.add_parser("verify-chain", help="Replay and verify the control-chain audit log.")
    p_chain.add_argument("--root", default=str(control), help="Control root.")
    p_chain.set_defaults(func=cmd_verify_chain)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
