import json

class UserRepository:
    def __init__(self, path):
        self.path = path

    def load(self):
        try:
            with open(self.path, 'r') as f:
                return json.load(f)
        except:
            return []

    def save(self, data):
        with open(self.path, 'w') as f:
            json.dump(data, f, indent=4)

    def add_user(self, user_name, api_key):
        data = self.load()
        data.append({
            "User": user_name,
            "API_key": api_key
        })
        self.save(data)