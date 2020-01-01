import pandas as pd
import glob
from joblib import dump, load
import os
from sklearn.model_selection import train_test_split
import scraper
import datetime
import time
import errno
from gensim.models import word2vec
from sklearn.ensemble import RandomForestClassifier
from nltk.tokenize import word_tokenize


def train(**kwargs):
    """
    This function will scrape the reviews and ratings inside
    Google Play Store. The links can be added or removed by
    editing the links.txt file inside dataset folder.
    """

    logger = kwargs.get('logger')
    config = kwargs.get('config')

    today = datetime.date.today()

    # Scrape reviews from Play Store if not available/outdated
    try:
        modified_date = os.path.getmtime(os.getcwd() + '/dataset/review_0.csv')
        modified_date = datetime.datetime.fromtimestamp(modified_date).date()

        if abs((today - modified_date).days) > 30:
            logger.info('Data is outdated, begin scraping...')
            scraper.scrape(config=config, logger=logger)
        else:
            pass
            logger.info('Data is available...')

    except IOError as e:
        if e.errno == errno.ENOENT:
            logger.info('Data is not available, begin scraping...')
            scraper.scrape(config=config, logger=logger)

    # Read scraped data
    data = import_data()

    # Pre-processing
    sentences = data2sentences(data)

    # TODO: word2vec

    # Creating the model and setting values for the various parameters
    num_features = 300  # Word vector dimensionality
    min_word_count = 40  # Minimum word count
    num_workers = 4  # Number of parallel threads
    context = 10  # Context window size
    downsampling = 1e-3  # (0.001) Downsample setting for frequent words

    model = word2vec.Word2Vec(sentences,
                              workers=num_workers,
                              size=num_features,
                              min_count=min_word_count,
                              window=context,
                              sample=downsampling)

    # To make the model memory efficient
    model.init_sims(replace=True)

    # Saving the model for later use. Can be loaded using Word2Vec.load()
    dump(model, 'word2vec.pkl')

    # Split dataset into train-test
    

    # Calculating average feature vector for training set
    clean_train_reviews = []
    for review in train['review']:
        clean_train_reviews.append(review_wordlist(review, remove_stopwords=True))

    train_data_vecs = get_avg_feature_vecs(clean_train_reviews, model, num_features)

    # Calculating average feature vactors for test set
    clean_test_reviews = []
    for review in test["review"]:
        clean_test_reviews.append(review_wordlist(review, remove_stopwords=True))

    test_data_vecs = get_avg_feature_vecs(clean_test_reviews, model, num_features)
    forest = RandomForestClassifier(n_estimators=100)

    print("Fitting random forest to training data....")
    forest = forest.fit(train_data_vecs, train["sentiment"])

    dump(forest, 'classifier.pkl')


def import_data():
    datasets = glob.glob(os.getcwd() + "/dataset/review_*.csv")
    data = pd.DataFrame()

    for dataset in datasets:
        temp_data = pd.read_csv(dataset, sep=";", decimal=",")
        data = pd.concat([data, temp_data])

    data['sentiment'] = data.rating.map(lambda x: 0 if (x <= 2.5) else 1)

    return data


def data2sentences(df):
    """
    Remove stop words and digits
    """

    stopwords = pd.read_csv(os.getcwd() + "/dataset/stopwordbahasa.csv", sep=",", header=None)
    stopwords = stopwords[0].values.tolist()
    stops = set(stopwords)

    sentences = []
    for review in df['review']:
        if len(review) > 0:
            review = re.sub(r'\d+', '', review)
            tokenize = word_tokenize(review)
            words = [w for w in tokenize if not w in stops]
            sentences.append(words)
    return sentences


def feature_vec_method(words, model, num_features):
    # Function to average all word vectors in a paragraph

    # Pre-initialising empty numpy array for speed
    feature_vec = np.zeros(num_features, dtype="float32")
    nwords = 0

    # Converting Index2Word which is a list to a set for better speed in the execution.
    index2word_set = set(model.wv.index2word)

    for word in words:
        if word in index2word_set:
            nwords = nwords + 1
            feature_vec = np.add(feature_vec, model[word])

    # Dividing the result by number of words to get average
    feature_vec = np.divide(feature_vec, nwords)
    return feature_vec


def get_avg_feature_vecs(reviews, model, num_features):
    # Function for calculating the average feature vector
    counter = 0
    review_feature_vecs = np.zeros((len(reviews), num_features), dtype="float32")
    for review in reviews:
        # Printing a status message every 1000th review
        if counter % 1000 == 0:
            print("Review %d of %d" % (counter, len(reviews)))

        review_feature_vecs[counter] = feature_vec_method(review, model, num_features)
        counter = counter + 1

    return review_feature_vecs


def predict():
    # Predicting the sentiment values for test data and saving the results in a csv file
    result = forest.predict(test_data_vecs)
    output = pd.DataFrame(data={"id": test["id"], "sentiment": result})
    output.to_csv("output.csv", index=False, quoting=3)