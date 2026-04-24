# Forge Phase — LLM-Powered Code Improvement

The Forge phase is the step that makes ASS-ADE a **fixer**, not just a classifier.
After the standard Ingest → Classify → Materialize passes produce a structurally
correct, tier-partitioned output, the optional `--forge` flag activates two new
components that analyze and improve the actual code.

## Pipeline with Forge

```
Ingest → Classify → Materialize → Epiphany (plan) → Forge (execute) → Audit → Certify
```

## Components

### 1. EpiphanyEngine (`a3_og_features/epiphany_engine.py`)

AST-analyzes every materialized Python file and generates a structured task plan:

- **missing_docstring** — functions and classes with no docstring
- **debug_hardcoded** — `app.run(debug=True)` and similar hardcoded flags
- **todo_comment** — `# TODO` / `# FIXME` markers in class and function bodies
- **missing_404** — Flask route handlers that call `.query.get()` without a None check

Each issue on each function/class becomes one `ForgeTask` — a focused, single-LLM-call
improvement ticket with an exact instruction.

```python
ForgeTask(
    file="a1_at_functions/app.py",
    node="get_product",
    issue="missing_404",
    instruction="Add 404 error handling when Product.query.get(id) returns None..."
)
```

### 2. ForgeLoop (`a3_og_features/forge_loop.py`)

Executes the Epiphany plan in parallel using a `ThreadPoolExecutor`. Key design:

- **Per-file serialization** — tasks on the same file run sequentially (prevents
  line-number drift from concurrent writes); tasks on different files run in parallel.
- **Focused prompts** — each LLM call gets exactly one function/class plus one
  specific instruction. No whole-file rewrites unless the fix is module-level.
- **Syntax validation** — every LLM response is `ast.parse()`-validated before
  writing. If the response has a syntax error, the task is skipped and the original
  is preserved. The rebuild never produces broken Python.
- **Provider cascade** — uses the full provider chain from your `.env`:
  Groq → Cerebras → Mistral → Together → OpenRouter → Ollama (local fallback).

## Usage

```bash
# Default forge (uses provider chain from .env)
ass-ade rebuild ./messy-project --output ./clean-project --forge

# Specify model explicitly
ass-ade rebuild ./messy-project --output ./clean-project \
  --forge --forge-model "llama-3.3-70b-versatile"
```

## Live Demo Results

**Target:** `demo2-half-built` — a 2-file Flask app with real production anti-patterns.

**BEFORE** (`app.py`):
```python
@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):                             # no docstring
    p = Product.query.get(id)                    # crashes if None
    return jsonify({'id': p.id, ...})

if __name__ == '__main__':
    app.run(debug=True)                          # hardcoded
```

**AFTER** (`app.py` — all changes verified with `ast.parse`):
```python
import os                                        # added

@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    """Retrieve product details by id.

    Args:
        id (int): The unique identifier of the product.

    Returns:
        dict: A dictionary containing the product's id, name, price, and stock.
    """
    p = Product.query.get(id)
    if p is None:                                # 404 handling added
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'id': p.id, ...})

if __name__ == '__main__':
    app.run(debug=os.getenv('FLASK_DEBUG', '0') == '1')   # env-driven
```

**BEFORE** (`models.py`):
```python
class Product(db.Model):                         # no docstring
    id = db.Column(db.Integer, primary_key=True)
    ...

class Order(db.Model):                           # no docstring
    id = db.Column(db.Integer, primary_key=True)
    # TODO: incomplete
```

**AFTER** (`models.py`):
```python
class Product(db.Model):
    """Represents a product with id, name, price, and stock."""
    id = db.Column(db.Integer, primary_key=True)
    ...

class Order(db.Model):
    """Represents a customer order in the database."""
    id = db.Column(db.Integer, primary_key=True)
```

**Pipeline output:**
```
[Phase 5]  Materialize: 4 components (2 modules)
[Phase 5b] Forge     : 6/6 fixes applied (2 files) — model=llama-3.3-70b-versatile
[Phase 6]  Audit     : 4/4 clean (100.0%), conformant
[Cert]     SHA-256   : cd17e2d8a84a6755...
```

| Fix | Before | After | Verified |
|-----|--------|-------|----------|
| `debug=True` | hardcoded | `os.getenv('FLASK_DEBUG', '0') == '1'` | ✅ |
| `list_products` docstring | missing | Google-style with Returns | ✅ |
| `get_product` docstring | missing | Google-style with Args + Returns | ✅ |
| 404 handling | crashes on None | `return jsonify({'error': 'Not found'}), 404` | ✅ |
| `Product` class docstring | missing | one-line summary | ✅ |
| `Order` class docstring | missing | one-line summary | ✅ |

**6/6 tasks applied. 2 files modified. Certificate re-issued.**

## Provider Configuration

The forge phase reads API keys from the `.env` file in your project root.
Priority order (fastest/most capable first):

| Provider | Env var | Model used |
|----------|---------|-----------|
| Groq | `GROQ_API_KEY` | `llama-3.3-70b-versatile` |
| Cerebras | `CEREBRAS_API_KEY` | `llama3.1-70b` |
| Mistral | `MISTRAL_API_KEY` | `mistral-large-latest` |
| Together | `TOGETHER_API_KEY` | `meta-llama/Llama-3-70b` |
| OpenRouter | `OPENROUTER_API_KEY` | `meta-llama/llama-3.3-70b` |
| Ollama | *(no key needed)* | `helix7b:latest` (local fallback) |

## Architecture Note

The Forge phase follows ASS-ADE's monadic law:

- `a3_og_features/epiphany_engine.py` — product-level analysis wrapper (a3 tier)
- `a3_og_features/forge_loop.py` — product-level execution wrapper (a3 tier)
- `src/ass_ade/engine/rebuild/forge.py` — engine-level implementation (called by a3)

The rebuild orchestrator (`engine/rebuild/orchestrator.py`) calls `run_forge_phase()`
between Phase 5 (Materialize) and Phase 6 (Audit), so the audit and certificate
always reflect the forged output, not the raw materialize output.
