from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext import Updater
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
