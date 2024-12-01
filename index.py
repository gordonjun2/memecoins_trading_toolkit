import logging
import telebot
import os
import time
from flask import Flask, request, abort
import threading
import schedule

from modules import modules
from handlers.routes import configure_routes
from get_token_balances_change import get_token_balance_change

from config import (TELEGRAM_BOT_TOKEN, TEST_TG_CHAT_ID, VERCEL_APP_URL,
                    OWNER_ID)

BOT_TOKEN = TELEGRAM_BOT_TOKEN or os.getenv('TELEGRAM_BOT_TOKEN')
APP_URL = VERCEL_APP_URL or os.getenv('VERCEL_APP_URL')
CHAT_ID = TEST_TG_CHAT_ID or os.getenv('TEST_TG_CHAT_ID')
OWNER_ID = OWNER_ID or os.getenv('OWNER_ID')

bot = telebot.TeleBot(token=BOT_TOKEN, threaded=False)
app = Flask(__name__)
configure_routes(app)

logging.basicConfig(level=logging.INFO,
                    format='%(message)s',
                    handlers=[logging.StreamHandler()])

logger = logging.getLogger(__name__)


def job_to_run_periodically():
    try:
        logger.info(
            f"Running function to get top traders' token balance change for: {OWNER_ID}"
        )
        bot.send_message(
            OWNER_ID,
            "Running function to get top traders' token balance change...")
        tg_msg = get_token_balance_change(logger)
        if tg_msg:
            logger.info(f"Sent token balance updates to: {OWNER_ID}")
            bot.send_message(OWNER_ID, tg_msg)
        else:
            logger.info("No token balance changes found.")
            bot.send_message(OWNER_ID, "No token balance changes found.")
        logger.info("Successfully ran get_token_balance_change function.")
    except Exception as e:
        msg = f"Error running get_token_balance_change function: {e}"
        logger.error(msg)
        bot.send_message(OWNER_ID, msg)


def run_periodic_jobs():
    schedule.every(1).hour.do(job_to_run_periodically)

    while True:
        schedule.run_pending()
        time.sleep(1)


threading.Thread(target=run_periodic_jobs, daemon=True).start()


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
    if message.chat.id != int(OWNER_ID):
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
