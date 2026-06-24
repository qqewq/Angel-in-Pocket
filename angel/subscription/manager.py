import time
from typing import Optional
from dataclasses import dataclass, field
from .plans import plans
from angel.localization import locale

@dataclass
class Subscription:
    user_id: int
    plan_id: str
    start_date: float
    end_date: float
    auto_renew: bool = True
    features: list = field(default_factory=list)

class SubscriptionManager:
    def __init__(self):
        self.active_subscriptions = {}  # user_id -> Subscription

    def get_plan(self, plan_id: str):
        for p in plans:
            if p['id'] == plan_id:
                return p
        return None

    def is_subscription_active(self, user_id: int) -> bool:
        sub = self.active_subscriptions.get(user_id)
        if not sub:
            return False
        return sub.end_date > time.time()

    def get_features(self, user_id: int):
        if not self.is_subscription_active(user_id):
            trial_plan = self.get_plan("free_trial")
            if trial_plan:
                self.activate_subscription(user_id, "free_trial")
                return trial_plan['features']['ru']
            return []
        sub = self.active_subscriptions[user_id]
        plan = self.get_plan(sub.plan_id)
        return plan['features']['ru'] if plan else []

    def activate_subscription(self, user_id: int, plan_id: str, duration_days: Optional[int] = None):
        plan = self.get_plan(plan_id)
        if not plan:
            raise ValueError("Unknown plan")
        period = duration_days if duration_days else plan['period_days']
        now = time.time()
        if self.is_subscription_active(user_id):
            self.active_subscriptions[user_id].end_date += period * 86400
        else:
            self.active_subscriptions[user_id] = Subscription(
                user_id=user_id,
                plan_id=plan_id,
                start_date=now,
                end_date=now + period * 86400
            )
        return self.active_subscriptions[user_id]

    def get_plan_for_currency(self, plan_id: str, currency_code: str):
        plan = self.get_plan(plan_id)
        if not plan:
            return None
        for cur in plan['currencies']:
            if cur['code'] == currency_code:
                return {
                    'price': cur['price'],
                    'symbol': cur.get('symbol', currency_code),
                    'currency': cur['code']
                }
        return None
