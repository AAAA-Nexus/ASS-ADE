"""Tier a2 — stateful PersonalAssistant managing tasks, insights, and documents."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Sequence

from ass_ade.a0_qk_constants.assistant_types import (
    ASSISTANT_DIR,
    INSIGHTS_FILENAME,
    TASKS_FILENAME,
    DocumentMetadata,
    EmailSummary,
    Insight,
    TaskItem,
    TaskStatus,
)
from ass_ade.a1_at_functions.research_harvester import (
    deduplicate_insights,
    extract_insights,
    extract_tasks_from_text,
    make_document_metadata,
)


class PersonalAssistant:
    """Manages the local knowledge base: tasks, insights, and document metadata."""

    def __init__(self, base_dir: Path | None = None) -> None:
        self._base = Path.home() / ASSISTANT_DIR if base_dir is None else base_dir
        self._base.mkdir(parents=True, exist_ok=True)
        self._tasks_path = self._base / TASKS_FILENAME
        self._insights_path = self._base / INSIGHTS_FILENAME
        self._tasks: list[TaskItem] = []
        self._insights: list[Insight] = []
        self._load()

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------
    def _load(self) -> None:
        if self._tasks_path.exists():
            self._tasks = json.loads(self._tasks_path.read_text(encoding="utf-8")).get("tasks", [])
        if self._insights_path.exists():
            self._insights = json.loads(self._insights_path.read_text(encoding="utf-8")).get("insights", [])

    def _save_tasks(self) -> None:
        self._tasks_path.write_text(json.dumps({"tasks": self._tasks}, indent=2), encoding="utf-8")

    def _save_insights(self) -> None:
        self._insights_path.write_text(json.dumps({"insights": self._insights}, indent=2), encoding="utf-8")

    # ------------------------------------------------------------------
    # Tasks
    # ------------------------------------------------------------------
    def list_tasks(self, status: TaskStatus | None = None) -> list[TaskItem]:
        if status is None:
            return list(self._tasks)
        return [t for t in self._tasks if t["status"] == status.value]

    def add_task(self, task: TaskItem) -> None:
        self._tasks.append(task)
        self._save_tasks()

    def complete_task(self, task_id: str) -> bool:
        for t in self._tasks:
            if t["id"] == task_id or t["id"].startswith(task_id):
                t["status"] = TaskStatus.DONE.value
                self._save_tasks()
                return True
        return False

    def ingest_tasks_from_text(self, text: str, source: str) -> list[TaskItem]:
        new_tasks = extract_tasks_from_text(text, source)
        existing_titles = {t["title"].lower() for t in self._tasks}
        added = [t for t in new_tasks if t["title"].lower() not in existing_titles]
        self._tasks.extend(added)
        if added:
            self._save_tasks()
        return added

    # ------------------------------------------------------------------
    # Insights
    # ------------------------------------------------------------------
    def list_insights(self, tag: str | None = None) -> list[Insight]:
        if tag is None:
            return list(self._insights)
        return [i for i in self._insights if i["tag"] == tag]

    def ingest_insights_from_text(self, text: str, source: str) -> list[Insight]:
        new_insights = extract_insights(text, source)
        existing_hashes = {i["hash"] for i in self._insights}
        added = [i for i in new_insights if i["hash"] not in existing_hashes]
        self._insights.extend(added)
        if added:
            self._save_insights()
        return added

    def deduplicate(self) -> int:
        before = len(self._insights)
        self._insights = deduplicate_insights(self._insights)
        after = len(self._insights)
        if before != after:
            self._save_insights()
        return before - after

    # ------------------------------------------------------------------
    # Document indexing
    # ------------------------------------------------------------------
    def scan_directory(
        self,
        root: Path,
        extensions: tuple[str, ...] = (".md", ".txt", ".rst", ".py", ".ts"),
        max_files: int = 500,
    ) -> list[DocumentMetadata]:
        docs: list[DocumentMetadata] = []
        for i, path in enumerate(root.rglob("*")):
            if i >= max_files:
                break
            if path.is_file() and path.suffix.lower() in extensions:
                try:
                    docs.append(make_document_metadata(path))
                except Exception:
                    pass
        return docs

    # ------------------------------------------------------------------
    # Status snapshot
    # ------------------------------------------------------------------
    def status(self) -> dict:
        open_tasks = [t for t in self._tasks if t["status"] == TaskStatus.OPEN.value]
        return {
            "tasks_total": len(self._tasks),
            "tasks_open": len(open_tasks),
            "insights_total": len(self._insights),
            "base_dir": str(self._base),
        }
