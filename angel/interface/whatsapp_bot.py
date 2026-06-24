import requests
from .base_interface import BaseInterface

class WhatsAppInterface(BaseInterface):
    def __init__(self, core, sub_mgr, user_mgr, config):
        super().__init__(core, sub_mgr, user_mgr)
        self.token = config['token']
        self.phone_number_id = config['phone_number_id']
        self.verify_token = config.get('verify_token', 'angel_verify')

    async def start(self):
        print("WhatsApp webhook server started (run webhook_handler.py separately)")

    async def stop(self):
        pass

    async def send_message(self, user_id: str, text: str, **kwargs):
        url = f"https://graph.facebook.com/v17.0/{self.phone_number_id}/messages"
        headers = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}
        data = {
            "messaging_product": "whatsapp",
            "to": user_id,
            "type": "text",
            "text": {"body": text}
        }
        requests.post(url, headers=headers, json=data)

    async def handle_webhook(self, body: dict):
        entry = body.get("entry", [{}])[0]
        change = entry.get("changes", [{}])[0]
        value = change.get("value", {})
        message = value.get("messages", [{}])[0]
        if message.get("type") == "text":
            user_id = message["from"]
            text = message["text"]["body"]
            angel_id = self.user_mgr.get_angel_id('whatsapp', user_id)
            await self.handle_incoming(angel_id, text, 'whatsapp')
