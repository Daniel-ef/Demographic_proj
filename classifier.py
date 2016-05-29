import logging
import os
import re
import time

import numpy
import scipy
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import MaxAbsScaler

from additional_features import add_feat


def getting_path():
    path = os.getcwd()
    while re.search('/[^\s/]+$', path).group(0) != '/Demographic_proj':
        path = re.sub('/[^\s/]+$', '', path)
    return path + '/'

# Получние пути корневой папки проекта
path_proj = getting_path()

logging.basicConfig(filename=path_proj + 'db/log'
                    , level=logging.INFO
                    , filemode='a', format='%(asctime)s %(message)s'
                    , datefmt='%d/%m/%Y %H:%M:%S'
                    )


class SimpleClassifier:
    def __init__(self):
        # Объявление глобальных переменных__________________________________________
        stop_words = list(set(stopwords.words('russian')).union(set(stopwords.words('english'))))

        self.link = re.compile('[a-zA-Z]+\.[a-zA-Z-]+')
        self.tag = re.compile('(\s|^)#\w+')

        self.np = numpy
        self.classifier = MultinomialNB()
        self.scaler = MaxAbsScaler()
        self.vectorizer = CountVectorizer(ngram_range=(1, 2)
                                     , stop_words=stop_words
                                     , max_df=0.75
                                     )

    def preprocessing(self, text):
        text = self.link.sub(' ', text)  # Удаляет ссылки
        text = text.replace('_', ' ')
        text = text.replace('...', '.')

        text = self.tag.sub('', text)  # Удаление тегов
        return text

    def fit(self, samples, labels):
        add_feat_train, self.functions = add_feat(samples)  # Признаки и массив функций для их получения

        samples = [self.preprocessing(comment) for comment in samples]  # Предобработка выборки

        samples = self.vectorizer.fit_transform(samples)
        samples = scipy.sparse.hstack([samples, add_feat_train])
        samples = self.scaler.fit_transform(samples)

        self.classifier.fit(samples, labels)

    def predict(self, samples):
        add_feat_train = add_feat(samples)[0]

        samples = [self.preprocessing(comment) for comment in samples]

        samples = self.vectorizer.transform(samples)
        samples = scipy.sparse.hstack([samples, add_feat_train])
        self.logger()
        return self.classifier.predict(samples)

    # Запись логов в файл

    def logger(self):
        logging.info(time.ctime(time.time())
                 + '\nClassifier: ' + str(self.classifier)
                 + '\nVectorizer: ' + str(self.vectorizer)
                 + '\nScaler: ' + str(self.scaler)
                 + '\nshufle: on'
                 + '\n' + ' '.join(self.functions)
                 + ' %\n'
                 )
