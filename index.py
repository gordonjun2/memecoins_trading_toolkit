import logging
import telebot
import os
from flask import Flask, request, abort

from modules import modules
from handlers.routes import configure_routes

from config import (TELEGRAM_BOT_TOKEN, TEST_TG_CHAT_ID, VERCEL_APP_URL,
                    USER_ID)

BOT_TOKEN = TELEGRAM_BOT_TOKEN or os.getenv('TELEGRAM_BOT_TOKEN')
APP_URL = VERCEL_APP_URL or os.getenv('VERCEL_APP_URL')
CHAT_ID = TEST_TG_CHAT_ID or os.getenv('TEST_TG_CHAT_ID')
USER_ID = USER_ID or os.getenv('USER_ID')

bot = telebot.TeleBot(token=BOT_TOKEN, threaded=False)
app = Flask(__name__)
configure_routes(app, bot)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s',
                    handlers=[logging.StreamHandler()])

logger = logging.getLogger(__name__)


@app.route(f"/{BOT_TOKEN}", methods=['POST'])
def telegram_webhook():
    if request.headers.get('content-type') == 'application/json':
        json_data = request.get_data().decode('utf-8')
        logger.debug(f"Received JSON: {json_data}")
        update = telebot.types.Update.de_json(json_data)
        bot.process_new_updates([update])
        logger.info("Processed new update")
        return 'OK', 200
    else:
        abort(403)


@bot.message_handler(commands=['start'])
def command_start(message):
    cid = message.chat.id
    logger.info(f"Received /start from chat_id: {cid}")
    bot.send_message(
        cid,
        "Welcome to Memecoins Trading Toolkit!\nType /help to find all commands."
    )


@bot.message_handler(commands=['help'])
def command_help(message):
    cid = message.chat.id
    logger.info(f"Received /help from chat_id: {cid}")
    help_text = "The following commands are available: \n"
    for key in modules.COMMANDS:
        help_text += '/' + key + ': '
        help_text += modules.COMMANDS[key] + '\n'
    bot.send_message(cid, help_text)


@bot.message_handler(commands=['ping', 'p'])
def command_ping(message):
    logger.info(f"Received /ping from chat_id: {message.chat.id}")
    if message.chat.id != int(USER_ID):
        bot.reply_to(message, "Sorry you are not allowed to use this command!")
        logger.warning(
            f"Unauthorized /ping attempt from chat_id: {message.chat.id}")
    else:
        bot.reply_to(message, "PONG!")
        logger.info(f"Responded to /ping to chat_id: {message.chat.id}")


@bot.message_handler(func=lambda message: modules.is_command(message.text))
def command_unknown(message):
    command = str(message.text).split()[0]
    logger.warning(
        f"Unknown command received: {command} from chat_id: {message.chat.id}")
    bot.reply_to(
        message,
        f"Sorry, {command} command not found!\nPlease use /help to find all commands."
    )
