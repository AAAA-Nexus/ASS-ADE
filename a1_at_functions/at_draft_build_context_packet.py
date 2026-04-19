# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_build_context_packet.py:7
# Component id: at.source.a1_at_functions.build_context_packet
from __future__ import annotations

__version__ = "0.1.0"

def build_context_packet(
    *,
    task_description: str,
    working_dir: str | Path = ".",
    file_paths: list[str] | None = None,
    source_urls: list[str] | None = None,
    max_files: int = 12,
    max_bytes_per_file: int = 4000,
) -> ContextPacket:
    """Build a compact context packet from repo files and source URLs."""
    root = Path(working_dir).resolve()
    sources = [source for source in (source_urls or []) if source.strip()]
    recon = phase0_recon(
        task_description=task_description,
        working_dir=root,
        provided_sources=sources,
        max_relevant_files=max_files,
    )

    selected_paths = list(file_paths or recon.codebase.relevant_files)[:max_files]
    warnings: list[str] = list(recon.required_actions)
    files: list[ContextFile] = []

    for rel in selected_paths:
        try:
            path = _safe_file(root, rel)
            excerpt, truncated = _read_excerpt(path, max_bytes_per_file)
        except (OSError, ValueError) as exc:
            warnings.append(str(exc))
            continue

        raw = path.read_bytes()
        files.append(ContextFile(
            path=path.relative_to(root).as_posix(),
            sha256=hashlib.sha256(raw).hexdigest(),
            size_bytes=len(raw),
            excerpt=excerpt,
            truncated=truncated,
        ))

    return ContextPacket(
        task_description=task_description,
        recon_verdict=recon.verdict,
        source_urls=sources,
        files=files,
        warnings=warnings,
    )
