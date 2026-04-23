"""Tier a1 — context preloading and lifecycle hooks for fractal subagents.

Provides utilities for parent → child context propagation and burst execution.
"""
from typing import Any, Dict, Callable

def preload_context(parent_context: Dict[str, Any], payload: Dict[str, Any], cna: str) -> Dict[str, Any]:
    """
    Prepare a context envelope for a fractal subagent.
    Args:
        parent_context: dict with 'receipts' and optional metadata
        payload: dict, task-specific input
        cna: str, canonical name authority id for the subagent
    Returns:
        dict: context envelope for subagent
    """
    return {
        'cna': cna,
        'parent_receipts': parent_context.get('receipts', {}),
        'payload': payload,
    }

def run_burst_lifecycle(subagent_fn: Callable[[Dict[str, Any]], Dict[str, Any]], context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Run a fractal subagent in burst mode and collect receipts.
    Args:
        subagent_fn: callable accepting context
        context: context envelope
    Returns:
        dict: result and receipts
    """
    return subagent_fn(context)

# Minimal test
def test_fractal_subagent_burst():
    from .fractal_subagent_template import run_fractal_subagent
    parent_ctx = {'receipts': {'trust': 'OK', 'drift': 'OK', 'hallucination': 'OK'}}
    payload = {'x': 42}
    cna = 'a1.fractal.test'
    context = preload_context(parent_ctx, payload, cna)
    result = run_burst_lifecycle(run_fractal_subagent, context)
    assert result['result']['echo'] == payload
    assert result['receipts']['trust'] == 'OK'
    print('Fractal subagent burst test passed.')
