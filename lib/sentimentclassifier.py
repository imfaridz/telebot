import pandas as pd
import glob
from joblib import dump
import os
import numpy as np
from sklearn.model_selection import train_test_split



def train():
    # read dataset
    dataset = glob.glob(os.getcwd() + "/dataset/*.txt")
    columns = ['word', 'sentiment']
    train_set = pd.DataFrame(columns=columns)

    for data in dataset:
        temp_data = pd.read_csv(data, sep="\n")
        if 'pos' in data:
            temp_data['sentiment'] = 1
            train_set = train_set.append(temp_data, ignore_index=True)
        else:
            temp_data['sentiment'] = 0
            train_set = train_set.append(temp_data, ignore_index=True)

    train_set['word'] = train_set['word'].str.lower()



def classify(sentence):
    neg, pos = 0, 0
    words = sentence.split(' ')
    for word in processed_words:
        classResult = classifier.predict(word.reshape(1, -1))
        if classResult == 0:
            neg = neg + 1
        if classResult == 1:
            pos = pos + 1
    return [float(pos) / len(words), float(neg) / len(words)]
