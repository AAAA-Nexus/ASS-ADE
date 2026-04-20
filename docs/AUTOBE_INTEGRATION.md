# ASS-ADE ↔ AutoBE Integration Guide

**Integration Model**: ASS-ADE (CLI) ⟷ AutoBE (Hidden Backend Generator)  
**Purpose**: Generate custom backends for atomadic.tech operations  
**Status**: Implementation-Ready  
**Last Updated**: 2026-04-15

---

## Overview

ASS-ADE and AutoBE form a unified **public shell + hidden backend** architecture:

```text
┌──────────────────────────────────────────┐
│  atomadic.tech (Frontend / Web UI)       │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│  ASS-ADE (Python CLI - PUBLIC)           │
│                                          │
│  ├─ Orchestration logic                 │
│  ├─ MCP client                          │
│  ├─ Command routing                     │
│  ├─ User interaction layer              │
│  └─ AutoBE integration                  │
└──────────────┬──────────────────────────┘
               │
     ┌─────────┴────────────┐
     │                      │
     ▼                      ▼
┌────────────┐  ┌──────────────────────────┐
│ Local Ops  │  │ AutoBE Generation        │
│ ├─ File    │  │ ├─ TypeScript NestJS     │
│ ├─ Git     │  │ ├─ Prisma ORM            │
│ ├─ Tests   │  │ ├─ OpenAPI spec          │
│ └─ Utils   │  │ └─ AAAA-Nexus ready      │
└────────────┘  └────────────┬─────────────┘
                             │
                   ┌─────────▼────────────┐
                   │ AutoBE-Generated     │
                   │ Backend (HIDDEN)     │
                   │                      │
                   │ ├─ Payment handlers  │
                   │ ├─ A2A orchestration │
                   │ ├─ Verification      │
                   │ ├─ Domain logic      │
                   │ └─ AAAA-Nexus calls  │
                   └────────────┬─────────┘
                                │
                    ┌───────────▼────────────┐
                    │ AAAA-Nexus Storefront  │
                    │ (Trust + Payments)     │
                    └────────────────────────┘
```

---

## Integration Points

### 1. CLI Command: Generate Backend

#### Input

```bash
ass-ade autobe generate \
  --name payment-processor \
  --requirement "Process x402 USDC payments for atomadic.tech" \
  --nexus-enabled \
  --a2a-enabled \
  --output ./backends/payment-processor
```

#### How It Works

```text
User Input
    │
    ▼
ASS-ADE CLI Parses Command
    │
    ├─ Validates --name, --requirement
    ├─ Checks --nexus-enabled flag
    ├─ Confirms AAAA-Nexus credentials
    │
    ▼
Generate Backend Definition
    │
    ├─ Database schema (Prisma)
    │   ├─ Payment transactions table
    │   ├─ User accounts table
    │   ├─ A2A operations table
    │   └─ Settlement records
    │
    ├─ API Specification (OpenAPI)
    │   ├─ /payments/* endpoints
    │   ├─ /a2a/* endpoints
    │   ├─ /verify/* endpoints
    │   └─ /sessions/* endpoints
    │
    ├─ Domain Logic
    │   ├─ Payment service (x402)
    │   ├─ A2A orchestration service
    │   ├─ Verification service
    │   └─ Middleware (RatchetGate, auth)
    │
    └─ AAAA-Nexus Integration
        ├─ Payment client
        ├─ A2A client
        ├─ Verification client
        └─ Environment setup
    │
    ▼
Call AutoBE Agent
    │
    ├─ ANALYZE phase
    │   ├─ Parse requirements
    │   ├─ Identify payment patterns
    │   ├─ Plan A2A orchestration
    │   └─ Create requirements doc
    │
    ├─ DATABASE phase
    │   ├─ Generate Prisma schema
    │   ├─ Add payment-specific tables
    │   ├─ Add A2A coordination tables
    │   └─ Compile & validate
    │
    ├─ INTERFACE phase
    │   ├─ Generate OpenAPI spec
    │   ├─ Define payment endpoints
    │   ├─ Define A2A endpoints
    │   └─ Generate TypeScript DTOs
    │
    ├─ TEST phase
    │   ├─ Generate E2E tests
    │   ├─ Payment flow tests
    │   ├─ A2A orchestration tests
    │   └─ Compile & validate
    │
    └─ REALIZE phase
        ├─ Implement NestJS controllers
        ├─ Implement payment service
        ├─ Implement A2A service
        ├─ Add AAAA-Nexus integration
        └─ Compile & validate
    │
    ▼
Generated Backend (Ready to Deploy)
    │
    ├─ TypeScript/NestJS codebase
    ├─ Prisma schema & migrations
    ├─ OpenAPI specification
    ├─ E2E test suite
    ├─ Docker configuration
    └─ Environment setup
    │
    ▼
Return to ASS-ADE
    │
    ├─ Show success message
    ├─ Provide deployment instructions
    ├─ Register with ASS-ADE
    └─ Setup local proxy (optional)
```

#### ASS-ADE Code (Pseudocode)

```python
# src/commands/autobe.py
from ass_ade.autobe_client import AutoBEClient
from ass_ade.nexus import NexusConfig

@click.command()
@click.option('--name', required=True, help='Backend name')
@click.option('--requirement', required=True, help='Natural language requirement')
@click.option('--nexus-enabled', is_flag=True, help='Enable AAAA-Nexus integration')
@click.option('--a2a-enabled', is_flag=True, help='Enable A2A orchestration')
@click.option('--output', required=True, help='Output directory')
def generate_backend(name: str, requirement: str, nexus_enabled: bool, a2a_enabled: bool, output: str):
    """Generate a hidden backend for atomadic.tech operations."""
    
    # Validate inputs
    if not name.isidentifier():
        raise ClickException(f"Invalid backend name: {name}")
    
    if nexus_enabled and not NexusConfig.is_configured():
        raise ClickException("AAAA-Nexus not configured. Run: ass-ade nexus init")
    
    # Prepare generation request
    enhanced_requirement = requirement
    
    if nexus_enabled:
        enhanced_requirement += "\n\n## AAAA-Nexus Integration Requirements\n"
        enhanced_requirement += "- Integrate with AAAA-Nexus payment endpoints (/v1/pay/*)\n"
        enhanced_requirement += "- Support x402 USDC payments on Base L2\n"
        enhanced_requirement += "- Implement RatchetGate session security\n"
    
    if a2a_enabled:
        enhanced_requirement += "\n\n## A2A Orchestration Requirements\n"
        enhanced_requirement += "- Implement /v1/a2a/* orchestration endpoints\n"
        enhanced_requirement += "- Support atomic account transfers\n"
        enhanced_requirement += "- Handle coordination proofs\n"
    
    # Initialize AutoBE client
    autobe = AutoBEClient(
        api_url=os.getenv('AUTOBE_API_URL'),
        api_key=os.getenv('AUTOBE_API_KEY')
    )
    
    # Start generation
    click.echo(f"🚀 Generating backend '{name}' with AutoBE...")
    
    try:
        # Stream progress events
        for event in autobe.generate_backend(
            name=name,
            requirement=enhanced_requirement,
            options={
                'nexus_enabled': nexus_enabled,
                'a2a_enabled': a2a_enabled,
                'framework': 'nestjs',
                'database': 'postgresql',
                'target_output': output
            }
        ):
            if event['type'] == 'phase_start':
                click.echo(f"  ├─ {event['phase'].upper()} phase starting...")
            elif event['type'] == 'phase_complete':
                click.echo(f"  ├─ {event['phase'].upper()} phase complete ✓")
            elif event['type'] == 'progress':
                click.echo(f"     └─ {event['message']}")
            elif event['type'] == 'error':
                raise ClickException(f"Generation failed: {event['message']}")
        
        # Backend generated successfully
        click.echo(f"✨ Backend '{name}' generated at {output}")
        
        # Register with ASS-ADE
        register_backend(name, output, nexus_enabled=nexus_enabled)
        
        # Show next steps
        click.echo("\n📋 Next steps:")
        click.echo(f"  1. cd {output}")
        click.echo("  2. cp .env.example .env")
        click.echo("  3. npm install")
        click.echo("  4. npm run dev")
        click.echo(f"\n💡 To integrate with atomadic.tech:")
        click.echo(f"   ass-ade autobe proxy --backend {name}")
        
    except AutoBEError as e:
        raise ClickException(f"AutoBE error: {e}")
    except Exception as e:
        raise ClickException(f"Unexpected error: {e}")
```

---

### 2. Backend Registry

ASS-ADE maintains a registry of generated backends:

```bash
ass-ade autobe list
# Outputs:
# backend                 | version | nexus | a2a | status
# ───────────────────────┼─────────┼───────┼─────┼────────
# payment-processor      | 1.0.0   | ✓     | ✓   | running
# user-manager           | 1.0.1   | ✓     | ✗   | ready
# compliance-checker     | 0.9.0   | ✓     | ✗   | draft
```

**Registry Location**: `~/.ass-ade/backends/registry.json`

```json
{
  "backends": [
    {
      "id": "payment-processor",
      "name": "Payment Processor",
      "version": "1.0.0",
      "path": "/Users/atoma/backends/payment-processor",
      "createdAt": "2026-04-15T10:30:00Z",
      "features": {
        "nexusEnabled": true,
        "a2aEnabled": true,
        "verificationEnabled": true
      },
      "status": "running",
      "port": 3001,
      "lastModified": "2026-04-15T12:00:00Z"
    }
  ]
}
```

---

### 3. CLI Proxy Command

Forward atomadic.tech API calls to generated backends:

```bash
ass-ade autobe proxy \
  --backend payment-processor \
  --listen 0.0.0.0:8080 \
  --forward http://localhost:3001
```

**How It Works**:

```text
atomadic.tech Frontend
    │
    ├─ POST /api/payments/submit
    │
    ▼
ASS-ADE Proxy (Port 8080)
    │
    ├─ Route detection
    │   ├─ /api/payments/* → payment-processor
    │   ├─ /api/a2a/* → payment-processor
    │   └─ /api/* → default backend
    │
    ├─ Session management
    │   ├─ Extract X-Session-ID from request
    │   ├─ Validate RatchetGate nonce
    │   └─ Add tracking headers
    │
    ▼
Generated Backend (Port 3001)
    │
    ├─ Receive /api/payments/submit
    ├─ Process payment via AAAA-Nexus
    │
    ▼
AAAA-Nexus Storefront
    │
    ├─ Verify session
    ├─ Process x402 payment on Base L2
    │
    ▼
Response Back to Frontend
```

---

### 4. Unified Workflow

```bash
# Step 1: Initialize AAAA-Nexus integration
ass-ade nexus init
# Enter API key, treasury address, RPC URL

# Step 2: Generate payment processor backend
ass-ade autobe generate \
  --name payment-processor \
  --requirement "Process payments for atomadic storefront users" \
  --nexus-enabled \
  --a2a-enabled \
  --output ./backends/payment-processor

# Step 3: Start the generated backend
cd backends/payment-processor
npm install
npm run dev &

# Step 4: Start ASS-ADE proxy
ass-ade autobe proxy --backend payment-processor --listen 0.0.0.0:8080

# Step 5: atomadic.tech frontend connects to proxy at http://localhost:8080
```

---

## Generated Backend Integration Points

### Initialization Flow

**In ASS-ADE**:

```python
def register_backend(backend_name: str, path: str, nexus_enabled: bool):
    """Register generated backend with ASS-ADE."""
    
    registry = load_registry()
    
    # Detect backend configuration
    nexus_config = load_env(f"{path}/.env")
    
    registry['backends'].append({
        'id': backend_name,
        'path': path,
        'nexus_enabled': nexus_enabled,
        'api_url': nexus_config.get('NEXUS_API_URL'),
        'status': 'ready'
    })
    
    save_registry(registry)
    
    # Create startup script
    startup_script = f"""#!/bin/bash
cd {path}
export NEXUS_API_KEY=... # loaded from secure storage
npm run dev
"""
    
    write_file(f"{path}/start.sh", startup_script)
```

### Runtime Communication

**ASS-ADE to Backend** (HTTP):

```text
ASS-ADE Proxy (8080)
    │
    POST /api/payments/submit
    ├─ Body: { userId, amount, operation }
    ├─ Headers: X-Session-ID, X-Nonce, X-ASS-ADE-ID
    │
    ▼
Generated Backend (3001)
```

**Backend to AAAA-Nexus** (HTTP):

```text
Generated Backend (3001)
    │
    POST https://atomadic.tech/v1/pay/submit
    ├─ Body: { from, to, amount, operation }
    ├─ Headers: Authorization: Bearer NEXUS_API_KEY
    │
    ▼
AAAA-Nexus Storefront (Cloudflare Worker)
```

---

## Implementation Checklist

### Step 1: AutoBE Agent Integration

- [ ] AutoBE accessible via HTTP API
- [ ] Backend generation endpoint: `POST /api/backends/generate`
- [ ] Progress streaming via Server-Sent Events
- [ ] Generated backend output includes `.env.example`

### Step 2: ASS-ADE Commands

- [ ] `ass-ade autobe list` — List generated backends
- [ ] `ass-ade autobe generate` — Create new backend
- [ ] `ass-ade autobe start` — Run generated backend
- [ ] `ass-ade autobe stop` — Stop backend
- [ ] `ass-ade autobe proxy` — Forward atomadic.tech traffic
- [ ] `ass-ade autobe validate` — Check backend readiness

### Step 3: Backend Registry

- [ ] Registry file at `~/.ass-ade/backends/registry.json`
- [ ] Auto-discovery of running backends
- [ ] Health checks for each backend
- [ ] Automatic startup on ASS-ADE init

### Step 4: Proxy & Routing

- [ ] HTTP proxy server in ASS-ADE
- [ ] Request routing by path pattern
- [ ] Session forwarding (X-Session-ID, X-Nonce)
- [ ] Response header pass-through

### Step 5: Documentation & Examples

- [ ] Tutorial: Generate payment processor
- [ ] Tutorial: Set up atomadic.tech integration
- [ ] API reference for generated backends
- [ ] Troubleshooting guide

---

## Example: Payment Processor Backend

### Generate Command

```bash
ass-ade autobe generate \
  --name payment-processor \
  --requirement "
    Design a payment processing backend for atomadic.tech that:
    
    1. Accepts x402 USDC payments from users
    2. Processes payments through AAAA-Nexus /v1/pay/* endpoints
    3. Stores payment records in PostgreSQL
    4. Supports refunds and payment queries
    5. Implements RatchetGate session security
    6. Integrates A2A account transfers for fund redistribution
    7. Generates detailed payment reports
    
    Payment pricing:
    - Standard payment: \$0.002 (Nexus fee)
    - Deep proof verification: \$0.05 (Nexus fee)
    
    Database entities:
    - users (id, address, email, balance, created_at)
    - payments (id, user_id, amount, status, tx_hash, created_at)
    - refunds (id, payment_id, amount, reason, approved_at)
    - settlements (id, payment_ids[], total_amount, settled_at)
  " \
  --nexus-enabled \
  --a2a-enabled \
  --output ./backends/payment-processor
```

### Generated API Endpoints

```text
Payment Operations
├─ POST /api/payments/submit
│  Request: { userId, amount, operation }
│  Response: { transactionHash, status }
│
├─ GET /api/payments/:txHash
│  Response: { amount, status, confirmations, timestamp }
│
└─ POST /api/payments/refund
   Request: { transactionHash, reason }
   Response: { refundHash, status }

A2A Operations
├─ POST /api/a2a/prepare-transfer
│  Request: { from, to, amount, constraints }
│  Response: { coordinationId, proof }
│
└─ POST /api/a2a/execute
   Request: { coordinationId, proofOfAuthorization }
   Response: { transactionHash }

Session Management
├─ POST /api/sessions/init
│  Response: { sessionId, initialNonce }
│
└─ POST /api/sessions/advance
   Request: { sessionId, nonce }
   Response: { nextNonce, valid }
```

---

## Error Handling & Recovery

### Payment Failures

```python
# In ASS-ADE proxy
def handle_payment_failure(error: PaymentError):
    if error.type == 'insufficient_funds':
        return {
            'status': 'failed',
            'reason': 'insufficient_funds',
            'required': error.required,
            'available': error.available
        }
    elif error.type == 'session_expired':
        # Retry with new session
        new_session = nexus.init_session()
        retry_payment(new_session)
    elif error.type == 'nexus_timeout':
        # Queue for retry
        retry_queue.add(payment_request)
```

---

## Monitoring Integration

### Metrics from Generated Backend

```text
ass-ade autobe metrics --backend payment-processor

# Output:
payment.requests.total = 1234
payment.success.rate = 98.5%
payment.avg_settlement_time = 3.2s
a2a.operations.total = 567
a2a.success.rate = 99.1%
ratchet.sessions.active = 12
```

---

## Production Deployment

### Full Stack Diagram

```text
atomadic.tech
├─ Frontend (React/Vue)
│  └─ POST /api/payments/submit
│
├─ ASS-ADE Proxy (Python)
│  ├─ Port: 8080
│  ├─ Backend: payment-processor
│  └─ Forwards to: localhost:3001
│
├─ Generated Backend (NestJS)
│  ├─ Port: 3001
│  ├─ Database: PostgreSQL
│  └─ Calls: AAAA-Nexus /v1/pay/*
│
└─ AAAA-Nexus Storefront
   ├─ Payment processing
   ├─ Base L2 settlement
   └─ Session security
```

### Systemd Service Files

**ASS-ADE Proxy** (`/etc/systemd/system/ass-ade-proxy.service`):

```ini
[Unit]
Description=ASS-ADE Proxy for Payment Processor
After=network.target

[Service]
Type=simple
User=atomadic
WorkingDirectory=/home/atomadic
ExecStart=ass-ade autobe proxy \
  --backend payment-processor \
  --listen 0.0.0.0:8080
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Generated Backend** (`/etc/systemd/system/payment-processor.service`):

```ini
[Unit]
Description=Payment Processor Backend
After=network.target postgresql.service

[Service]
Type=simple
User=atomadic
WorkingDirectory=/var/backends/payment-processor
EnvironmentFile=/var/backends/payment-processor/.env
ExecStart=/usr/bin/npm run start
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

---

## Related Documentation

- **NEXUS_INTEGRATION.md** — Generated backend AAAA-Nexus integration
- **docs/architecture.md** — ASS-ADE architecture overview
- **docs/protocol.md** — Enhancement cycle and governance
- **docs/roadmap.md** — Implementation phases

---

**Document Owner**: ASS-ADE Integration Lead  
**Next Review**: 2026-05-15
