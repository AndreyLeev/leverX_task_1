import json

from DataHandler import DataHandler


class JSONHandler(DataHandler):
    def load(self, filename):
        with open(filename, 'r') as f:
            return json.loads(f.read())
        
    def dump(self, data, filename):
        with open(filename, 'w') as f:
            f.write(json.dumps(data, indent=2))

