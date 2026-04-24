"""Tier a2 — JSON-backed cron job store."""

from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from ass_ade.a0_qk_constants.cron_types import (
    CRON_DIR_NAME,
    CRON_STORE_FILENAME,
    CronJob,
    CronState,
)


def _default_store_path() -> Path:
    base = Path.home() / CRON_DIR_NAME
    base.mkdir(parents=True, exist_ok=True)
    return base / CRON_STORE_FILENAME


class CronStore:
    def __init__(self, store_path: Path | None = None) -> None:
        self._path = store_path or _default_store_path()
        self._jobs: dict[str, CronJob] = {}
        self._load()

    def _load(self) -> None:
        if self._path.exists():
            data = json.loads(self._path.read_text(encoding="utf-8"))
            self._jobs = {j["id"]: j for j in data.get("jobs", [])}

    def _save(self) -> None:
        self._path.write_text(
            json.dumps({"jobs": list(self._jobs.values())}, indent=2),
            encoding="utf-8",
        )

    def upsert(self, job: CronJob) -> None:
        self._jobs[job["id"]] = job
        self._save()

    def get(self, job_id: str) -> CronJob | None:
        return self._jobs.get(job_id)

    def list_jobs(self, state: CronState | None = None) -> list[CronJob]:
        jobs = list(self._jobs.values())
        if state is not None:
            jobs = [j for j in jobs if j["state"] == state.value]
        return jobs

    def set_state(self, job_id: str, state: CronState) -> None:
        if job_id in self._jobs:
            self._jobs[job_id]["state"] = state.value
            self._save()

    def delete(self, job_id: str) -> None:
        self._jobs.pop(job_id, None)
        self._save()

    def run_job(self, job_id: str) -> tuple[int, str]:
        """Execute the job's command and record the result. Returns (exit_code, output)."""
        job = self._jobs.get(job_id)
        if job is None:
            raise KeyError(f"Job not found: {job_id}")
        result = subprocess.run(
            job["command"],
            shell=True,
            capture_output=True,
            text=True,
            timeout=300,
        )
        now = datetime.now(tz=timezone.utc).isoformat(timespec="seconds")
        job["last_run"] = now
        job["last_exit"] = result.returncode
        job["run_count"] = job["run_count"] + 1
        self._save()
        output = result.stdout + result.stderr
        return result.returncode, output
