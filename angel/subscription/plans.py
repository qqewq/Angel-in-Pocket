import yaml
from pathlib import Path

_plans_path = Path(__file__).parent.parent.parent / "config" / "subscription_plans.yaml"

with open(_plans_path, encoding="utf-8") as f:
    _data = yaml.safe_load(f)
    plans = _data.get("plans", [])
