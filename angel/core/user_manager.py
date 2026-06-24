class UserManager:
    def __init__(self, config=None):
        self.channel_bindings = {}
        self.user_profiles = {}

    def get_angel_id(self, channel: str, channel_id: str) -> str:
        key = (channel, str(channel_id))
        if key in self.channel_bindings:
            return self.channel_bindings[key]
        new_id = f"angel_{len(self.user_profiles) + 1}"
        self.channel_bindings[key] = new_id
        self.user_profiles[new_id] = {
            "language": "ru" if channel == "telegram" and str(channel_id).startswith("7") else "en",
            "channels": {channel: str(channel_id)}
        }
        return new_id

    def link_channel(self, angel_id: str, channel: str, channel_id: str):
        if angel_id in self.user_profiles:
            self.channel_bindings[(channel, str(channel_id))] = angel_id
            self.user_profiles[angel_id]["channels"][channel] = str(channel_id)

    def get_language(self, angel_id: str, channel: str = None) -> str:
        profile = self.user_profiles.get(angel_id)
        return profile.get("language", "en") if profile else "en"

    def set_language(self, angel_id: str, lang: str):
        if angel_id in self.user_profiles:
            self.user_profiles[angel_id]["language"] = lang

    def get_channel_address(self, angel_id: str, channel: str) -> str:
        profile = self.user_profiles.get(angel_id)
        if profile and channel in profile.get("channels", {}):
            return profile["channels"][channel]
        return None
