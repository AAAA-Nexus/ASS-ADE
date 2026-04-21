Improve ASS-ADE auto-evolve and MCP tooling so enhancement cycles only touch `src/ass_ade/**` and never
generated trees under `.ass-ade/builds/**` or `.ass-ade/selfbuild/**`. Add verification
that each evolution PR passes `pytest tests/` and `ass-ade doctor --no-remote` before
merge. Document the MAP=TERRAIN gate in CONTRIBUTING.md when behavior changes.
