# Angel-in-Pocket

**Bilingual repository** (English / Русский)

Personal AI based on GRA-nullification with multi-currency subscription support and localization.

## Quick Start

```bash
pip install -r requirements.txt
python examples/run_angel.py
```

## Structure

- `angel/localization/` — language files (en, ru)
- `angel/subscription/` — subscription and payment management
- `angel/interface/telegram_bot.py` — bilingual Telegram bot
- `config/subscription_plans.yaml` — plans with multi-currency prices

## Subscription

The bot automatically detects user language and shows prices in local currency:
- Russian-speaking users — rubles (₽)
- Others — US dollars ($) or euros (€)

## License

MIT
