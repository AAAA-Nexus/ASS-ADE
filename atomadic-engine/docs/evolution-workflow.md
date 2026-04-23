# Split-Branch Evolution Workflow

This demo shows how ASS-ADE can evolve along several public-safe branches,
record evidence for each path, then merge the strongest line after review.

## Baseline

```bash
ass-ade doctor
python -m pytest tests/ -q --no-header
ass-ade protocol evolution-record baseline --summary "Baseline before branch evolution" --command "ass-ade doctor" --command "python -m pytest tests/ -q --no-header"
```

## Branch Tracks

### `evolve/tests-first`

```bash
git switch -c evolve/tests-first
ass-ade context pack "evolution tests-first iteration 1" --path . --json
ass-ade design "tests-first iteration 1: improve the strongest measured gap" --path . --local-only --out blueprints/tests-first-iteration-1.json
ass-ade enhance . --local-only --json --limit 10
ass-ade rebuild . --yes --git-track
python -m pytest tests/ -q --no-header
ass-ade protocol evolution-record iteration --summary "tests-first iteration 1" --version 0.0.1 --artifact blueprints/tests-first-iteration-1.json --command "ass-ade context pack" --command "ass-ade design" --command "ass-ade enhance" --command "ass-ade rebuild . --yes --git-track" --command "python -m pytest tests/ -q --no-header"
ass-ade context pack "evolution tests-first iteration 2" --path . --json
ass-ade design "tests-first iteration 2: improve the strongest measured gap" --path . --local-only --out blueprints/tests-first-iteration-2.json
ass-ade enhance . --local-only --json --limit 10
ass-ade rebuild . --yes --git-track
python -m pytest tests/ -q --no-header
ass-ade protocol evolution-record iteration --summary "tests-first iteration 2" --version 0.0.1 --artifact blueprints/tests-first-iteration-2.json --command "ass-ade context pack" --command "ass-ade design" --command "ass-ade enhance" --command "ass-ade rebuild . --yes --git-track" --command "python -m pytest tests/ -q --no-header"
ass-ade context pack "evolution tests-first iteration 3" --path . --json
ass-ade design "tests-first iteration 3: improve the strongest measured gap" --path . --local-only --out blueprints/tests-first-iteration-3.json
ass-ade enhance . --local-only --json --limit 10
ass-ade rebuild . --yes --git-track
python -m pytest tests/ -q --no-header
ass-ade protocol evolution-record iteration --summary "tests-first iteration 3" --version 0.0.1 --artifact blueprints/tests-first-iteration-3.json --command "ass-ade context pack" --command "ass-ade design" --command "ass-ade enhance" --command "ass-ade rebuild . --yes --git-track" --command "python -m pytest tests/ -q --no-header"
git switch -
```

### `evolve/docs-first`

```bash
git switch -c evolve/docs-first
ass-ade context pack "evolution docs-first iteration 1" --path . --json
ass-ade design "docs-first iteration 1: improve the strongest measured gap" --path . --local-only --out blueprints/docs-first-iteration-1.json
ass-ade enhance . --local-only --json --limit 10
ass-ade rebuild . --yes --git-track
python -m pytest tests/ -q --no-header
ass-ade protocol evolution-record iteration --summary "docs-first iteration 1" --version 0.0.1 --artifact blueprints/docs-first-iteration-1.json --command "ass-ade context pack" --command "ass-ade design" --command "ass-ade enhance" --command "ass-ade rebuild . --yes --git-track" --command "python -m pytest tests/ -q --no-header"
ass-ade context pack "evolution docs-first iteration 2" --path . --json
ass-ade design "docs-first iteration 2: improve the strongest measured gap" --path . --local-only --out blueprints/docs-first-iteration-2.json
ass-ade enhance . --local-only --json --limit 10
ass-ade rebuild . --yes --git-track
python -m pytest tests/ -q --no-header
ass-ade protocol evolution-record iteration --summary "docs-first iteration 2" --version 0.0.1 --artifact blueprints/docs-first-iteration-2.json --command "ass-ade context pack" --command "ass-ade design" --command "ass-ade enhance" --command "ass-ade rebuild . --yes --git-track" --command "python -m pytest tests/ -q --no-header"
ass-ade context pack "evolution docs-first iteration 3" --path . --json
ass-ade design "docs-first iteration 3: improve the strongest measured gap" --path . --local-only --out blueprints/docs-first-iteration-3.json
ass-ade enhance . --local-only --json --limit 10
ass-ade rebuild . --yes --git-track
python -m pytest tests/ -q --no-header
ass-ade protocol evolution-record iteration --summary "docs-first iteration 3" --version 0.0.1 --artifact blueprints/docs-first-iteration-3.json --command "ass-ade context pack" --command "ass-ade design" --command "ass-ade enhance" --command "ass-ade rebuild . --yes --git-track" --command "python -m pytest tests/ -q --no-header"
git switch -
```

### `evolve/safety-first`

```bash
git switch -c evolve/safety-first
ass-ade context pack "evolution safety-first iteration 1" --path . --json
ass-ade design "safety-first iteration 1: improve the strongest measured gap" --path . --local-only --out blueprints/safety-first-iteration-1.json
ass-ade enhance . --local-only --json --limit 10
ass-ade rebuild . --yes --git-track
python -m pytest tests/ -q --no-header
ass-ade protocol evolution-record iteration --summary "safety-first iteration 1" --version 0.0.1 --artifact blueprints/safety-first-iteration-1.json --command "ass-ade context pack" --command "ass-ade design" --command "ass-ade enhance" --command "ass-ade rebuild . --yes --git-track" --command "python -m pytest tests/ -q --no-header"
ass-ade context pack "evolution safety-first iteration 2" --path . --json
ass-ade design "safety-first iteration 2: improve the strongest measured gap" --path . --local-only --out blueprints/safety-first-iteration-2.json
ass-ade enhance . --local-only --json --limit 10
ass-ade rebuild . --yes --git-track
python -m pytest tests/ -q --no-header
ass-ade protocol evolution-record iteration --summary "safety-first iteration 2" --version 0.0.1 --artifact blueprints/safety-first-iteration-2.json --command "ass-ade context pack" --command "ass-ade design" --command "ass-ade enhance" --command "ass-ade rebuild . --yes --git-track" --command "python -m pytest tests/ -q --no-header"
ass-ade context pack "evolution safety-first iteration 3" --path . --json
ass-ade design "safety-first iteration 3: improve the strongest measured gap" --path . --local-only --out blueprints/safety-first-iteration-3.json
ass-ade enhance . --local-only --json --limit 10
ass-ade rebuild . --yes --git-track
python -m pytest tests/ -q --no-header
ass-ade protocol evolution-record iteration --summary "safety-first iteration 3" --version 0.0.1 --artifact blueprints/safety-first-iteration-3.json --command "ass-ade context pack" --command "ass-ade design" --command "ass-ade enhance" --command "ass-ade rebuild . --yes --git-track" --command "python -m pytest tests/ -q --no-header"
git switch -
```

## Compare And Merge

```bash
git log --oneline --graph --all --decorate
ass-ade protocol evolution-record merge-candidate --summary "Compare branch evidence"
git switch main
# Merge the branch with passing tests, fresh docs, and the strongest evidence ledger.
git merge --no-ff evolve/tests-first
python -m pytest tests/ -q --no-header
ass-ade protocol evolution-record merge --summary "Merged selected evolution branch" --command "git merge --no-ff <branch>" --command "python -m pytest tests/ -q --no-header"
```

## Merge Rule

A branch is merge-ready only when tests pass, public docs are current,
`EVOLUTION.md` has the event trail, and any release needs a fresh certificate.

## Version Rule

Use `ass-ade protocol version-bump patch|minor|major` after the winning path is merged.
The command updates package version surfaces and records the bump in the evolution ledger.
