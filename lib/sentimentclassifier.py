import pandas as pd
from nltk.classify import NaiveBayesClassifier


def word_feats(words):
    return dict([(word, True) for word in words])


def train():
    # add dataset
    positive = pd.read_fwf('../telebot/dataset/positive.txt')
    negative = pd.read_fwf('../telebot/dataset/negative.txt')

    # lowercase
    positive['word'] = positive['word'].str.lower()
    negative['word'] = negative['word'].str.lower()

    # take samples
    positive_sample = positive.iloc[0:1000]
    negative_sample = negative.iloc[0:1000]

    positive_features = [(word_feats(word), 'positive') for word in positive_sample['word'].tolist()]
    negative_features = [(word_feats(word), 'negative') for word in negative_sample['word'].tolist()]
    train_set = positive_features + negative_features

    return NaiveBayesClassifier.train(train_set)


def classify(classifier, sentence):
    neg = 0
    pos = 0
    words = sentence.split(' ')
    for word in words:
        classResult = classifier.classify(word_feats(word))
        if classResult == 'negative':
            neg = neg + 1
        if classResult == 'positive':
            pos = pos + 1
    return [float(pos) / len(words), float(neg) / len(words)]

