"""
Tier a1 — pure inventory scanner for umbrella and sibling ASS-ADE repos.
"""
import os
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict

@dataclass
class Candidate:
    name: str
    path: str
    git_short: Optional[str]
    has_pyproject: bool
    tier_map_path: Optional[str]
    ass_ade_pattern: bool
    is_ephemeral: bool

def scan_umbrella(roots: List[str]) -> Dict[str, Any]:
    """
    Scan one or more umbrella directories for candidate repos.
    Args:
        roots: list of absolute paths to scan (e.g., ['C:/!atomadic'])
    Returns:
        dict with keys 'candidates', 'stats'
    """
    candidates = []
    for root in roots:
        root_path = Path(root)
        if not root_path.is_dir():
            continue
        for entry in root_path.iterdir():
            if entry.is_dir() and not entry.name.startswith('.'):
                cand = _fingerprint_dir(entry)
                candidates.append(asdict(cand))
    # compute stats
    stats = {
        "ass_ade_dir_count": sum(1 for c in candidates if c["ass_ade_pattern"]),
        "tier_map_count": sum(1 for c in candidates if c["tier_map_path"]),
        "ephemeral_count": sum(1 for c in candidates if c["is_ephemeral"]),
        "total_candidates": len(candidates)
    }
    return {"candidates": candidates, "stats": stats}

def _fingerprint_dir(dir_path: Path) -> Candidate:
    name = dir_path.name
    ass_ade_pattern = name.startswith("ass-ade")
    is_ephemeral = any(x in name.lower() for x in ["tmp", "test", "backup"])
    git_short = _get_git_short(dir_path)
    has_pyproject = (dir_path / "pyproject.toml").exists()
    tier_map = (dir_path / ".ass-ade" / "tier-map.json")
    tier_map_path = str(tier_map) if tier_map.exists() else None
    return Candidate(
        name=name,
        path=str(dir_path),
        git_short=git_short,
        has_pyproject=has_pyproject,
        tier_map_path=tier_map_path,
        ass_ade_pattern=ass_ade_pattern,
        is_ephemeral=is_ephemeral
    )

def _get_git_short(dir_path: Path) -> Optional[str]:
    try:
        head_file = dir_path / ".git" / "HEAD"
        if head_file.exists():
            ref = head_file.read_text().strip()
            if ref.startswith("ref:"):
                ref_path = dir_path / ".git" / ref[5:]
                if ref_path.exists():
                    return ref_path.read_text().strip()[:7]
            else:
                return ref[:7]
    except Exception:
        pass
    return None
