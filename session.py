import json
from pathlib import Path

SESSION_FILE = Path("session.json")


# mcp session token stored here ..
class SessionStore :
    
    def __init__(self):
        self.token = None # cookie stored 
        self.cookie_name = None
        self.user = None

    def save(self):
        SESSION_FILE.write_text(json.dumps({
            "token": self.token,
            "cookie_name": self.cookie_name,
            "user": self.user,
        }))

    def load(self):
        if SESSION_FILE.exists():
            data = json.loads(SESSION_FILE.read_text())

            self.token = data.get("token")
            self.cookie_name = data.get("cookie_name")
            self.user = data.get("user")

        
session = SessionStore()