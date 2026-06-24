https://orcid.org/my-orcid?orcid=0009-0004-1872-1153 
https://doi.org/10.5281/zenodo.20829385

# Angel-in-Pocket

**Bilingual repository** (Russian / English) for a personal AI assistant with multi‑currency subscriptions.

**Angel-in-Pocket** is a personal AI assistant based on the GRA‑nullification concept that runs as a Telegram bot, automatically detects the user’s language and shows prices in their local currency. [itbb](https://itbb.ru/blog/biznes_model_saas)

***

## Features

- Bilingual (RU / EN)  
  All texts, messages and bot interface are available in Russian and English. The bot automatically detects the user’s language and talks in that language.

- Personal AI based on GRA‑nullification  
  The assistant’s logic is built on GRA‑nullification and can serve as a base for your own semantic / AGI experiments.

- Multi‑currency subscription  
  Support for plans in multiple currencies: rubles (₽), US dollars ($), euros (€) and others if needed.

- Telegram interface  
  Ready‑to‑use **bilingual Telegram bot** for end users — no need to build your own interface from scratch.

***

## Quick start

```bash
pip install -r requirements.txt
python examples/run_angel.py
```

After starting:
1. Make sure the Telegram bot token and subscription parameters are set in the configuration.
2. Send a message to your bot in Telegram.
3. The bot will detect your language and show current plans in the appropriate currency.

***

## Project structure

- `angel/localization/` — localization files (ru, en)  
- `angel/subscription/` — subscription and payments logic  
- `angel/interface/telegram_bot.py` — bilingual Telegram bot  
- `config/subscription_plans.yaml` — plans with multi‑currency prices  

***

## Subscription and currency logic

The bot automatically detects the user’s language from Telegram settings and uses it to choose the currency. [itbb](https://itbb.ru/blog/biznes_model_saas)

By default:
- Russian‑speaking users — prices in rubles (₽).  
- Other users — prices in US dollars ($) or euros (€), depending on the configured plans.

You can change this behavior in `config/subscription_plans.yaml` and in the `angel/subscription/` module.

***

## Configuration

1. Create and configure your Telegram bot via @BotFather (get the token). [yookassa](https://yookassa.ru/docs/support/payments/onboarding/integration/cms-module/telegram)
2. Put the bot token and connection parameters into the configuration (see `examples/run_angel.py` and `angel/interface/telegram_bot.py`).  
3. Edit `config/subscription_plans.yaml`:
   - add or modify plans;
   - set prices in required currencies;
   - add new currencies and plans if needed.

***

## Adapting to your own product

- Adjust texts in `angel/localization/` to match your business logic and tone of voice.  
- Extend modules in `angel/subscription/` with integration to your payment provider (YooKassa, Stripe, etc.). [selectel](https://selectel.ru/blog/tutorials/telegram-bot-with-monetization/)
- Customize `angel/interface/telegram_bot.py` so that commands and flows reflect your product (personal assistant, educational bot, trading helper, etc.).

***

## License

This project is distributed under the **MIT** license.  
See the `LICENSE` file for details.
