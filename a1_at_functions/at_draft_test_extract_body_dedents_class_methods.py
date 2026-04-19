# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_extract_body_dedents_class_methods.py:7
# Component id: at.source.a1_at_functions.test_extract_body_dedents_class_methods
from __future__ import annotations

__version__ = "0.1.0"

def test_extract_body_dedents_class_methods(tmp_path: Path) -> None:
    source = tmp_path / "sample.py"
    source.write_text(
        "class Widget:\n"
        "    def available(self) -> int:\n"
        "        return 1\n",
        encoding="utf-8",
    )

    extracted = extract_body(source, "available")

    assert extracted is not None
    assert extracted.body.startswith("def available")
    ast.parse(extracted.body)
