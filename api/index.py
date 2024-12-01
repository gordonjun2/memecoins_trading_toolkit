import sys
import os
from flask import Flask
import telegram

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import (TELEGRAM_BOT_TOKEN, TEST_TG_CHAT_ID, VERCEL_APP_URL)

BOT_TOKEN = TELEGRAM_BOT_TOKEN or os.getenv('TELEGRAM_BOT_TOKEN')
APP_URL = VERCEL_APP_URL or os.getenv('VERCEL_APP_URL')
CHAT_ID = TEST_TG_CHAT_ID or os.getenv('TEST_TG_CHAT_ID')
bot = telegram.Bot(token=BOT_TOKEN)

app = Flask(__name__)


@app.route('/')
def home():
    if not BOT_TOKEN:
        return "TELEGRAM_BOT_TOKEN is not set in the environment variables."

    return 'Bot is running.'


@app.route('/send_message')
def send_message():
    bot.send_message(chat_id=CHAT_ID, text="Hello from Flask! Bot is running.")
    return "Message sent!"


@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=APP_URL, HOOK=BOT_TOKEN))
    if s:
        return "Webhook setup successful"
    else:
        return "Webhook setup failed"


if __name__ == '__main__':
    app.run(threaded=True)
