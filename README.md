# Firefly III Telegram Bot

A Telegram bot that allows you to interact with your Firefly III instance remotely. You can check balances and trigger imports through Telegram commands.

## Features

- Get current account balances
- Trigger new imports
- Secure access control through Telegram user IDs

## Setup

1. Create a new Telegram bot using [@BotFather](https://t.me/botfather) and get the bot token
2. Get your Firefly III API token from your Firefly III instance
3. Copy `.env.example` to `.env` and fill in the required values:
   ```
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
   FIREFLY_URL=http://firefly:8080
   FIREFLY_API_TOKEN=your_firefly_api_token_here
   ALLOWED_USER_IDS=123456789,987654321
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run the bot:
   ```bash
   python firefly_bot.py
   ```

## Available Commands

- `/start` - Start the bot and see available commands
- `/balance` - Get current account balances
- `/import` - Trigger a new import
- `/help` - Show help message

## Security

The bot implements security through Telegram user ID verification. Only users whose IDs are listed in the `ALLOWED_USER_IDS` environment variable can use the bot.

To get your Telegram user ID, you can use [@userinfobot](https://t.me/userinfobot) on Telegram.
