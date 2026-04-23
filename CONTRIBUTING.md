# Contributing — Atomadic workspace hygiene

**IP wall:** **`C:\!atomadic`** is **private** development — IP-sensitive; **do not `git push` it to public GitHub.** **`C:\!aaaa-nexus`** holds **public**-intent material. When ASS-ADE is production-ready, **move** it into `!aaaa-nexus` (scrubbed export per Stream B), then **push to GitHub from `!aaaa-nexus` only** (see `ass-ade/README.md` §IP rules, `LICENSE`, root `README.md`).

This tree mixes multiple products. For **ASS-ADE** ship hygiene (`ASS_ADE_SHIP_PLAN.md` Phase 0):

- Do **not** commit under `ass-ade-v1/.pytest_tmp/`, `ass-ade-v1/.claude/worktrees/` scratch outputs, or other engine temp dirs unless they are **checked-in golden fixtures**.
- Dated `*-backup-*` trees: move under an `archive/` path or delete after you have a recorded decision (link the PR or plan note).
- Install the monadic spine from the **repository root**: `pip install -e ".[dev]"` (see root `pyproject.toml`).

CI for the spine lives in `.github/workflows/ass-ade-ship.yml`.
