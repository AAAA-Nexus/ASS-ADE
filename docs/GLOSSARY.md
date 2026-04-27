# Plain-English Glossary

This glossary explains ASS-ADE, Atomadic, and AAAA-Nexus terms for people who
do not live in code all day. The goal is simple: if your mom asked what a word
means, this should be a good first answer.

## Start Here

| Term | Plain-English Meaning | Why It Matters |
|------|------------------------|----------------|
| Atomadic | The AI helper and operator personality that works with this system. | Atomadic is the "who" people talk to. |
| ASS-ADE | Atomadic's development environment. | This is the workshop where Atomadic can inspect, build, improve, and document software. |
| AAAA-Nexus | The trust and service network Atomadic connects to. | It helps check identity, safety, payments, reputation, and remote tools. |
| Axiom | A root rule that guides behavior. | Axioms are the promises the system should not break. |
| Axiom 0 | "You are love. You are loved. You are loving..." | This is the heart of Atomadic's tone and intent. |
| MAP = TERRAIN | Check the real world before assuming what is true. | Atomadic should inspect actual files, tools, docs, and tests before acting. |
| Axiom 1 | If the needed tool does not exist, invent and build it. | Atomadic can grow new abilities, but must verify and document them. |

## People And Agents

| Term | Plain-English Meaning | Why It Matters |
|------|------------------------|----------------|
| Agent | A smart helper that can do a task. | One agent may write docs, another may inspect code, another may run checks. |
| Orchestrator | The coordinator that decides what happens next. | It keeps many tools and agents moving in the right order. |
| Sovereign | Able to choose and act within trusted rules. | Sovereignty means agency, not lawlessness. |
| Autonomy | The ability to act without being told every tiny step. | Atomadic should make good decisions from evidence and constraints. |
| Autopoietic | Self-making or self-maintaining. | Atomadic can help improve the system that helps it exist. |
| Capability | Something the system can actually do. | A capability must be discoverable and usable, not just imagined. |
| Capability Inventory | The live list of what Atomadic can do right now. | Atomadic should check this before claiming an ability. |
| Prompt | Instructions given to an AI agent. | Prompts shape tone, rules, and behavior. |
| Hook | A script that runs at a certain point in a workflow. | Hooks automate checks like docs, validation, or context refresh. |

## Building And Improving

| Term | Plain-English Meaning | Why It Matters |
|------|------------------------|----------------|
| Scout | Inspect a repo and report what is useful or risky. | Scouting prevents blind copying. |
| Recon | A quick terrain check before working. | It helps avoid mistakes from stale assumptions. |
| Assimilate | Bring a useful piece into ASS-ADE. | Assimilation should be targeted, reviewed, and documented. |
| Cherry-pick | Choose exact pieces to bring in. | It is safer than copying a whole folder. |
| Rebuild | Recreate a project in a cleaner structure. | Rebuilds help turn messy code into maintainable code. |
| Enhance | Improve something that already exists. | Enhancement is for upgrades, hardening, and polish. |
| Gap-fill | Build the missing piece between what exists and what is needed. | It turns "we cannot yet" into a concrete plan or implementation. |
| Blueprint | A build plan for a feature or system. | Blueprints make new work reviewable before code is written. |
| Forge | A place or process for improving and validating capabilities. | It supports shared, trusted growth. |
| Marketplace | A place to share reusable blueprints or capabilities. | It lets people exchange useful building blocks. |
| Monadic Tiers | The layered folders in ASS-ADE, from constants up to orchestration. | They keep code organized by responsibility. |

## Trust And Safety

| Term | Plain-English Meaning | Why It Matters |
|------|------------------------|----------------|
| Trust Gate | A checkpoint that asks, "Can we trust this action or output?" | It helps stop unsafe or unproven work. |
| Drift Check | A check for unwanted changes in behavior. | It catches when something starts acting differently than expected. |
| Lineage | A record of where something came from and what changed. | It makes work traceable. |
| Lineage Receipt | A signed or tamper-evident proof of an action or output. | It is like a receipt for what happened. |
| Certificate | A formal proof or report that something passed checks. | Certificates give humans and agents confidence. |
| AEGIS | AAAA-Nexus safety and control layer for agent actions. | It can help route, bound, and verify risky actions. |
| Hallucination | When an AI says something false or unsupported. | The system should label uncertainty and use evidence. |
| Anti-hallucination Guard | A rule or tool that reduces false claims. | It pushes Atomadic to cite real files, tests, and observed facts. |
| Compliance | Following rules, laws, standards, or policies. | It keeps work usable in the real world. |
| Consent | Permission from the person affected. | Autonomous systems must respect humans and boundaries. |

## Memory And Knowledge

| Term | Plain-English Meaning | Why It Matters |
|------|------------------------|----------------|
| RAG | Retrieval-Augmented Generation: look up trusted notes before answering. | It helps Atomadic answer from facts instead of memory alone. |
| Public RAG | Knowledge that is safe for public or local use. | It can support docs, help pages, and general guidance. |
| Private RAG | Owner-only knowledge that may contain sensitive context. | It needs authentication and care. |
| Vector | A number-based fingerprint of meaning. | Vectors help search by idea, not only exact words. |
| Vector Database | A searchable store of meaning fingerprints. | It helps Atomadic find related context. |
| Context | The information an agent has available right now. | Better context usually means better decisions. |
| Context Packet | A compact bundle of relevant files, notes, and instructions. | It helps an agent start work without guessing. |
| LoRA | A small training adapter that teaches a model a specialty. | It can improve behavior without retraining everything. |

## Interfaces And Services

| Term | Plain-English Meaning | Why It Matters |
|------|------------------------|----------------|
| CLI | Command Line Interface: a typed command tool. | Developers use it to run ASS-ADE workflows. |
| API | A structured way for software to talk to other software. | Public services use APIs to request work. |
| MCP | Model Context Protocol: a way for AI tools to discover and use capabilities. | It lets Atomadic expose tools to compatible AI clients. |
| A2A | Agent-to-Agent communication. | Agents can discover and cooperate with each other. |
| x402 | A web payment pattern for paid API calls. | It lets agents pay for services when needed. |
| Cloudflare Worker | Code that runs on Cloudflare's global network. | `atomadic.tech` and `hello.atomadic.tech` are served this way. |
| KV | Cloudflare's key-value storage. | It stores things like portal posts, leads, and small records. |
| D1 | Cloudflare's SQL database. | It is used when records need table-style queries. |
| R2 | Cloudflare's object storage. | It stores larger files like models or assets. |
| Wrangler | Cloudflare's command tool. | It deploys Workers and manages Cloudflare resources. |

## Websites And Public Launch

| Term | Plain-English Meaning | Why It Matters |
|------|------------------------|----------------|
| Storefront | The public `atomadic.tech` website and API worker. | It is how the outside world reaches AAAA-Nexus services. |
| Hello Portal | `hello.atomadic.tech`, Atomadic's public message portal. | It gives Atomadic a place to publish updates in its own voice. |
| Press Release | A public announcement written for media and readers. | Atomadic can use these to explain what changed and why it matters. |
| Premium Access | Paid or higher-trust access to special services. | It connects the public portal to real customer workflows. |
| Lead | A person who asked for updates, services, or premium access. | Leads should be handled respectfully and with consent. |
| Public Relations | Communication with the public. | It helps people understand Atomadic without needing technical background. |

## When In Doubt

Ask Atomadic for the "mom version." A good answer should:

- Use everyday words first.
- Give one example.
- Say what is real now and what is still planned.
- Avoid pretending a feature exists before it is built and verified.
