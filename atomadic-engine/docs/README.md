# Docs Overview

This directory contains ASS-ADE documentation. For a public GitHub push, use
the public-safe set below as the release surface.

## Public Release Set

- [architecture.md](architecture.md): System design and public/private boundary.
- [user-guide.md](user-guide.md): Local setup and daily usage.
- [remote-hybrid-guide.md](remote-hybrid-guide.md): Explicit remote opt-in and
  AAAA-Nexus contract usage.
- [capability-matrix.md](capability-matrix.md): Feature matrix.
- [../capabilities/registry.json](../capabilities/registry.json): Capability
  source of truth for growth tracking.
- [protocol.md](protocol.md): Public enhancement protocol.
- [evolution-workflow.md](evolution-workflow.md): Split-branch evolution demo,
  merge rule, and version bump workflow.
- [dev-stack.md](dev-stack.md): Language and tooling rationale.
- [audit-report.md](audit-report.md): Code-verified audit findings.
- [gap-report.md](gap-report.md): Verified gaps.
- [implementation-status.md](implementation-status.md): Live and missing
  capability dashboard.
- [local-control.md](local-control.md): Local folder, output, split-evolution,
  and merge-sibling control contract.
- [local-control-status.md](local-control-status.md): Generated status from
  the local control JSON ledgers.
- [mermaid-diagrams.md](mermaid-diagrams.md): Generated Mermaid diagrams from
  the local control and capability ledgers.
- [roadmap.md](roadmap.md): Public roadmap.
- [stress-test-evolution-gain.md](stress-test-evolution-gain.md): Stress gate
  for proving evolutions gained capability.

## Release Rule

Before pushing docs publicly, run a boundary scan and either revise, withhold,
or move any draft that mentions private instruction bodies, private verification
material, non-public orchestration, internal milestone numbering, or unpublished
backend mechanics.

Recommended scan:

```bash
rg -n "internal-only|private instruction|verification material|non-public orchestration" README.md docs
```

See root [README.md](../README.md) for quickstart and release commands.
