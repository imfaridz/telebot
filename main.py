from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import warnings
import sentimentclassifier as sc
import random
warnings.filterwarnings('ignore')

token = '561092228:AAHsDIL835n-Ht3L-BastdUGGgv6qCtBWvk'
updater = Updater(token=token)


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="hai")


def echo(bot, update):
    positive_response = ['makasih bro', 'mantap lu memang bro terbaik', 'lu emang bro gw banget']
    negative_response = ['EH SI ANJING', 'BANGSAT NGEGAS', 'TAI BABI']
    neutral_response = ['ogitu', 'ok', 'sip']
    classifier = sc.train()
    classification = sc.classify(classifier, update.message.text.lower())
    if classification[1] > classification[0]:
        bot.send_message(chat_id=update.message.chat_id, text=random.choice(positive_response))
    elif classification[1] < classification[0]:
        bot.send_message(chat_id=update.message.chat_id, text=random.choice(negative_response))
    else:
        bot.send_message(chat_id=update.message.chat_id, text=random.choice(neutral_response))


dispatcher = updater.dispatcher
echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)
dispatcher.add_handler(CommandHandler('start', start))
updater.start_polling()
