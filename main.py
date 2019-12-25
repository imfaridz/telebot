from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import os
import configparser
import warnings
from lib import sentimentclassifier as sc
from joblib import load
import random
import signal
import sys
warnings.filterwarnings('ignore')


def signal_handler(signal, frame):
    sc.train()
    print('shutting down bot..')
    sys.exit(0)


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="hai")


def echo(bot, update):
    positive_response = ['makasih bro', 'mantap lu memang bro terbaik', 'lu emang bro gw banget']
    negative_response = ['EH SI ANJING', 'BANGSAT NGEGAS', 'TAI BABI']
    neutral_response = ['ogitu', 'ok', 'sip']
    classifier = load('model.pkl')
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


def main():
    path_config = os.getcwd() + '/configs/config.ini'
    config = configparser.ConfigParser()
    config.read(path_config)
    token = str(config['DEFAULT'].get('TOKEN', None))
    updater = Updater(token=token)

    signal.signal(signal.SIGINT, signal_handler)

    dispatcher = updater.dispatcher
    echo_handler = MessageHandler(Filters.text & (~ Filters.forwarded), echo)
    dispatcher.add_handler(echo_handler)
    dispatcher.add_handler(CommandHandler('start', start))
    updater.start_polling()



if __name__ == '__main__':
    main()
