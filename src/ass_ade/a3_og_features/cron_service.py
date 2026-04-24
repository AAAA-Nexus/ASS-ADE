"""Tier a3 — cron scheduling service."""

from __future__ import annotations

from pathlib import Path

from ass_ade.a0_qk_constants.cron_types import CronJob, CronState
from ass_ade.a1_at_functions.cron_helpers import make_cron_job, validate_schedule
from ass_ade.a2_mo_composites.cron_store import CronStore


class CronService:
    def __init__(self, store_path: Path | None = None) -> None:
        self._store = CronStore(store_path)

    def add(self, name: str, schedule: str, command: str) -> CronJob:
        err = validate_schedule(schedule)
        if err:
            raise ValueError(f"Invalid schedule {schedule!r}: {err}")
        job = make_cron_job(name, schedule, command)
        self._store.upsert(job)
        return job

    def remove(self, job_id: str) -> None:
        job = self._resolve(job_id)
        self._store.delete(job["id"])

    def list_jobs(self, *, all_: bool = False) -> list[CronJob]:
        state = None if all_ else CronState.ENABLED
        return self._store.list_jobs(state)

    def enable(self, job_id: str) -> CronJob:
        job = self._resolve(job_id)
        self._store.set_state(job["id"], CronState.ENABLED)
        return self._store.get(job["id"])  # type: ignore[return-value]

    def disable(self, job_id: str) -> CronJob:
        job = self._resolve(job_id)
        self._store.set_state(job["id"], CronState.DISABLED)
        return self._store.get(job["id"])  # type: ignore[return-value]

    def run(self, job_id: str) -> tuple[int, str]:
        job = self._resolve(job_id)
        return self._store.run_job(job["id"])

    def _resolve(self, job_id: str) -> CronJob:
        """Support short-prefix lookup."""
        if len(job_id) < 36:
            matches = [j for j in self._store.list_jobs(None) if j["id"].startswith(job_id)]
            if len(matches) == 1:
                return matches[0]
            if len(matches) > 1:
                raise ValueError(f"Ambiguous prefix {job_id!r}: {len(matches)} matches")
            raise KeyError(f"Job not found: {job_id}")
        job = self._store.get(job_id)
        if job is None:
            raise KeyError(f"Job not found: {job_id}")
        return job
