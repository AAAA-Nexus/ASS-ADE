import ast
from pathlib import Path

from ass_ade.engine.rebuild.body_extractor import extract_body


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
