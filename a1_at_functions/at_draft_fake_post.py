# Extracted from C:/!ass-ade/tests/test_capabilities.py:72
# Component id: at.source.ass_ade.fake_post
from __future__ import annotations

__version__ = "0.1.0"

def fake_post(url: str, **kwargs):
    captured["url"] = url
    captured["json"] = kwargs["json"]
    response = MagicMock()
    response.json.return_value = {
        "choices": [
            {
                "message": {
                    "content": (
                        '{"type":"command","intent":"help","path":null,'
                        '"output_path":null,"feature_desc":null}'
                    )
                }
            }
        ]
    }
    response.raise_for_status.return_value = None
    return response
