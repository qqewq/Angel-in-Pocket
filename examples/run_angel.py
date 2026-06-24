import asyncio
from angel.core.engine import AngelEngine
from angel.core.user_manager import UserManager
from angel.subscription.manager import SubscriptionManager
from angel.interface.telegram_bot import TelegramInterface
from angel.interface.whatsapp_bot import WhatsAppInterface
from angel.interface.web_app import WebInterface
from angel.interface.email_interface import EmailInterface
from config.config import cfg

async def main():
    engine = AngelEngine()
    sub_mgr = SubscriptionManager()
    user_mgr = UserManager(cfg.user_management)
    tasks = []
    if cfg.interfaces.get('telegram', {}).get('enabled', False):
        tel = TelegramInterface(engine, sub_mgr, user_mgr, cfg.interfaces['telegram'])
        tasks.append(tel.start())
    if cfg.interfaces.get('whatsapp', {}).get('enabled', False):
        wa = WhatsAppInterface(engine, sub_mgr, user_mgr, cfg.interfaces['whatsapp'])
        tasks.append(wa.start())
    if cfg.interfaces.get('web_app', {}).get('enabled', False):
        web = WebInterface(engine, sub_mgr, user_mgr, cfg.interfaces['web_app'])
        tasks.append(web.start())
    if cfg.interfaces.get('email', {}).get('enabled', False):
        em = EmailInterface(engine, sub_mgr, user_mgr, cfg.interfaces['email'])
        tasks.append(em.start())
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
