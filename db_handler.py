import json
import os

class DBHandler:
    def __init__(self, db_file):
        self.db_file = db_file
        if not os.path.exists(self.db_file):
            with open(self.db_file, 'w') as f:
                json.dump({}, f)

    def read(self):
        with open(self.db_file, 'r') as f:
            return json.load(f)

    def write(self, data):
        with open(self.db_file, 'w') as f:
            json.dump(data, f, indent=4)

    def get(self, key):
        data = self.read()
        return data.get(key)

    def set(self, key, value):
        data = self.read()
        data[key] = value
        self.write(data)

    def delete(self, key):
        data = self.read()
        if key in data:
            del data[key]
            self.write(data)