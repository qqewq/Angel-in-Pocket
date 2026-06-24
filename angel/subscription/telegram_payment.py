from aiogram import Bot, types
from aiogram.types import LabeledPrice
from .manager import SubscriptionManager
from angel.localization import locale
import time
from .plans import plans

class TelegramPaymentProcessor:
    def __init__(self, bot_token: str, provider_token: str, sub_manager: SubscriptionManager):
        self.bot = Bot(token=bot_token)
        self.provider_token = provider_token
        self.sub_manager = sub_manager

    def _get_user_lang(self, user: types.User) -> str:
        return user.language_code if user.language_code in ('ru', 'en') else 'en'

    async def send_invoice(self, user_id: int, plan_id: str, user: types.User):
        lang = self._get_user_lang(user)
        plan = next(p for p in plans if p['id'] == plan_id)
        currency = "RUB" if lang == "ru" else "USD"
        price_info = self.sub_manager.get_plan_for_currency(plan_id, currency)
        if not price_info:
            currency = "USD"
            price_info = self.sub_manager.get_plan_for_currency(plan_id, "USD")
        amount = int(price_info['price'] * 100)
        title = plan['name'][lang]
        description = "\n".join(plan['features'][lang])
        prices = [LabeledPrice(label=title, amount=amount)]
        await self.bot.send_invoice(
            chat_id=user_id,
            title=title,
            description=description,
            provider_token=self.provider_token,
            currency=currency,
            prices=prices,
            payload=plan_id,
            start_parameter="subscribe",
            need_name=True,
            need_phone_number=True,
            is_flexible=False
        )

    async def process_pre_checkout(self, pre_checkout_query: types.PreCheckoutQuery):
        await self.bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

    async def process_successful_payment(self, message: types.Message, user: types.User):
        lang = self._get_user_lang(user)
        plan_id = message.successful_payment.invoice_payload
        self.sub_manager.activate_subscription(user.id, plan_id)
        sub = self.sub_manager.active_subscriptions[user.id]
        plan = self.sub_manager.get_plan(plan_id)
        end_date_str = time.strftime('%d.%m.%Y', time.localtime(sub.end_date))
        await message.answer(
            locale.get("payment_success", lang) + "\n" +
            locale.get("subscription_active", lang).format(plan=plan['name'][lang], end_date=end_date_str)
        )
