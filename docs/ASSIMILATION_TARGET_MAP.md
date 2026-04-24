# Assimilation Target Map

ASS-ADE-SEED should grow by surveying sibling repos first, then deciding what
to assimilate, rebuild, enhance, or skip. The target map is the pre-flight
artifact for that flow.

## Command

```powershell
python -m ass_ade selfbuild target-map `
  --primary . `
  --sibling ..\!ass-ade-dev `
  --sibling ..\!aaaa-nexus-mcp `
  --out .ass-ade\target-map.json
```

Sibling discovery can also use a parent glob:

```powershell
python -m ass_ade selfbuild target-map `
  --primary . `
  --parent C:\!aaaa-nexus `
  --pattern "!ass-ade*" `
  --focus mcp `
  --out .ass-ade\target-map-mcp.json
```

## Actions

- `assimilate`: new, low-risk, documented or tested symbol. Candidate for a
  policy-scoped `ass-ade assimilate` run.
- `rebuild`: new symbol with risk, private shape, large body, risky imports, or
  missing nearby test evidence. Rebuild as a tier-safe component before taking it.
- `enhance`: primary already has a related symbol. Use the sibling as a source
  of tests, docs, alternate behavior, or hardening.
- `skip`: duplicate body already exists in primary. Keep it as provenance, but
  do not copy it again.

## Growth Loop

1. Run `selfbuild target-map` against selected siblings.
2. Review `rebuild` targets first; they need tier-safe reconstruction.
3. Feed approved `assimilate` and `enhance` candidates into policy-scoped
   `ass-ade assimilate` runs.
4. Keep `skip` records as evidence that the sibling was surveyed without blind
   duplication.
