import pandas as pd
import glob
from joblib import dump
import os
from sklearn.model_selection import train_test_split
import scraper
import datetime


def train(**kwargs):
    """
    This function will scrape the reviews and ratings inside
    Google Play Store. The links can be added or removed by
    editing the links.txt file inside dataset folder.
    """

    # read dataset
    logger = kwargs.get('logger')
    config = kwargs.get('config')

    today = datetime.date.today()
    if abs((today - modified_date).days) > 30:
        scraper.scrape(config=config, logger=logger)
    else:
        pass

    datasets = glob.glob(os.getcwd() + "/dataset/*.csv")
    columns = ['word', 'sentiment']
    data = pd.DataFrame(columns=columns)

    for dataset in datasets:
        temp_data = pd.read_csv(dataset, sep=";")
        data = pd.concat([data, temp_data])



    # TODO: word2vec