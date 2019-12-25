import pandas as pd
from nltk.classify import NaiveBayesClassifier
import glob
from joblib import dump
import os


def word_feats(words):
    return dict([(word, True) for word in words])


def train():
    # add dataset
    dataset = glob.glob(os.getcwd() + "/dataset/*.txt")
    positive = pd.DataFrame()
    negative = positive.copy()

    for data in dataset:
        temp_data = pd.read_csv(data, sep="\n", header=None)
        if 'pos' in data:
            positive = pd.concat([positive, temp_data])
        else:
            negative = pd.concat([negative, temp_data])

    # lowercase
    positive[0] = positive[0].str.lower()
    negative[0] = negative[0].str.lower()

    positive_features = [(word_feats(word), 'positive') for word in positive[0].tolist()]
    negative_features = [(word_feats(word), 'negative') for word in negative[0].tolist()]
    train_set = positive_features + negative_features
    dump(NaiveBayesClassifier.train(train_set), 'model.pkl')


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
