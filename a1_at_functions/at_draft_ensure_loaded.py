# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/scripts/lora_training/serve_lora.py:75
# Component id: at.source.ass_ade.ensure_loaded
__version__ = "0.1.0"

    def ensure_loaded(self) -> None:
        with self._lock:
            if self._model is None:
                self._load()
