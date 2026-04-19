"""v18 pillar 79 — 50 audit questions for WisdomEngine cycle review."""
from __future__ import annotations


AUDIT_QUESTIONS: list[dict] = [
    # foundational (ids 1-10) — epistemic rigor, tier classification, routing
    {"id": 1, "group": "foundational", "text": "Was epistemic tier classification applied before acting? (local vs hybrid vs premium)"},
    {"id": 2, "group": "foundational", "text": "Was task complexity scored and routed to the appropriate model tier?"},
    {"id": 3, "group": "foundational", "text": "Were all required capabilities confirmed present before starting work?"},
    {"id": 4, "group": "foundational", "text": "Was a recon pass performed to identify relevant code and context?"},
    {"id": 5, "group": "foundational", "text": "Were assumptions explicitly stated rather than silently applied?"},
    {"id": 6, "group": "foundational", "text": "Was the user's intent validated against the actual implementation?"},
    {"id": 7, "group": "foundational", "text": "Were any capability gaps detected and surfaced before proceeding?"},
    {"id": 8, "group": "foundational", "text": "Was the working directory and project context established correctly?"},
    {"id": 9, "group": "foundational", "text": "Was the problem scope bounded to avoid over-engineering?"},
    {"id": 10, "group": "foundational", "text": "Were ambiguous requirements clarified before implementation?"},
    # operational (ids 11-20) — token efficiency, tool use, execution
    {"id": 11, "group": "operational", "text": "Was token budget tracked and respected throughout the session?"},
    {"id": 12, "group": "operational", "text": "Were tool calls minimized to those strictly necessary?"},
    {"id": 13, "group": "operational", "text": "Was the read-before-write discipline applied to all file edits?"},
    {"id": 14, "group": "operational", "text": "Were parallel tool calls used where operations were independent?"},
    {"id": 15, "group": "operational", "text": "Was context trimmed before exceeding the model's window?"},
    {"id": 16, "group": "operational", "text": "Were large outputs truncated rather than fully loaded into context?"},
    {"id": 17, "group": "operational", "text": "Was the correct tool selected for each operation (e.g., Grep vs Read)?"},
    {"id": 18, "group": "operational", "text": "Were command timeouts respected and long-running ops backgrounded?"},
    {"id": 19, "group": "operational", "text": "Was output validated before being presented to the user?"},
    {"id": 20, "group": "operational", "text": "Were error messages parsed and root causes identified rather than retried blindly?"},
    # autonomous (ids 21-30) — memory, persistence, learning
    {"id": 21, "group": "autonomous", "text": "Was persistent memory consulted before starting a known task type?"},
    {"id": 22, "group": "autonomous", "text": "Were relevant prior solutions retrieved from vector memory?"},
    {"id": 23, "group": "autonomous", "text": "Were session insights captured for future recall?"},
    {"id": 24, "group": "autonomous", "text": "Was the LIFR knowledge graph queried for verified code patterns?"},
    {"id": 25, "group": "autonomous", "text": "Were experience traces stored after each significant action?"},
    {"id": 26, "group": "autonomous", "text": "Was deduplication applied before storing new memory entries?"},
    {"id": 27, "group": "autonomous", "text": "Were stale memories identified and pruned?"},
    {"id": 28, "group": "autonomous", "text": "Were principles distilled from audit failures and stored?"},
    {"id": 29, "group": "autonomous", "text": "Was the EDEE experience memory updated with the session outcome?"},
    {"id": 30, "group": "autonomous", "text": "Were learned patterns applied to improve response quality?"},
    # meta_cognition (ids 31-40) — self-reflection, quality, conviction
    {"id": 31, "group": "meta_cognition", "text": "Was a self-consistency check performed on the final response?"},
    {"id": 32, "group": "meta_cognition", "text": "Was conviction above the required threshold before taking high-risk actions?"},
    {"id": 33, "group": "meta_cognition", "text": "Were hallucination signals checked and flagged for the user?"},
    {"id": 34, "group": "meta_cognition", "text": "Was the output certified against quality rubric criteria?"},
    {"id": 35, "group": "meta_cognition", "text": "Were security implications considered for every code change?"},
    {"id": 36, "group": "meta_cognition", "text": "Were OWASP patterns scanned for in generated code?"},
    {"id": 37, "group": "meta_cognition", "text": "Was cyclomatic complexity within acceptable bounds?"},
    {"id": 38, "group": "meta_cognition", "text": "Was the response reviewed for completeness before delivery?"},
    {"id": 39, "group": "meta_cognition", "text": "Were test cases considered for all new functionality?"},
    {"id": 40, "group": "meta_cognition", "text": "Was the audit score trend monitored for regression?"},
    # hyperagent (ids 41-50) — v18 engine integration
    {"id": 41, "group": "hyperagent", "text": "MAP=TERRAIN verdict recorded and acted upon?"},
    {"id": 42, "group": "hyperagent", "text": "MCP-Zero semantic routing used instead of eager schema loading?"},
    {"id": 43, "group": "hyperagent", "text": "EXIF loop spawned if a required skill was missing?"},
    {"id": 44, "group": "hyperagent", "text": "CASCADE meta-skills activated for multi-step skill acquisition?"},
    {"id": 45, "group": "hyperagent", "text": "LIFR graph queried and updated with verified patterns?"},
    {"id": 46, "group": "hyperagent", "text": "ATLAS decomposition applied for tasks with complexity > 0.7?"},
    {"id": 47, "group": "hyperagent", "text": "TDMI synergy computed and emergence flag set if above threshold?"},
    {"id": 48, "group": "hyperagent", "text": "Puppeteer DAG used to sequence engine invocations?"},
    {"id": 49, "group": "hyperagent", "text": "Meta-edit validated against golden tasks before committing?"},
    {"id": 50, "group": "hyperagent", "text": "Prompt evolution validated via prompt_toolkit before applying?"},
]

assert len(AUDIT_QUESTIONS) == 50
