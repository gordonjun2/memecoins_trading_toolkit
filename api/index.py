import sys
import os
from flask import Flask, request
import telegram

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import (TELEGRAM_BOT_TOKEN, TEST_TG_CHAT_ID, VERCEL_APP_URL)

BOT_TOKEN = TELEGRAM_BOT_TOKEN or os.getenv('TELEGRAM_BOT_TOKEN')
APP_URL = VERCEL_APP_URL or os.getenv('VERCEL_APP_URL')
CHAT_ID = TEST_TG_CHAT_ID or os.getenv('TEST_TG_CHAT_ID')
bot = telegram.Bot(token=BOT_TOKEN)
commands = [
    telegram.BotCommand("status", "Check bot status"),
]
bot.set_my_commands(commands)

app = Flask(__name__)


@app.route('/')
def home():
    if not BOT_TOKEN:
        return "TELEGRAM_BOT_TOKEN is not set in the environment variables."

    return 'Bot is running.'


@app.route('/status')
def send_message():
    if not CHAT_ID:
        return "TEST_TG_CHAT_ID is not set."
    bot.send_message(chat_id=CHAT_ID, text="Hello from Flask! Bot is running.")
    return "Message sent!"


@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        update = telegram.Update.de_json(request.get_json(force=True), bot)

        if update.message and update.message.text == '/status':
            bot.send_message(chat_id=CHAT_ID,
                             text="Hello from Flask! Bot is running.")

    except Exception as e:
        print(f"Error handling update: {e}")

    return 'OK'


@app.before_first_request
def setup_webhook():
    success = bot.setWebhook(f"{APP_URL}/webhook")
    if success:
        print("Webhook successfully set!")
    else:
        print("Webhook setup failed.")


if __name__ == '__main__':
    app.run(threaded=True)
