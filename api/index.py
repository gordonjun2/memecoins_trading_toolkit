import telebot
import os
import time
from flask import Flask

from modules import modules
from handlers.routes import configure_routes
from config import (TELEGRAM_BOT_TOKEN, TEST_TG_CHAT_ID, VERCEL_APP_URL,
                    OWNER_ID)

BOT_TOKEN = TELEGRAM_BOT_TOKEN or os.getenv('TELEGRAM_BOT_TOKEN')
APP_URL = VERCEL_APP_URL or os.getenv('VERCEL_APP_URL')
CHAT_ID = TEST_TG_CHAT_ID or os.getenv('TEST_TG_CHAT_ID')
OWNER_ID = OWNER_ID or os.getenv('OWNER_ID')

bot = telebot.TeleBot(token=BOT_TOKEN, threaded=False)
app = Flask(__name__, template_folder="../templates")
configure_routes(app, bot, APP_URL)


@bot.message_handler(commands=['start'])
def command_start(message):
    cid = message.chat.id
    bot.send_message(
        cid,
        "Welcome to Memecoins Trading Toolkit!\nType /help to find all commands."
    )


@bot.message_handler(commands=['help'])
def command_help(message):
    cid = message.chat.id
    help_text = "The following commands are available: \n"
    for key in modules.COMMANDS:
        help_text += '/' + key + ': '
        help_text += modules.COMMANDS[key] + '\n'
    bot.send_message(cid, help_text)


@bot.message_handler(commands=['ping', 'p'])
def command_ping(message):
    if message.chat.id != int(OWNER_ID):
        bot.reply_to(message, "Sorry you are not allowed to use this command!")
    else:
        start_time = time.time()
        ping = modules.get_running_time(start_time)
        bot.reply_to(message, "PONG! Running time: {:.3f} s.".format(ping))


@bot.message_handler(func=lambda message: modules.is_command(message.text))
def command_unknown(message):
    command = str(message.text).split()[0]
    bot.reply_to(
        message,
        "Sorry, {} command not found!\nPlease use /help to find all commands.".
        format(command))


if __name__ == '__main__':
    app.run(threaded=False)