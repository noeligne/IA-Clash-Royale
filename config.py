import json

class Config:
    def __init__(self, filename):
        self.filename = filename
        self.data = {}

        with open(filename, encoding="utf-8") as f:
            self.data = json.load(f)

    def save(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4)