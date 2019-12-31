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