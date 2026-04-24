from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import tomllib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from pydantic import BaseModel, ConfigDict, Field

from ass_ade.engine.rebuild.version_tracker import INITIAL_VERSION, bump_version


EVOLUTION_SCHEMA = "ass-ade.evolution.v1"
DEFAULT_EVOLUTION_DIR = Path(".ass-ade") / "evolution"
DEFAULT_LEDGER_PATH = DEFAULT_EVOLUTION_DIR / "ledger.jsonl"
DEFAULT_EVENTS_DIR = DEFAULT_EVOLUTION_DIR / "events"
DEFAULT_MARKDOWN_PATH = Path("EVOLUTION.md")
DEFAULT_DEMO_PATH = Path("docs") / "evolution-workflow.md"
_SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(?:[-+][A-Za-z0-9.-]+)?$")


class EvolutionCommand(BaseModel):
    command: str
    status: str = "recorded"
    notes: str = ""


class EvolutionGitState(BaseModel):
    available: bool
    branch: str = "unknown"
    commit: str = "unknown"
    dirty: bool = False
    staged: int = 0
    unstaged: int = 0
    untracked: int = 0
    status: list[str] = Field(default_factory=list)


class EvolutionEvent(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_id: str = Field(default=EVOLUTION_SCHEMA, alias="schema")
    event_id: str
    timestamp_utc: str
    event_type: str
    summary: str
    version: str
    root: str
    git: EvolutionGitState
    commands: list[EvolutionCommand] = Field(default_factory=list)
    metrics: dict[str, Any] = Field(default_factory=dict)
    reports: list[str] = Field(default_factory=list)
    artifacts: list[str] = Field(default_factory=list)
    rationale: str = ""
    next_steps: list[str] = Field(default_factory=list)
    rebuild: dict[str, Any] = Field(default_factory=dict)
    certificates: list[dict[str, Any]] = Field(default_factory=list)
    lineage_ids: list[str] = Field(default_factory=list)


class EvolutionRecordResult(BaseModel):
    event: EvolutionEvent
    ledger_path: str
    snapshot_path: str
    markdown_path: str


class VersionBumpResult(BaseModel):
    old_version: str
    new_version: str
    bump: str
    dry_run: bool
    files_updated: list[str] = Field(default_factory=list)
    backup_dir: str = ""
    files_backed_up: list[str] = Field(default_factory=list)


def _run_git(root: Path, args: list[str]) -> tuple[bool, str]:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), *args],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return False, ""
    if result.returncode != 0:
        return False, result.stderr.strip()
    return True, result.stdout.strip()


def collect_git_state(root: Path) -> EvolutionGitState:
    root = root.resolve()
    ok_status, status_text = _run_git(root, ["status", "--short"])
    ok_branch, branch = _run_git(root, ["rev-parse", "--abbrev-ref", "HEAD"])
    ok_commit, commit = _run_git(root, ["rev-parse", "--short", "HEAD"])
    if not ok_status:
        return EvolutionGitState(available=False)

    lines = [line for line in status_text.splitlines() if line.strip()]
    staged = 0
    unstaged = 0
    untracked = 0
    for line in lines:
        marker = line[:2]
        if marker == "??":
            untracked += 1
            continue
        if marker[:1].strip():
            staged += 1
        if len(marker) > 1 and marker[1:2].strip():
            unstaged += 1

    return EvolutionGitState(
        available=True,
        branch=branch if ok_branch and branch else "unknown",
        commit=commit if ok_commit and commit else "unknown",
        dirty=bool(lines),
        staged=staged,
        unstaged=unstaged,
        untracked=untracked,
        status=lines[:200],
    )


def read_project_version(root: Path) -> str:
    root = root.resolve()
    pyproject = root / "pyproject.toml"
    if pyproject.exists():
        try:
            data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
            version = data.get("project", {}).get("version")
            if isinstance(version, str) and version.strip():
                return version.strip()
        except (OSError, tomllib.TOMLDecodeError):
            pass

    init_file = root / "src" / "ass_ade" / "__init__.py"
    if init_file.exists():
        match = re.search(
            r"^__version__\s*=\s*['\"]([^'\"]+)['\"]",
            init_file.read_text(encoding="utf-8"),
            flags=re.MULTILINE,
        )
        if match:
            return match.group(1)

    version_file = root / "VERSION"
    if version_file.exists():
        lines = version_file.read_text(encoding="utf-8").splitlines()
        if lines and lines[0].strip():
            return lines[0].strip()
    return INITIAL_VERSION


def _coerce_metric_value(value: str) -> Any:
    text = value.strip()
    lowered = text.lower()
    if lowered in {"true", "false"}:
        return lowered == "true"
    try:
        return int(text)
    except ValueError:
        pass
    try:
        return float(text)
    except ValueError:
        return text


def parse_metrics(items: Iterable[str]) -> dict[str, Any]:
    metrics: dict[str, Any] = {}
    for item in items:
        for part in item.split(","):
            if not part.strip():
                continue
            if "=" not in part:
                raise ValueError(f"Metric must use key=value format: {part}")
            key, value = part.split("=", 1)
            key = key.strip()
            if not key:
                raise ValueError("Metric key cannot be empty")
            metrics[key] = _coerce_metric_value(value)
    return metrics


def parse_command_specs(items: Iterable[str]) -> list[EvolutionCommand]:
    commands: list[EvolutionCommand] = []
    for item in items:
        text = item.strip()
        if not text:
            continue
        status = "recorded"
        notes = ""
        command = text
        if "::" in text:
            prefix, command = text.split("::", 1)
            for part in prefix.split(","):
                if "=" not in part:
                    continue
                key, value = part.split("=", 1)
                if key.strip() == "status":
                    status = value.strip() or status
                elif key.strip() == "notes":
                    notes = value.strip()
        commands.append(EvolutionCommand(command=command.strip(), status=status, notes=notes))
    return commands


def _read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def _certificate_summary(path: Path) -> dict[str, Any]:
    data = _read_json(path)
    if not data:
        return {}
    keys = (
        "schema",
        "version",
        "certificate_version",
        "certificate_sha256",
        "certificate_hash",
        "sha256",
        "digest",
        "valid",
        "signed_by",
    )
    summary = {key: data[key] for key in keys if key in data}
    summary["path"] = str(path)
    return summary


def collect_certificate_summaries(root: Path, rebuild_path: Path | None = None) -> list[dict[str, Any]]:
    paths = [root.resolve() / "CERTIFICATE.json"]
    if rebuild_path is not None:
        paths.append(rebuild_path.resolve() / "CERTIFICATE.json")
    summaries: list[dict[str, Any]] = []
    for path in paths:
        if path.exists():
            summary = _certificate_summary(path)
            if summary:
                summaries.append(summary)
    return summaries


def collect_rebuild_summary(rebuild_path: Path | None) -> dict[str, Any]:
    if rebuild_path is None:
        return {}
    root = rebuild_path.resolve()
    if not root.exists():
        return {"path": str(root), "exists": False}

    summary: dict[str, Any] = {"path": str(root), "exists": True}
    version_file = root / "VERSION"
    if version_file.exists():
        lines = version_file.read_text(encoding="utf-8").splitlines()
        if lines:
            summary["version"] = lines[0].strip()
    manifest = _read_json(root / "MANIFEST.json")
    if manifest:
        components = manifest.get("components")
        if isinstance(components, list):
            summary["component_count"] = len(components)
        tier_distribution = manifest.get("tier_distribution")
        if isinstance(tier_distribution, dict):
            summary["tier_distribution"] = tier_distribution
    cert = _certificate_summary(root / "CERTIFICATE.json")
    if cert:
        summary["certificate"] = cert
    report_path = root / "REBUILD_REPORT.md"
    if report_path.exists():
        summary["report"] = str(report_path)
    return summary


def collect_lineage_ids(root: Path) -> list[str]:
    birth_dir = root.resolve() / ".ass-ade" / "birth"
    if not birth_dir.exists():
        return []
    lineage_ids: list[str] = []
    for path in sorted(birth_dir.glob("*.response.json")):
        data = _read_json(path)
        for key in ("lineage_id", "lineageId", "id"):
            value = data.get(key)
            if isinstance(value, str) and value.startswith("dlv-"):
                lineage_ids.append(value)
        nested = data.get("lineage")
        if isinstance(nested, dict):
            value = nested.get("id")
            if isinstance(value, str) and value.startswith("dlv-"):
                lineage_ids.append(value)
    return sorted(set(lineage_ids))


def _event_id(timestamp_utc: str, event_type: str, summary: str) -> str:
    payload = f"{timestamp_utc}|{event_type}|{summary}".encode("utf-8")
    digest = hashlib.sha256(payload).hexdigest()[:12]
    slug = re.sub(r"[^a-z0-9]+", "-", event_type.lower()).strip("-") or "event"
    return f"{slug}-{digest}"


def _event_filename(timestamp_utc: str, event_id: str) -> str:
    safe_timestamp = timestamp_utc.replace("-", "").replace(":", "").replace("+", "")
    safe_timestamp = safe_timestamp.replace(".", "").replace("Z", "Z")
    return f"{safe_timestamp}-{event_id}.json"


def _display_path(root: Path, path_text: str) -> str:
    try:
        path = Path(path_text)
        if path.is_absolute():
            return str(path.relative_to(root))
    except (OSError, ValueError):
        pass
    return path_text


def _load_ledger(root: Path) -> list[EvolutionEvent]:
    ledger_path = root.resolve() / DEFAULT_LEDGER_PATH
    if not ledger_path.exists():
        return []
    events: list[EvolutionEvent] = []
    for line in ledger_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            events.append(EvolutionEvent.model_validate_json(line))
        except ValueError:
            continue
    return events


def render_evolution_markdown(root: Path, events: list[EvolutionEvent] | None = None) -> str:
    root = root.resolve()
    events = events if events is not None else _load_ledger(root)
    current_version = read_project_version(root)
    git = collect_git_state(root)
    lines = [
        "# ASS-ADE Evolution Ledger",
        "",
        "This file is generated by `ass-ade protocol evolution-record` and related protocol commands.",
        "It records public-safe decision summaries, command receipts, metrics, and artifact paths.",
        "It does not store secrets or private chain-of-thought.",
        "",
        "## Current State",
        "",
        f"- Version: {current_version}",
        f"- Git branch: {git.branch if git.available else 'unavailable'}",
        f"- Git commit: {git.commit if git.available else 'unavailable'}",
        f"- Dirty worktree: {git.dirty if git.available else 'unknown'}",
        "",
        "## Events",
        "",
    ]
    if not events:
        lines.append("No evolution events have been recorded yet.")
        return "\n".join(lines)

    for event in sorted(events, key=lambda item: item.timestamp_utc, reverse=True):
        lines.extend(
            [
                f"### {event.timestamp_utc} - {event.event_type}",
                "",
                f"- Event ID: `{event.event_id}`",
                f"- Version: {event.version}",
                f"- Summary: {event.summary}",
            ]
        )
        if event.rationale:
            lines.append(f"- Rationale: {event.rationale}")
        if event.git.available:
            lines.append(
                f"- Git: `{event.git.branch}` at `{event.git.commit}` "
                f"(dirty={event.git.dirty}, staged={event.git.staged}, "
                f"unstaged={event.git.unstaged}, untracked={event.git.untracked})"
            )
        if event.commands:
            lines.extend(["", "Commands:"])
            for command in event.commands:
                note = f" - {command.notes}" if command.notes else ""
                lines.append(f"- [{command.status}] `{command.command}`{note}")
        if event.metrics:
            lines.extend(["", "Metrics:"])
            for key, value in sorted(event.metrics.items()):
                lines.append(f"- `{key}`: {value}")
        if event.rebuild:
            lines.extend(["", "Rebuild:"])
            for key, value in sorted(event.rebuild.items()):
                if key == "certificate":
                    continue
                lines.append(f"- `{key}`: {value}")
            cert = event.rebuild.get("certificate")
            if isinstance(cert, dict):
                sha = cert.get("certificate_sha256") or cert.get("certificate_hash") or cert.get("sha256")
                if sha:
                    lines.append(f"- `certificate_sha256`: {sha}")
        if event.reports:
            lines.extend(["", "Reports:"])
            lines.extend(f"- `{_display_path(root, item)}`" for item in event.reports)
        if event.artifacts:
            lines.extend(["", "Artifacts:"])
            lines.extend(f"- `{_display_path(root, item)}`" for item in event.artifacts)
        if event.next_steps:
            lines.extend(["", "Next Steps:"])
            lines.extend(f"- {item}" for item in event.next_steps)
        if event.lineage_ids:
            lines.extend(["", f"Lineage receipts: {len(event.lineage_ids)}"])
        lines.append("")
    return "\n".join(lines).rstrip()


def record_evolution_event(
    *,
    root: Path,
    event_type: str,
    summary: str,
    version: str = "",
    rebuild_path: Path | None = None,
    commands: list[EvolutionCommand] | None = None,
    metrics: dict[str, Any] | None = None,
    reports: list[str] | None = None,
    artifacts: list[str] | None = None,
    rationale: str = "",
    next_steps: list[str] | None = None,
    lineage_ids: list[str] | None = None,
    timestamp_utc: str = "",
) -> EvolutionRecordResult:
    root = root.resolve()
    timestamp = timestamp_utc or datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    if timestamp.endswith("+00:00"):
        timestamp = f"{timestamp[:-6]}Z"
    version_value = version.strip() or read_project_version(root)
    event_id = _event_id(timestamp, event_type, summary)
    event = EvolutionEvent(
        event_id=event_id,
        timestamp_utc=timestamp,
        event_type=event_type,
        summary=summary,
        version=version_value,
        root=str(root),
        git=collect_git_state(root),
        commands=commands or [],
        metrics=metrics or {},
        reports=reports or [],
        artifacts=artifacts or [],
        rationale=rationale,
        next_steps=next_steps or [],
        rebuild=collect_rebuild_summary(rebuild_path),
        certificates=collect_certificate_summaries(root, rebuild_path),
        lineage_ids=lineage_ids if lineage_ids is not None else collect_lineage_ids(root),
    )

    evolution_dir = root / DEFAULT_EVOLUTION_DIR
    events_dir = root / DEFAULT_EVENTS_DIR
    ledger_path = root / DEFAULT_LEDGER_PATH
    markdown_path = root / DEFAULT_MARKDOWN_PATH
    evolution_dir.mkdir(parents=True, exist_ok=True)
    events_dir.mkdir(parents=True, exist_ok=True)
    snapshot_path = events_dir / _event_filename(timestamp, event_id)

    payload = event.model_dump(mode="json", by_alias=True)
    snapshot_path.write_text(f"{json.dumps(payload, indent=2, default=str)}\n", encoding="utf-8")
    with ledger_path.open("a", encoding="utf-8") as fh:
        fh.write(f"{json.dumps(payload, sort_keys=True, default=str)}\n")

    events = _load_ledger(root)
    markdown_path.write_text(f"{render_evolution_markdown(root, events)}\n", encoding="utf-8")
    return EvolutionRecordResult(
        event=event,
        ledger_path=str(ledger_path),
        snapshot_path=str(snapshot_path),
        markdown_path=str(markdown_path),
    )


def _replace_project_version(text: str, new_version: str) -> str:
    lines = text.splitlines()
    in_project = False
    replaced = False
    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped == "[project]":
            in_project = True
            continue
        if in_project and stripped.startswith("[") and stripped.endswith("]"):
            break
        if in_project and stripped.startswith("version"):
            lines[index] = re.sub(
                r"version\s*=\s*['\"][^'\"]+['\"]",
                f'version = "{new_version}"',
                line,
                count=1,
            )
            replaced = True
            break
    if not replaced:
        raise ValueError("No [project] version field found in pyproject.toml")
    trailing = "\n" if text.endswith("\n") else ""
    return "\n".join(lines) + trailing


def _replace_init_version(text: str, new_version: str) -> str:
    return re.sub(
        r"^__version__\s*=\s*['\"][^'\"]+['\"]",
        f'__version__ = "{new_version}"',
        text,
        count=1,
        flags=re.MULTILINE,
    )


def _replace_readme_version(text: str, new_version: str) -> str:
    updated, count = re.subn(
        r"^\*\*Version:\*\*\s*.+$",
        f"**Version:** {new_version}",
        text,
        count=1,
        flags=re.MULTILINE,
    )
    return updated if count else text


def _insert_changelog_entry(text: str, new_version: str, summary: str, timestamp: str) -> str:
    if f"## [{new_version}]" in text:
        return text
    release_date = timestamp.split("T", 1)[0]
    entry = f"## [{new_version}] - {release_date}\n\n- {summary}\n\n"
    marker = "## [Unreleased]"
    index = text.find(marker)
    if index == -1:
        return f"{text.rstrip()}\n\n{entry}"
    next_heading = text.find("\n## ", index + len(marker))
    if next_heading == -1:
        return f"{text.rstrip()}\n\n{entry}"
    return f"{text[:next_heading].rstrip()}\n\n{entry}{text[next_heading:].lstrip()}"


def calculate_next_version(root: Path, bump: str, new_version: str = "") -> tuple[str, str]:
    old_version = read_project_version(root)
    requested = new_version.strip()
    if requested:
        if not _SEMVER_RE.match(requested):
            raise ValueError(f"Version must be semantic version-like: {requested}")
        return old_version, requested
    if bump not in {"patch", "minor", "major"}:
        raise ValueError("Bump must be one of: patch, minor, major")
    return old_version, bump_version(old_version, bump)


def bump_project_version(
    *,
    root: Path,
    bump: str,
    new_version: str = "",
    summary: str = "Version update",
    dry_run: bool = False,
) -> VersionBumpResult:
    root = root.resolve()
    old_version, target_version = calculate_next_version(root, bump, new_version)
    files_updated: list[str] = []
    files_backed_up: list[str] = []
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup_dir = root / DEFAULT_EVOLUTION_DIR / "version-backups" / f"{old_version}-to-{target_version}-{timestamp}"

    def backup_file(path: Path) -> None:
        if dry_run or not path.exists():
            return
        rel = path.relative_to(root)
        target = backup_dir / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
        files_backed_up.append(str(target))

    pyproject = root / "pyproject.toml"
    if pyproject.exists():
        backup_file(pyproject)
        updated = _replace_project_version(pyproject.read_text(encoding="utf-8"), target_version)
        if not dry_run:
            pyproject.write_text(updated, encoding="utf-8")
        files_updated.append(str(pyproject))

    init_file = root / "src" / "ass_ade" / "__init__.py"
    if init_file.exists():
        backup_file(init_file)
        updated = _replace_init_version(init_file.read_text(encoding="utf-8"), target_version)
        if not dry_run:
            init_file.write_text(updated, encoding="utf-8")
        files_updated.append(str(init_file))

    readme = root / "README.md"
    if readme.exists():
        original = readme.read_text(encoding="utf-8")
        updated = _replace_readme_version(original, target_version)
        if updated != original:
            backup_file(readme)
            if not dry_run:
                readme.write_text(updated, encoding="utf-8")
            files_updated.append(str(readme))

    changelog = root / "CHANGELOG.md"
    if changelog.exists():
        backup_file(changelog)
        release_timestamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        updated = _insert_changelog_entry(
            changelog.read_text(encoding="utf-8"),
            target_version,
            summary,
            release_timestamp,
        )
        if not dry_run:
            changelog.write_text(updated, encoding="utf-8")
        files_updated.append(str(changelog))

    return VersionBumpResult(
        old_version=old_version,
        new_version=target_version,
        bump=bump,
        dry_run=dry_run,
        files_updated=files_updated,
        backup_dir=str(backup_dir) if files_backed_up else "",
        files_backed_up=files_backed_up,
    )


def normalize_branch_tracks(branches: Iterable[str]) -> list[str]:
    normalized: list[str] = []
    for branch in branches:
        item = branch.strip()
        if not item:
            continue
        item = re.sub(r"[^A-Za-z0-9/_-]+", "-", item).strip("-/")
        if not item:
            continue
        if not item.startswith("evolve/"):
            item = f"evolve/{item}"
        normalized.append(item)
    return normalized or ["evolve/tests-first", "evolve/docs-first", "evolve/safety-first"]


def render_branch_evolution_demo(
    *,
    root: Path,
    branches: Iterable[str],
    iterations: int,
) -> str:
    root = root.resolve()
    tracks = normalize_branch_tracks(branches)
    iterations = max(1, iterations)
    version = read_project_version(root)
    lines = [
        "# Split-Branch Evolution Workflow",
        "",
        "This demo shows how ASS-ADE can evolve along several public-safe branches,",
        "record evidence for each path, then merge the strongest line after review.",
        "",
        "## Baseline",
        "",
        "```bash",
        "ass-ade doctor",
        "python -m pytest tests/ -q --no-header",
        (
            "ass-ade protocol evolution-record baseline "
            "--summary \"Baseline before branch evolution\" "
            "--command \"ass-ade doctor\" "
            "--command \"python -m pytest tests/ -q --no-header\""
        ),
        "```",
        "",
        "## Branch Tracks",
        "",
    ]
    for track in tracks:
        short = track.split("/", 1)[-1]
        lines.extend(
            [
                f"### `{track}`",
                "",
                "```bash",
                f"git switch -c {track}",
            ]
        )
        for index in range(1, iterations + 1):
            lines.extend(
                [
                    f"ass-ade context pack \"evolution {short} iteration {index}\" --path . --json",
                    (
                        "ass-ade design "
                        f"\"{short} iteration {index}: improve the strongest measured gap\" "
                        "--path . --local-only --out "
                        f"blueprints/{short}-iteration-{index}.json"
                    ),
                    "ass-ade enhance . --local-only --json --limit 10",
                    "ass-ade rebuild . --yes --git-track",
                    "python -m pytest tests/ -q --no-header",
                    (
                        "ass-ade protocol evolution-record iteration "
                        f"--summary \"{short} iteration {index}\" "
                        f"--version {version} "
                        f"--artifact blueprints/{short}-iteration-{index}.json "
                        "--command \"ass-ade context pack\" "
                        "--command \"ass-ade design\" "
                        "--command \"ass-ade enhance\" "
                        "--command \"ass-ade rebuild . --yes --git-track\" "
                        "--command \"python -m pytest tests/ -q --no-header\""
                    ),
                ]
            )
        lines.extend(["git switch -", "```", ""])

    lines.extend(
        [
            "## Compare And Merge",
            "",
            "```bash",
            "git log --oneline --graph --all --decorate",
            "ass-ade protocol evolution-record merge-candidate --summary \"Compare branch evidence\"",
            "git switch main",
            "# Merge the branch with passing tests, fresh docs, and the strongest evidence ledger.",
            "git merge --no-ff evolve/tests-first",
            "python -m pytest tests/ -q --no-header",
            (
                "ass-ade protocol evolution-record merge "
                "--summary \"Merged selected evolution branch\" "
                "--command \"git merge --no-ff <branch>\" "
                "--command \"python -m pytest tests/ -q --no-header\""
            ),
            "```",
            "",
            "## Merge Rule",
            "",
            "A branch is merge-ready only when tests pass, public docs are current,",
            "`EVOLUTION.md` has the event trail, and any release needs a fresh certificate.",
            "",
            "## Version Rule",
            "",
            "Use `ass-ade protocol version-bump patch|minor|major` after the winning path is merged.",
            "The command updates package version surfaces and records the bump in the evolution ledger.",
        ]
    )
    return "\n".join(lines)


def write_branch_evolution_demo(
    *,
    root: Path,
    branches: Iterable[str],
    iterations: int,
    output: Path | None = None,
) -> Path:
    root = root.resolve()
    target = output if output is not None else root / DEFAULT_DEMO_PATH
    if not target.is_absolute():
        target = root / target
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        f"{render_branch_evolution_demo(root=root, branches=branches, iterations=iterations)}\n",
        encoding="utf-8",
    )
    return target
