
"""
LoRA Flywheel Expansion for multi-agent, multi-session learning.
Hardened with type hints, docstrings, and input validation.
"""

from typing import List, Dict, Any, Optional
import time
import logging

logger = logging.getLogger("ass_ade.lora_flywheel_expansion")

# In-memory demo store
_CONTRIBUTIONS: List[Dict[str, Any]] = []
_PRINCIPLES: Dict[str, List[str]] = {}  # agent_id -> principles

def contribute(agent_id: str, kind: str, content: dict, confidence: float = 1.0) -> None:
	"""
	Add a contribution for an agent.
	"""
	_CONTRIBUTIONS.append({
		"agent_id": agent_id,
		"kind": kind,
		"content": content,
		"confidence": confidence,
		"ts": time.time(),
	})
	if kind == "principle":
		_PRINCIPLES.setdefault(agent_id, []).append(content.get("principle", ""))

def get_contributions(agent_id: Optional[str] = None) -> List[dict]:
	"""
	Get all contributions, optionally filtered by agent.
	"""
	if agent_id:
		return [c for c in _CONTRIBUTIONS if c["agent_id"] == agent_id]
	return list(_CONTRIBUTIONS)

def share_principles(from_agent: str, to_agent: str) -> None:
	"""
	Share principles from one agent to another.
	"""
	if from_agent not in _PRINCIPLES:
		return
	_PRINCIPLES.setdefault(to_agent, []).extend(_PRINCIPLES[from_agent])

def get_principles(agent_id: str) -> List[str]:
	"""
	Get principles for an agent.
	"""
	if not agent_id or not isinstance(agent_id, str):
		return []
	return _PRINCIPLES.get(agent_id, [])
