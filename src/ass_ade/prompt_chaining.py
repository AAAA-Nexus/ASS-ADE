
"""
Prompt chaining and live editing for ASS-ADE agents.
Hardened with type hints, docstrings, and input validation.
"""

from typing import List, Dict, Any
import logging

logger = logging.getLogger("ass_ade.prompt_chaining")

# In-memory prompt template store (for demo)
_PROMPT_TEMPLATES: Dict[str, str] = {
	"default": "You are an assistant. {{context}}",
}

def chain_prompts(prompts: List[str], context: Dict[str, Any]) -> str:
	"""
	Chain a list of prompts, injecting context variables.
	"""
	chained = "\n---\n".join(prompts)
	for k, v in context.items():
		chained = chained.replace(f"{{{{{k}}}}}", str(v))
	return chained

def edit_prompt_live(prompt_id: str, new_content: str) -> None:
	"""
	Edit a prompt template live.
	"""
	_PROMPT_TEMPLATES[prompt_id] = new_content

def get_prompt_template(agent_id: str) -> str:
	"""
	Get the prompt template for an agent.
	"""
	if not agent_id or not isinstance(agent_id, str):
		return _PROMPT_TEMPLATES["default"]
	return _PROMPT_TEMPLATES.get(agent_id, _PROMPT_TEMPLATES["default"])
