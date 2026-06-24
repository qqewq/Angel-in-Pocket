from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import uvicorn
from .base_interface import BaseInterface

class WebInterface(BaseInterface):
    def __init__(self, core, sub_mgr, user_mgr, config):
        super().__init__(core, sub_mgr, user_mgr)
        self.app = FastAPI()
        self.domain = config['domain']
        self.port = config['port']
        self.setup_routes()

    def setup_routes(self):
        @self.app.get("/", response_class=HTMLResponse)
        async def index():
            return "<h1>Angel Web App</h1><p>Chat will be here...</p>"

        @self.app.websocket("/ws/{user_id}")
        async def websocket_endpoint(websocket: WebSocket, user_id: str):
            await websocket.accept()
            angel_id = self.user_mgr.get_angel_id('web', user_id)
            while True:
                data = await websocket.receive_text()
                # обработка через handle_incoming
                lang = self.user_mgr.get_language(angel_id, 'web')
                if not self.sub_manager.is_subscription_active(angel_id):
                    resp = self.loc("subscribe_prompt", lang)
                elif data == "/buy_coffee":
                    resp = await self.core.buy_item(angel_id, "coffee")
                else:
                    resp = self.loc("help", lang)
                await websocket.send_text(resp)

    async def send_message(self, user_id: str, text: str, **kwargs):
        print(f"Web push to {user_id}: {text}")

    async def start(self):
        config = uvicorn.Config(self.app, host="0.0.0.0", port=self.port)
        server = uvicorn.Server(config)
        await server.serve()

    async def stop(self):
        pass
