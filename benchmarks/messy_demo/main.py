import sys
import os
from config import load_config, load_config_again
from utils import get_value, process_data, process_data_copy, helper_thing, another_helper_thing
from helpers import format_output, format_output_again, DataManager

GLOBAL_STATE = {}
GLOBAL_STATE_COPY = {}

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

def run_again():
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

if __name__ == "__main__":
    run()
    run_again()
