from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import os
import configparser
import warnings
from lib import sentimentclassifier as sc
import random
warnings.filterwarnings('ignore')

path_config = os.getcwd() + '/config.ini'
config = configparser.ConfigParser()
config.read()
token = str(config['DEFAULT'].get('TOKEN', None))
updater = Updater(token=token)


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="hai")


def echo(bot, update):
    positive_response = ['makasih bro', 'mantap lu memang bro terbaik', 'lu emang bro gw banget']
    negative_response = ['EH SI ANJING', 'BANGSAT NGEGAS', 'TAI BABI']
    neutral_response = ['ogitu', 'ok', 'sip']
    answer_list = ['bro', 'bot', 'brobot']
    if any(s in answer_list for s in update.message.text.lower().split(" ")) == True:
        classifier = sc.train()
        classification = sc.classify(classifier, update.message.text.lower())
        if classification[1] > classification[0]:
            bot.send_message(chat_id=update.message.chat_id,
                             text=update.message.reply_text(random.choice(positive_response), quote=True))
        elif classification[1] < classification[0]:
            bot.send_message(chat_id=update.message.chat_id,
                             text=update.message.reply_text(random.choice(negative_response), quote=True))
        else:
            bot.send_message(chat_id=update.message.chat_id,
                             text=update.message.reply_text(random.choice(neutral_response), quote=True))


dispatcher = updater.dispatcher
echo_handler = MessageHandler(Filters.text & (~ Filters.forwarded), echo)
dispatcher.add_handler(echo_handler)
dispatcher.add_handler(CommandHandler('start', start))
updater.start_polling()

