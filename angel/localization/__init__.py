import json
from pathlib import Path

class Locale:
    def __init__(self):
        self.strings = {}
        self.load_all()

    def load_all(self):
        base = Path(__file__).parent
        for lang_file in base.glob("*.json"):
            lang = lang_file.stem  # 'ru', 'en'
            with open(lang_file, encoding="utf-8") as f:
                self.strings[lang] = json.load(f)

    def get(self, key, lang="en"):
        # fallback to en if key not found
        return self.strings.get(lang, {}).get(key) or self.strings["en"].get(key, key)

locale = Locale()
