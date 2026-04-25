# ASS-ADE Launch Readiness Audit

**Date:** 2026-04-24
**Auditor:** Claude (Final pre-launch audit)
**Verdict:** 6 READY / 4 NOT READY / 2 BLOCKED

---

## 1. GitHub — AAAA-Nexus/ASS-ADE

**Status: NOT READY**

The repo exists at `github.com/AAAA-Nexus/ASS-ADE` with remotes configured. Latest commits look solid:

```
67683529 Merge branch 'release/v1.0.0'
85261b14 fix(ci): track self-assimilate.yaml + strip ANSI in book delegate test
7222a6ad security: redact sovereign IP constants from public release surface
ffce61a8 release: v1.0.0 — unified monorepo, ass_ade_v11 spine, atomadic-engine subpkg, 288 tests green
```

**Issues found:**

- **README is not professional.** It reads like an auto-generated manifest — raw class/function lists, no hero description, no badges that render, no screenshots, no "Why ASS-ADE?" section, no architecture diagram. The image badges `![Language](python)` are broken (not valid badge URLs). Compare to any top-tier dev tool README: Cursor, Cline, Ruff — they all lead with a clear value prop, a GIF/screenshot, and install instructions.
- **Not indexed by Google/GitHub search** — web search for "AAAA-Nexus ASS-ADE" returns zero results. This means the repo is either private, very new, or has zero SEO signals. If it's private, that's a blocker for launch day.

**Action items:**
- [ ] Rewrite README with: hero tagline, architecture diagram, 3-step quickstart, proper shields.io badges, link to docs
- [ ] Confirm repo is PUBLIC before launch day
- [ ] Add GitHub topics: `ai`, `developer-tools`, `code-architecture`, `autonomous-agent`, `python`

---

## 2. Website — atomadic.tech

**Status: NOT READY**

The Cloudflare Worker routes are configured for `atomadic.tech`, `www.atomadic.tech`, and `hello.atomadic.tech`. The storefront codebase (Rust/Wasm on CF Workers) is substantial with templates for home, pay, chat, benchmarks, aegis, etc.

**Issues found:**

- **No dedicated `/ass-ade` product page.** The route `/ass-ade` exists in the router but falls through to `serve_home()` — it just shows the homepage. There is no `ass_ade.html` template in `templates/pages/`. For launch day, people clicking the GitHub link to learn more will land on a generic homepage.
- **hello.atomadic.tech** — Routes exist and the HELLO_PORTAL.md documents the architecture (KV-backed feed, subscribe, publish endpoints). Whether it's actually deployed and serving HTML is unverified (web fetch blocked by network policy). Needs manual browser check.
- **Could not verify live status** — network egress is restricted to `*.anthropic.com` from this sandbox. Thomas must manually verify `atomadic.tech` loads in a browser.

**Action items:**
- [ ] Create `templates/pages/ass_ade.html` product page with: hero, demo video/GIF, architecture diagram, pricing CTA, GitHub link
- [ ] Wire `/ass-ade` route to `pages::serve_ass_ade()` instead of falling through to home
- [ ] Manual browser check: confirm `atomadic.tech`, `hello.atomadic.tech`, and `/ass-ade` all load
- [ ] Verify SSL certs are valid on all subdomains

---

## 3. Inference — atomadic.tech/v1/inference

**Status: BLOCKED (by network egress policy)**

Cannot test from this sandbox — `atomadic.tech` is not on the network allowlist.

**Action items:**
- [ ] Thomas: manually `curl https://atomadic.tech/v1/inference` and verify a response
- [ ] Confirm the inference route exists in the Worker router (not found in current codebase scan — may need to be added)
- [ ] If inference is proxied to a model backend (Helix, etc.), verify that backend is up

---

## 4. CLI — `pip install ass-ade`

**Status: NOT READY**

`pyproject.toml` is well-structured with version `1.0.0`, proper dependencies, entry points (`ass-ade` and `atomadic` commands), and dev extras. The package builds from source with `pip install .` or `pip install -e ".[dev]"`.

**Issues found:**

- **Not on PyPI.** Web search for `ass-ade` on PyPI returns zero results. `pip install ass-ade` will fail for anyone who doesn't clone the repo first.
- **Python >=3.12 requirement** is aggressive — many devs are still on 3.10/3.11. Consider whether this is intentional.
- **No `__version__` verification** — confirm `ass_ade_v11.__version__` matches `1.0.0` in pyproject.toml.

**Action items:**
- [ ] Register `ass-ade` on PyPI (create account, `python -m build && twine upload dist/*`)
- [ ] Set up Trusted Publishers on PyPI so GitHub Actions can auto-publish on tag
- [ ] Test `pip install ass-ade` from a clean venv after upload
- [ ] Consider adding a `[project.urls]` section (Homepage, Documentation, Repository, Changelog)

---

## 5. Stripe — Payment Configuration

**Status: READY**

Stripe is well-configured:

- **Live keys deployed** — `pk_live_*` publishable key is in `wrangler.toml` (correct: publishable keys are public)
- **Secret key** is via `wrangler secret put STRIPE_SECRET_KEY` (correct: never in code)
- **22 price IDs configured** in `stripe_price_ids.json` covering:
  - Credits: 500 / 2,500 / 10,000
  - Helix models: llama3.2-1b, phi3.5-mini, qwen2.5-7b, bundle
  - Prompt packs: 14 domain bundles (healthcare, legal, fintech, etc.)
- **Checkout flow exists** — `/pay` route serves `pay.html` template
- **OpenAPI spec** documents Stripe session creation and price listing endpoints

**Minor concerns:**
- [ ] Verify Stripe webhook endpoint is configured for `payment_intent.succeeded` / `checkout.session.completed`
- [ ] Test a $0.50 purchase end-to-end before launch

---

## 6. Press Kit — ASS-CLAW/PRESS_KIT.md & SOCIAL_POSTS.md

**Status: READY**

Both files exist and are polished:

**PRESS_KIT.md** includes:
- Compelling hook: "13,286 files, 3 repos, 24 minutes, zero human intervention"
- Clear explanation of ASS-CLAW demo and ASS-ADE engine
- Source repo table with star counts
- Output architecture table (92,305 files across 5 tiers)
- License note (BSL 1.1)

**SOCIAL_POSTS.md** includes:
- 3 Twitter/X posts (varying angles: stats, positioning, detailed breakdown)
- LinkedIn long-form post
- All reference `github.com/AAAA-Nexus/ASS-ADE`

**Minor concerns:**
- [ ] Verify OpenClaw "361K stars" claim is current and accurate
- [ ] Confirm the stats (13,286 files, 92,305 output, 24 minutes) are from an actual reproducible run
- [ ] Add a Hacker News post draft to SOCIAL_POSTS.md (HN is critical for dev tool launches)
- [ ] Press kit should mention the website URL (atomadic.tech) — currently only links to GitHub

---

## 7. Legal — BSL 1.1 LICENSE

**Status: READY**

`LICENSE` file is present in the repo root with a proper BSL 1.1 license:

- **Licensor:** Atomadic and contributors
- **Licensed Work:** ASS-ADE (Autonomous Sovereign System: Atomadic Development Environment)
- **Change Date:** 2029-04-23
- **Change License:** GPL-2.0-or-later
- **Additional Use Grant:** None

License is authoritative: BSL 1.1, Change Date 2029-04-23, Change License GPL-2.0-or-later.
All documentation must reference these values. Previous references to "Apache 2.0 in 2030" were incorrect and have been corrected.

**Action items:**
- [x] License terms confirmed: BSL 1.1 → GPL-2.0-or-later on 2029-04-23 (DONE)
- [ ] Add `SECURITY.md` contact email (file exists but verify it has a real contact)

---

## 8. IP — MHED/Leech/Monster Term Leaks

**Status: READY**

Comprehensive grep across all public-facing files:

- `README.md` — clean
- `pyproject.toml` — clean
- `LICENSE` — clean
- `FEATURES.md` — clean
- `AGENTS.md` — clean
- `docs/` directory — clean
- `ass-ade-v1.1/src/` — clean
- `atomadic-engine/src/` — clean
- `ASS-CLAW/PRESS_KIT.md` — clean
- `ASS-CLAW/SOCIAL_POSTS.md` — clean

No instances of "mhed", "leech", or "monster" found anywhere in the codebase. The `7222a6ad` commit ("security: redact sovereign IP constants from public release surface") appears to have been effective.

---

## 9. CI — GitHub Actions

**Status: READY (with caveat)**

Two workflow files exist:

**`ass-ade-ship.yml`** — comprehensive CI pipeline:
- Python 3.12, pip cache
- Swarm prompt alignment check
- Monadic import layer linting (`lint-imports`)
- Pytest (excluding dogfood tests)
- Synth-test manifest check
- Golden assimilate (single-root and multi-root with `--policy`)

**`auto-evolve.yml`** — automated evolution pipeline (9.7KB, substantial)

**Caveat:** Cannot verify whether Actions are currently green — GitHub is not accessible from this sandbox. Thomas must check `github.com/AAAA-Nexus/ASS-ADE/actions` manually.

**Action items:**
- [ ] Manual check: verify last CI run is green on `main`
- [ ] Ensure branch protection requires CI pass before merge

---

## 10. Social — Accounts Thomas Needs

**Status: NOT READY (action required)**

For a dev tool launch, Thomas needs accounts on these platforms:

**Must-have (launch day):**
- [ ] **Twitter/X** — `@atomadic` or `@atomadic_tech` — primary dev community channel
- [ ] **Product Hunt** — maker account, pre-create the product listing
- [ ] **Hacker News** — account with some karma before posting (ideally comment for a week+ before launch)
- [ ] **Reddit** — for r/programming, r/MachineLearning, r/LocalLLaMA, r/devtools
- [ ] **Discord** — Atomadic community server (see item 11)

**Should-have (week 1):**
- [ ] **LinkedIn** — company page for Atomadic
- [ ] **YouTube** — for demo videos, recorded walkthroughs
- [ ] **Dev.to** — cross-post launch blog post
- [ ] **GitHub Discussions** — enable on the AAAA-Nexus/ASS-ADE repo

**Nice-to-have (month 1):**
- [ ] **Bluesky** — growing dev audience
- [ ] **Mastodon** — Fediverse dev community
- [ ] **Substack/Blog** — `blog.atomadic.tech` for long-form content

---

## 11. Discord — Bot & Community Server

**Status: BLOCKED (needs setup)**

No Discord configuration found in the codebase.

**Action items:**
- [ ] Create Discord server with channels: `#announcements`, `#general`, `#support`, `#show-and-tell`, `#bug-reports`, `#feature-requests`
- [ ] Set up a Discord bot for:
  - Welcome messages with quickstart link
  - `/ass-ade status` command (ping the inference endpoint)
  - GitHub webhook integration (new releases, CI status)
  - Support ticket routing
- [ ] Create invite link and add to: README, website, press kit
- [ ] Consider a Discord bot that can run ASS-ADE commands (stretch goal for post-launch)

---

## 12. Documentation — Getting Started Guide

**Status: NOT READY**

Documentation exists but is scattered and not user-facing:

- `.ass-ade-rebuild-out/1_QUICKSTART.md` — decent quickstart but buried in a hidden rebuild output directory, not accessible to users
- `.ass-ade-rebuild-out/3_USER_GUIDE.md` — same problem, hidden
- `docs/` — contains 12 files but they're internal RFCs and audits (`ASS_ADE_SPINE_RFC.md`, `ATOMADIC_SWARM_SURFACE_AUDIT.md`), not user docs
- `CONTRIBUTING.md` — basic but functional
- `FEATURES.md` — exists (26KB) but not verified for user-readiness

**Issues:**
- No top-level `docs/getting-started.md` or `docs/quickstart.md` visible to users
- The quickstart is in a hidden `.ass-ade-rebuild-out/` directory
- No hosted docs site (ReadTheDocs, Docusaurus, etc.)

**Action items:**
- [ ] Move `1_QUICKSTART.md` to `docs/QUICKSTART.md` (visible, top-level)
- [ ] Move `3_USER_GUIDE.md` to `docs/USER_GUIDE.md`
- [ ] Create a `docs/index.md` that links: Quickstart, User Guide, Architecture, API Reference
- [ ] Consider a docs site: GitHub Pages, ReadTheDocs, or Docusaurus
- [ ] Link docs from README and website

---

## Launch Tactics — What Successful Dev Tools Did

### Cursor's Playbook
- **Launched 5 times on Product Hunt** (2024-2025), consistently Top 5 Product of the Day
- **Feature-forward messaging** — no marketing fluff, just "here's what it does"
- **Minimalist visuals** — 2-4 product screenshots, no stock photos
- **Strategic hunter** — established PH user with 50K+ followers
- **Rapid release cadence** — 3 product launches + full UI rebuild in one month
- **Developer-native tone** — devs are allergic to marketing speak

### Winning Dev Tool Launch Patterns (2025-2026)

1. **Pre-launch audience (6 weeks out):**
   - Build a waitlist or email list before launch day
   - Post teasers on Twitter/X showing the tool in action
   - Get 5-10 beta users who will vouch on launch day

2. **Launch day timing:**
   - **12:01 AM PT** on Product Hunt (Tuesday-Thursday preferred)
   - **6-9 AM PT window is critical** — need 30+ upvotes/hour
   - Post HN "Show HN" between 8-10 AM ET
   - Tweet thread at peak dev Twitter hours (10 AM ET)

3. **Content strategy:**
   - **GIF/video first** — show, don't tell. A 30-second GIF of ASS-ADE rebuilding a codebase is worth 1000 words
   - **"Show HN" post** — keep it to 3 paragraphs: what it does, how it works, try it yourself
   - **Technical blog post** — deep dive into the architecture for credibility
   - **Comparison angle** — "Every other tool is a copilot. ASS-ADE is the architect." (you already have this — it's strong)

4. **Day-of engagement:**
   - Answer EVERY comment in the first 3 hours
   - Have 2-3 friends/beta users ready to leave genuine reviews
   - Cross-post to Reddit (r/programming, r/devtools) a few hours after PH launch
   - Don't ask for upvotes — ask people to "check it out"

5. **What NOT to do:**
   - Don't launch on a Friday or weekend
   - Don't use jargon-heavy descriptions (ASS-ADE's "monadic tiers" language needs a plain-English wrapper for non-experts)
   - Don't link to a repo with a broken README
   - Don't launch without a working `pip install` command

### Specific Tactics to Steal

- **Cursor:** Keep visuals minimal and let the product speak. Your ASS-CLAW stats (13K files, 24 minutes) are your equivalent of a product screenshot
- **Cline:** Open-source credibility. BSL 1.1 is close enough — lean into transparency
- **Windsurf:** Generous free tier to reduce friction. Consider a free tier for repos under 1000 files
- **Devin (Cognition):** The waitlist/hype model — probably not right for ASS-ADE since you have a working product, but the "apply for access" angle creates scarcity

---

## Summary Scorecard

| Area | Status | Blocker |
|------|--------|---------|
| 1. GitHub README | NOT READY | Needs rewrite — broken badges, no hero section |
| 2. Website `/ass-ade` | NOT READY | No product page — route falls through to homepage |
| 3. Inference endpoint | BLOCKED | Can't verify — needs manual curl test |
| 4. PyPI `pip install` | NOT READY | Not published to PyPI |
| 5. Stripe payments | READY | Verify webhook + test purchase |
| 6. Press kit | READY | License confirmed: BSL 1.1 → GPL-2.0-or-later on 2029-04-23 |
| 7. BSL 1.1 License | READY | Consistent: Change Date 2029-04-23, Change License GPL-2.0-or-later |
| 8. IP leak check | READY | Clean — no MHED/Leech/Monster found |
| 9. CI / GitHub Actions | READY | Manual green check needed |
| 10. Social accounts | NOT READY | Need to create Twitter, PH, HN, Reddit, LinkedIn |
| 11. Discord | BLOCKED | Server + bot need full setup |
| 12. Documentation | NOT READY | Quickstart buried in hidden dir, no docs site |

## Top 5 Priorities Before Launch

1. **Rewrite the GitHub README** — this is the first thing everyone sees
2. **Publish to PyPI** — `pip install ass-ade` must work
3. **Create the `/ass-ade` product page** on atomadic.tech
4. **Move quickstart docs** to visible location + link from README
5. **Create Twitter/X account** and schedule the SOCIAL_POSTS.md content
