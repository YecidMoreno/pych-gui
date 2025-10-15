import json
import os
from datetime import datetime
CFG_PATH = os.path.join(os.path.dirname(__file__), "config/pych-gui.cfg")

class AppConfig:
    def __init__(self, path=CFG_PATH):
        self.path = path
        self.cfg = {}
        self.load()

    def load(self):
        try:
            with open(self.path, 'r') as f:
                self.cfg = json.load(f)
        except FileNotFoundError:
            with open(self.path, 'w') as f:
                json.dump({}, f)
            self.cfg = {}

    def save(self):
        self.cfg["LAST_UPDATE"] = datetime.now().isoformat()    
        self.cfg["VERSION"] = "0.1.0"

        with open(self.path, 'w') as f:
            json.dump(self.cfg, f, indent=4)

    def get(self, key, default=None):
        return self.cfg.get(key, default)

    def update(self, key, value):
        self.cfg[key] = value

    def clear(self):
        self.cfg.clear()
