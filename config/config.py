import yaml
from pathlib import Path

class Config:
    def __init__(self, path="config/angel_config.yaml"):
        with open(Path(path).resolve(), encoding="utf-8") as f:
            data = yaml.safe_load(f)
        self.interfaces = data.get("interfaces", {})
        self.payments = data.get("payments", {})
        self.billing = data.get("billing", {})
        self.user_management = data.get("user_management", {})
        self.me = data.get("me", {})

cfg = Config()
BOT_TOKEN = cfg.interfaces.get("telegram", {}).get("token", "")
PROVIDER_TOKEN = cfg.billing.get("provider_token", "")
