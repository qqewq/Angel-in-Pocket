import imaplib, email, asyncio, smtplib
from email.mime.text import MIMEText
from .base_interface import BaseInterface

class EmailInterface(BaseInterface):
    def __init__(self, core, sub_mgr, user_mgr, config):
        super().__init__(core, sub_mgr, user_mgr)
        self.imap_host = config['imap_host']
        self.email_addr = config['login']
        self.password = config['password']
        self.smtp_host = config.get('smtp_host', 'smtp.gmail.com')
        self.smtp_port = config.get('smtp_port', 587)

    async def start(self):
        asyncio.create_task(self._poll_email())

    async def _poll_email(self):
        while True:
            await asyncio.sleep(30)
            try:
                mail = imaplib.IMAP4_SSL(self.imap_host)
                mail.login(self.email_addr, self.password)
                mail.select("inbox")
                result, data = mail.search(None, "UNSEEN")
                if result == "OK":
                    for num in data[0].split():
                        typ, msg_data = mail.fetch(num, "(RFC822)")
                        for response_part in msg_data:
                            if isinstance(response_part, tuple):
                                msg = email.message_from_bytes(response_part[1])
                                sender = email.utils.parseaddr(msg["from"])[1]
                                body = ""
                                if msg.is_multipart():
                                    for part in msg.walk():
                                        if part.get_content_type() == "text/plain":
                                            body = part.get_payload(decode=True).decode()
                                            break
                                else:
                                    body = msg.get_payload(decode=True).decode()
                                angel_id = self.user_mgr.get_angel_id('email', sender)
                                await self.handle_incoming(angel_id, body, 'email')
                mail.logout()
            except Exception as e:
                print(f"Email poll error: {e}")

    async def send_message(self, user_id: str, text: str, **kwargs):
        to_addr = self.user_mgr.get_channel_address(user_id, 'email')
        msg = MIMEText(text)
        msg["Subject"] = "Angel-in-Pocket Reply"
        msg["From"] = self.email_addr
        msg["To"] = to_addr
        with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
            server.starttls()
            server.login(self.email_addr, self.password)
            server.sendmail(self.email_addr, [to_addr], msg.as_string())

    async def stop(self):
        pass
