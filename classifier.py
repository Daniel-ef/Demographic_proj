import logging
import time

import nltk
import numpy
import scipy
from sklearn.cross_validation import LeaveOneOut
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import MaxAbsScaler

from additional_features import add_feat
from tokenize_lemmatize import preprocessing

logging.basicConfig(filename='db/log'
                    , level=logging.INFO
                    , filemode='a', format='%(asctime)s %(message)s'
                    , datefmt='%d/%m/%Y %H:%M:%S'
                    )

# TODO: разобраться с test_clf
# TODO: быть может добавить признак - количество каждого смайлика
# TODO: сделать из всего этого shit - class
# TODO: фигануть Джанго - хей


class SimpleClassifier:
    def __init__(self):
        # Объявление глобальных переменных__________________________________________
        with open('db/stop_word_dic', 'r') as f:
            stop_words = f.read().split('\n')

        self.np = numpy
        self.classifier = MultinomialNB()
        self.tokenizer = nltk.tokenize.TweetTokenizer
        self.scaler = MaxAbsScaler()
        self.vectorizer = CountVectorizer(ngram_range=(1, 2)
                                     , tokenizer=self.tokenizer().tokenize
                                     , stop_words=stop_words
                                     , max_df=0.75
                                     )

        self.fold_nums = 5
        self.loo = LeaveOneOut(self.fold_nums)

        # ___________________________________________________________________________

    # Очистка комментариев
    def preprocessing(self, comments):
        for i in range(len(comments)):
            comments[i] = preprocessing(comments[i])
        return comments

    def fit(self, samples, labels):
        # samples = self.preprocessing(samples)
        add_feat_train, self.functions = add_feat(samples)
        samples = self.vectorizer.fit_transform(samples)
        samples = scipy.sparse.hstack([samples, add_feat_train])
        samples = self.scaler.fit_transform(samples)

        self.classifier.fit(samples, labels)

    def predict(self, samples):
        add_feat_train = add_feat(samples)[0]
        samples = self.vectorizer.transform(samples)
        samples = scipy.sparse.hstack([samples, add_feat_train])
        self.logger()
        return self.classifier.predict(samples)

    # Запись логов в файл

    def logger(self):
        logging.info(time.ctime(time.time())
                 + '\nClassifier: ' + str(self.classifier)
                 + '\nVectorizer: ' + str(self.vectorizer)
                 + '\nTokenizer: ' + str(self.tokenizer)
                 + '\nScaler: ' + str(self.scaler)
                 + '\nshufle: on'
                 + '\n' + ' '.join(self.functions)
                 + ' %\n'
                 )
