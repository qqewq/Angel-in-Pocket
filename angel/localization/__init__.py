import json
from pathlib import Path

class Locale:
    def __init__(self):
        self.strings = {}
        base = Path(__file__).parent
        for lang_file in base.glob("*.json"):
            lang = lang_file.stem
            with open(lang_file, encoding="utf-8") as f:
                self.strings[lang] = json.load(f)

    def get(self, key, lang="en"):
        return self.strings.get(lang, {}).get(key) or self.strings["en"].get(key, key)

locale = Locale()
