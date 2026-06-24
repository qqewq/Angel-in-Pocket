import yaml
from pathlib import Path

with open(Path("config/subscription_plans.yaml").resolve(), encoding="utf-8") as f:
    plans = yaml.safe_load(f)["plans"]
