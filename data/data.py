import json


class Data:
    def Fetch(self):
        with open("data.json", "r") as f:
            data = json.load(f)
        return data

    def Update(self, data):
        with open("data.json", "w") as f:
            json.dump(data, f, indent=4)
