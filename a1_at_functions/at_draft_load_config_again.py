# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_load_config_again.py:7
# Component id: at.source.a1_at_functions.load_config_again
from __future__ import annotations

__version__ = "0.1.0"

def load_config_again():
    val = get_value("config")
    return {"host": DB_HOST, "port": DB_PORT, "secret": SECRET}
