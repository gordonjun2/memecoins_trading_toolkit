from flask import render_template, request
from modules import modules
import telebot
import time


def configure_routes(app, bot):

    @app.route("/")
    def index():
        hello = modules.hello()
        content = modules.content()
        return render_template("index.html", hello=hello, content=content)
