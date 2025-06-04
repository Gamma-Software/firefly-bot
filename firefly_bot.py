import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import requests
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
FIREFLY_URL = os.getenv('FIREFLY_URL')
FIREFLY_API_TOKEN = os.getenv('FIREFLY_API_TOKEN')
ALLOWED_USER_IDS = [int(id) for id in os.getenv('ALLOWED_USER_IDS', '').split(',') if id]

# Firefly III API headers
FIREFLY_HEADERS = {
    'Authorization': f'Bearer {FIREFLY_API_TOKEN}',
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

def is_authorized(user_id: int) -> bool:
    """Check if the user is authorized to use the bot."""
    return user_id in ALLOWED_USER_IDS

def start(update: Update, context: CallbackContext):
    """Send a message when the command /start is issued."""
    if not is_authorized(update.effective_user.id):
        update.message.reply_text("You are not authorized to use this bot.")
        return

    update.message.reply_text(
        "Welcome to Firefly III Bot! Available commands:\n"
        "/balance - Get current account balances\n"
        "/import - Trigger a new import\n"
        "/help - Show this help message"
    )

def get_balance(update: Update, context: CallbackContext):
    """Get current account balances."""
    if not is_authorized(update.effective_user.id):
        update.message.reply_text("You are not authorized to use this bot.")
        return

    try:
        response = requests.get(
            f"{FIREFLY_URL}/api/v1/accounts",
            headers=FIREFLY_HEADERS
        )
        response.raise_for_status()
        accounts = response.json()['data']

        message = "Current Account Balances:\n\n"
        for account in accounts:
            if account['attributes']['type'] == 'asset':
                balance = float(account['attributes']['current_balance'])
                currency = account['attributes']['currency_symbol']
                message += f"{account['attributes']['name']}: {balance} {currency}\n"

        update.message.reply_text(message)
    except Exception as e:
        logger.error(f"Error getting balances: {e}")
        update.message.reply_text("Sorry, there was an error getting the balances.")

def trigger_import(update: Update, context: CallbackContext):
    """Trigger a new import."""
    if not is_authorized(update.effective_user.id):
        update.message.reply_text("You are not authorized to use this bot.")
        return

    try:
        # Trigger import job
        response = requests.post(
            f"{FIREFLY_URL}/api/v1/import/start",
            headers=FIREFLY_HEADERS
        )
        response.raise_for_status()

        update.message.reply_text("Import job has been triggered successfully!")
    except Exception as e:
        logger.error(f"Error triggering import: {e}")
        update.message.reply_text("Sorry, there was an error triggering the import.")

def help_command(update: Update, context: CallbackContext):
    """Send a message when the command /help is issued."""
    if not is_authorized(update.effective_user.id):
        update.message.reply_text("You are not authorized to use this bot.")
        return

    update.message.reply_text(
        "Available commands:\n"
        "/balance - Get current account balances\n"
        "/import - Trigger a new import\n"
        "/help - Show this help message"
    )

def error_handler(update: Update, context: CallbackContext):
    """Log the error and send a message to the user."""
    logger.error(f"Update {update} caused error {context.error}")
    if update and update.effective_message:
        update.effective_message.reply_text("Sorry, an error occurred while processing your request.")

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("balance", get_balance))
    dispatcher.add_handler(CommandHandler("import", trigger_import))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # Add error handler
    dispatcher.add_error_handler(error_handler)

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()