import sys
import os
from flask import Flask, request
import telegram
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import (TELEGRAM_BOT_TOKEN, TEST_TG_CHAT_ID, VERCEL_APP_URL)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = TELEGRAM_BOT_TOKEN or os.getenv('TELEGRAM_BOT_TOKEN')
APP_URL = VERCEL_APP_URL or os.getenv('VERCEL_APP_URL')
CHAT_ID = TEST_TG_CHAT_ID or os.getenv('TEST_TG_CHAT_ID')

if not all([BOT_TOKEN, APP_URL, CHAT_ID]):
    logger.error(
        "Missing environment variables. Please set TELEGRAM_BOT_TOKEN, VERCEL_APP_URL, and TEST_TG_CHAT_ID."
    )
    exit(1)

bot = telegram.Bot(token=BOT_TOKEN)
commands = [
    telegram.BotCommand("status", "Check bot status"),
]
bot.set_my_commands(commands)

app = Flask(__name__)


def send_status_message():
    """Sends a status message to the specified chat."""
    try:
        bot.send_message(chat_id=CHAT_ID,
                         text="Hello from Flask! Bot is running.")
        logger.info("Status message sent successfully.")
    except Exception as e:
        logger.error(f"Failed to send status message: {e}")


@app.route('/')
def home():
    """Home route to check if the bot is running."""
    return 'Bot is running.'


@app.route('/webhook', methods=['POST'])
def webhook():
    """Webhook endpoint to process incoming updates from Telegram."""
    try:
        update = telegram.Update.de_json(request.get_json(force=True), bot)

        if update.message and update.message.text == '/status':
            send_status_message()

    except Exception as e:
        logger.error(f"Error handling update: {e}")

    return 'OK'


def set_webhook():
    """Sets the webhook URL for the bot."""
    try:
        success = bot.setWebhook(f"{APP_URL}/webhook")
        if success:
            logger.info("Webhook successfully set!")
        else:
            logger.error("Webhook setup failed.")
    except Exception as e:
        logger.error(f"Error setting webhook: {e}")


if __name__ == '__main__':
    set_webhook()
    app.run(threaded=True)
