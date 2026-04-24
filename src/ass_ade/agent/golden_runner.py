"""Golden task runner — deterministic surrogate for offline DGM-H simulation.

By design this does NOT call an LLM. It runs the golden task set through a
cheap synthetic-response scorer so the DGM-H / AlphaVerus plumbing can be
exercised in <1s. The SHAPE of the output matches what a real inference
layer would produce, so it can be swapped later.
"""
from __future__ import annotations

import hashlib
import json
import math
import random
from pathlib import Path
from typing import Any


def _load_tasks(task_path: Path, limit: int) -> list[dict[str, Any]]:
    tasks: list[dict[str, Any]] = []
    if not task_path.exists():
        return tasks
    with task_path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            try:
                tasks.append(json.loads(line))
            except json.JSONDecodeError:
                continue
            if len(tasks) >= limit:
                break
    return tasks


def _synthesize_response(task: dict[str, Any], prompt_suffix: str = "") -> str:
    """Deterministic synthetic response for offline DGM-H simulation."""
    kind = str(task.get("kind", ""))
    prompt = str(task.get("prompt", ""))
    expected = task.get("expected_contains") or []
    hint = " ".join(str(e) for e in expected)
    return f"[{kind}] synthetic-response for: {prompt} :: {hint} :: {prompt_suffix}"


def _score_task(
    task: dict[str, Any],
    rng: random.Random,
    prompt_suffix: str = "",
) -> dict[str, Any]:
    response = _synthesize_response(task, prompt_suffix)
    prompt = str(task.get("prompt", ""))
    combined = (prompt + " " + response).lower()
    expected = [str(x).lower() for x in (task.get("expected_contains") or [])]
    hits = sum(1 for sub in expected if sub in combined)
    base_pass = 1.0 if (expected and hits == len(expected)) else (hits / max(1, len(expected)))
    noise = rng.gauss(0.0, 0.05)
    passed = max(0.0, min(1.0, base_pass + noise)) >= 0.5
    tokens = len(prompt) + 200
    return {
        "id": task.get("id"),
        "kind": task.get("kind"),
        "pass": bool(passed),
        "tokens": tokens,
        "base_pass": base_pass,
        "noise": noise,
    }


def run_golden(
    task_path: Path,
    tasks_limit: int = 10,
    repeats: int = 10,
    *,
    prompt_suffix: str = "",
    seed: int | None = None,
) -> dict[str, Any]:
    """Run the golden task set and return per-task + aggregate metrics.

    Parameters
    ----------
    task_path : Path
        JSONL file with tasks ({id, kind, prompt, expected_contains}).
    tasks_limit : int
        Max tasks to load from the file.
    repeats : int
        Repeats per task; audit_pass is averaged across repeats.
    prompt_suffix : str
        Extra text appended to the synthetic response — lets the DGM-H
        "after" run measure prompt-level influence of a proposed patch.
    seed : int | None
        Deterministic seed. When None, noise is still injected but repeats
        differ; pass a stable seed for before/after reproducibility.
    """
    task_path = Path(task_path)
    tasks = _load_tasks(task_path, tasks_limit)
    if not tasks:
        return {
            "per_task": [],
            "aggregate": {"pass_rate": 0.0, "avg_tokens": 0.0, "task_count": 0, "repeats": repeats},
            "source": str(task_path),
            "empty": True,
        }

    rng_seed = seed
    if rng_seed is None:
        digest = hashlib.sha256((str(task_path) + prompt_suffix).encode("utf-8")).hexdigest()
        rng_seed = int(digest[:8], 16)
    rng = random.Random(rng_seed)

    per_task: list[dict[str, Any]] = []
    total_pass = 0
    total_runs = 0
    total_tokens = 0
    for task in tasks:
        passes = 0
        tokens_sum = 0
        for _ in range(repeats):
            scored = _score_task(task, rng, prompt_suffix=prompt_suffix)
            passes += 1 if scored["pass"] else 0
            tokens_sum += int(scored["tokens"])
            total_runs += 1
        pass_rate = passes / max(1, repeats)
        avg_tokens = tokens_sum / max(1, repeats)
        total_pass += passes
        total_tokens += tokens_sum
        per_task.append({
            "id": task.get("id"),
            "kind": task.get("kind"),
            "pass_rate": pass_rate,
            "avg_tokens": avg_tokens,
            "repeats": repeats,
        })

    aggregate_pass_rate = total_pass / max(1, total_runs)
    aggregate_tokens = total_tokens / max(1, total_runs)
    # Noise floor: stdev across per-task pass rates as a cheap σ estimate.
    if len(per_task) > 1:
        mean = sum(p["pass_rate"] for p in per_task) / len(per_task)
        var = sum((p["pass_rate"] - mean) ** 2 for p in per_task) / len(per_task)
        noise_sigma = math.sqrt(var)
    else:
        noise_sigma = 0.05
    return {
        "per_task": per_task,
        "aggregate": {
            "pass_rate": aggregate_pass_rate,
            "avg_tokens": aggregate_tokens,
            "task_count": len(tasks),
            "repeats": repeats,
            "noise_sigma": noise_sigma,
        },
        "source": str(task_path),
        "seed": rng_seed,
    }
