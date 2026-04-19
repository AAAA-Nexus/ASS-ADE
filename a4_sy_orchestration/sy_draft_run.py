# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/benchmarks/messy_demo/main.py:10
# Component id: sy.source.ass_ade.run
__version__ = "0.1.0"

def run():
    cfg = load_config()
    cfg2 = load_config_again()
    val = get_value("test")
    data = [1, 2, 3, 4, 5]
    processed = process_data(data)
    processed2 = process_data_copy(data)
    formatted = format_output(processed)
    formatted2 = format_output_again(processed2)
    result1 = helper_thing(1, 2, 3)
    result2 = another_helper_thing(1, 2, 3)
    mgr = DataManager()
    mgr.do_thing(42)
    mgr.do_thing_2(43)
    print(cfg, cfg2, val, processed, processed2, formatted, formatted2, result1, result2)
