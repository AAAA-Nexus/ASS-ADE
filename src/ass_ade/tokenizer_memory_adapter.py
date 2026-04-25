
"""
Tokenizer and Memory Adapter Integration for ASS-ADE.
Hardened with type hints, docstrings, and error handling.
"""

from typing import Any, Optional
import logging

logger = logging.getLogger("ass_ade.tokenizer_memory_adapter")

def count_tokens(text: str, model: str = "gpt-3.5-turbo") -> int:
	"""
	Count tokens using tiktoken or HuggingFace (stubbed, with fallback).
	"""
	try:
		import tiktoken
		enc = tiktoken.encoding_for_model(model)
		return len(enc.encode(text))
	except ImportError:
		pass
	except Exception:
		pass
	try:
		from transformers import AutoTokenizer
		tokenizer = AutoTokenizer.from_pretrained(model)
		return len(tokenizer.encode(text))
	except ImportError:
		pass
	except Exception:
		pass
	# Fallback: whitespace split
	return len(text.split())

def get_tokenizer(model: str = "gpt-3.5-turbo") -> Optional[Any]:
	"""
	Get a tokenizer instance (tiktoken or HuggingFace, stubbed).
	"""
	try:
		import tiktoken
		return tiktoken.encoding_for_model(model)
	except ImportError:
		pass
	except Exception:
		pass
	try:
		from transformers import AutoTokenizer
		return AutoTokenizer.from_pretrained(model)
	except ImportError:
		pass
	except Exception:
		pass
	return None

def memory_adapter(config: dict) -> Any:
	"""
	Factory for memory backend adapter (local, redis, etc.).
	"""
	backend = config.get("backend", "local")
	if backend == "local":
		return LocalMemoryAdapter()
	raise NotImplementedError(f"Unknown memory backend: {backend}")

class LocalMemoryAdapter:
	"""
	Minimal in-memory key-value store for agent memory.
	"""
	def __init__(self):
		self._store = {}
	def set(self, key: str, value: Any) -> None:
		self._store[key] = value
	def get(self, key: str, default: Any = None) -> Any:
		return self._store.get(key, default)
