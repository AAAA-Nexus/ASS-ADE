---
title: ASS-ADE LoRA Trainer
emoji: ⚙️
colorFrom: indigo
colorTo: cyan
sdk: gradio
sdk_version: 4.44.1
app_file: app.py
pinned: false
license: mit
hardware: zero-gpu
---

# ASS-ADE LoRA Trainer

Fine-tune the shared adapter from the live code-fix sample pool at [atomadic.tech](https://atomadic.tech).

Requires two secrets in the Space:
- `AAAA_NEXUS_OWNER_TOKEN` — for owner-only sample export
- `HF_TOKEN` — write access to your target HF model repo
