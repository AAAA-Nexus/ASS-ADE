# ASS-ADE — phased ship plan (spaghetti → shippable)

This is the **execution roadmap**: ordered work you can assign, schedule, and verify. It turns the technical truth in [`ASS_ADE_GOAL_PIPELINE.md`](ASS_ADE_GOAL_PIPELINE.md) into **week-sized phases** with **exit criteria**. The “cure” for spaghetti is **repeatable law** (CNA + monadic tiers + CI + one CLI), not a one-off rewrite.

**Companion docs:** [`docs/ATOMADIC_SWARM_SURFACE_AUDIT.md`](docs/ATOMADIC_SWARM_SURFACE_AUDIT.md) (Cursor / hooks / agents alignment), [`ASS_ADE_GOAL_PIPELINE.md`](ASS_ADE_GOAL_PIPELINE.md) (HAVE/GAP per track), [`docs/ASS_ADE_UNIFICATION.md`](docs/ASS_ADE_UNIFICATION.md), [`docs/ASS_ADE_SPINE_RFC.md`](docs/ASS_ADE_SPINE_RFC.md), [`ASS_ADE_MATRIX.md`](ASS_ADE_MATRIX.md).

**Current trunk decision (2026-04-23):** build and ship from `C:\!aaaa-nexus\!ass-ade` only. The product now vendors the restored engine at `atomadic-engine/src/ass_ade` beside the v1.1 spine at `ass-ade-v1.1/src/ass_ade_v11`. See [`docs/ONE_WORKING_PRODUCT.md`](docs/ONE_WORKING_PRODUCT.md).

---

## How to use this plan

1. **Do phases in order** unless explicitly marked “parallel.” Skipping phases creates fake progress (green demos, red production).
2. For each phase, tick **exit criteria** before starting the next. If an exit criterion fails, **stop** and file a gap in [`ASS_ADE_GOAL_PIPELINE.md`](ASS_ADE_GOAL_PIPELINE.md) under the right track.
3. **Default spine for new work:** ASS-ADE monadic spine; operator entry [`ass-ade`](ass-ade-v1.1/src/ass_ade_v11/a4_sy_orchestration/unified_cli.py). Runtime engine/studio work now lives inside this product trunk.

---

## Success definition (what “shippable” means)

| # | Criterion | Verifiable by |
|---|-----------|----------------|
| S1 | One documented **golden assimilate** (multi-root → monadic tree → tests pass) | CI job + README section |
| S2 | **Assimilation policy** exists as data (not prose only) and is enforced on multi-root runs | Failing CI when policy missing or violated |
| S3 | **No accidental edit** of ephemeral dirs (`pytest_tmp`, stale backups) | `.gitignore` / CONTRIBUTING + optional pre-commit |
| S4 | **Import law** holds on emitted + spine packages | `import-linter` (or equivalent) in CI |
| S5 | **Single install story** documented for your first external user | Fresh venv + copy-paste from README works |
| S6 | **Roadmap to one `pyproject`** is either done or time-boxed with next milestone | [`docs/ASS_ADE_UNIFICATION.md`](docs/ASS_ADE_UNIFICATION.md) updated |

“Cures future spaghetti” means **the same pipeline runs on the next messy repo** without inventing new steps—only tuning policy and fixtures.

### Atomadic workspace — evidence vs this table (2026-04)

Use this as a **MAP = TERRAIN** snapshot for the `!atomadic` umbrella; it does **not** replace ticking exit criteria when your fork differs.

| Criterion | In this workspace |
|-----------|---------------------|
| **S1** | **HAVE:** `.github/workflows/ass-ade-ship.yml` golden assimilate on `ass-ade-v1.1/tests/fixtures/minimal_pkg` (single-root); root `README.md` documents install + assimilate. **PARTIAL:** CI does not yet run a **public multi-root** trio with `--also` (covered in pytest / `-m usecase`, not the default CI assimilate step). |
| **S2** | **HAVE (CLI + schema):** `--policy` YAML + JSON Schema; fail-closed `--also` under `CI` / `ASS_ADE_ASSIMILATE_REQUIRE_POLICY`; `--plan-out` + book `ASSIMILATE_PLAN`. **PARTIAL:** Phase engines do not yet enforce every policy row beyond the CLI gate. |
| **S3** | **HAVE:** `CONTRIBUTING.md` hygiene; `.gitignore` patterns on subtrees. |
| **S4** | **HAVE:** `lint-imports` in `ass-ade-ship` workflow; contract in root `pyproject.toml`. |
| **S5** | **HAVE:** Root `README.md` + [`docs/ASS_ADE_UNIFICATION.md`](docs/ASS_ADE_UNIFICATION.md) copy-paste venv path. |
| **S6** | **HAVE:** One **`[project]`** for `ass-ade` at **repo root** `pyproject.toml`; `ass-ade-v1.1/pyproject.toml` is pointer-only. Legacy sibling distributions are donors/archives, not product roots. |

---


## Live terrain (auto-generated)

<!-- ASS_ADE_AUTOGEN:BEGIN -->
_Terrain refresh: **2026-04-22 22:51 UTC** — [`ASS_ADE_SUITE_SNAPSHOT.md`](ASS_ADE_SUITE_SNAPSHOT.md) has the full machine snapshot._

- **Repo root:** `C:/!atomadic`
- **Umbrella git (short):** `—`
- **`ass-ade*` dirs at root:** 8
- **`tier-map.json` files:** 11 (5 ephemeral / under tmp or backup paths)
- **Spine hint:** ass_ade_v11 under ass-ade-v1.1/src/ (T12 root pyproject)

**Subtrees (name → git short):**

- `ass-ade` → `1eca9b9`
- `ass-ade-v1` → `883a2dc`
- `ass-ade-v1-test` → `—`
- `ass-ade-v1-test-backup-20260421-134252` → `—`
- `ass-ade-v1-test-backup-20260421-155054` → `—`
- `ass-ade-v1-test-bridges` → `—`
- `ass-ade-v1-test-selfcheck` → `—`
- `ass-ade-v1.1` → `—`

**Other tier-mapped repo-root siblings:**
- `!atomadic-uep` → `b317051`

<!-- ASS_ADE_AUTOGEN:END -->

> **Public GitHub readers:** The **Live terrain** block above is machine-generated from the publisher’s workspace and may list absolute paths (`C:/!atomadic`, extra `ass-ade*` siblings) that **do not exist** in your clone. Use this document for **phases, exit criteria, and S1–S6**; ignore paths that are not in your checkout.

## Phase 0 — Terrain truth & noise control (3–7 days)

**Goal:** Everyone (human + agent) agrees **what exists**, **what is garbage**, and **what not to touch**.

### Actions (do all)

1. **Run terrain refresh** on every machine that matters:  
   `python scripts/regenerate_ass_ade_docs.py` (cross-platform; updates inventory, snapshot, and autogen blocks in matrix / ship / goal). Optionally also `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/inventory_ass_ade.ps1` for a **wider** Windows disk fingerprint.  
   Commit [`ASS_ADE_INVENTORY.md`](ASS_ADE_INVENTORY.md), [`ASS_ADE_SUITE_SNAPSHOT.md`](ASS_ADE_SUITE_SNAPSHOT.md), and related deltas when they reflect reality.
2. **Classify each `ass-ade*` row** in [`ASS_ADE_MATRIX.md`](ASS_ADE_MATRIX.md) as exactly one of: **spine**, **input**, **archive**, **delete candidate**, **ephemeral**. Put one sentence per row in a short table appendix or in matrix “Notes.”
3. **Hygiene rules** (pick one set and document in root `CONTRIBUTING.md` or [`AGENTS.md`](AGENTS.md)):  
   - Never commit under `ass-ade-v1/.pytest_tmp/`, `rebuild-outputs/` (unless golden fixtures).  
   - Dated `*-backup-*`: move to `archive/` or delete after N days—**write the rule**.
4. **Single “start here” path** for operators: ensure [`AGENTS.md`](AGENTS.md) + [`docs/ASS_ADE_UNIFICATION.md`](docs/ASS_ADE_UNIFICATION.md) list `ass-ade doctor` and `assimilate` first.

### Exit criteria

- [ ] Terrain refresh (`python scripts/regenerate_ass_ade_docs.py`) recorded (UTC in autogen blocks + snapshot) and paths triaged.  
- [ ] Matrix / notes show **no ambiguous “maybe product”** folders.  
- [ ] Written rule for temp/backup dirs exists and is linked from `AGENTS.md`.

### Anti-patterns

- Adding features before inventory is stable (you will automate the wrong tree).  
- “We’ll clean pytest_tmp later” with no rule—**later never ships**.

---

## Phase 1 — Golden assimilate path (1–2 weeks)

**Goal:** **One** end-to-end story: *N sibling Python repos → monadic emit → automated checks pass*, documented so a new engineer can repeat it.

### Actions

1. **Pick three real inputs:** one **primary** (MAP), two **siblings** (smaller). Prefer repos you can legally merge and that are mostly Python.
2. **Dry run book:**  
   `ass-ade assimilate <PRIMARY> <OUT> --also <A> --also <B> --stop-after gapfill`  
   Inspect JSON stdout; fix recon exclusions until `READY_FOR_PHASE_1`.
3. **Full emit:** same command **without** early stop (default `--stop-after package` or explicit `package`).
4. **Run tests on output:** at minimum `pytest` on generated package if present; use **`ass-ade book synth-tests --check --repo <path>`** where applicable ([`ASS_ADE_GOAL_PIPELINE.md`](ASS_ADE_GOAL_PIPELINE.md) S1).
5. **Document the exact commands** in [`docs/ASS_ADE_UNIFICATION.md`](docs/ASS_ADE_UNIFICATION.md) or a new `docs/tutorials/GOLDEN_ASSIMILATE.md` (recommended): prerequisites, Windows paths, failure modes, time expectations.
6. **Add CI job** (GitHub Actions or local harness) that runs **only** the golden fixture (small synthetic multi-root under `ass-ade-v1.1/tests/fixtures/` if real repos cannot be public). Job must fail if assimilate fails.

### Exit criteria

- [ ] **S1** satisfied: golden path in CI.  
- [ ] Tutorial doc exists; someone else can run it without asking you.  
- [ ] Known limitations listed honestly (e.g. “non-Python assets not merged”).

### Anti-patterns

- Only demoing on `minimal_pkg`—it proves wiring, not your real spaghetti.  
- Skipping CI because “too heavy”—then you don’t have a product, you have a demo.

---

## Phase 2 — Policy & plan artifacts (1–2 weeks, can overlap Phase 1 tail)

**Goal:** Multi-root runs produce **machine-readable decisions** humans can review in minutes, not hours.

### Actions

1. **Author `assimilate-policy.yaml`** (in-repo: `ass-ade-v1.1/.ass-ade/specs/` + JSON Schema `assimilate-policy.schema.json`; bundled copy under `ass_ade_v11/_bundled_ade_specs/`):  
   - Allowed/forbidden globs per root role.  
   - License class per root (compatible / incompatible).  
   - Max file size / binary handling rule.
2. **Wire policy load** in phase 0 or 1 ([`ASS_ADE_GOAL_PIPELINE.md`](ASS_ADE_GOAL_PIPELINE.md) P1): fail-closed when `--also` is used without policy in CI; warn-only locally if you must.
3. **Emit `ASSIMILATE_PLAN.json` + `.md`** after phase 1 or 2 (per goal pipeline B1/B2): include `namespace_conflicts`, primary, extras, and “recommended human actions.”
4. **Optional:** `--dry-run` flag on `assimilate` that maps to `--stop-after gapfill` and **does not** write past a staging prefix (document behavior; implement if cheap).

### Exit criteria

- [ ] **S2** satisfied for CI runs with `--also`.  
- [ ] At least one real multi-root run archived with plan artifact in repo or artifact store.

### Anti-patterns

- 40-page human policy nobody enforces—**YAML + CI** or it doesn’t exist.  
- Silent auto-merge of `LICENSE` / `NOTICE` files—**always** surface conflicts.

---

## Phase 3 — Regression grid & “spaghetti zoo” (2–3 weeks)

**Goal:** The pipeline **does not regress** when you change ingest or materialize; new messes become **new fixtures**, not emergencies.

### Actions

1. **Curate a fixture zoo** (small copies or submodules):  
   - cyclic imports,  
   - duplicate module names across siblings,  
   - legacy `src` layout vs flat layout,  
   - one “bad” repo that must **refuse** under policy.
2. **Matrix CI:** one job per fixture × `stop_after` ∈ {`gapfill`, `package`} where feasible; cap runtime with markers.
3. **Performance budget:** record wall time for each fixture on CI runner; fail if >2× baseline (catches accidental O(n²) scans).
4. **Update [`ASS_ADE_GOAL_PIPELINE.md`](ASS_ADE_GOAL_PIPELINE.md)** after each closed gap (keep it the living audit).

### Exit criteria

- [ ] ≥5 distinct fixtures, all green on main.  
- [ ] At least one **expected failure** test (policy or recon refuse).  
- [ ] **S4** on spine package in CI (`import-linter` or scripted import graph check).

### Anti-patterns

- Infinite fixtures—**cap** and rotate; prioritize shapes that burned you before.  
- Flaky CI “because Windows paths”—normalize on forward slashes in artifacts and tests.

---

## Phase 4 — Engine convergence (3–8 weeks, highest risk)

**Goal:** **One** authoritative emit path for “monadic product out of chaos,” with v1-only pieces **ported or wrapped**, not forked forever ([`ASS_ADE_GOAL_PIPELINE.md`](ASS_ADE_GOAL_PIPELINE.md) Track R vs B5).

### Actions

1. **Inventory emitter parity:** list outputs v1 `ass-ade rebuild` produces that v1.1 `materialize` does not (docs, bridges, coverage sidecars, etc.)—table in `docs/EMITTER_PARITY.md`.
2. **Per emitter, choose:** **port** into `ass_ade_v11` (preferred) vs **thin subprocess bridge** (time-boxed), with CNA rows in [`ass-ade-v1.1/.ass-ade/tier-map.json`](ass-ade-v1.1/.ass-ade/tier-map.json).
3. **Delete or archive** duplicate implementations once parity tests pass (same input → equivalent or better output per golden diff).
4. **Reduce `studio` dependency:** as parity rises, fewer reasons to install v1 side-by-side.

### Exit criteria

- [ ] Parity doc complete; **≥1** high-value emitter ported with tests.  
- [ ] Golden assimilate still green after each port (Phase 3 grid).

### Anti-patterns

- Rewriting everything before parity table exists—**you will miss invisible outputs**.  
- Keeping two silent forks “temporarily” for >1 release—**temporarily** is permanent.

---

## Phase 5 — Single package & CLI (4–12 weeks, calendar-driven)

**Goal:** **S6**—one distribution, one primary CLI, `import ass_ade` only—per [`docs/ASS_ADE_UNIFICATION.md`](docs/ASS_ADE_UNIFICATION.md).

### Actions

1. **Choose final PyPI name** (`ass-ade` vs bump) and **version policy** (semver; pre-1.0 if needed).  
2. **Mechanical rename plan:** `ass_ade_v11` → `ass_ade` (or keep package name but unify **distribution**—pick one; document tradeoffs).  
3. **Collapse console scripts:** keep `ass-ade` as the product CLI and `atomadic` as an alias; remove transitional scripts from the root distribution.  
4. **Merge optional deps** (x402, dev) from legacy [`ass-ade`](ass-ade) tree into unified `pyproject.toml` extras.  
5. **Migration guide** for early adopters (import paths, CLI flags).

### Exit criteria

- [ ] **S5** and **S6** satisfied: external user doc + single install.  
- [ ] Deprecation window announced for old entrypoints (if any remain).

### Anti-patterns

- Big-bang rename without a **compat** release—give users one migration release.  
- Renaming before Phase 4 parity—**you rename chaos**.

---

## Phase 6 — Ship, support, and “next spaghetti” (ongoing)

**Goal:** Product loop: releases, security, and **each new messy repo** is a **fixture + policy tweak**, not a new architecture.

### Actions

1. **Release checklist:** version bump, changelog, signed tags if you use them, smoke on clean VM/container.  
   Before any public push, run `ass-ade ade ship-audit --staging-root C:\!aaaa-nexus\!ass-ade` so the scrubbed checkout is clean, git-backed, and still mirrors the private ship surface.
2. **Security:** dependency audit on unified package; secrets policy for assimilate on private repos.  
3. **Support playbook:** “file an issue with `ASSIMILATE_PLAN.json` + policy file + versions.”  
4. **Quarterly:** rerun Phase 0 inventory; prune fixtures; re-read [`ASS_ADE_GOAL_PIPELINE.md`](ASS_ADE_GOAL_PIPELINE.md) and move GAP → HAVE.

### Exit criteria

- [ ] First public or private **release artifact** exists with the unified story.  
- [ ] Support template issue exists.  
- [ ] Recurring calendar reminder for inventory/tech-debt pass.

---

## Parallel tracks (optional staffing)

| Track | When | Notes |
|-------|------|--------|
| **Docs / tutorial** | Phase 1+ | Reduces repeat questions; ship with product. |
| **Nexus / trust hooks** | Phase 2+ | Optional; don’t block Phase 1 golden path on paid APIs. |
| **OpenClaw / OMC / Claw-Code** | After Phase 3 | Product-specific policies + legal review before assimilating. |

---

## Rough timeline (single strong engineer, order-of-magnitude)

| Phase | Duration | Cumulative |
|-------|----------|--------------|
| 0 | ~1 week | Week 1 |
| 1 | ~2 weeks | Week 3 |
| 2 | ~2 weeks | Week 5 |
| 3 | ~3 weeks | Week 8 |
| 4 | ~2 months | ~4 months |
| 5 | ~2–3 months | ~6–7 months |
| 6 | Ongoing | — |

Parallelizing Phase 2 with Phase 1 tail and Phase 3 design can pull **~2–4 weeks** out if staffing allows—**Phase 4 remains the long pole** until parity is honest.

---

## First 48 hours (if you want momentum Monday)

1. Run Phase 0 inventory + triage matrix rows (2–4 hours).  
2. Pick golden trio of repos; run `assimilate` to `gapfill`; save logs (2–4 hours).  
3. Open `docs/tutorials/GOLDEN_ASSIMILATE.md` with exact commands and failures (2 hours).  
4. Add one CI job running existing small fixture + `assimilate` gapfill (4–6 hours).

That alone converts “vision” into **proof the machine can be operated**.

---

*This plan is meant to be edited: dates, owners, and links can be appended per team. Keep it boring and checkable—that is how spaghetti dies.*
