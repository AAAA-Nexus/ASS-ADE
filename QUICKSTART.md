# ASS-ADE Quickstart

Get from zero to a full codebase analysis and rebuild in under 5 minutes.

## Install

```bash
pip install -e .
```

Verify the CLI is available:

```bash
ass-ade --help
```

## Configure (optional)

Copy `.env.example` to `.env` and fill in at least one provider key.
ASS-ADE works out of the box with no keys (falls back to Pollinations AI),
but adding a key unlocks faster models and higher rate limits.

```bash
cp .env.example .env
# Edit .env — add e.g. GROQ_API_KEY=gsk_...
```

Check your toolchain and connectivity:

```bash
ass-ade doctor
```

## Recon — scan any codebase (no LLM, < 5 s)

```bash
ass-ade recon .
```

This runs 5 parallel agents locally and produces a structured report:
languages, test coverage, docstring coverage, tier purity, and
next-action recommendations.

## Rebuild — restructure into clean tiers

Single source:

```bash
ass-ade rebuild /path/to/your/project --output /path/to/output
```

Merge multiple sources into one unified output:

```bash
ass-ade rebuild /source-a /source-b /source-c --output /unified --yes
```

ASS-ADE analyzes the codebase and produces a folder partitioned into the
five composition tiers (`qk`, `at`, `mo`, `og`, `sy`). When merging
multiple sources, newer files win on symbol conflicts.

## Design — blueprint a new feature

```bash
ass-ade design "add OAuth2 login"
```

Produces a `blueprint_*.json` ready to feed into `rebuild`.

## Docs — generate documentation

```bash
ass-ade docs .
```

## Certify — run the full CIE pipeline

```bash
ass-ade certify .
```

Runs lint → type check → tests → produces a signed certificate JSON.

## Verify the install works end-to-end

```bash
# 1. Self-recon on the ass-ade repo
ass-ade recon .

# 2. Health check + remote probe
ass-ade doctor

# 3. Run the test suite
python -m pytest tests/ -q
```

All three should succeed with zero errors.

## No API keys?

ASS-ADE falls back to Pollinations AI (anonymous, no signup).
Most commands work. For higher throughput, add a free key from
Groq, Gemini, or any provider listed in `.env.example`.

Run `ass-ade providers list` to see which providers are active.
