"""Tier a3 — harvest feature: crawl directories, extract insights, build knowledge base."""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Sequence

from ass_ade.a0_qk_constants.assistant_types import (
    HARVEST_REPORT_FILENAME,
    DocumentMetadata,
    Insight,
    TaskItem,
)
from ass_ade.a1_at_functions.research_harvester import (
    _read_safe,
    deduplicate_insights,
    extract_insights,
    extract_tasks_from_text,
    make_document_metadata,
)
from ass_ade.a2_mo_composites.personal_assistant import PersonalAssistant

_DEFAULT_EXTENSIONS = (".md", ".txt", ".rst", ".py", ".ts", ".js", ".json", ".yaml", ".yml")
_SKIP_DIRS = frozenset({
    "__pycache__", ".git", "node_modules", ".venv", "venv", "dist",
    "build", ".mypy_cache", ".pytest_cache", ".ruff_cache",
})


class HarvestResult:
    def __init__(
        self,
        docs: list[DocumentMetadata],
        insights: list[Insight],
        tasks: list[TaskItem],
        duration_s: float,
    ) -> None:
        self.docs = docs
        self.insights = insights
        self.tasks = tasks
        self.duration_s = duration_s

    def to_dict(self) -> dict:
        return {
            "docs_found": len(self.docs),
            "insights_extracted": len(self.insights),
            "tasks_extracted": len(self.tasks),
            "duration_seconds": round(self.duration_s, 2),
            "docs": self.docs,
            "insights": self.insights,
            "tasks": self.tasks,
        }

    def summary_line(self) -> str:
        return (
            f"Harvested {len(self.docs)} docs · "
            f"{len(self.insights)} insights · "
            f"{len(self.tasks)} tasks  ({self.duration_s:.1f}s)"
        )


def harvest(
    paths: Sequence[str | Path],
    *,
    extensions: tuple[str, ...] = _DEFAULT_EXTENSIONS,
    max_files: int = 1000,
    save: bool = True,
    base_dir: Path | None = None,
) -> HarvestResult:
    """Crawl paths, extract insights and tasks, persist to the assistant store."""
    t0 = time.monotonic()
    assistant = PersonalAssistant(base_dir)

    all_docs: list[DocumentMetadata] = []
    all_insights: list[Insight] = []
    all_tasks: list[TaskItem] = []
    file_count = 0

    for raw_path in paths:
        root = Path(raw_path).expanduser().resolve()
        if not root.exists():
            continue
        iterator = root.rglob("*") if root.is_dir() else iter([root])
        for path in iterator:
            if file_count >= max_files:
                break
            if not path.is_file():
                continue
            if any(part in _SKIP_DIRS for part in path.parts):
                continue
            if path.suffix.lower() not in extensions:
                continue
            file_count += 1
            try:
                text = _read_safe(path)
                doc = make_document_metadata(path, text)
                all_docs.append(doc)
                insights = extract_insights(text, str(path))
                all_insights.extend(insights)
                tasks = extract_tasks_from_text(text, str(path))
                all_tasks.extend(tasks)
            except Exception:
                continue

    # Deduplicate
    all_insights = deduplicate_insights(all_insights)

    # Persist
    if save:
        existing_hashes = {i["hash"] for i in assistant.list_insights()}
        for ins in all_insights:
            if ins["hash"] not in existing_hashes:
                assistant._insights.append(ins)  # noqa: SLF001
        if all_insights:
            assistant._save_insights()  # noqa: SLF001

        existing_titles = {t["title"].lower() for t in assistant.list_tasks()}
        for task in all_tasks:
            if task["title"].lower() not in existing_titles:
                assistant._tasks.append(task)  # noqa: SLF001
                existing_titles.add(task["title"].lower())
        if all_tasks:
            assistant._save_tasks()  # noqa: SLF001

    duration = time.monotonic() - t0
    result = HarvestResult(all_docs, all_insights, all_tasks, duration)

    if save:
        report_path = assistant._base / HARVEST_REPORT_FILENAME  # noqa: SLF001
        report_path.write_text(json.dumps(result.to_dict(), indent=2), encoding="utf-8")

    return result
