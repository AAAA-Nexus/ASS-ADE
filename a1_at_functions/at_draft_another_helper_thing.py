# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/benchmarks/messy_demo/utils.py:30
# Component id: at.source.ass_ade.another_helper_thing
__version__ = "0.1.0"

def another_helper_thing(x, y, z):
    if x > 0:
        if y > 0:
            if z > 0:
                return x + y + z
            else:
                return x + y
        else:
            return x
    else:
        return 0
