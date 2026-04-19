# Quick Start

## Prerequisites

- Python 3.11+
- ASS-ADE installed (`pip install ass-ade` or `pip install -e .`)
- Optional: AAAA-Nexus API key for premium features

## Basic usage

```bash
# Chat with Atomadic (the interactive front door)
ass-ade chat

# Rebuild any codebase into clean tiers
ass-ade rebuild ./my-project ./my-project-rebuilt

# Generate documentation
ass-ade docs ./my-project

# Run the lint pipeline
ass-ade lint ./my-project

# Certify the output
ass-ade certify ./my-project-rebuilt

# Enhance a codebase
ass-ade enhance ./my-project
```

## Tier layout after rebuild

```
!ass-ade-v0.0.1-final/
├── a0_qk_constants/        # stateless invariants, constants, axioms
├── a1_at_functions/        # pure functions
├── a2_mo_composites/       # stateful compositions
├── a3_og_features/         # feature modules
├── a4_sy_orchestration/    # top-level orchestration
├── 0_README.md
├── 1_QUICKSTART.md
├── 2_ARCHITECTURE.md
├── 3_USER_GUIDE.md
├── 4_FEATURES.md
├── 5_CONTRIBUTING.md
├── CHANGELOG.md
├── CERTIFICATE.json
└── NEXT_ENHANCEMENT.md
```

## Verify certificate

```bash
python -c "import json,hashlib; c=json.load(open('CERTIFICATE.json')); h=c.pop('certificate_sha256'); b=json.dumps(c,sort_keys=True).encode(); print('VERIFIED' if hashlib.sha256(b).hexdigest()==h else 'TAMPERED')"
```

Rebuild tag: `20260418_220755` · Issued: 2026-04-19
