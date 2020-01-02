from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext import Updater
import os
import pandas as pd
import configparser
import warnings
from lib import sentimentclassifier as sc
import random
import signal
from emoji import emojize
import sys
import logging
warnings.filterwarnings('ignore')


# Enable logging
fileh = logging.FileHandler(os.getcwd() + '/log/logfile', 'a')
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
logger.addHandler(fileh)

path_config = os.getcwd() + '/configs/config.ini'
config = configparser.ConfigParser()
config.read(path_config)


def signal_handler(signal, frame):
    sc.train(logger=logger, config=config)
    logger.info('Shutting down bot...')
    sys.exit(0)


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Hai {}!".format(update.message.from_user.first_name))


def echo(bot, update):
    user = update.message.from_user
    logger.info("User {} says : {}".format(user.first_name, update.message.text))
    classification = sc.predict(update.message.text)
    response_list = pd.read_csv(os.getcwd() + "/dataset/response_list.txt")
    if classification == 1:
        response = random.choice(response_list['positive'].values.tolist())
    else:
        response = random.choice(response_list['negative'].values.tolist())

    update.message.reply_text(emojize("{}".format(response), use_aliases=True), quote=True)
    logger.info("Bot reply : {}".format(response))


if __name__ == '__main__':

    # train if model doesn't exist
    if os.path.exists(os.getcwd()+"/model/classifier.pkl"):
        pass
    else:
        sc.train(logger=logger, config=config)

    token = str(config['DEFAULT'].get('TOKEN', None))
    updater = Updater(token=token)

    signal.signal(signal.SIGINT, signal_handler)

    dispatcher = updater.dispatcher
    echo_handler = MessageHandler(Filters.text & (~ Filters.forwarded), echo)
    dispatcher.add_handler(echo_handler)
    dispatcher.add_handler(CommandHandler('start', start))
    updater.start_polling()
