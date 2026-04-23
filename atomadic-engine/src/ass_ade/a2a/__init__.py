"""A2A (Agent-to-Agent) interop — agent card validation and negotiation.

Implements the A2A specification for agent discovery and capability
negotiation. ASS-ADE can:

  1. Fetch and validate remote agent cards from /.well-known/agent.json
  2. Validate agent cards against the A2A schema
  3. Compare two agent cards for capability overlap (negotiation)
  4. Generate a local agent card for ASS-ADE itself

The A2A spec defines an agent card as a JSON document at a well-known URL
that advertises an agent's identity, capabilities, skills, authentication
requirements, and pricing. This module provides typed models and validation
without depending on any private backend logic.

References:
  - Google A2A spec: https://google.github.io/A2A/
  - AAAA-Nexus agent card: https://atomadic.tech/.well-known/agent.json
"""

from __future__ import annotations

import json
import socket
from dataclasses import dataclass, field
from typing import Any
from urllib.parse import urlparse

import httpx
from pydantic import BaseModel, Field, ValidationError, field_validator

from ass_ade import __version__
from ass_ade.nexus.validation import validate_https_public_url


def _check_ssrf(url: str) -> str | None:
    """Return an error message if the URL is unsafe, else None."""
    try:
        validate_https_public_url(url, field_name="Agent card URL")
    except ValueError as exc:
        return str(exc)
    return None

# ── A2A Agent Card models (public spec) ───────────────────────────────────────


class A2ASkill(BaseModel):
    """A single skill advertised by an agent."""

    id: str
    name: str
    description: str = ""
    tags: list[str] = Field(default_factory=list)
    examples: list[str] = Field(default_factory=list)


class A2AAuthentication(BaseModel):
    """Authentication requirements for the agent."""

    schemes: list[str] = Field(default_factory=list)  # e.g. ["bearer", "x402"]
    credentials: str | None = None  # human-readable note


class A2AProvider(BaseModel):
    """Organization or individual providing the agent."""

    organization: str = ""
    url: str = ""


class A2ACapabilities(BaseModel):
    """Agent capability flags per A2A spec."""

    streaming: bool = False
    pushNotifications: bool = False
    stateTransitionHistory: bool = False


class A2AAgentCard(BaseModel):
    """Full A2A agent card — the public identity manifest.

    Fetched from /.well-known/agent.json per the A2A specification.
    """

    name: str
    description: str = ""
    url: str = ""
    version: str = ""
    provider: A2AProvider | None = None
    capabilities: A2ACapabilities = Field(default_factory=A2ACapabilities)
    authentication: A2AAuthentication | None = None
    skills: list[A2ASkill] = Field(default_factory=list)
    defaultInputModes: list[str] = Field(default_factory=lambda: ["text/plain"])
    defaultOutputModes: list[str] = Field(default_factory=lambda: ["text/plain"])

    # Extension fields (non-standard but useful)
    payment: dict[str, Any] | None = None
    endpoints: str | None = None

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Agent card name must not be empty")
        return v


# ── Validation ────────────────────────────────────────────────────────────────


@dataclass
class ValidationIssue:
    """A single validation finding."""

    severity: str  # "error" | "warning" | "info"
    field: str
    message: str


@dataclass
class ValidationReport:
    """Result of validating an agent card."""

    valid: bool
    issues: list[ValidationIssue] = field(default_factory=list)
    card: A2AAgentCard | None = None

    @property
    def errors(self) -> list[ValidationIssue]:
        return [i for i in self.issues if i.severity == "error"]

    @property
    def warnings(self) -> list[ValidationIssue]:
        return [i for i in self.issues if i.severity == "warning"]


def validate_agent_card(data: dict[str, Any]) -> ValidationReport:
    """Validate a raw dict against the A2A agent card schema.

    Returns a ValidationReport with structured findings.
    """
    issues: list[ValidationIssue] = []

    # Required fields
    if "name" not in data or not data.get("name", "").strip():
        issues.append(ValidationIssue("error", "name", "Agent card must have a non-empty 'name' field"))

    # Parse into model
    try:
        card = A2AAgentCard.model_validate(data)
    except ValidationError as exc:
        issues.append(ValidationIssue("error", "_parse", f"Failed to parse agent card: {exc}"))
        return ValidationReport(valid=False, issues=issues)

    # Structural warnings
    if not card.description:
        issues.append(ValidationIssue("warning", "description", "Missing description — agents should describe themselves"))

    if not card.url:
        issues.append(ValidationIssue("warning", "url", "Missing url — no way to reach this agent"))
    elif card.url:
        parsed = urlparse(card.url)
        if parsed.scheme not in ("http", "https"):
            issues.append(ValidationIssue("error", "url", f"Invalid URL scheme: {parsed.scheme}"))

    if not card.version:
        issues.append(ValidationIssue("warning", "version", "Missing version — consider semver"))

    if not card.skills:
        issues.append(ValidationIssue("warning", "skills", "No skills advertised — agent has no discoverable capabilities"))

    for i, skill in enumerate(card.skills):
        if not skill.id:
            issues.append(ValidationIssue("error", f"skills[{i}].id", "Skill must have an id"))
        if not skill.name:
            issues.append(ValidationIssue("error", f"skills[{i}].name", "Skill must have a name"))

    if card.authentication and not card.authentication.schemes:
        issues.append(ValidationIssue("warning", "authentication.schemes", "Authentication declared but no schemes listed"))

    has_errors = any(i.severity == "error" for i in issues)
    return ValidationReport(valid=not has_errors, issues=issues, card=card)


# ── Fetching ──────────────────────────────────────────────────────────────────


def fetch_agent_card(url: str, *, timeout: float = 10.0) -> ValidationReport:
    """Fetch and validate an agent card from a URL.

    If the URL doesn't end with /.well-known/agent.json, it is appended.
    
    SSRF validation is performed immediately before the network request to
    minimize the DNS rebinding TOCTOU window (time-of-check to time-of-use).
    """
    if not url.endswith("/.well-known/agent.json"):
        url = url.rstrip("/") + "/.well-known/agent.json"

    # Early format check only (hostname, scheme)
    parsed = urlparse(url)
    if parsed.scheme != "https":
        return ValidationReport(
            valid=False,
            issues=[ValidationIssue("error", "_fetch", "Only HTTPS URLs are permitted for agent card fetching.")],
        )
    if not parsed.hostname:
        return ValidationReport(
            valid=False,
            issues=[ValidationIssue("error", "_fetch", "URL has no hostname.")],
        )

    try:
        # CRITICAL: Re-validate immediately before the actual network request
        # to minimize DNS rebinding TOCTOU attacks. We check that:
        # 1. The hostname resolves
        # 2. All resolved IPs are in public ranges (not private/loopback)
        ssrf_err = _check_ssrf(url)
        if ssrf_err:
            return ValidationReport(
                valid=False,
                issues=[ValidationIssue("error", "_fetch", ssrf_err)],
            )
        
        resp = httpx.get(url, timeout=timeout, follow_redirects=False)
        resp.raise_for_status()
        data = resp.json()
    except httpx.HTTPStatusError as exc:
        return ValidationReport(
            valid=False,
            issues=[ValidationIssue("error", "_fetch", f"HTTP {exc.response.status_code}: {url}")],
        )
    except httpx.RequestError as exc:
        return ValidationReport(
            valid=False,
            issues=[ValidationIssue("error", "_fetch", f"Network error: {exc}")],
        )
    except json.JSONDecodeError:
        return ValidationReport(
            valid=False,
            issues=[ValidationIssue("error", "_fetch", "Response is not valid JSON")],
        )

    return validate_agent_card(data)


# ── Negotiation ───────────────────────────────────────────────────────────────


@dataclass
class NegotiationResult:
    """Result of comparing two agent cards for interop."""

    compatible: bool
    shared_skills: list[str] = field(default_factory=list)
    local_only: list[str] = field(default_factory=list)
    remote_only: list[str] = field(default_factory=list)
    auth_compatible: bool = True
    notes: list[str] = field(default_factory=list)


def negotiate(local: A2AAgentCard, remote: A2AAgentCard) -> NegotiationResult:
    """Compare two agent cards and assess interoperability.

    Checks:
      - Skill overlap (by skill id)
      - Authentication compatibility
      - Input/output mode compatibility
    """
    local_skill_ids = {s.id for s in local.skills}
    remote_skill_ids = {s.id for s in remote.skills}

    shared = sorted(local_skill_ids & remote_skill_ids)
    local_only = sorted(local_skill_ids - remote_skill_ids)
    remote_only = sorted(remote_skill_ids - local_skill_ids)

    # Auth compat: if remote requires auth, check local can provide it
    auth_ok = True
    notes: list[str] = []

    if remote.authentication and remote.authentication.schemes:
        local_schemes = set(local.authentication.schemes) if local.authentication else set()
        required = set(remote.authentication.schemes)
        if not required & local_schemes:
            auth_ok = False
            notes.append(
                f"Auth mismatch: remote requires {required}, local has {local_schemes or 'none'}"
            )

    # I/O mode compat
    local_in = set(local.defaultInputModes)
    remote_out = set(remote.defaultOutputModes)
    if not local_in & remote_out:
        notes.append(f"Output format mismatch: remote outputs {remote_out}, local accepts {local_in}")

    compatible = bool(shared) and auth_ok

    return NegotiationResult(
        compatible=compatible,
        shared_skills=shared,
        local_only=local_only,
        remote_only=remote_only,
        auth_compatible=auth_ok,
        notes=notes,
    )


# ── Local agent card generation ───────────────────────────────────────────────


def local_agent_card(working_dir: str = ".") -> A2AAgentCard:
    """Generate an A2A agent card for this ASS-ADE instance.

    Lists all built-in tool capabilities as A2A skills.
    """
    from ass_ade.tools.registry import default_registry

    registry = default_registry(working_dir)

    skills = [
        A2ASkill(
            id=name,
            name=name,
            description=schema.description,
        )
        for name, schema in zip(registry.list_tools(), registry.schemas())
    ]

    return A2AAgentCard(
        name="ASS-ADE",
        description="Autonomous Sovereign Systems: Atomadic Development Environment — agentic IDE with multi-model support",
        url="",  # local instance
        version=__version__,
        provider=A2AProvider(organization="Atomadic", url="https://atomadic.tech"),
        capabilities=A2ACapabilities(
            streaming=True,
            pushNotifications=False,
            stateTransitionHistory=True,
        ),
        authentication=A2AAuthentication(schemes=["bearer"]),
        skills=skills,
        defaultInputModes=["text/plain", "application/json"],
        defaultOutputModes=["text/plain", "application/json"],
    )
