# Extracted from C:/!ass-ade/scripts/lora_training/serve_lora.py:80
# Component id: at.source.ass_ade.generate
from __future__ import annotations

__version__ = "0.1.0"

def generate(self, prompt: str, max_new_tokens: int = 256, temperature: float = 0.7) -> str:
    import torch

    self.ensure_loaded()
    assert self._model is not None and self._tokenizer is not None

    inputs = self._tokenizer(prompt, return_tensors="pt")
    use_gpu = next(self._model.parameters()).is_cuda
    if use_gpu:
        inputs = {k: v.cuda() for k, v in inputs.items()}

    with torch.no_grad():
        out = self._model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=max(temperature, 1e-3),
            do_sample=temperature > 0,
            pad_token_id=self._tokenizer.eos_token_id,
        )
    new_tokens = out[0][inputs["input_ids"].shape[-1]:]
    return self._tokenizer.decode(new_tokens, skip_special_tokens=True)
