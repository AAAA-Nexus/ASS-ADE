"""Prompt artifact introspection tools.

These helpers operate only on explicit prompt text or prompt files supplied by
the caller. They do not expose hidden runtime prompts from the host model.
"""

from __future__ import annotations

import difflib
import hashlib
import json
import re
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

_SECRET_RE = re.compile(
    r"(?i)(api[_-]?key|authorization|bearer|private[_-]?key|secret|token)\s*[:=]\s*\S+"
)


class PromptArtifact(BaseModel):
    source: str
    text: str


class PromptHashResult(BaseModel):
    source: str
    sha256: str
    bytes: int
    lines: int


class PromptValidateResult(BaseModel):
    source: str
    sha256: str
    expected_sha256: str | None = None
    valid: bool = False
    manifest_path: str | None = None
    manifest_signature_present: bool = False
    signature_verified: bool = False
    notes: list[str] = Field(default_factory=list)


class PromptSectionResult(BaseModel):
    source: str
    section: str
    found: bool
    text: str = ""
    sha256: str | None = None


class PromptDiffResult(BaseModel):
    source: str
    baseline_source: str
    current_sha256: str
    baseline_sha256: str
    diff: str
    redacted: bool = True
    truncated: bool = False


class PromptProposalResult(BaseModel):
    proposal_id: str
    source: str
    prompt_sha256: str
    objective: str
    recommended_changes: list[str]
    verification_criteria: list[str]
    requires_human_approval: bool = True
    next_action: str


def _resolve_under(root: Path, value: str | Path) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = root / path
    path = path.resolve()
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"prompt path escapes working directory: {value}") from exc
    if not path.is_file():
        raise ValueError(f"prompt path does not exist: {value}")
    return path


def load_prompt_artifact(
    *,
    working_dir: str | Path = ".",
    prompt_text: str | None = None,
    prompt_path: str | Path | None = None,
    source_label: str | None = None,
) -> PromptArtifact:
    if bool(prompt_text) == bool(prompt_path):
        raise ValueError("provide exactly one of prompt_text or prompt_path")

    if prompt_text is not None:
        return PromptArtifact(source=source_label or "inline", text=prompt_text)

    root = Path(working_dir).resolve()
    path = _resolve_under(root, prompt_path or "")
    return PromptArtifact(
        source=source_label or path.relative_to(root).as_posix(),
        text=path.read_text(encoding="utf-8", errors="replace"),
    )


def prompt_hash(
    *,
    working_dir: str | Path = ".",
    prompt_text: str | None = None,
    prompt_path: str | Path | None = None,
) -> PromptHashResult:
    artifact = load_prompt_artifact(
        working_dir=working_dir,
        prompt_text=prompt_text,
        prompt_path=prompt_path,
    )
    encoded = artifact.text.encode()
    return PromptHashResult(
        source=artifact.source,
        sha256=hashlib.sha256(encoded).hexdigest(),
        bytes=len(encoded),
        lines=len(artifact.text.splitlines()),
    )


def _extract_expected_hash(manifest: dict[str, Any], *, prompt_name: str | None) -> str | None:
    direct = manifest.get("sha256") or manifest.get("prompt_sha256")
    if isinstance(direct, str):
        return direct

    if prompt_name:
        prompts = manifest.get("prompts")
        if isinstance(prompts, dict):
            entry = prompts.get(prompt_name)
            if isinstance(entry, dict):
                value = entry.get("sha256") or entry.get("prompt_sha256")
                if isinstance(value, str):
                    return value
    return None


def prompt_validate(
    *,
    manifest_path: str | Path,
    working_dir: str | Path = ".",
    prompt_text: str | None = None,
    prompt_path: str | Path | None = None,
    prompt_name: str | None = None,
) -> PromptValidateResult:
    root = Path(working_dir).resolve()
    manifest_file = _resolve_under(root, manifest_path)
    artifact = load_prompt_artifact(
        working_dir=root,
        prompt_text=prompt_text,
        prompt_path=prompt_path,
    )
    prompt_digest = hashlib.sha256(artifact.text.encode()).hexdigest()

    try:
        manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"manifest is not valid JSON: {exc}") from exc
    if not isinstance(manifest, dict):
        raise ValueError("manifest must be a JSON object")

    expected = _extract_expected_hash(manifest, prompt_name=prompt_name)
    signature_present = bool(manifest.get("signature") or manifest.get("signatures"))
    notes: list[str] = []
    if expected is None:
        notes.append("No expected prompt hash found in manifest.")
    if signature_present:
        notes.append("Signature metadata is present; local toolkit verifies hash only.")
    else:
        notes.append("No signature metadata present; local toolkit verifies hash only.")

    return PromptValidateResult(
        source=artifact.source,
        sha256=prompt_digest,
        expected_sha256=expected,
        valid=bool(expected and prompt_digest.lower() == expected.lower()),
        manifest_path=manifest_file.relative_to(root).as_posix(),
        manifest_signature_present=signature_present,
        signature_verified=False,
        notes=notes,
    )


def _markdown_section(text: str, section: str) -> str | None:
    lines = text.splitlines()
    target = section.strip().lower()
    start: int | None = None
    level = 0

    for idx, line in enumerate(lines):
        match = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if not match:
            continue
        title = match.group(2).strip().lower()
        if title == target or target in title:
            start = idx
            level = len(match.group(1))
            break
    if start is None:
        return None

    end = len(lines)
    for idx in range(start + 1, len(lines)):
        match = re.match(r"^(#{1,6})\s+", lines[idx])
        if match and len(match.group(1)) <= level:
            end = idx
            break
    return "\n".join(lines[start:end]).strip()


def _xml_section(text: str, section: str) -> str | None:
    tag = section.strip().strip("<>/").split()[0]
    if not tag:
        return None
    match = re.search(
        rf"<{re.escape(tag)}(?:\s[^>]*)?>.*?</{re.escape(tag)}>",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )
    return match.group(0).strip() if match else None


def prompt_section(
    *,
    section: str,
    working_dir: str | Path = ".",
    prompt_text: str | None = None,
    prompt_path: str | Path | None = None,
) -> PromptSectionResult:
    artifact = load_prompt_artifact(
        working_dir=working_dir,
        prompt_text=prompt_text,
        prompt_path=prompt_path,
    )
    found = _xml_section(artifact.text, section) or _markdown_section(artifact.text, section)
    if found is None:
        return PromptSectionResult(source=artifact.source, section=section, found=False)
    return PromptSectionResult(
        source=artifact.source,
        section=section,
        found=True,
        text=found,
        sha256=hashlib.sha256(found.encode()).hexdigest(),
    )


def _redact_line(line: str) -> str:
    if _SECRET_RE.search(line):
        return _SECRET_RE.sub(r"\1=[redacted]", line)
    return line


def prompt_diff(
    *,
    baseline_path: str | Path,
    working_dir: str | Path = ".",
    prompt_text: str | None = None,
    prompt_path: str | Path | None = None,
    redacted: bool = True,
    max_lines: int = 200,
) -> PromptDiffResult:
    root = Path(working_dir).resolve()
    current = load_prompt_artifact(
        working_dir=root,
        prompt_text=prompt_text,
        prompt_path=prompt_path,
    )
    baseline_file = _resolve_under(root, baseline_path)
    baseline = PromptArtifact(
        source=baseline_file.relative_to(root).as_posix(),
        text=baseline_file.read_text(encoding="utf-8", errors="replace"),
    )

    current_lines = current.text.splitlines()
    baseline_lines = baseline.text.splitlines()
    if redacted:
        current_lines = [_redact_line(line) for line in current_lines]
        baseline_lines = [_redact_line(line) for line in baseline_lines]

    diff_lines = list(difflib.unified_diff(
        baseline_lines,
        current_lines,
        fromfile=f"a/{baseline.source}",
        tofile=f"b/{current.source}",
        lineterm="",
    ))
    truncated = len(diff_lines) > max_lines
    if truncated:
        diff_lines = diff_lines[:max_lines] + ["... [diff truncated]"]

    return PromptDiffResult(
        source=current.source,
        baseline_source=baseline.source,
        current_sha256=hashlib.sha256(current.text.encode()).hexdigest(),
        baseline_sha256=hashlib.sha256(baseline.text.encode()).hexdigest(),
        diff="\n".join(diff_lines) or "(no changes)",
        redacted=redacted,
        truncated=truncated,
    )


def prompt_propose(
    *,
    objective: str,
    working_dir: str | Path = ".",
    prompt_text: str | None = None,
    prompt_path: str | Path | None = None,
) -> PromptProposalResult:
    artifact = load_prompt_artifact(
        working_dir=working_dir,
        prompt_text=prompt_text,
        prompt_path=prompt_path,
    )
    digest = hashlib.sha256(artifact.text.encode()).hexdigest()

    recommended = [
        "Add or refresh a source-boundary section that says the prompt artifact "
        "must not expose hidden runtime prompts or private credentials.",
        "Add a verification section requiring prompt_hash and prompt_validate "
        "before deployment.",
        "Add a drift-control section requiring prompt_diff against the approved "
        "baseline before activation.",
        "Add a rollback section naming the prior prompt hash and restore path.",
    ]
    if objective.strip():
        recommended.insert(0, f"Address objective: {objective.strip()}")

    proposal_id = hashlib.sha256(f"{digest}\0{objective}".encode()).hexdigest()[:24]
    return PromptProposalResult(
        proposal_id=proposal_id,
        source=artifact.source,
        prompt_sha256=digest,
        objective=objective,
        recommended_changes=recommended,
        verification_criteria=[
            "New prompt hash is recorded in a manifest.",
            "prompt_validate passes against the intended manifest.",
            "prompt_diff is reviewed with redaction enabled.",
            "Human approval is recorded before deployment.",
        ],
        next_action="Review the proposal, edit the prompt artifact, then validate against manifest.",
    )
