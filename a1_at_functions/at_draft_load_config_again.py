# Extracted from C:/!ass-ade/benchmarks/messy_demo/config.py:13
# Component id: at.source.ass_ade.load_config_again
from __future__ import annotations

__version__ = "0.1.0"

def load_config_again():
    val = get_value("config")
    return {"host": DB_HOST, "port": DB_PORT, "secret": SECRET}
