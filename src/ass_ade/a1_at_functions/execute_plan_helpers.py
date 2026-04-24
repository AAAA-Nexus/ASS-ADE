"""Tier a1 — assimilated function 'execute_plan'

Assimilated from: rebuild/forge.py:743-801
"""

from __future__ import annotations


# --- assimilated symbol ---
def execute_plan(
    plan: EpiphanyPlan,
    model: str = _FORGE_MODEL,
    max_workers: int = _MAX_WORKERS,
) -> ForgeResult:
    """ForgeLoop — execute all tasks in the Epiphany plan using a thread pool.

    Tasks on the same file run sequentially (same-file serialization) to avoid
    line-number drift from concurrent writes. Tasks on different files run in
    parallel.
    """
    result = ForgeResult(plan_tasks=len(plan.experiments), model_used=model)

    # Build provider pool — one provider per available API key for true parallel
    provider_pool = _get_all_providers()
    n_providers = len(provider_pool)
    if n_providers > 1:
        log.info(
            "Forge multi-provider: %d providers available for %d file group(s)",
            n_providers, len({t.file for t in plan.experiments}),
        )

    # Group tasks by file to serialize per-file execution
    from collections import defaultdict
    by_file: dict[str, list[ForgeTask]] = defaultdict(list)
    for task in plan.experiments:
        by_file[task.file].append(task)

    def _run_file_tasks(tasks: list[ForgeTask], provider: Any) -> list[TaskResult]:
        # Module-level tasks (debug fix) must run FIRST since they rewrite the whole file
        ordered = sorted(tasks, key=lambda t: (0 if t.node_type == "module" else 1, t.start_line))
        return [_execute_task(t, model, provider=provider) for t in ordered]

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {
            pool.submit(_run_file_tasks, tasks, provider_pool[i % n_providers]): file
            for i, (file, tasks) in enumerate(by_file.items())
        }
        for future in as_completed(futures):
            file_path = futures[future]
            try:
                task_results = future.result()
            except Exception as exc:
                log.error("Forge task group failed for %s: %s", file_path, exc)
                continue
            for tr in task_results:
                result.results.append(tr)
                if tr.verified:
                    result.applied += 1
                    result.files_modified.add(tr.file)
                else:
                    result.skipped += 1
                    log.warning("Task %s skipped: %s", tr.task_id, tr.error)

    log.info(
        "Forge complete: %d/%d tasks applied, %d files modified",
        result.applied, result.plan_tasks, len(result.files_modified),
    )
    return result

