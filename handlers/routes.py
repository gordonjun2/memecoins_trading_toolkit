from flask import render_template, request
from modules import modules
import telebot
import time


def configure_routes(app, bot, BOT_TOKEN, APP_URL):

    @app.route("/")
    def index():
        bot.remove_webhook()
        time.sleep(1)
        webhook_url = f"{APP_URL}/{BOT_TOKEN}"
        bot.set_webhook(url=webhook_url)

        hello = modules.hello()
        content = modules.content()
        return render_template("index.html", hello=hello, content=content)

    @app.route('/webhook', methods=['POST'])
    def webhook():
        update = telebot.types.Update.de_json(
            request.stream.read().decode("utf-8"))
        bot.process_new_updates([update])
        return "ok", 200
