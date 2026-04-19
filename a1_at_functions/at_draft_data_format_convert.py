# Extracted from C:/!ass-ade/src/ass_ade/nexus/client.py:1153
# Component id: at.source.ass_ade.data_format_convert
from __future__ import annotations

__version__ = "0.1.0"

def data_format_convert(self, data: str, from_format: str, to_format: str, **kwargs: Any) -> FormatConversion:
    """/v1/data/format-convert — JSON ↔ CSV transformation. $0.020/request"""
    return self._post_model("/v1/data/format-convert", FormatConversion, {
        "data": data, "from_format": from_format, "to_format": to_format, **kwargs,
    })
