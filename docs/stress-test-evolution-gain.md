# Stress Testing Evolution Gain

An evolution is only useful if it increases measurable capability without
breaking the baseline. Rebuilds that only change component counts, generated
names, or docs noise are not feature gains by themselves.

## What Counts As Gain

The stress gate records these growth signals:

- new capability IDs in `capabilities/registry.json`
- capability status improvement, such as `missing` to `partial`
- new CLI commands
- new public Python API symbols
- new tests or increased pytest collection count
- increased rebuild component count when paired with evidence

The gate treats these as severe regressions:

- removed capability IDs
- downgraded capability statuses
- removed CLI commands
- removed public Python API symbols
- lower pytest collection count when collection is enabled
- unsynced version surfaces

## Baseline Command

```powershell
python scripts\ass_ade_local_control.py snapshot C:\!aaaa-nexus\ass-ade-github-latest `
  --collect-pytest `
  --out C:\!aaaa-nexus\!ass-ade-control\outputs\stress\baseline-main.json
```

## Candidate Command

```powershell
python scripts\ass_ade_local_control.py stress-gain `
  C:\!aaaa-nexus\ass-ade-github-latest `
  C:\!aaaa-nexus\!ass-ade-control\evo\worktrees\wt_20260420_memory_durable-store_6499a168 `
  --collect-pytest `
  --out C:\!aaaa-nexus\!ass-ade-control\outputs\stress\memory-durable-store-gain.json
```

## Diff The Reports

When a candidate has more than one run, compare stress reports directly:

```powershell
python scripts\ass_ade_local_control.py diff-json `
  C:\!aaaa-nexus\!ass-ade-control\outputs\stress\candidate-before.json `
  C:\!aaaa-nexus\!ass-ade-control\outputs\stress\candidate-after.json
```

For feature snapshots, this uses the same gain/regression logic as the merge
gate. For other JSON files, it emits a bounded structural diff.

## Reading The Report

`passed: true` means the candidate gained at least one measurable signal and did
not hit a severe regression.

`passed: false` means either:

- it did not gain a measurable capability, or
- it regressed an existing capability, command, API, test count, or version
  surface.

The report is intentionally strict. It is a merge gate, not a celebration meter.

## Human Review Still Matters

The stress gate can prove that something measurable changed. It cannot prove
that the change is strategically good. A merge reviewer still decides whether
the gain belongs in the product.
