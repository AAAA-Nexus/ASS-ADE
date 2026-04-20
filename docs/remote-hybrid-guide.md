# Remote And Hybrid Guide

This guide explains when and how ASS-ADE should talk to
AAAA-Nexus, and what expectations are reasonable in the
public repo.

## Operating Rule

Local mode is the default.

Remote calls should happen only when one of these is true:

- you explicitly opt in with `--allow-remote`
- your config profile is `hybrid`
- your config profile is `premium`

That rule keeps the public shell safe and predictable.

## What Remote Mode Is For

Use remote mode when you want public contract-backed features such as:

- trust and hallucination checks
- security scans and certificates
- workflow pipelines that rely on AAAA-Nexus
- MCP manifest discovery and invocation
- A2A interoperability checks against live agent cards

Use local mode when you want:

- repo inspection
- planning
- local agent runs
- local file and shell tooling
- mock MCP development

## Configuring Hybrid Mode

Example `.ass-ade/config.json`:

```json
{
  "profile": "hybrid",
  "nexus_base_url": "https://atomadic.tech",
  "request_timeout_s": 20.0,
  "agent_id": "ass-ade-local",
  "agent_model": "gpt-4o"
}
```

Recommended environment variables:

```bash
set AAAA_NEXUS_API_KEY=your-key
set AAAA_NEXUS_BASE_URL=https://atomadic.tech
```

## Safe First Commands

Confirm the repo still treats remote use as opt-in:

```bash
ass-ade doctor --remote
```

Inspect public service health:

```bash
ass-ade nexus health --allow-remote
ass-ade nexus overview --allow-remote
```

Inspect public MCP contracts:

```bash
ass-ade mcp tools --allow-remote
ass-ade mcp estimate-cost 1 --allow-remote
ass-ade mcp invoke 1 --dry-run --allow-remote
```

Run a safe remote workflow:

```bash
ass-ade workflow trust-gate 13608 --allow-remote --json
ass-ade workflow certify "The answer is 42." --allow-remote --json
```

## Cost And Consent Expectations

The current public repo exposes a wide remote command
surface, but its billing UX is still lightweight.

Reasonable current practice:

- use dry-run and estimate commands before invoking billable tools
- prefer local mode for exploration
- prefer hybrid mode only for checks or workflows
  that clearly need remote contracts
- treat premium mode as a deliberate operational choice,
  not the default developer path

## Public Contract Principle

When a remote feature is valuable but strategically
sensitive, this repo should expose only:

- a typed client
- a contract consumer
- a degraded local fallback
- a certificate or attestation viewer

It should not recreate backend decision logic locally.

## Known Gaps In Hybrid Mode

- payment consent and budget controls are still thinner than they should be
- some advanced command families are still thin wrappers
  over evolving public endpoints
- durable cross-session memory is not yet integrated into the agent loop
- editor-native remote onboarding is not yet shipped

## What To Report As A User

If you find a remote command that feels unclear, the
most useful report includes:

- the command you ran
- whether the profile was local, hybrid, or premium
- whether `--allow-remote` was required
- whether the output was a contract mismatch,
  transport issue, or documentation issue

That distinction matters for public-repo triage.
