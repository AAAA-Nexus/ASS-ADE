# Sample Task Manager Project

This is a minimal toy project used to demonstrate the ASS-ADE rebuild engine.

## What This Is

A simple task manager with 5 Python files totaling about 480 lines of code. It's intentionally small and simple so the rebuild output is easy to understand, but large enough to show real tier composition.

## What This Is Not

- Not production code
- Not a complete application
- Not meant to be run or used as a real task manager

## Project Structure

```
sample_project/
  README.md               (this file)
  constants.py            (qk_codex tier — data types)
  filters.py              (at_kernel tier — pure functions)
  validators.py           (at_kernel tier — pure functions)
  task_manager.py         (mo_engines tier — stateful class)
  task_reporter.py        (og_swarm tier — feature module)
```

## The Code

See `main.py` for a walkthrough of how the pieces fit together.

## How To Use This Example

1. From the parent directory, run the rebuild engine:

```bash
ass-ade rebuild sample_project/
```

2. Read the generated reports in `sample_project/.ass-ade/rebuild/`

3. Look at the structure and understand why code was placed in each tier

4. Try the validation command:

```bash
ass-ade rebuild --validate sample_project/.ass-ade/rebuild/<timestamp>
```

## The Five Tiers Explained

### qk_codex: Constants and Type Definitions

```python
# constants.py
from enum import Enum
from dataclasses import dataclass

class TaskStatus(Enum):
    TODO = "todo"
    DONE = "done"
    BLOCKED = "blocked"

@dataclass
class Task:
    id: str
    title: str
    status: TaskStatus
    priority: int
```

No logic. Just data structures that everything else depends on.

### at_kernel: Pure Functions

```python
# filters.py
def filter_tasks_by_priority(tasks, priority):
    """Pure function — no side effects."""
    return [t for t in tasks if t.priority >= priority]

# validators.py
def validate_task_name(name):
    """Pure function — no side effects."""
    return len(name) > 0 and len(name) <= 255
```

Logic with no state. These can be tested in isolation.

### mo_engines: Stateful Classes

```python
# task_manager.py
class TaskManager:
    def __init__(self):
        self.tasks = {}
    
    def add_task(self, task):
        """Manages state."""
        self.tasks[task.id] = task
```

Manages state. Depends on qk_codex and at_kernel.

### og_swarm: Feature Modules

```python
# task_reporter.py
class TaskReporter:
    def __init__(self, task_manager):
        self.manager = task_manager
    
    def report_completion_rate(self):
        """High-level feature."""
        return self.manager.completion_rate()
```

High-level features built from lower tiers.

### sy_manifold: Orchestration

Not represented in this sample (would be main.py in a real app).

This is where you'd have:

```python
# main.py
from task_manager import TaskManager
from task_reporter import TaskReporter

def main():
    manager = TaskManager()
    reporter = TaskReporter(manager)
    # ... orchestrate
```

## Rebuild Output

When you run `ass-ade rebuild sample_project/`, it will:

1. Read all Python files
2. Classify each into one of the 5 tiers
3. Verify that dependencies point downward (higher tiers can use lower)
4. Generate a report showing the structure
5. Produce a gap plan with recommendations

The resulting `REBUILD.md` will show:

```
## Tier Breakdown

### qk_codex (Constants & Types)
Files: 1
Examples: TaskStatus enum, Task dataclass

### at_kernel (Pure Functions)
Files: 2
Examples: filter_tasks_by_priority(), validate_task_name()

### mo_engines (Stateful Modules)
Files: 1
Examples: TaskManager class

### og_swarm (Feature Modules)
Files: 1
Examples: TaskReporter feature

### sy_manifold (Top-level Orchestration)
Files: 0
```

## Why This Structure Matters

1. **Testing**: at_kernel functions are easy to test (no setup needed)
2. **Reuse**: qk_codex types are used everywhere safely
3. **Refactoring**: Changes to mo_engines don't break og_swarm
4. **Onboarding**: New developers understand the dependency direction
5. **Maintenance**: Clear organization makes code easier to understand

## Next Steps

- Read `../README.md` to understand how to interpret the rebuild report
- Try rebuild on your own project
- Examine the gap plan for improvement recommendations
