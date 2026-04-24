"""Tier a1 — pure functions to extract and deduplicate insights from text sources."""

from __future__ import annotations

import hashlib
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Sequence

from ass_ade.a0_qk_constants.assistant_types import (
    DocumentMetadata,
    Insight,
    InsightTag,
    TaskItem,
    TaskStatus,
)

# ------------------------------------------------------------------
# Insight extraction patterns
# ------------------------------------------------------------------
_DECISION_RE = re.compile(
    r"(?:decided|decision|agreed|going with|chose|will use|we'll)\s+(.{10,120}?)(?:[.!]|$)",
    re.IGNORECASE,
)
_ACTION_RE = re.compile(
    r"(?:TODO|FIXME|ACTION|action item|next step|will do|I'll|we need to|must|should)\s*[:\-]?\s*(.{10,100}?)(?:[.!]|$)",
    re.IGNORECASE,
)
_QUESTION_RE = re.compile(
    r"(?:unclear|TBD|open question|needs clarification|why|how|what is)\s+(.{10,80}?)\?",
    re.IGNORECASE,
)
_IDEA_RE = re.compile(
    r"(?:idea:|could try|what if|consider|proposal|suggestion)\s+(.{10,100}?)(?:[.!]|$)",
    re.IGNORECASE,
)
_RISK_RE = re.compile(
    r"(?:risk|warning|danger|concern|issue|problem|bug|error|failure)\s*[:\-]?\s*(.{10,100}?)(?:[.!]|$)",
    re.IGNORECASE,
)

_PATTERN_MAP = [
    (_DECISION_RE, InsightTag.DECISION),
    (_ACTION_RE, InsightTag.ACTION),
    (_QUESTION_RE, InsightTag.QUESTION),
    (_IDEA_RE, InsightTag.IDEA),
    (_RISK_RE, InsightTag.RISK),
]


def _sha256_short(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:16]


def extract_insights(text: str, source: str, min_confidence: float = 0.4) -> list[Insight]:
    now = datetime.now(tz=timezone.utc).isoformat(timespec="seconds")
    results: list[Insight] = []
    seen_hashes: set[str] = set()
    for pattern, tag in _PATTERN_MAP:
        for m in pattern.finditer(text):
            snippet = m.group(1).strip().rstrip(".,;:")
            if len(snippet) < 10:
                continue
            h = _sha256_short(snippet.lower())
            if h in seen_hashes:
                continue
            seen_hashes.add(h)
            results.append(
                Insight(
                    id=str(uuid.uuid4()),
                    text=snippet,
                    tag=tag.value,
                    source=source,
                    confidence=0.7,
                    created_at=now,
                    hash=h,
                )
            )
    return results


def deduplicate_insights(insights: Sequence[Insight]) -> list[Insight]:
    """Remove duplicate insights by text hash, keeping the highest-confidence one."""
    best: dict[str, Insight] = {}
    for ins in insights:
        h = ins["hash"]
        if h not in best or ins["confidence"] > best[h]["confidence"]:
            best[h] = ins
    return list(best.values())


def extract_tasks_from_text(text: str, source: str) -> list[TaskItem]:
    """Pull TODO/FIXME/action items out of any text block."""
    now = datetime.now(tz=timezone.utc).isoformat(timespec="seconds")
    tasks: list[TaskItem] = []
    seen: set[str] = set()
    todo_re = re.compile(
        r"(?:^|\n)\s*[-*]?\s*(?:TODO|FIXME|HACK|NOTE|ACTION)\s*[:\-]?\s*(.{5,120}?)(?:\n|$)",
        re.IGNORECASE,
    )
    for m in todo_re.finditer(text):
        title = m.group(1).strip()
        low = title.lower()
        if low in seen or len(title) < 5:
            continue
        seen.add(low)
        tasks.append(
            TaskItem(
                id=str(uuid.uuid4()),
                title=title,
                source=source,
                status=TaskStatus.OPEN.value,
                priority="normal",
                due="",
                created_at=now,
                tags=[],
            )
        )
    return tasks


def classify_document(path: Path) -> str:
    """Return a simple doc_type label based on extension."""
    suffix = path.suffix.lower()
    return {
        ".md": "markdown",
        ".txt": "txt",
        ".pdf": "pdf",
        ".rst": "rst",
        ".py": "code",
        ".ts": "code",
        ".js": "code",
        ".rs": "code",
        ".go": "code",
        ".json": "json",
        ".yaml": "yaml",
        ".yml": "yaml",
        ".toml": "toml",
    }.get(suffix, "other")


def make_document_metadata(path: Path, text: str | None = None) -> DocumentMetadata:
    stat = path.stat()
    mod = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(timespec="seconds")
    body = text if text is not None else _read_safe(path)
    return DocumentMetadata(
        path=str(path),
        title=path.stem.replace("_", " ").replace("-", " ").title(),
        size_bytes=stat.st_size,
        modified=mod,
        doc_type=classify_document(path),
        summary=body[:500].replace("\n", " "),
        tags=[],
    )


def _read_safe(path: Path, max_bytes: int = 32_768) -> str:
    try:
        data = path.read_bytes()[:max_bytes]
        return data.decode("utf-8", errors="replace")
    except Exception:
        return ""
