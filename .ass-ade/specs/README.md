# `.ass-ade/specs` — contract artifacts (ship track)

| File | Purpose |
|------|--------|
| `assimilate-policy.schema.json` | JSON Schema for `assimilate-policy.yaml` (P1) — per [`ASS_ADE_GOAL_PIPELINE.md`](../../../ASS_ADE_GOAL_PIPELINE.md) |
| `assimilate-plan.schema.json` | Target shape for `ASSIMILATE_PLAN.json` — **emitted by `ass-ade-unified assimilate`** (validated; see `--plan-out`). |

**Note:** Code may not emit every `DEFER` field yet; schemas define the **agreed** contract for CI and docs.

**Runtime (S2):** `ass-ade-unified assimilate … --also …` requires `--policy PATH` when `CI=true` or `ASS_ADE_ASSIMILATE_REQUIRE_POLICY=1`; the file is YAML, structurally checked in-process, then validated against **`assimilate-policy.schema.json`** via **`jsonschema`** (draft 2020-12) when that schema file is readable. **Wheel installs:** canonical copies ship under `ass_ade_v11/_bundled_ade_specs/` (`pyproject.toml` `[tool.setuptools.package-data]`). **Repo checkout:** the same bytes are mirrored here under `.ass-ade/specs/` for human review; `pytest` asserts parity. **Custom installs:** if no schema file is found, `load_and_validate_assimilate_policy(..., skip_jsonschema=True)` skips JSON Schema (tests / exotic layouts).
