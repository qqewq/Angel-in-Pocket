"""Tests for subscription module."""
import pytest
from angel.subscription.manager import SubscriptionManager

def test_subscription_manager():
    sm = SubscriptionManager()
    assert sm is not None
