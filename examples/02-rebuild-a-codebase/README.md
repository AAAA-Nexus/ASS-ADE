# Example 2: Rebuild a Codebase

The rebuild engine transforms any codebase into a tier-partitioned modular structure. This example walks through the entire process, from initial analysis to reading the final report.

## What You'll Do

1. Run the rebuild engine on the sample project
2. Understand the five composition tiers
3. Read and interpret the rebuild report
4. Read the gap plan
5. Validate an existing rebuild folder

## Prerequisites

- Python 3.12+
- ASS-ADE installed: `pip install ass-ade`
- No remote calls required (local mode)

## Background: What Is Rebuild?

The rebuild engine reads your codebase and reorganizes it into five composition tiers:

| Tier | Name | Purpose |
|------|------|---------|
| 1 | **qk_codex** | Constants, enums, type aliases, and axioms — pure data, no logic |
| 2 | **at_kernel** | Pure functions and algorithms — deterministic, no side effects |
| 3 | **mo_engines** | Stateful compositions — classes, modules with managed state |
| 4 | **og_swarm** | Feature modules — high-level features built from molecules |
| 5 | **sy_manifold** | Top-level orchestration — main entry points, CLI, APIs |

This structure makes large codebases easier to reason about, test, and refactor.

## Step 1: Run Rebuild on the Sample Project

The sample project is in `sample_project/` — a toy task manager to demonstrate rebuild:

```bash
ass-ade rebuild sample_project/
```

Expected output (with elapsed time):

```
Reading codebase: sample_project/
Analyzing imports and dependencies...
Classifying code into 5 tiers...
Building tier relationships...
Validating structural invariants...
Generating rebuild output...

Rebuild complete in 2.34s

Output folder:  sample_project/.ass-ade/rebuild/2026-04-18T14-45-32Z
Report:         sample_project/.ass-ade/rebuild/2026-04-18T14-45-32Z/REBUILD.md
JSON report:    sample_project/.ass-ade/rebuild/2026-04-18T14-45-32Z/REBUILD.json
Certificate:    sample_project/.ass-ade/rebuild/2026-04-18T14-45-32Z/CERTIFICATE.json
Gap plan:       sample_project/.ass-ade/rebuild/2026-04-18T14-45-32Z/GAP_PLAN.md
Codex report:   sample_project/.ass-ade/rebuild/2026-04-18T14-45-32Z/CODEX_INVARIANTS.json
```

## Step 2: Read the Rebuild Report

Open the generated REBUILD.md:

```bash
cat sample_project/.ass-ade/rebuild/2026-04-18T14-45-32Z/REBUILD.md
```

Example output:

```markdown
# Rebuild Report

Project:        sample_project
Timestamp:      2026-04-18T14:45:32Z
Total files:    5
Total lines:    480
Build time:     2.34s

## Summary

Rebuilt 5 Python files into 5 composition tiers.

High-quality composition: code is well-organized across tiers
with clear dependency direction (lower tiers support higher tiers).

## Tier Breakdown

### qk_codex (Constants & Types)
Files: 1
Lines: 45
Examples: TaskStatus enum, TaskPriority enum, Task dataclass

### at_kernel (Pure Functions)
Files: 2
Lines: 180
Examples: filter_tasks_by_priority(), calculate_due_date(),
validate_task_name()

### mo_engines (Stateful Modules)
Files: 1
Lines: 120
Examples: TaskManager class with add_task(), complete_task()

### og_swarm (Feature Modules)
Files: 1
Lines: 95
Examples: TaskFilter feature, TaskReporter feature

### sy_manifold (Top-level Orchestration)
Files: 0
Lines: 0
Note: CLI orchestration is minimal in this sample

## Structure

```
qk_codex/
  constants.py

at_kernel/
  filters.py
  validators.py

mo_engines/
  task_manager.py

og_swarm/
  task_filter.py
  task_reporter.py

sy_manifold/
  (empty in sample)
```

## Invariant Validation

- Tier composition: valid (no lower tiers depend on higher tiers)
- Type consistency: valid (all imports are resolvable)
- Structural parity: valid (composition pattern is consistent)

## Recommendations

1. Move CLI code from og_swarm to sy_manifold when main() is added
2. Extract database logic into a separate mo_engines module
3. Add comprehensive docstrings to at_kernel functions
```

## Step 3: Read the JSON Report

The JSON report contains structured data for tool integration:

```bash
cat sample_project/.ass-ade/rebuild/2026-04-18T14-45-32Z/REBUILD.json
```

Example structure:

```json
{
  "project": "sample_project",
  "timestamp": "2026-04-18T14:45:32Z",
  "stats": {
    "total_files": 5,
    "total_lines": 480,
    "build_time_seconds": 2.34,
    "tiers": {
      "qk_codex": {
        "count": 1,
        "lines": 45
      },
      "at_kernel": {
        "count": 2,
        "lines": 180
      },
      "mo_engines": {
        "count": 1,
        "lines": 120
      },
      "og_swarm": {
        "count": 1,
        "lines": 95
      },
      "sy_manifold": {
        "count": 0,
        "lines": 0
      }
    }
  },
  "tiers": {
    "qk_codex": [
      {
        "file": "constants.py",
        "lines": 45,
        "exports": ["TaskStatus", "TaskPriority", "Task"],
        "dependencies": []
      }
    ],
    "at_kernel": [
      {
        "file": "filters.py",
        "lines": 90,
        "exports": ["filter_tasks_by_priority", "filter_tasks_by_due_date"],
        "dependencies": ["qk_codex"]
      }
    ]
  }
}
```

## Step 4: Read the Certificate

The certificate proves integrity of the rebuild:

```bash
cat sample_project/.ass-ade/rebuild/2026-04-18T14-45-32Z/CERTIFICATE.json
```

Example output:

```json
{
  "version": "1",
  "timestamp": "2026-04-18T14:45:32Z",
  "project": "sample_project",
  "rebuild_hash": "sha256:a7f3e9c2d5b8f1e4c6a9d2b7e1f4c9a8d5e2b7f1a4c9d6e3a0b5c8f1e4a7d",
  "codex_invariants_met": true,
  "structural_parity_valid": true,
  "tier_composition_valid": true,
  "file_count": 5,
  "line_count": 480,
  "verified_at": "2026-04-18T14:45:32Z"
}
```

The certificate allows you to verify later that the rebuild folder hasn't been tampered with:

```bash
ass-ade rebuild --validate sample_project/.ass-ade/rebuild/2026-04-18T14-45-32Z
```

Expected output:

```
Validating rebuild folder...
rebuild_hash:              valid (matches CERTIFICATE.json)
codex_invariants:          passed
tier_composition:          valid
File integrity:            verified

Rebuild is valid. No tampering detected.
```

## Step 5: Read the Gap Plan

The gap plan identifies improvement opportunities:

```bash
cat sample_project/.ass-ade/rebuild/2026-04-18T14-45-32Z/GAP_PLAN.md
```

Example output:

```markdown
# Gap Plan

Generated for: sample_project
Date: 2026-04-18T14:45:32Z

## Priority 1: Structure

- [ ] Create sy_manifold/main.py — currently no top-level orchestration
- [ ] Move database initialization to mo_engines
- [ ] Extract configuration to qk_codex

Effort: 2 hours
Impact: High (enables better testing and deployment)

## Priority 2: Documentation

- [ ] Add module docstrings to all qk_codex exports
- [ ] Document function signatures in at_kernel
- [ ] Add usage examples to og_swarm features

Effort: 3 hours
Impact: Medium (improves developer experience)

## Priority 3: Testing

- [ ] Unit tests for at_kernel pure functions (high ROI)
- [ ] Integration tests for mo_engines state management
- [ ] End-to-end tests for og_swarm features

Effort: 4 hours
Impact: High (reduces regression risk)

## Priority 4: Composition

- [ ] Consider extracting TaskReporter into a separate mo_engines module
- [ ] Consolidate filter logic into a single at_kernel module

Effort: 1 hour
Impact: Low (modest improvement to maintainability)
```

## Step 6: Validate the Rebuild Folder

After any changes to the code, validate the rebuild folder to ensure structural invariants are still met:

```bash
ass-ade rebuild --validate sample_project/.ass-ade/rebuild/2026-04-18T14-45-32Z
```

If the rebuild is still valid:

```
Validating rebuild folder...
rebuild_hash:              valid
codex_invariants:          passed
tier_composition:          valid
File integrity:            verified

Rebuild is valid.
```

If something changed, you'll see detailed errors:

```
Validating rebuild folder...
rebuild_hash:              MISMATCH (folder was modified after rebuild)

Error: Structural-parity invariant `AN-TH-STRUCT-PARITY` violated:
  File at_kernel/new_file.py imports from og_swarm
  This creates a circular dependency

Recommendation: Run rebuild again to generate an updated report
```

## Understanding the Sample Project

The sample project (`sample_project/`) is a minimal task manager demonstrating:

- **qk_codex**: Data types (Task, TaskStatus, TaskPriority)
- **at_kernel**: Pure helper functions (filter, validate, calculate)
- **mo_engines**: Stateful TaskManager class
- **og_swarm**: Feature modules (TaskFilter, TaskReporter)

It's not a real production system — just enough code to show how rebuild works.

To see the actual code:

```bash
cat sample_project/main.py
```

This shows real rebuild output on small, understandable code.

## Common Patterns

### Reading a rebuild report for a real project

1. Start with the Summary section — what's the overall health?
2. Look at Tier Breakdown — is code distributed reasonably?
3. Check Recommendations — what's the most impactful next step?
4. Review Gap Plan Priority 1 — start there

### When to rebuild

- After major refactoring
- Before a large architectural change (to understand current state)
- When onboarding new developers (to explain the structure)
- When code quality seems to be declining

### When to validate

- After editing files directly (instead of using rebuilds)
- Before committing architectural changes
- As part of your CI/CD pipeline to enforce structure

## Verification

Rebuild the sample project again and verify the hash matches:

```bash
ass-ade rebuild sample_project/
cat sample_project/.ass-ade/rebuild/2026-04-18T14-45-32Z/CERTIFICATE.json | grep rebuild_hash
```

Then validate it:

```bash
ass-ade rebuild --validate sample_project/.ass-ade/rebuild/2026-04-18T14-45-32Z
```

Expected output:

```
Validating rebuild folder...
rebuild_hash:              valid
codex_invariants:          passed
tier_composition:          valid
File integrity:            verified

Rebuild is valid. No tampering detected.
```

## Next Steps

1. Try rebuild on your own codebase:

```bash
ass-ade rebuild /path/to/your/project
```

2. Read the gap plan and prioritize improvements
3. Use the tier structure to guide refactoring
4. Set up validation in your CI pipeline

## Resources

- [../docs/architecture.md](../../docs/architecture.md) — Architecture details
- [../README.md](../../README.md) — Rebuild engine overview
- `ass-ade rebuild --help` — Command reference
