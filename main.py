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
import logging
warnings.filterwarnings('ignore')

#TODO : change response to emoticons, move telegram actions to another lib


# Enable logging
fileh = logging.FileHandler(os.getcwd() + '/log/logfile', 'a')
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
logger.addHandler(fileh)


def signal_handler(signal, frame):
    # sc.train()
    print('shutting down bot..')
    sys.exit(0)


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Hai {}!".format(update.message.from_user.first_name))


def echo(bot, update):
    positive_response = ['makasih bro', 'mantap lu memang bro terbaik', 'lu emang bro gw banget']
    negative_response = ['EH SI ANJING', 'BANGSAT NGEGAS', 'TAI BABI']
    neutral_response = ['ogitu', 'ok', 'sip']

    classifier = load('model.pkl')
    user = update.message.from_user
    # check message whether its classified or not
    # if exist train unclassified else do classification

    # classify sentence
    # classification = sc.classify(classifier, vectorizer, update.message.text.lower())


    logger.info("User {} says : {}".format(user.first_name, update.message.text))

    if classification[1] > classification[0]:
        response = random.choice(positive_response)
    elif classification[1] < classification[0]:
        response = random.choice(negative_response)
    else:
        response = random.choice(neutral_response)

    update.message.reply_text(response, quote=True)

    logger.info("Bot reply : {}".format(response))


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
