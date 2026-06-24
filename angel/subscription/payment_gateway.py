import stripe
import yookassa
from angel.localization import locale
from .manager import SubscriptionManager

class PaymentGateway:
    def __init__(self, config):
        self.providers = config.payments.get('providers', []) if hasattr(config, 'payments') else []
        self.active = {}
        for p in self.providers:
            if p['name'] == 'stripe':
                stripe.api_key = p['api_key']
                self.active['stripe'] = p
            elif p['name'] == 'yookassa':
                yookassa.Configuration.account_id = p['shop_id']
                yookassa.Configuration.secret_key = p['secret_key']
                self.active['yookassa'] = p
            elif p['name'] == 'crypto':
                self.active['crypto'] = p

    def create_invoice(self, plan_id, user_id, lang, currency='USD'):
        from .manager import SubscriptionManager
        sub_mgr = SubscriptionManager()
        plan = sub_mgr.get_plan(plan_id)
        price_info = sub_mgr.get_plan_for_currency(plan_id, currency)
        amount = price_info['price']
        description = plan['name'].get(lang, plan['name']['en'])
        if 'stripe' in self.active:
            return self._create_stripe_session(plan_id, amount, currency, description, user_id)
        elif 'yookassa' in self.active:
            return self._create_yookassa_payment(plan_id, amount, currency, description, user_id)
        elif 'crypto' in self.active:
            return self._create_crypto_invoice(plan_id, amount, currency, description, user_id)
        return None

    def _create_stripe_session(self, plan_id, amount, currency, description, user_id):
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': currency.lower(),
                    'product_data': {'name': description},
                    'unit_amount': int(amount * 100),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=f'https://myangel.app/success?user={user_id}&plan={plan_id}',
            cancel_url=f'https://myangel.app/cancel',
            client_reference_id=user_id,
            metadata={'plan_id': plan_id}
        )
        return session.url

    def _create_yookassa_payment(self, plan_id, amount, currency, description, user_id):
        payment = yookassa.Payment.create({
            "amount": {
                "value": f"{amount:.2f}",
                "currency": currency
            },
            "confirmation": {
                "type": "redirect",
                "return_url": f"https://myangel.app/success?user={user_id}&plan={plan_id}"
            },
            "capture": True,
            "description": description,
            "metadata": {"user_id": user_id, "plan_id": plan_id}
        })
        return payment.confirmation.confirmation_url

    def _create_crypto_invoice(self, plan_id, amount, currency, description, user_id):
        btc_rate = 30000  # dummy
        btc_amount = amount / btc_rate
        return f"bitcoin:{self.active['crypto']['wallet']}?amount={btc_amount:.8f}&label={user_id}"
