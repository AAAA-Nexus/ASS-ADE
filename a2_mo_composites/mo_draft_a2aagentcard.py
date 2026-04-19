# Extracted from C:/!ass-ade/src/ass_ade/a2a/__init__.py:79
# Component id: mo.source.ass_ade.a2aagentcard
from __future__ import annotations

__version__ = "0.1.0"

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
