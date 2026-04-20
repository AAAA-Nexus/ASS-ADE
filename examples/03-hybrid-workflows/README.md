# Example 3: Hybrid Workflows

Hybrid workflows combine local processing with AAAA-Nexus remote contracts for trust verification, security scanning, and formal certification.

## What You'll Do

1. Configure hybrid mode
2. Run a trust-gate to verify agent identity
3. Use the certify workflow to attest to output
4. Run safe-execute to run untrusted code safely
5. Compose multi-step workflows with the pipeline engine
6. Interpret JSON certificates and attestations

## Prerequisites

- Python 3.12+
- ASS-ADE installed: `pip install ass-ade`
- AAAA-Nexus API key (get one at https://atomadic.tech)
- Network connectivity to AAAA-Nexus

## Background: What Is Hybrid Mode?

Hybrid mode means:

- Your config profile is set to `hybrid`
- You have an AAAA-Nexus API key
- Local commands work as-is
- Remote commands execute through public AAAA-Nexus contracts
- You opt-in to specific workflows that need remote verification

This is useful when you need:

- Trust verification for agent identity
- Hallucination detection on AI-generated content
- Security scanning for code or prompts
- Formal certificates and attestations
- Multi-agent coordination

## Step 1: Configure Hybrid Mode

Edit your config file (`~/.ass-ade/config.json` or use the sample):

```json
{
  "profile": "hybrid",
  "nexus_base_url": "https://atomadic.tech",
  "request_timeout_s": 20.0,
  "agent_id": "your-agent-id-here",
  "epistemic": {
    "ask_threshold": 0.70,
    "abstain_threshold": 0.50
  },
  "confidence": {
    "local_threshold": 0.85,
    "uncertainty_gate": 0.65
  }
}
```

Set your AAAA-Nexus API key as an environment variable:

```bash
export AAAA_NEXUS_API_KEY="your-api-key-here"
```

Or on Windows:

```cmd
set AAAA_NEXUS_API_KEY=your-api-key-here
```

Verify hybrid mode is configured:

```bash
ass-ade doctor --remote
```

Expected output:

```
Python version:     3.12.1 ✓
ASS-ADE version:    1.0.0
Config path:        /home/user/.ass-ade/config.json
Profile:            hybrid ✓
Config valid:       ✓
Remote connectivity:
  - AAAA-Nexus base URL: https://atomadic.tech
  - API key configured: ✓
  - Network test: ✓ (latency: 125ms)
```

## Step 2: Trust-Gate Workflow

The trust-gate verifies an agent's identity using remote contracts.

```bash
ass-ade workflow trust-gate 13608 --allow-remote --json
```

Expected output (formatted):

```json
{
  "agent_id": 13608,
  "identity_verified": true,
  "trust_score": 0.9991,
  "tier": "sovereign",
  "checks_passed": {
    "identity": true,
    "reputation": true,
    "no_recent_violations": true
  },
  "issued_at": "2026-04-18T14:50:00Z",
  "valid_until": "2026-05-18T14:50:00Z"
}
```

You can also trust-gate yourself:

```bash
ass-ade workflow trust-gate $(ass-ade config get agent_id) --allow-remote --json
```

The trust-gate checks:

1. Agent identity is registered
2. Reputation history is clean
3. No recent violations or warnings
4. Agent is in good standing

Use this before coordinating with other agents or running high-stakes workflows.

## Step 3: Certify Workflow

The certify workflow creates a formal attestation that text (code, output, or documentation) meets quality standards.

Create a test file to certify:

```bash
cat > sample_output.txt << 'EOF'
# Task Summary

I have completed the following:

1. Analyzed the codebase structure
2. Identified performance bottlenecks
3. Proposed three optimization strategies
4. Estimated implementation effort at 6-8 hours

Next steps: Review findings with team.
EOF
```

Certify the output:

```bash
ass-ade workflow certify sample_output.txt --allow-remote --json
```

Expected output:

```json
{
  "certificate_id": "cert_8f3a2b1c9d7e4a5f",
  "text_hash": "sha256:a7f3e9c2d5b8f1e4c6a9d2b7e1f4c9a8d5e2b7f1a4c9d6e3a0b5c8f1e4a7d",
  "checks": {
    "hallucination_oracle": {
      "passed": true,
      "confidence": 0.987,
      "risk_level": "low"
    },
    "toxicity_scan": {
      "passed": true,
      "score": 0.02
    },
    "factuality_check": {
      "passed": true,
      "sources_verified": 3
    }
  },
  "overall_verdict": "PASS",
  "issued_at": "2026-04-18T14:52:00Z",
  "valid_until": "2026-07-18T14:52:00Z",
  "issuer": "AAAA-Nexus Attestation Authority"
}
```

You can verify the certificate later:

```bash
ass-ade workflow certify cert_8f3a2b1c9d7e4a5f --verify --allow-remote --json
```

Use certify for:

- Attest to AI-generated code before merging
- Prove that documentation is accurate
- Create audit trails for decisions
- Validate that safety checks have been run

## Step 4: Safe-Execute Workflow

Safe-execute runs untrusted code or logic with safety gates and monitoring.

Create a sample script:

```bash
cat > sample_script.py << 'EOF'
def process_data(items):
    """Process a list of items."""
    result = []
    for item in items:
        if isinstance(item, str) and len(item) > 0:
            result.append(item.upper())
    return result

# Test
data = ["hello", "world", ""]
print(process_data(data))
EOF
```

Run it through safe-execute:

```bash
ass-ade workflow safe-execute sample_script.py --allow-remote --json
```

Expected output:

```json
{
  "execution_id": "exec_5c2a1d9e3b7f4a8c",
  "script_hash": "sha256:f1e4c9a8d5e2b7f1a4c9d6e3a0b5c8f1e4a7d2b9f3c6e1a4d7b0e3f6c9a2d",
  "sandbox_info": {
    "type": "isolated_container",
    "timeout_seconds": 30,
    "memory_limit_mb": 512
  },
  "execution_result": {
    "exit_code": 0,
    "stdout": "['HELLO', 'WORLD']",
    "stderr": "",
    "duration_ms": 145
  },
  "safety_checks": {
    "no_file_access": true,
    "no_network_access": true,
    "no_unsafe_imports": true,
    "resource_limits_respected": true
  },
  "verdict": "SAFE",
  "issued_at": "2026-04-18T14:55:00Z"
}
```

Use safe-execute for:

- Run user-submitted code safely
- Test code from untrusted sources
- Isolate side effects and verify behavior
- Create execution audit trails

## Step 5: Pipeline Composition

Compose multiple workflows into a single pipeline.

Create a pipeline definition:

```bash
cat > sample_pipeline.json << 'EOF'
{
  "name": "Code Review Pipeline",
  "steps": [
    {
      "name": "scan",
      "workflow": "safe-execute",
      "input": "sample_script.py",
      "options": {
        "timeout_seconds": 30
      }
    },
    {
      "name": "certify_execution",
      "workflow": "certify",
      "input": "result:scan.stdout",
      "options": {
        "check_hallucination": true,
        "check_toxicity": true
      }
    },
    {
      "name": "report",
      "workflow": "generate_report",
      "input": {
        "execution": "result:scan",
        "certification": "result:certify_execution"
      }
    }
  ]
}
EOF
```

Run the pipeline:

```bash
ass-ade pipeline run sample_pipeline.json --allow-remote --json
```

Expected output:

```json
{
  "pipeline_id": "pipe_9d2e5f8a1c6b3e7a",
  "name": "Code Review Pipeline",
  "status": "completed",
  "steps": [
    {
      "name": "scan",
      "status": "completed",
      "result": {
        "exit_code": 0,
        "stdout": "['HELLO', 'WORLD']"
      }
    },
    {
      "name": "certify_execution",
      "status": "completed",
      "result": {
        "certificate_id": "cert_7c4b9a2e1f6d3a5c",
        "verdict": "PASS"
      }
    },
    {
      "name": "report",
      "status": "completed",
      "result": {
        "html": "<report>...</report>",
        "summary": "Code executed safely and output verified"
      }
    }
  ],
  "overall_status": "success",
  "duration_ms": 2143,
  "issued_at": "2026-04-18T14:58:00Z"
}
```

## Step 6: Interpret Certificates

Certificates are cryptographically signed attestations. They contain:

- **certificate_id**: Unique identifier for this certificate
- **text_hash**: SHA-256 hash of what was certified (immutable)
- **checks**: Detailed results of each verification step
- **overall_verdict**: PASS, WARN, or FAIL
- **issued_at / valid_until**: Timestamp and expiration
- **issuer**: Who issued the certificate (e.g., AAAA-Nexus)

Example: Reading a certificate

```bash
ass-ade workflow certify cert_8f3a2b1c9d7e4a5f --view --allow-remote
```

Output:

```
Certificate ID:      cert_8f3a2b1c9d7e4a5f
Status:              VALID
Issued:              2026-04-18T14:52:00Z
Expires:             2026-07-18T14:52:00Z

Verified Checks:
  - Hallucination oracle: PASS (confidence 0.987)
  - Toxicity scan: PASS (score 0.02)
  - Factuality check: PASS (3 sources verified)

Text Hash: sha256:a7f3e9c2d5b8f1e4c6a9d2b7e1f4c9a8d5e2b7f1a4c9d6e3a0b5c8f1e4a7d

To verify the text hasn't changed, check its hash:
  sha256sum sample_output.txt
```

## Practical Workflows

### Workflow 1: Verify Code Before Merge

```bash
# 1. Trust-gate the code reviewer
ass-ade workflow trust-gate $(git config user.email | md5sum | cut -c1-5) \
  --allow-remote --json

# 2. Run static analysis
ass-ade workflow safe-execute lint.py --allow-remote --json

# 3. Certify the review comments
ass-ade workflow certify review_comments.md --allow-remote --json

# All results are now formally attested
```

### Workflow 2: Audit AI-Generated Documentation

```bash
# 1. Generate documentation (with your local AI)
ass-ade agent run "Write user guide for feature X" > user_guide.md

# 2. Certify the generated content
ass-ade workflow certify user_guide.md --allow-remote --json

# 3. If certification passes, it's safe to publish
```

### Workflow 3: Coordinate Multi-Agent Tasks

```bash
# 1. Verify all agents involved
for agent in 13608 13932 14256; do
  ass-ade workflow trust-gate $agent --allow-remote --json
done

# 2. Run the pipeline
ass-ade pipeline run multi-agent-tasks.json --allow-remote --json

# All decisions are recorded and auditable
```

## Cost Expectations

Each workflow call has a cost:

| Workflow | Cost | Useful For |
|----------|------|-----------|
| trust-gate | $0.040 | Verify agent identity |
| certify | $0.060 | Attest to output quality |
| safe-execute | $0.100 | Run untrusted code |
| pipeline (N steps) | $0.040 × N | Multi-step workflows |

Estimate cost before running:

```bash
ass-ade workflow certify sample_output.txt --estimate --allow-remote
```

Expected output:

```
Workflow:        certify
Steps:           4
Estimated cost:  $0.060
Duration:        ~2-3 seconds
```

## Troubleshooting

### "Certificate validation failed"

The certificate may have expired or been tampered with. Recertify:

```bash
ass-ade workflow certify fresh_output.txt --allow-remote --json
```

### "AAAA-Nexus returned 401"

Your API key is invalid or missing. Check:

```bash
echo $AAAA_NEXUS_API_KEY
```

If empty, set it:

```bash
export AAAA_NEXUS_API_KEY="your-key-here"
```

### "Request timed out"

The AAAA-Nexus service may be overloaded or you have network issues. Check service status:

```bash
ass-ade nexus health --allow-remote
```

### "Profile is local but --allow-remote was not set"

You're in local mode. Either:

1. Set `--allow-remote` flag:

```bash
ass-ade workflow trust-gate 13608 --allow-remote --json
```

2. Or change profile to hybrid:

```bash
ass-ade config set profile hybrid
```

## Verification

After completing all steps, run the full workflow stack:

```bash
# 1. Verify configuration
ass-ade doctor --remote

# 2. Trust-gate yourself
ass-ade workflow trust-gate $(ass-ade config get agent_id) --allow-remote --json

# 3. Certify a sample document
echo "Test document" > test.txt
ass-ade workflow certify test.txt --allow-remote --json

# All should succeed
```

## Next Steps

1. Integrate hybrid workflows into your CI/CD pipeline
2. Use trust-gate for multi-agent coordination
3. Create audit trails with certify for important decisions
4. Compose reusable pipelines for common patterns

## Resources

- [../docs/remote-hybrid-guide.md](../../docs/remote-hybrid-guide.md) — Hybrid mode guide
- [../docs/architecture.md](../../docs/architecture.md) — Architecture details
- `ass-ade workflow --help` — Workflow reference
- `ass-ade pipeline --help` — Pipeline reference
