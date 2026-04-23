# ASS-ADE v1.1 — agent pointers

This folder holds **v1.1-specific** prompt forks. Canonical Atomadic protocol and the full prompt library live next to the monorepo workspace root when present:

- `../../agents/_PROTOCOL.md` — gate discipline, §11 Nexus, gaps-not-stubs.
- `../../agents/INDEX.md` — numbered builder prompts (00–24).
- `../../agents/ASS_ADE_MONADIC_CODING.md` — tier layout for legacy `ass_ade` packages (v1.1 uses `ass_ade_v11` and `ass-ade-v1.1/.ass-ade/tier-map.json`).

Rebuild orchestration for **this** repo:

- **CLI:** `ass-ade-v11 rebuild <SOURCE> -o <OUTPUT_PARENT> [--stop-after recon|ingest|gapfill|enrich|validate|materialize|audit|package]`
- **Python:** `from ass_ade_v11.a4_sy_orchestration import rebuild_project_v11`

Synthesis / forge parity with legacy `ass-ade-v1` `selfbuild` is intentionally not bundled; file a gap or use env-gated Nexus flows per protocol.
