# ASS-ADE Data Agreement

**Version 0.0.1 — April 2026**

This document explains exactly what happens to your data when you use ASS-ADE's LoRA training features. It is written to be read by a developer in five minutes, not by a lawyer.

---

## The short version

- **Local training is 100% private.** `ass-ade train --collect`, `--run`, and `--serve` never send anything anywhere.
- **Submission is opt-in.** Data only leaves your machine if you run `ass-ade lora capture`, and even then, only anonymized structural patterns are sent — not your source code.
- **You can stop at any time.** Request deletion of your contributions by emailing privacy@atomadic.tech with your agent ID.

---

## What you're submitting (if you opt in)

When you run `ass-ade lora capture`, the system extracts **anonymized code transformation patterns**:

- The *structure* of a before/after code change (control flow, AST shape, error type, fix category)
- Quality scores from the CIE lint pipeline
- The programming language

**What is NOT sent:**
- Variable names, function names, class names, string literals
- File paths or directory names
- Comments or docstrings
- Business logic or proprietary algorithms
- Any data from `--collect` mode (local only)

The anonymization happens locally on your machine before any network request. You can inspect the exact payload with `ass-ade lora buffer-inspect` before submitting.

---

## What we do with submitted patterns

1. **Quality gate** — Each submission is scored by the Nexus quality gate. Patterns below the threshold (score < 0.7) are discarded immediately.
2. **Community adapter training** — Accepted patterns are added to the shared training pool and used to fine-tune the community LoRA adapter.
3. **Credit rewards** — You earn API credits for accepted submissions (see [TRAINING_GUIDE.md](TRAINING_GUIDE.md) for tier details).
4. **Aggregate statistics only** — We track submission counts, acceptance rates, and quality distributions. We do not maintain per-submission provenance beyond what is needed to process deletion requests.

---

## What we don't do

- We do not store your source code.
- We do not sell your data to third parties.
- We do not use your submissions for anything other than training the shared community adapter.
- We do not share individual submissions or link them back to you publicly.
- We do not train on data from `--collect` or `--serve` mode — those are entirely local.

---

## Your rights

**Access:** You can inspect your local training buffer at any time with `ass-ade lora buffer-inspect`.

**Deletion:** To request deletion of your contributed patterns from the shared training pool, email privacy@atomadic.tech with your agent ID (find it with `ass-ade nexus status`). We will process deletion requests within 30 days.

**Opt-out:** You can use ASS-ADE indefinitely — including `--collect`, `--run`, and `--serve` — without ever submitting anything. Submission requires an explicit `ass-ade lora capture` call.

---

## Trust gate

Only patterns that pass the Nexus trust gate are accepted. The gate evaluates:

- **Novelty** — is this pattern meaningfully different from what is already in the pool?
- **Quality** — does the transformation produce a measurable improvement (lint score, test pass rate)?
- **Safety** — does the pattern introduce any OWASP Top 10 vulnerabilities?

Patterns that fail any of these checks are rejected and never stored.

---

## Local data

Data collected by `ass-ade train --collect` is stored in `training_data/training_data.jsonl` on your machine. This file is in `.gitignore` by default and is never transmitted unless you deliberately upload it (e.g., to Colab for training). You own it entirely.

---

## Changes to this agreement

If we make material changes to what data is collected or how it is used, we will increment the version number and announce it in the CHANGELOG. You can always compare this document in git history.

---

## Contact

Questions? Email privacy@atomadic.tech or open an issue at github.com/atomadictech/ass-ade.
