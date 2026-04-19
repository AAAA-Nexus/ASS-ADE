# Extracted from C:/!ass-ade/src/ass_ade/prompt_toolkit.py:146
# Component id: at.source.ass_ade.prompt_validate
from __future__ import annotations

__version__ = "0.1.0"

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
