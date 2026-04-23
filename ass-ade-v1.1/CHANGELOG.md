# Changelog

All notable changes to this project are documented in this file. The format is informal; version headings follow the distribution version in the **repository root** `pyproject.toml` (T12; sources under `ass-ade-v1.1/src/`).

## 1.1.0a1

- Monadic package `ass_ade_v11` (distribution `ass-ade-v1-1`): phased rebuild pipeline 0–7 (recon through package emit).
- Library entry `rebuild_project_v11`; unified runner `pipeline_book.run_book_until` with numeric stop-after.
- Typer CLI `ass-ade-v11` with `--stop-after` (`recon` … `package`); module entry `python -m ass_ade_v11.a4_sy_orchestration`.
- CI: import-linter gate, pytest on Ubuntu and Windows, CLI smoke.
- Self-dogfood (source = this repo, output = scratch): full pipeline completes with conformant sidecar audit; see plan `evolution.log` for recorded metrics.
