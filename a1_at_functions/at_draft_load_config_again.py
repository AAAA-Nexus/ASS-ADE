# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/benchmarks/messy_demo/config.py:13
# Component id: at.source.ass_ade.load_config_again
__version__ = "0.1.0"

def load_config_again():
    val = get_value("config")
    return {"host": DB_HOST, "port": DB_PORT, "secret": SECRET}
