def test_subscription_activation():
    from angel.subscription.manager import SubscriptionManager
    sm = SubscriptionManager()
    sm.activate_subscription("test", "angel_basic")
    assert sm.is_subscription_active("test")
