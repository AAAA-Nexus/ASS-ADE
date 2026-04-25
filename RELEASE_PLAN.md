# ASS-ADE v1.0.0 — Release Plan

**Generated:** 2026-04-24 | **Status:** Actionable Playbook
**Owner:** Thomas Colvin | **Engine:** Atomadic Research Center

---

## 1. Release Readiness Checklist

### DONE (ship-ready)

| Item | Evidence | Owner |
|------|----------|-------|
| Seed codebase: 922 files, 374 Python modules | Local, verified | Thomas |
| 1,511 tests, 0 failures | pytest pass, all green | Thomas |
| 68 CLI commands functional | `ass-ade --help` verified | Thomas |
| pyproject.toml v1.0.0 pinned, Python >=3.12 | `pyproject.toml` line 27 | Thomas |
| BSL 1.1 license file present | `LICENSE` in seed root | Thomas |
| Monadic tier enforcement via import-linter | 6-layer contract in pyproject.toml | Auto |
| CLAW demo completed: 13,286 files -> 92,305 components, 24 min | WITNESS.md, CERTIFICATE.json | Thomas |
| Press kit: Twitter x3, LinkedIn, HN, Reddit, Product Hunt copy | PRESS_KIT.md, SOCIAL_POSTS.md | Thomas |
| Release masterplan: 8 epiphanies, pricing, GTM, moat analysis | ASS_ADE_RELEASE_MASTERPLAN.md | Thomas |
| Inference live at atomadic.tech with HELIX anti-hallucination | Running | Thomas |
| Pricing set: $29 / $99 / $499 + per-call metering | Masterplan section 7 | Thomas |
| Forge bridge (fractal subagents) built | In seed, a3 layer | Claude |
| Wiring agent (AST-level import rewiring) built | In seed, a2 layer | Claude |
| Three evolution lanes (conservative/exploratory/adversarial) | Committed locally, not pushed | Claude |
| CI config (GitHub Actions) referenced in README | Needs verification on push | Thomas |

### BLOCKING (must fix before Day 1)

| Item | Description | Owner | Est. Time |
|------|-------------|-------|-----------|
| Push seed to GitHub | `AAAA-Nexus/ASS-ADE` repo exists but is empty. Push the 922-file seed. | Thomas | 30 min |
| PyPI test publish | Run `python -m build && twine upload --repository testpypi dist/*` to verify the package installs cleanly from TestPyPI. Fix any missing data files or broken entry points. | Thomas | 1 hr |
| README overhaul | Current README is a stub with class/function lists. Replace with: one-liner, install, quickstart (3 commands), CLAW demo stats, architecture diagram (ASCII), link to docs. | Claude | 2 hr |
| LICENSE file audit | DONE: BSL 1.1 in repo root, Change Date 2029-04-23, Change License GPL-2.0-or-later. | Thomas | DONE |
| CI green on GitHub | Push triggers GitHub Actions. Ensure the workflow runs pytest, ruff, import-linter. First run must pass publicly. | Thomas | 1 hr |
| Recon depth bug | Known: recon phase sometimes under-counts nested directories. Write a regression test and fix. | Claude | 2 hr |
| Eco-scan coverage misreport | Known: coverage report double-counts some modules. Fix the coverage config or filter. | Claude | 1 hr |
| Smoke test on clean venv | `pip install .` from a fresh Python 3.12 venv must succeed. All 68 CLI commands must respond to `--help`. | Thomas | 30 min |

### NICE-TO-HAVE (Week 1, not blocking launch)

| Item | Owner | Est. Time |
|------|-------|-----------|
| CHANGELOG.md (v1.0.0 entry) | Claude | 1 hr |
| CONTRIBUTING.md (BSL contribution terms) | Claude | 1 hr |
| Architecture diagram (SVG, for README and docs site) | Claude | 2 hr |
| `ass-ade demo` command that runs a mini CLAW on a bundled sample repo | Claude | 4 hr |
| Tauri + AG-UI dashboard scaffold pushed to separate repo | Thomas | 2 hr |
| Docs site on atomadic.tech/docs (MkDocs or similar) | Thomas | 4 hr |
| Video: 2-min terminal recording of CLAW rebuild | Thomas | 2 hr |

---

## 2. Day 1 Launch Plan

**Target date:** As soon as all BLOCKING items are green. Realistically: April 26-27, 2026 (Saturday/Sunday).

Weekend launch is intentional: HN and Reddit engagement peaks on weekends for Show HN / r/programming.

### Hour-by-hour

| Time | Action | Owner | Notes |
|------|--------|-------|-------|
| T-2h | Final `pytest` + `ruff` + `import-linter` pass locally | Thomas | All green or no-go |
| T-1h | `git push origin main` -- seed goes public | Thomas | 922 files land on GitHub |
| T-45m | Verify GitHub Actions CI passes on push | Thomas | Watch the run; fix if red |
| T-30m | `python -m build && twine upload dist/*` to real PyPI | Thomas | `pip install ass-ade` goes live |
| T-15m | Verify `pip install ass-ade && ass-ade --help` works from PyPI | Thomas | Test from a fresh venv on a different machine if possible |
| T-0 | Post Twitter/X Post 1 (stats-only, curiosity hook) | Thomas | From SOCIAL_POSTS.md |
| T+5m | Submit Show HN post | Thomas | From PRESS_KIT.md HN section |
| T+10m | Submit r/programming post | Thomas | From PRESS_KIT.md Reddit section |
| T+15m | Post LinkedIn article | Thomas | From SOCIAL_POSTS.md |
| T+30m | Monitor HN, Reddit, Twitter for questions. Respond to every comment within 2 hours. | Thomas | This is the make-or-break window |
| T+2h | Post Twitter/X Post 2 (positioning angle) | Thomas | Space the posts out |
| T+4h | Post Twitter/X Post 3 (raw numbers) | Thomas | |
| T+6h | Cross-post to dev.to (longer-form version of HN post) | Thomas | |
| T+12h | Review all feedback. Note top 3 feature requests. | Thomas | Feed into Week 1 sprint |
| T+24h | Submit to Product Hunt (schedule for next weekday morning PST) | Thomas | From PRESS_KIT.md PH section |

---

## 3. Week 1 Enhancement Sprint

Priority-ranked. Each item directly addresses a launch concern or user request.

### Sprint 1: Post-Launch (Days 2-7)

| # | Item | Why | Owner | Est. |
|---|------|-----|-------|------|
| 1 | **`ass-ade demo` command** | HN/Reddit users will want to try it immediately on something. Bundle a small sample repo so `ass-ade demo` gives instant gratification in <60 seconds. | Claude | 4 hr |
| 2 | **Docs site v1** | Traffic from HN/Reddit needs somewhere to land beyond the README. Deploy MkDocs at atomadic.tech/docs with: install, quickstart, CLI reference (auto-generated from the 68 commands), architecture explainer, CLAW case study. | Thomas + Claude | 8 hr |
| 3 | **Fix top 3 issues from launch feedback** | Whatever breaks for real users in the first 48 hours. Reserve capacity. | Thomas + Claude | 6 hr |
| 4 | **Architecture Score Badge** | Let users add a shield.io-style badge to their repo READMEs showing monadic purity score. Viral loop: every badge is a link back to ASS-ADE. | Claude | 3 hr |
| 5 | **Stripe integration for Starter tier** | Enable $29/mo signups at atomadic.tech. Even if only 5 people sign up in Week 1, it proves the revenue model works. | Thomas | 4 hr |

---

## 4. Revenue Activation

**Goal:** First paying customer within 48 hours of launch.

### Strategy: "Founder's Circle" pre-launch DM campaign

| Step | Action | Owner | Timing |
|------|--------|-------|--------|
| 1 | Identify 20 developers Thomas already knows or has interacted with who maintain Python repos with >1K stars. | Thomas | Before launch |
| 2 | DM each one personally: "I'm launching ASS-ADE tomorrow. I'd love for you to be one of the first 10 paying users. Founder's Circle: $29/mo Starter, but I'll personally run a CLAW-scale rebuild on your repo and walk you through the results. Interested?" | Thomas | T-12h |
| 3 | For anyone who says yes, run `ass-ade rebuild` on their repo and send them the WITNESS report + certificate. | Thomas | T+0 to T+24h |
| 4 | When they see their own repo rebuilt, send the Stripe payment link. | Thomas | T+24h |

### Backup: Community-driven conversion

| Trigger | Action |
|---------|--------|
| Someone comments "this is amazing" on HN/Reddit | Reply: "Want me to run it on your repo? DM me." Then deliver a rebuild + payment link. |
| Someone opens a GitHub issue asking for a feature | Reply with the feature's tier (Starter/Pro/Enterprise) and a link to sign up. |
| 48 hours pass with 0 paying customers | Post a "Launch Week Special: first 50 Starter users get 3 months for $19/mo" offer on Twitter. |

### Stripe setup checklist (do before launch)

| Item | Owner |
|------|-------|
| Stripe account verified and live | Thomas |
| Three products created: Starter ($29/mo), Pro ($99/mo), Enterprise ($499/mo) | Thomas |
| Payment links generated for each tier | Thomas |
| Checkout page at atomadic.tech/pricing that links to Stripe | Thomas |
| Webhook to send a welcome email + CLI license key on successful payment | Thomas |

---

## 5. Content Calendar (Weeks 1-2)

### Week 1 (Launch Week)

| Day | Platform | Content | Owner |
|-----|----------|---------|-------|
| Sat (D1) | Twitter, HN, Reddit, LinkedIn | Launch posts (see Day 1 Plan) | Thomas |
| Sun (D2) | dev.to | Long-form: "I built an architecture compiler. Here's what happened when I fed it 13K files." | Thomas |
| Mon (D3) | Product Hunt | PH launch (scheduled from D1) | Thomas |
| Mon (D3) | Twitter | Thread: "Why SHA-256 certification matters for AI-generated code" (5 tweets) | Thomas |
| Tue (D4) | Twitter | Share first user's rebuild result (with permission). "Our first user ran ASS-ADE on [repo]. Here's what happened." | Thomas |
| Wed (D5) | LinkedIn | "The $2.41 trillion problem nobody's solving" — enterprise angle post | Thomas |
| Thu (D6) | Twitter | Technical thread: "How the 5-tier monadic architecture works" (diagram + explanation) | Thomas |
| Fri (D7) | dev.to / blog | "Week 1 numbers: X installs, Y rebuilds, Z certified repos" — transparency post | Thomas |

### Week 2 (Momentum)

| Day | Platform | Content | Owner |
|-----|----------|---------|-------|
| Mon (D8) | Twitter | "Copilot generates code. ASS-ADE gives it a skeleton." — positioning thread | Thomas |
| Tue (D9) | YouTube | 2-minute terminal recording: watch a real rebuild happen in real-time | Thomas |
| Wed (D10) | HN | "Ask HN: What's your biggest architectural debt problem?" — community engagement (soft sell) | Thomas |
| Thu (D11) | LinkedIn | "Why we chose BSL 1.1" — license philosophy post | Thomas |
| Fri (D12) | Twitter | "Rebuild Friday" — pick a popular open-source repo, rebuild it live, post the results | Thomas |
| Sat (D13) | Reddit r/Python | "I rebuilt [popular Python repo] with ASS-ADE. Before/after architecture comparison." | Thomas |
| Sun (D14) | Blog | "Two weeks in: what we learned, what we're building next" — retrospective | Thomas |

### Recurring (ongoing after Week 2)

| Cadence | Content | Platform |
|---------|---------|----------|
| Every Friday | "Rebuild Friday" — public rebuild of a popular repo | Twitter + Reddit |
| Every 2 weeks | Technical deep-dive blog post | dev.to + blog |
| Monthly | "State of ASS-ADE" numbers post (installs, rebuilds, purity scores) | All platforms |

---

## 6. Risk Matrix

| # | Risk | Likelihood | Impact | Mitigation | Owner |
|---|------|-----------|--------|------------|-------|
| 1 | **PyPI install fails** for users (missing dep, platform issue) | Medium | Critical | Test on macOS, Linux, Windows before launch. Pin all deps. Have a Docker fallback: `docker run atomadic/ass-ade`. | Thomas |
| 2 | **HN/Reddit hostile reception** ("this is just a linter" or "the name is unprofessional") | Medium | High | Prepare rebuttals. Lead with numbers (92K components, 24 min). The name is memorable and intentional — lean into it. Don't be defensive. | Thomas |
| 3 | **CI fails publicly on first push** | Low | High | Run full test suite locally before push. Have a fix-and-force-push plan ready. | Thomas |
| 4 | **No paying customers in Week 1** | Medium | Medium | Activate backup plan (discount offer). Founder's Circle DMs are the primary hedge. Even 1 customer validates the model. | Thomas |
| 5 | **atomadic.tech goes down under traffic** | Low | High | Ensure the site is on a CDN or can handle a HN hug-of-death. Static pages > dynamic. GitHub is the real landing page anyway. | Thomas |
| 6 | **Someone finds a critical bug in the seed** | Medium | High | The 1,511 tests provide good coverage. Monitor GitHub issues obsessively in Week 1. Fix within hours, not days. | Thomas + Claude |
| 7 | **x402/cryptography dep causes install issues** | Medium | Medium | The `x402[evm,httpx]` dependency is niche. If it causes friction, make it an optional extra: `pip install ass-ade[payments]`. | Claude |
| 8 | **Competitor copies the concept quickly** | Low (short-term) | Low | The reentrant evolution loop and 1,511-test seed are 6+ months ahead. Moat deepens with every rebuild cycle. Ship fast, iterate faster. | Auto-evolve |
| 9 | **License confusion** (BSL misunderstood as proprietary) | Medium | Medium | Add a clear LICENSE-FAQ.md. One-liner in README: "Free for personal and open-source use. Commercial use requires a license. Converts to GPL-2.0-or-later on 2029-04-23." | Claude |
| 10 | **Recon depth bug causes incorrect results for a user's repo** | Medium | High | Fix is in the BLOCKING list. Write regression tests for edge cases (deeply nested dirs, symlinks, monorepos). | Claude |

---

## 7. Version Roadmap

### v1.0.0 — "The Seed" (Now)

**Theme:** Ship the architecture compiler. Prove it works at scale.

| Feature | Status |
|---------|--------|
| 5-tier monadic rebuild engine | Done |
| 68 CLI commands | Done |
| SHA-256 certification | Done |
| BSL 1.1 license | Done |
| CLAW demo proof (92K components, 24 min) | Done |
| PyPI distribution | Blocking (pre-launch) |
| GitHub public repo | Blocking (pre-launch) |

### v1.1.0 — "The Hook" (Weeks 3-6)

**Theme:** Make it irresistible to try. Lower friction to zero.

| Feature | Owner | Est. |
|---------|-------|------|
| `ass-ade demo` instant demo command | Claude | 4 hr |
| Architecture Score Badge (shields.io) | Claude | 3 hr |
| `ass-ade report` — HTML/PDF architecture report for a repo | Claude | 8 hr |
| Docs site at atomadic.tech/docs | Thomas | 8 hr |
| GitHub Action: run ASS-ADE on every PR (architecture CI) | Claude | 6 hr |
| Three evolution lanes pushed and documented | Claude | 4 hr |
| Improved error messages for common failure modes | Claude | 4 hr |
| `ass-ade score` — print monadic purity score without full rebuild | Claude | 3 hr |

### v1.2.0 — "The Engine" (Weeks 7-12)

**Theme:** Unlock the evolution loop. Make rebuilds addictive.

| Feature | Owner | Est. |
|---------|-------|------|
| Reentrant rebuild: feed output back as input, track generation number | Claude | 12 hr |
| Generation dashboard: purity score over time, drift detection | Claude | 8 hr |
| Forge mode GA: LLM-powered body generation for blueprint stubs | Claude | 16 hr |
| Multi-language support: TypeScript/JavaScript classification (not just blueprinting) | Claude | 20 hr |
| Per-call metering infrastructure (usage-based billing) | Thomas | 12 hr |
| Tauri desktop dashboard v1 (read-only: view scores, history, certificates) | Thomas | 20 hr |
| `ass-ade diff` — show architectural diff between two generations | Claude | 6 hr |

### v2.0.0 — "The Platform" (Months 4-6)

**Theme:** From CLI tool to platform. Team features. Enterprise readiness.

| Feature | Owner | Est. |
|---------|-------|------|
| Team workspaces: shared rebuild history, team purity dashboards | Thomas + Claude | 40 hr |
| CI/CD integrations: GitHub, GitLab, Bitbucket native | Claude | 20 hr |
| Enterprise SSO (SAML/OIDC) | Thomas | 16 hr |
| Compliance reporting: SOC 2, ISO 27001 audit trail from certificates | Claude | 12 hr |
| API: rebuild-as-a-service (POST a repo URL, GET a certificate) | Thomas + Claude | 24 hr |
| Plugin system: custom tier definitions, custom classification rules | Claude | 20 hr |
| Rust/Go/Java classification (beyond Python/TS) | Claude | 40 hr |
| Self-hosted Enterprise deployment option | Thomas | 20 hr |
| Rebuild Challenge web app (viral loop) | Thomas + Claude | 30 hr |

---

## Execution Summary

**Before launch (24-48 hours):**
Fix the 8 blocking items. Estimated total: ~8 hours of work.

**Day 1:**
Push, publish, post. Follow the hour-by-hour plan. Monitor and respond to everything.

**Week 1:**
Ship the demo command, stand up docs, fix what breaks, get Stripe live, land first customer.

**Weeks 2-6:**
Ship v1.1.0 features. Build content flywheel. Convert free users to paid.

**Weeks 7-12:**
Ship v1.2.0. Unlock the evolution loop. Start enterprise conversations.

**Months 4-6:**
Ship v2.0.0. Platform play. Team features. API. Enterprise.

---

*This is the playbook. Execute it.*
