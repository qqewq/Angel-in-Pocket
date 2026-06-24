import time, asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from angel.subscription.manager import SubscriptionManager
from angel.subscription.telegram_payment import TelegramPaymentProcessor
from angel.localization import locale
from config.config import BOT_TOKEN, PROVIDER_TOKEN
import yaml

with open("config/subscription_plans.yaml", encoding="utf-8") as f:
    plans_data = yaml.safe_load(f)['plans']

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
sub_manager = SubscriptionManager()
payment_proc = TelegramPaymentProcessor(BOT_TOKEN, PROVIDER_TOKEN, sub_manager)

def get_lang(message: types.Message):
    return message.from_user.language_code if message.from_user.language_code in ('ru','en') else 'en'

def require_subscription(feature_key: str = None):
    def decorator(func):
        async def wrapper(message: types.Message, **kwargs):
            user_id = message.from_user.id
            lang = get_lang(message)
            if not sub_manager.is_subscription_active(user_id):
                await message.answer(locale.get("subscribe_prompt", lang))
                return
            return await func(message, **kwargs)
        return wrapper
    return decorator

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    lang = get_lang(message)
    await message.answer(
        locale.get("welcome", lang) + "\n" + locale.get("subscribe_prompt", lang)
    )
    if not sub_manager.is_subscription_active(message.from_user.id):
        trial_plan = sub_manager.get_plan("free_trial")
        if trial_plan:
            sub_manager.activate_subscription(message.from_user.id, "free_trial")
            await message.answer(
                locale.get("trial_activated", lang).format(days=trial_plan['period_days'])
            )

@dp.message(Command("subscribe"))
async def cmd_subscribe(message: types.Message):
    lang = get_lang(message)
    text = locale.get("choose_plan", lang) + "\n\n"
    for plan in plans_data:
        pid = plan['id']
        plan_name = plan['name'][lang]
        price_info = sub_manager.get_plan_for_currency(pid, "RUB" if lang=="ru" else "USD")
        price_str = f"{price_info['price']} {price_info['symbol']}" if price_info else ""
        text += f"{plan_name} — {price_str}\n"
        text += f"/buy_{pid}\n\n"
    await message.answer(text)

@dp.message(Command("buy_angel_basic"))
async def buy_basic(message: types.Message):
    await payment_proc.send_invoice(message.from_user.id, "angel_basic", message.from_user)

@dp.message(Command("buy_angel_family"))
async def buy_family(message: types.Message):
    await payment_proc.send_invoice(message.from_user.id, "angel_family", message.from_user)

@dp.message(Command("buy_angel_lifetime"))
async def buy_lifetime(message: types.Message):
    await payment_proc.send_invoice(message.from_user.id, "angel_lifetime", message.from_user)

@dp.message(Command("status"))
async def cmd_status(message: types.Message):
    lang = get_lang(message)
    user_id = message.from_user.id
    if sub_manager.is_subscription_active(user_id):
        sub = sub_manager.active_subscriptions[user_id]
        plan = sub_manager.get_plan(sub.plan_id)
        end = time.strftime('%d.%m.%Y', time.localtime(sub.end_date))
        await message.answer(locale.get("subscription_active", lang).format(plan=plan['name'][lang], end_date=end))
    else:
        await message.answer(locale.get("subscription_expired", lang))

@dp.pre_checkout_query()
async def pre_checkout(pre_checkout_query: types.PreCheckoutQuery):
    await payment_proc.process_pre_checkout(pre_checkout_query)

@dp.message(F.successful_payment)
async def successful_payment(message: types.Message):
    await payment_proc.process_successful_payment(message, message.from_user)

@dp.message(Command("buy_coffee"))
@require_subscription()
async def buy_coffee(message: types.Message):
    lang = get_lang(message)
    await message.answer("☕ " + locale.get("searching_coffee", lang))
