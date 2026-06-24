from abc import ABC, abstractmethod

class BaseInterface(ABC):
    def __init__(self, core_engine, subscription_manager, user_manager):
        self.core = core_engine
        self.sub_manager = subscription_manager
        self.user_mgr = user_manager

    @abstractmethod
    async def start(self):
        ...

    @abstractmethod
    async def stop(self):
        ...

    @abstractmethod
    async def send_message(self, user_id: str, text: str, **kwargs):
        ...

    async def handle_incoming(self, user_id: str, text: str, channel: str):
        lang = self.user_mgr.get_language(user_id, channel)
        if not self.sub_manager.is_subscription_active(user_id):
            await self.send_message(user_id, self.loc("subscribe_prompt", lang))
            return
        if text.startswith("/buy_coffee"):
            result = await self.core.buy_item(user_id, "coffee")
            await self.send_message(user_id, result)
        else:
            await self.send_message(user_id, self.loc("help", lang))

    def loc(self, key, lang):
        from angel.localization import locale
        return locale.get(key, lang)
