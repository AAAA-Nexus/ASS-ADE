from helpers import format_output

def get_value(key):
    return key.upper()

def process_data(data):
    result = []
    for item in data:
        result.append(item * 2)
    return result

def process_data_copy(data):
    result = []
    for item in data:
        result.append(item * 2)
    return result

def helper_thing(x, y, z):
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
