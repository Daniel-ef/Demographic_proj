import json
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

        np = numpy
        classifier = MultinomialNB()
        tokenizer = nltk.tokenize.TweetTokenizer
        scaler = MaxAbsScaler()
        vectorizer = CountVectorizer(ngram_range=(1, 2)
                                     , tokenizer=tokenizer().tokenize
                                     , stop_words=stop_words
                                     , max_df=0.75
                                     )

        fold_nums = 5
        loo = LeaveOneOut(fold_nums)

        # ___________________________________________________________________________



    # Слияние массивов
    def ravel(mas):
        merged = []
        for l in mas:
            merged.extend(l)
        return merged

    """
    # Проведение кросс-валидации 4:1 ______________________
    def fill_cross_val(fold_nums):
        with open('db/sample', 'r') as f:
            people_sample = json.load(f)

        comments = [[] for el in range(fold_nums)]
        mes_class = [[] for el in range(fold_nums)]

        for mas in people_sample['comments-class']:
            mas = np.array(list(mas.items()))
            np.random.shuffle(mas)
            submas = dict(mas)
            fold_len = len(submas) / fold_nums
            i = 0
            for key in submas.keys():
                comments[int(i // fold_len)].append(key)
                mes_class[int(i // fold_len)].append(submas[key])
                i += 1

        return [np.array(comments), np.array(mes_class)]

    """
    comments, comments_class = fill_cross_val(fold_nums)
    # ______________________________________________________

    # Очистка комментариев
    def preprocessing(self, comments_mas):
        for comments_mas in comments:
            for i in range(len(comments_mas)):
                comments_mas[i] = preprocessing(comments_mas[i])

    estim = 0
    functions = set()
    for train_index, test_index in loo:

        # Обучающая и тестирующая выборки
        Com_train, Class_train = ravel(comments[train_index]), ravel(comments_class[train_index])
        Com_test, Class_test = comments[test_index][0], comments_class[test_index][0]


        # Собственные признаки
        add_feat_train, functions = add_feat(ravel(comments[train_index]))
        add_feat_test = add_feat(comments[test_index[0]])[0]

        #     Подсчёт количества слов
        #     Конкатенация признаков
        #     Приведение к нормальному виду

        # Обработка обучающей выборки:
        Com_train = vectorizer.fit_transform(Com_train)
        Com_train = scipy.sparse.hstack([Com_train, add_feat_train])
        Com_train = scaler.fit_transform(Com_train)

        # Обработка тестирующей выборки
        Com_test = vectorizer.transform(Com_test)
        Com_test = scipy.sparse.hstack([Com_test, add_feat_test])
        Com_test = scaler.transform(Com_test)


        # Обучение классификатора
        classifier.fit(Com_train, Class_train)
        ans = classifier.predict(Com_test)

        # Оценка предсказаний классификатора
        tr = 0
        for i in range(len(ans)):
            if ans[i] == Class_test[i]:
                tr += 1
        estim += tr / len(Class_test)
        print(str((tr / len(Class_test)) * 100) + ' %')

    print('\n' + str((estim / fold_nums) * 100) + ' %')

    # Запись логов в файл

    logging.info(time.ctime(time.time())
             + '\nClassifier: ' + str(classifier)
             + '\nVectorizer: ' + str(vectorizer)
             + '\nTokenizer: ' + str(tokenizer)
             + '\nScaler: ' + str(scaler)
             + '\nshufle: on'
             + '\n' + ' '.join(functions)
             + "\nEstimation " + str((estim / fold_nums) * 100)
             + ' %\n\n')

