import re
import time

COMMANDS = {
    'start': 'Gives information about the bot',
    'help': 'Gives information about all of the available commands',
    'ping': 'Measure the execution time to run test and send a message',
}


def is_command(string):
    pattern = r"^\/.*$"
    return bool(re.match(pattern, string))


def hello():
    return "Welcome to Memecoins Trading Toolkit!"


def content():
    return '''
            This message shows that the bot is working properly. Please use the bot in Telegram.
            '''
