from utils import process_data

def format_output(data):
    processed = process_data(data)
    return str(processed)

def format_output_again(data):
    processed = process_data(data)
    return str(processed)

class DataManager:
    def __init__(self):
        self.data = []
        self.cache = {}
        self.temp = None
        self.flag = False
        self.count = 0
        self.total = 0
        self.average = 0
        self.maximum = 0
        self.minimum = 0

    def do_thing(self, x):
        self.data.append(x)
        self.count += 1
        self.total += x
        self.average = self.total / self.count
        if x > self.maximum: self.maximum = x
        if x < self.minimum: self.minimum = x
        return self.data

    def do_thing_2(self, x):
        self.data.append(x)
        self.count += 1
        self.total += x
        self.average = self.total / self.count
        if x > self.maximum: self.maximum = x
        if x < self.minimum: self.minimum = x
        return self.data
