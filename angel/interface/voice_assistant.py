from .base_interface import BaseInterface

class VoiceAssistant(BaseInterface):
    async def start(self):
        # Подключение к телефонии (Twilio/Voximplant)
        pass
    async def stop(self):
        pass
    async def send_message(self, user_id: str, text: str, **kwargs):
        # Синтез речи и звонок
        pass
    async def handle_call(self, user_id, audio):
        text = "распознанный текст"
        await self.handle_incoming(user_id, text, 'voice')
