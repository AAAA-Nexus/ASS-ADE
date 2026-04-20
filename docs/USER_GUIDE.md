# ASS-ADE User Guide

Complete walkthroughs and examples for common ASS-ADE workflows.

## Table of Contents

- [The Design Engine](#the-design-engine)
- [The Rebuild Engine](#the-rebuild-engine)
- [Auto-Documentation](#auto-documentation)
- [Monadic Linter](#monadic-linter)
- [Codebase Certification](#codebase-certification)
- [Full Build Pipeline](#full-build-pipeline)
- [Free Tier & Pricing](#free-tier--pricing)
- [Repository Inspection](#repository-inspection)
- [Agent Chat](#agent-chat)
- [MCP Integration](#mcp-integration)

---

## The Design Engine

The Design Engine turns natural language ideas into production-ready component blueprints. It combines local repository analysis with optional remote synthesis through AAAA-Nexus quality and enhancement gates.

### Quick Start

Generate a blueprint for a new feature:

```bash
ass-ade design "add OAuth2 login"
```

Output: `blueprint_add_oauth2_login.json` ready for materialization.

### What Happens

1. **Local Analysis (Free, Instant)**
   - Scans your repository structure
   - Detects programming languages
   - Identifies entry points, dependencies, current architecture
   - Determines which composition tiers to target

2. **Remote Synthesis (Optional)**
   - If you use `--allow-remote`, sends analysis to atomadic.tech
   - Intelligent blueprint generation based on repo context
   - Fits the blueprint into your specific codebase patterns

### Examples

#### Single Blueprint

```bash
# Generate locally without remote synthesis
ass-ade design "add Redis caching layer"

# Same, but with remote synthesis (requires free tier or paid API)
ass-ade design "add Redis caching layer" --allow-remote

# Specify the target repo
ass-ade design "add OAuth2 login" --path ~/myproject

# Custom output filename
ass-ade design "add WebSocket support" --out my_blueprint.json

# Print as JSON (don't write file)
ass-ade design "add Prometheus metrics" --json
```

#### Parallel Blueprints

The monadic tier system prevents conflicts, so you can generate multiple blueprints without interference:

```bash
# Create a file with one description per line
cat > feature_list.txt << 'EOF'
add OAuth2 login
add Redis caching layer
add Prometheus metrics
EOF

# Generate all at once
ass-ade design --parallel feature_list.txt --allow-remote
```

Output:
- `blueprint_add_oauth2_login.json`
- `blueprint_add_redis_caching_layer.json`
- `blueprint_add_prometheus_metrics.json`

### Exploring the Blueprint

```bash
# View the generated blueprint
cat blueprint_add_oauth2_login.json
```

Example output:

```json
{
  "schema": "AAAA-SPEC-004",
  "description": "add OAuth2 login",
  "tiers": ["at", "mo"],
  "components": [],
  "status": "draft",
  "source": "local",
  "repo": null,
  "languages": ["python", "json"]
}
```

Key fields:
- `schema`: AAAA-SPEC-004 format
- `tiers`: which composition tiers this blueprint targets (qk, at, mo, og, sy)
- `components`: list of component definitions (populated by remote synthesis)
- `status`: draft (local) or refined (remote-synthesized)

### Next Step: Rebuild

After designing, materialize the blueprint:

```bash
ass-ade rebuild . --blueprint blueprint_add_oauth2_login.json
```

This creates a fresh folder with the new components integrated into your tier-partitioned structure.

### Free Tier & Rate Limits

- **Local analysis**: unlimited, free, instant
- **Remote synthesis**: 3 calls/day free tier per IP
- **Paid access**: x402 USDC per call on Base L2, or API key credit pack

```bash
# Check your status
ass-ade lora-credit
ass-ade lora-status
```

---

## The Rebuild Engine

The Rebuild Engine transforms any codebase into a clean, tier-partitioned modular structure based on the five-tier composition law.

### Quick Start

```bash
ass-ade rebuild /path/to/repo
```

### The Five Tiers

Each tier represents a layer of composition:

| Tier | Purpose | Examples |
|---|---|---|
| **qk** | Stateless constants and axioms | Config values, enums, magic numbers |
| **at** | Pure functions | Utilities, algorithms, validators |
| **mo** | Stateful compositions | Drivers, orchestrators, services |
| **og** | Feature organisms | Domain modules, APIs, handlers |
| **sy** | Top-level system | Main entry points, routers, orchestration |

### Examples

#### Basic Rebuild

```bash
ass-ade rebuild .
```

Produces a new folder (e.g., `rebuild_2026_04_18/`) with the codebase reorganized into tiers.

#### With a Blueprint

```bash
ass-ade design "add OAuth2 login"
ass-ade rebuild . --blueprint blueprint_add_oauth2_login.json
```

The blueprint guides where new components are placed.

#### Validate an Existing Rebuild

```bash
ass-ade rebuild --validate ./existing_rebuild_folder
```

Checks that the tier structure is valid and invariants are maintained.

#### Scan Before Rebuilding

Get a snapshot of your repo structure:

```bash
ass-ade eco-scan .
```

Outputs:
- `ONBOARDING.md` — Human-readable brief
- `ONBOARDING.json` — Machine-readable structure
- `QUICK_START.md` — Common commands and entry points

---

## Auto-Documentation

The docs command generates a complete documentation suite: README.md, ARCHITECTURE.md, FEATURES.md, USER_GUIDE.md, CONTRIBUTING.md, CHANGELOG.md, and .gitignore.

### Quick Start

```bash
ass-ade docs .
```

Generates docs in the current folder using local AST analysis.

### What Gets Generated

1. **README.md** — Overview, installation, quickstart, features
2. **ARCHITECTURE.md** — System design, module layout, data flow
3. **FEATURES.md** — Feature list with descriptions
4. **USER_GUIDE.md** — How to use the project
5. **CONTRIBUTING.md** — Developer guidelines, setup, testing
6. **.gitignore** — Language-specific ignores (Python, Node, Rust, etc.)
7. **CHANGELOG.md** — Release notes template

### Examples

#### Local Analysis Only

```bash
# Generate docs without remote synthesis
ass-ade docs .
```

#### With Remote Synthesis

```bash
# Intelligent enrichment via Nexus docs engine
ass-ade docs . --allow-remote
```

Adds:
- Gap analysis (detects missing sections)
- Copy optimization (adjusts tone and clarity)
- Link suggestions (cross-references between docs)

#### Custom Output Directory

```bash
ass-ade docs . --output-dir ./my-docs
```

Writes all files to `./my-docs/`.

#### JSON Output

```bash
ass-ade docs . --allow-remote --json
```

Returns the entire result as JSON (useful for scripting).

#### With Specific Repository

```bash
ass-ade docs ~/myproject
```

### Exploring Generated Docs

After running `ass-ade docs .`, inspect the files:

```bash
cat README.md
cat ARCHITECTURE.md
cat CONTRIBUTING.md
```

Each file is production-ready and ready to commit to version control.

### Free Tier & Rate Limits

- **Local-only**: unlimited, free
- **Remote synthesis**: 3 calls/day free tier
- **Paid**: x402 USDC per call or API key

---

## Monadic Linter

The monadic linter auto-detects which linters to run (ruff for Python, eslint for JavaScript, clippy for Rust, etc.), then optionally sends findings to Nexus for intelligent gap analysis and remediation suggestions.

### Quick Start

```bash
ass-ade lint .
```

Detects your languages and runs appropriate linters.

### Supported Linters

| Language | Tool | Feature |
|---|---|---|
| Python | ruff | Error detection, formatting, complexity |
| TypeScript/JavaScript | eslint | Code quality, security, style |
| Rust | clippy | Warnings, idioms, performance |
| Go | go vet | Correctness issues |
| Others | — | Detected but skipped if not installed |

### Examples

#### Local Linting

```bash
# Run native linters only (no remote call)
ass-ade lint .
```

Output example (Python repo):
```
Linting C:\myproject

[OK] ruff check . — 0 findings
Lint result: PASS
```

#### With Auto-Fix

```bash
# Auto-fix where supported (ruff --fix, eslint --fix, etc.)
ass-ade lint . --fix
```

Some linters support auto-fixes for common issues.

#### Remote Gap Analysis

```bash
# Send findings to Nexus for intelligent remediation suggestions
ass-ade lint . --allow-remote
```

Nexus returns:
- Root cause analysis of each finding
- Suggested fixes with code examples
- Custom remediation advice based on your codebase

#### JSON Output

```bash
ass-ade lint . --allow-remote --json
```

Returns structured findings for integration with CI/CD.

#### Specific Path

```bash
ass-ade lint ~/myproject
```

### Fixing Issues

If lint reports issues, fix them manually or use auto-fix:

```bash
ass-ade lint . --fix
```

Then run again to verify:

```bash
ass-ade lint .
```

### Free Tier & Rate Limits

- **Local-only (native linters)**: unlimited, free
- **Remote synthesis**: 3 calls/day free tier
- **Paid**: x402 USDC per call or API key

---

## Codebase Certification

Generate tamper-evident certificates for your codebase. A local certificate proves integrity; a server-signed certificate is third-party verifiable.

### Quick Start

```bash
ass-ade certify .
```

Generates `CERTIFICATE.json` with SHA-256 digests of all source files.

### What Happens

**Phase 1: Local (Free)**
- Walks your codebase
- Computes SHA-256 digest for each source file
- Bundles into CERTIFICATE.json payload
- Records timestamp

**Phase 2: Remote (Optional, Paid)**
- Sends digest to atomadic.tech
- Server signs with post-quantum cryptography (ML-DSA/Dilithium)
- Certificate becomes third-party verifiable
- Includes signature and certificate authority metadata

### Examples

#### Local-Only Certificate

```bash
ass-ade certify .
```

Output: `CERTIFICATE.json`

```
ASS-ADE Codebase Certificate
========================================
Schema:      ASS-ADE-CERT-001
Version:     unknown
Root:        /path/to/repo
File count:  42
Root digest: 2d908e0ff8d600e05c8119f332e56d6b
Computed at: 2026-04-18T19:14:50Z
Valid:       False
Signature:   none

Note: Certificate is not server-signed. Use --allow-remote for a 
verifiable certificate.
```

#### With Version String

```bash
ass-ade certify . --version 1.2.0
```

Embeds version in the certificate for release tracking.

#### Server-Signed Certificate

```bash
ass-ade certify . --version 1.2.0 --allow-remote
```

Output now includes:
```
Valid:       True
Signature:   ML-DSA-87 signature from atomadic.tech
Authority:   AAAA-NEXUS-CA (atomadic.tech)
```

This certificate can be verified by third parties.

#### Custom Output Path

```bash
ass-ade certify . --out ~/certs/CERTIFICATE.json
```

#### JSON View

```bash
ass-ade certify . --json
cat CERTIFICATE.json
```

Example structure:
```json
{
  "schema": "ASS-ADE-CERT-001",
  "version": "1.2.0",
  "root": "/path/to/repo",
  "file_count": 42,
  "root_digest": "2d908e0ff8d600e05c8119f332e56d6b",
  "computed_at": "2026-04-18T19:14:50Z",
  "files": [
    {
      "path": "src/main.py",
      "digest": "a1b2c3d4...",
      "size": 1024
    }
  ],
  "signature": null,
  "signature_algorithm": "ML-DSA-87"
}
```

### Use Cases

- **Release verification**: Sign each release candidate
- **Security audits**: Prove code state at a point in time
- **Compliance**: Tamper-evident proof of source integrity
- **Supply chain**: Third-party verification of build inputs

### Free Tier & Rate Limits

- **Local certificate**: unlimited, free
- **Server signing**: 3 calls/day free tier
- **Paid**: x402 USDC per call or API key

---

## Full Build Pipeline

This is the recommended end-to-end workflow combining design, rebuild, lint, docs, and certification.

### Workflow

```bash
# Step 1: Design new features
ass-ade design "add OAuth2 login" --allow-remote
ass-ade design "add WebSocket support" --allow-remote

# Step 2: Rebuild with blueprints
ass-ade rebuild . --blueprint blueprint_add_oauth2_login.json

# Step 3: Verify quality
ass-ade lint . --fix --allow-remote

# Step 4: Generate documentation
ass-ade docs . --allow-remote

# Step 5: Certify release
ass-ade certify . --version 1.0.1 --allow-remote
```

### Expected Output

After completing this workflow:

```
.
├── blueprint_add_oauth2_login.json
├── blueprint_add_websocket_support.json
├── CERTIFICATE.json               (server-signed)
├── README.md                       (auto-generated)
├── ARCHITECTURE.md                 (auto-generated)
├── FEATURES.md                     (auto-generated)
├── USER_GUIDE.md                   (auto-generated)
├── CONTRIBUTING.md                 (auto-generated)
├── CHANGELOG.md                    (auto-generated)
├── .gitignore                      (auto-generated)
└── src/
    └── [tier-partitioned structure from rebuild]
```

### Credits & Rewards

Every API call you make is captured by the LoRA flywheel. Check your accrued credits:

```bash
ass-ade lora-credit
```

Example output:
```
LoRA Flywheel Credits
========================================
Reputation:      45 points
Nexus API credit: 4500 micro-USDC ($0.0045)
Contributions:   45 accepted samples
Status:          Active
Next batch:      2 samples until contribution
```

Your credits auto-apply to future API calls, reducing or eliminating costs.

---

## Free Tier & Pricing

### What's Always Free

- **Local repository analysis** (eco-scan, repo summary)
- **Local blueprint generation** (design without --allow-remote)
- **Local linting** (runs native linters without synthesis)
- **Local certification** (digest generation without signing)
- **File system tools** (read, write, edit, list)
- **Shell execution** (local development commands)
- **Agent chat** with free providers (Groq, Gemini, OpenRouter, Ollama)

### What Requires an API Call

| Feature | Free Tier | Paid |
|---|---|---|
| Design synthesis | 3/day | x402 USDC or API key |
| Docs synthesis | 3/day | x402 USDC or API key |
| Lint synthesis | 3/day | x402 USDC or API key |
| Certify signing | 3/day | x402 USDC or API key |
| Agent inference | Limited via free providers | AAAA-Nexus (high-capacity) |

### How to Get Paid Access

#### Option 1: x402 Autonomous Payment (Base L2)

```bash
ass-ade wallet
```

Follow interactive setup. Your wallet auto-pays per API call.

Cost: ~$0.001 per call (design, docs, lint, certify)

#### Option 2: API Key Credit Pack

```bash
# Get an API key at https://atomadic.tech
export AAAA_NEXUS_API_KEY=sk_...

# Now use --allow-remote freely until credits run out
ass-ade design "your feature" --allow-remote
```

#### Option 3: Earn Credits via LoRA Flywheel

Every API call you make trains the shared LoRA adapter. In return, you earn:

- **+10 reputation** per accepted result
- **+100 micro-USDC credit** ($0.0001 equivalent) per result

After 10 good contributions, you've earned $0.001 in free API credits.

Check balance:
```bash
ass-ade lora-credit
```

### Rate Limits

**Free tier**: 3 API calls per endpoint per 24 hours per IP address.

Example:
- 3 `design --allow-remote` calls/day
- 3 `docs --allow-remote` calls/day
- 3 `lint --allow-remote` calls/day
- 3 `certify --allow-remote` calls/day

If you exceed limits, switch to paid access.

---

## Repository Inspection

ASS-ADE includes tools for understanding any codebase quickly.

### Summary

```bash
ass-ade repo summary /path/to/repo
```

Outputs:
- Project structure
- Key files and entry points
- Dependencies
- Language distribution
- Git info (if available)

### Scan

```bash
ass-ade eco-scan /path/to/repo
```

Generates:
- `ONBOARDING.md` — Human summary
- `ONBOARDING.json` — Machine summary
- `QUICK_START.md` — Quick commands

---

## Agent Chat

Run an interactive chat session with ASS-ADE's agentic capabilities.

```bash
ass-ade agent chat
```

The agent automatically:
- Routes tasks to free providers (Groq, Gemini, OpenRouter)
- Manages context tokens
- Executes filesystem and shell tools
- Tracks costs and usage

### Single Tasks

```bash
ass-ade agent "Summarize the current directory"
```

---

## MCP Integration

ASS-ADE exposes its tools as an MCP server for integration with Claude and other MCP clients.

### Start the Server

```bash
ass-ade mcp serve
```

Exposes 14 built-in tools:
- read_file, write_file, edit_file
- list_directory, grep_search, search_files
- run_command, safe_execute
- trust_gate, certify_output
- a2a_validate, a2a_negotiate
- ask_agent

### Discover Remote Tools

```bash
ass-ade mcp tools --allow-remote
```

---

## Troubleshooting

### "Rate limit exceeded"

You've hit the free tier limit (3 calls/day per endpoint). Either:

1. Wait 24 hours
2. Enable paid access (x402 or API key)
3. Earn credits via LoRA contributions

```bash
ass-ade lora-credit
```

### "Blueprint failed to materialize"

Check the blueprint file is valid:

```bash
cat blueprint_*.json
```

Ensure the target repo matches the blueprint's language expectations.

### "Certification not verifiable"

Certificates are only third-party verifiable when server-signed. Use `--allow-remote`:

```bash
ass-ade certify . --allow-remote
```

### "Linter not found"

Native linters (ruff, eslint, etc.) must be installed. Install the relevant tools:

```bash
# Python
pip install ruff

# JavaScript/TypeScript
npm install -g eslint

# Rust
rustup component add clippy
```

Then retry:

```bash
ass-ade lint .
```

---

## Next Steps

- See [README.md](../README.md) for architecture and Python API
- See [docs/architecture.md](architecture.md) for system design
- Check [docs/](.) for detailed technical documentation
- Visit https://atomadic.tech for service status and contracts
