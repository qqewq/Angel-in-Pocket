import asyncio, time
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .base_interface import BaseInterface
from angel.subscription.manager import SubscriptionManager
from angel.subscription.telegram_payment import TelegramPaymentProcessor
from angel.subscription.payment_gateway import PaymentGateway
from angel.localization import locale
from config.config import BOT_TOKEN, PROVIDER_TOKEN, cfg

class TelegramInterface(BaseInterface):
    def __init__(self, core_engine, sub_mgr, user_mgr, config):
        super().__init__(core_engine, sub_mgr, user_mgr)
        self.bot = Bot(token=BOT_TOKEN)
        self.dp = Dispatcher()
        self.payment_proc = TelegramPaymentProcessor(BOT_TOKEN, PROVIDER_TOKEN, sub_mgr)
        self.gateway = PaymentGateway(cfg)
        self._setup_handlers()

    def _setup_handlers(self):
        dp = self.dp
        dp.message.register(self.cmd_start, Command("start"))
        dp.message.register(self.cmd_subscribe, Command("subscribe"))
        dp.message.register(self.cmd_status, Command("status"))
        dp.message.register(self.cmd_buy_basic, Command("buy_angel_basic"))
        dp.message.register(self.cmd_buy_family, Command("buy_angel_family"))
        dp.message.register(self.cmd_buy_lifetime, Command("buy_angel_lifetime"))
        dp.message.register(self.cmd_buy_coffee, Command("buy_coffee"))
        dp.pre_checkout_query.register(self.pre_checkout)
        dp.message.register(self.successful_payment, F.successful_payment)

    async def cmd_start(self, message: types.Message):
        lang = self._lang(message)
        await message.answer(locale.get("welcome", lang) + "\n" + locale.get("subscribe_prompt", lang))
        angel_id = self.user_mgr.get_angel_id("telegram", message.from_user.id)
        if not self.sub_manager.is_subscription_active(angel_id):
            trial = self.sub_manager.get_plan("free_trial")
            if trial:
                self.sub_manager.activate_subscription(angel_id, "free_trial")
                await message.answer(locale.get("trial_activated", lang).format(days=trial["period_days"]))

    async def cmd_subscribe(self, message: types.Message):
        lang = self._lang(message)
        from angel.subscription.plans import plans
        text = locale.get("choose_plan", lang) + "\n\n"
        for plan in plans:
            pid = plan["id"]
            name = plan["name"][lang]
            curr = "RUB" if lang == "ru" else "USD"
            price_info = self.sub_manager.get_plan_for_currency(pid, curr)
            price_str = f"{price_info['price']} {price_info['symbol']}" if price_info else ""
            text += f"{name} — {price_str}\n"
            text += f"/buy_{pid}\n\n"
        angel_id = self.user_mgr.get_angel_id("telegram", message.from_user.id)
        web_url = self.gateway.create_invoice("angel_basic", angel_id, lang, curr)
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=locale.get("pay_on_website", lang), url=web_url)]
        ]) if web_url else None
        await message.answer(text, reply_markup=keyboard)

    async def cmd_status(self, message: types.Message):
        lang = self._lang(message)
        angel_id = self.user_mgr.get_angel_id("telegram", message.from_user.id)
        if self.sub_manager.is_subscription_active(angel_id):
            sub = self.sub_manager.active_subscriptions[angel_id]
            plan = self.sub_manager.get_plan(sub.plan_id)
            end = time.strftime('%d.%m.%Y', time.localtime(sub.end_date))
            await message.answer(locale.get("subscription_active", lang).format(plan=plan["name"][lang], end_date=end))
        else:
            await message.answer(locale.get("subscription_expired", lang))

    async def cmd_buy_basic(self, message: types.Message):
        await self.payment_proc.send_invoice(message.from_user.id, "angel_basic", message.from_user)

    async def cmd_buy_family(self, message: types.Message):
        await self.payment_proc.send_invoice(message.from_user.id, "angel_family", message.from_user)

    async def cmd_buy_lifetime(self, message: types.Message):
        await self.payment_proc.send_invoice(message.from_user.id, "angel_lifetime", message.from_user)

    async def cmd_buy_coffee(self, message: types.Message):
        lang = self._lang(message)
        angel_id = self.user_mgr.get_angel_id("telegram", message.from_user.id)
        features = self.sub_manager.get_features(angel_id, lang)
        if "Полный доступ к покупкам" not in features and "Full shopping access" not in features:
            await message.answer(locale.get("subscribe_prompt", lang))
            return
        result = await self.core.buy_item(angel_id, "coffee")
        await message.answer(result)

    async def pre_checkout(self, pre_checkout_query: types.PreCheckoutQuery):
        await self.payment_proc.process_pre_checkout(pre_checkout_query)

    async def successful_payment(self, message: types.Message):
        await self.payment_proc.process_successful_payment(message, message.from_user)

    def _lang(self, message: types.Message) -> str:
        return message.from_user.language_code if message.from_user.language_code in ("ru", "en") else "en"

    async def start(self):
        await self.dp.start_polling(self.bot)

    async def stop(self):
        await self.bot.session.close()

    async def send_message(self, user_id: str, text: str, **kwargs):
        # предполагаем, что user_id == telegram_id (упрощение)
        await self.bot.send_message(user_id, text, **kwargs)
