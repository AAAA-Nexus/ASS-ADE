# Email Sequences — ASS-ADE v0.0.1

---

## Sequence 1: Cold CTO Outreach

**Goal:** Get a 20-minute discovery call with a CTO/VP Eng at a 50-250 person engineering org
**Cadence:** Day 1 → Day 4 → Day 8 → Day 14

---

### Email 1 of 4 — Day 1 (Opening)

**Subject:** Your codebase and your architecture diagram — how far apart are they?

Hi [Name],

Most engineering teams I talk to have the same quiet problem: the architecture diagram describes what they *intended* to build, and the running system describes what they *actually* built. Six to eighteen months in, those two things diverge measurably.

The standard fix is architecture review meetings, style guides, and code review. Those help at the margins. They don't close the gap structurally.

I'm Thomas at Atomadic Tech. We just shipped ASS-ADE — a blueprint-driven synthesis engine that treats the gap as a tooling problem, not a process problem.

The short version: the blueprint is the canonical truth, the code is synthesized from it, and every build produces a cryptographic conformance certificate. You can measure architecture drift instead of guessing at it.

On launch day, the engine rebuilt its own 2,195-component codebase at 100% conformance in 75.7 seconds.

Would 20 minutes to walk through how this works be worth your time? I can show you a live synthesis run — not a demo environment.

Thomas
Atomadic Tech · atomadic.tech/ass-ade

---

### Email 2 of 4 — Day 4 (Follow-up with value)

**Subject:** RE: Your codebase and your architecture diagram

Hi [Name],

Following up briefly — wanted to share one specific detail that tends to resonate with CTOs.

For large, mature codebases — the ones with 10,000+ files, duplicated utilities, copy-pasted helpers, tangled dependencies — ASS-ADE's rebuild often *reduces* total component count. Duplicate functions collapse into single reusable components. Shared constants stop living in seventeen different files.

The maiden rebuild of our own codebase went from 95 source files to 2,195 independently versioned components — that's the decomposition effect on a small, clean project. On a large, messy codebase, the direction inverts: what was 10,000 files becomes 3,000 clean, tiered components.

The messier the input, the more dramatic the cleanup.

If that matches what you're dealing with, I think the 20 minutes would be worthwhile.

[Calendar link]

Thomas

---

### Email 3 of 4 — Day 8 (Social proof + specifics)

**Subject:** ASS-ADE — what the enterprise tier covers

Hi [Name],

One more note since you're evaluating enterprise tooling.

The enterprise tier ($499/month) covers three things that tend to matter at your scale:

**IP Guard** — blueprint artifacts, tier configurations, and LoRA adaptors are isolated per tenant. Your synthesis patterns stay yours. No cross-contamination between customer codebases.

**Split/merge evolution branches** — teams can explore divergent architectural directions, synthesize both, and merge the winning blueprint. Architectural experiments without forking the repository.

**Full audit trail** — every synthesis event is logged: what was built, what blueprint it came from, what conformance score it produced. You have a paper trail from design intent to running code.

All of this is available through the MCP integration in Claude Code and VS Code — so it fits into whatever AI-assisted workflow your team is already using.

Happy to talk through any of this. Still have time this week?

Thomas

---

### Email 4 of 4 — Day 14 (Breakup)

**Subject:** Closing the loop — ASS-ADE

Hi [Name],

I've reached out a few times and haven't heard back — that usually means timing or relevance is off.

I'll stop following up. If the architecture drift / synthesis quality problem becomes relevant later, ASS-ADE is at atomadic.tech/ass-ade and the source is on GitHub.

One thing worth knowing: the Blueprint Bundle is $19 one-time — it lets you run synthesis on your own blueprint before committing to a subscription. If you want to test the concept without a sales conversation, that's the path.

Best of luck with whatever you're shipping.

Thomas
Atomadic Tech

---

---

## Sequence 2: Developer Onboarding

**Goal:** Convert trial/install to active paid user over 7 days
**Trigger:** `pip install ass-ade` or GitHub star/clone

---

### Email 1 of 5 — Day 0 (Immediate install confirmation)

**Subject:** You just installed ASS-ADE — here's where to start

Welcome.

You've installed something different. Here's how to actually use it in the first 30 minutes:

**Step 1: Map your terrain**
```bash
ass-ade phase0-recon --path .
```
This surveys your current codebase and identifies decomposition candidates. Takes about 20 seconds.

**Step 2: Run a synthesis**
```bash
ass-ade synthesize --blueprint blueprint.toml
```
Generates your component manifest, runs synthesis, produces a conformance report.

**Step 3: Check your certificate**
```bash
ass-ade certify --verify
```
Every synthesis run produces a SHA-256 verified certificate. This is your proof of conformance.

If you get stuck: docs are at atomadic.tech/ass-ade. The GitHub repo has annotated examples.

One thing worth knowing: if you're on a small, clean codebase, synthesis will decompose it into more independently versioned components. On a large, messy codebase, it does the opposite — collapses duplicates, reduces total count. Either way, what you get is a properly tiered, fully certified output.

Reply to this if anything breaks. I read these.

Thomas
Atomadic Tech

---

### Email 2 of 5 — Day 2 (Depth: blueprints)

**Subject:** Blueprints — the part that changes how you think

Hi,

Two days in — wanted to go a level deeper on blueprints.

The blueprint isn't just a config file. It's the semantic description of what your codebase *is* — its tiers, its modules, their dependency contracts, their version constraints.

When the blueprint changes, you synthesize. When you synthesize, you get a MANIFEST (what was built), a CERTIFICATE (cryptographic proof), and a conformance score (how close the output is to the blueprint).

The part most people miss at first: **you can diff two blueprints**. If you made a change and want to understand the delta before synthesizing, blueprint diff shows you exactly what would change at the component level — before you build.

```bash
ass-ade blueprint diff v1.toml v2.toml
```

This makes blueprint changes reversible in a way code changes often aren't. You can inspect, back out, or branch.

Try it with a small evolution — add one module at a tier level and see what the diff looks like.

---

### Email 3 of 5 — Day 4 (Feature: MCP + IDE integration)

**Subject:** ASS-ADE in your editor (MCP setup takes 3 minutes)

Quick note on the IDE integration — this changes the workflow significantly.

ASS-ADE ships a full MCP server. If you're using Claude Code or VS Code with Cline, you can add it with:

```json
{
  "mcpServers": {
    "ass-ade": {
      "command": "python",
      "args": ["-m", "ass_ade.mcp_server"]
    }
  }
}
```

Once it's connected, you have synthesis capabilities as native chat tools:
- `map_terrain` — survey codebase structure
- `prompt_diff` — diff two blueprints or synthesis runs
- `phase0_recon` — run recon phase
- `trust_gate` — check trust score on a synthesis
- `certify_output` — get a certificate for a synthesis run

Working with blueprints in your editor instead of the terminal changes how fast you iterate. Worth the 3 minutes.

---

### Email 4 of 5 — Day 6 (Upgrade prompt)

**Subject:** What you get on Pro ($99/mo)

Quick breakdown of what the Pro tier adds:

**Pro ($99/month) vs Starter ($29/month):**
- Full LoRA flywheel — corrections you make get captured as training signals, synthesis improves over time
- Split/merge evolution branches — run parallel architectural experiments, merge the winner
- Expanded conformance history — longer synthesis audit trail
- Priority support

If you've been running synthesis daily, Pro pays back in synthesis quality improvements within a few weeks.

If you want to try blueprints standalone before subscribing, the Blueprint Bundle ($19 one-time) gives you the full blueprint toolkit without the synthesis subscription.

Upgrade or trial options at atomadic.tech/ass-ade/pricing.

---

### Email 5 of 5 — Day 7 (Community invitation)

**Subject:** The trust-gated community — you're eligible

One week in — you've done enough synthesis runs to qualify for the community tier.

What the community is:

A trust-gated space for sharing blueprints, evolution patterns, and synthesis strategies. Entry requires a verified reputation score based on actual synthesis history and contributions — not a payment or a badge.

Why the gate matters: blueprints are operational artifacts. A blueprint shared by a verified user with real synthesis history carries real signal. We're building a pool of high-quality blueprints, not a forum.

As an early member, you get:
- Founding cohort status
- Input into the blueprint repository structure
- Priority access to new synthesis capabilities
- Your synthesis history counts double toward reputation for the first 90 days

You can access the community portal at atomadic.tech/ass-ade/community.

---

---

## Sequence 3: Enterprise Nurture

**Goal:** Move an enterprise lead from awareness to evaluation call over 4 weeks
**Target:** Engineering Director, VP Eng, CTO at 200+ person org
**Trigger:** Downloaded whitepaper, Enterprise page visit, or inbound inquiry

---

### Email 1 of 4 — Day 0 (Welcome / positioning)

**Subject:** ASS-ADE for enterprise engineering teams

Hi [Name],

Thanks for your interest in ASS-ADE at the enterprise tier.

The short version of what we've built: a blueprint-driven synthesis engine that gives large engineering organizations a measurable, auditable bridge between architectural intent and running implementation.

Enterprise teams specifically get:
- IP Guard (tenant-isolated synthesis patterns — your blueprints never cross organizational boundaries)
- Full split/merge evolution branch support
- Complete audit trail from blueprint to every synthesized component
- Per-module semantic versioning across large, distributed codebases
- MCP integration for Claude Code and VS Code workflows

The reference data point: on v0.0.1 launch day, the engine rebuilt 2,195 components at 100% blueprint conformance in 75.7 seconds, SHA-256 verified.

I'd like to understand what you're currently working with — codebase scale, AI tooling in use, where architecture conformance is most painful.

Would a 30-minute discovery call work? I can also send a technical brief if you'd prefer to review before talking.

Thomas
Atomadic Tech · atomadic.tech/ass-ade

---

### Email 2 of 4 — Day 7 (IP Guard deep dive)

**Subject:** IP Guard — how synthesis isolation works at the enterprise tier

Hi [Name],

Following up with more detail on IP Guard, since this tends to be the first question from enterprise evaluators.

The concern is always the same: if we use an AI-assisted synthesis tool, does our proprietary code get used to improve the model for other customers?

IP Guard addresses this in three ways:

**Blueprint isolation** — your blueprint artifacts live in a tenant-isolated namespace. No blueprint content crosses organizational boundaries under any conditions.

**LoRA adaptor isolation** — the LoRA flywheel (which improves synthesis quality based on developer corrections) trains per-tenant. Your domain vocabulary, your patterns, your corrections — those improvements stay in your synthesis environment.

**Audit trail** — every synthesis event is logged with its input blueprint hash, output component hashes, and conformance score. You have a complete provenance record from design intent to running code.

The enterprise SLA covers access to these logs, tenant configuration audits, and priority support.

Happy to send the technical architecture document for IP Guard if your security team wants to review before the evaluation call.

Thomas

---

### Email 3 of 4 — Day 14 (ROI framing)

**Subject:** Quantifying the architecture drift cost

Hi [Name],

One more note before we talk, framed differently.

Architecture drift has a cost that's rarely measured directly. Here's a rough model:

- Engineering orgs typically spend 20-30% of senior engineer time on "archaeology" — understanding why code is the way it is before changing it
- Architectural misalignments generate roughly 2x the bug density of intentional design decisions
- Onboarding time to a drifted codebase is 40-60% longer than a coherent one

ASS-ADE makes conformance measurable. Once it's measurable, you can track it, gate on it, and improve it deliberately.

The blueprint is the contract. The conformance score is the measurement. The certificate is the audit artifact.

For a 50-engineer team, closing a 20% archaeology overhead pays the Enterprise plan back in hours per month.

If you want to run this calculation against your actual team size and current drift level, I can help with that on the discovery call.

[Calendar link]

Thomas

---

### Email 4 of 4 — Day 21 (Final decision prompt)

**Subject:** Two paths for evaluating ASS-ADE at [Company]

Hi [Name],

I want to make the evaluation decision easy.

**Path A: Live evaluation**
We run a synthesis against a non-production slice of your codebase. You see the conformance report, the MANIFEST, and the certificate. You get a read on what the rebuild quality looks like for your specific patterns. Takes about two hours of your team's time.

**Path B: Blueprint Bundle trial**
Your team works through the Blueprint Bundle ($19 one-time) independently. You evaluate the blueprint format, run synthesis against sample blueprints, and form a judgment before any larger commitment.

Either way, the goal is the same: you make a go/no-go decision based on evidence, not a vendor presentation.

Which path fits better for your evaluation process?

Thomas
Atomadic Tech · atomadic.tech/ass-ade

---
