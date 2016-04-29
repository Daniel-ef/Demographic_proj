import json
import time

import nltk
import numpy
from sklearn.cross_validation import LeaveOneOut
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import MinMaxScaler

from additional_features import add_feat


def init():
    with open('db/stop_word_dic', 'r') as f:
        stop_words = f.read().split('\n')

    np = numpy
    classifier = GaussianNB()
    tokenizer = nltk.tokenize.TweetTokenizer
    scaler = MinMaxScaler((0, 2))
    vectorizer = CountVectorizer(ngram_range=(1, 2),
                                 tokenizer=tokenizer().tokenize,
                                 stop_words=stop_words)

    fold_nums = 5
    loo = LeaveOneOut(fold_nums)
    mes_amount = -1  # Количество комментариев для каждого fold'а (-1 == все)

    log = ''
    log += time.ctime(time.time())
    log += '\nClassifier: ' + str(classifier)
    log += '\nVectorizer: ' + str(vectorizer)
    log += '\nTokenizer: ' + str(tokenizer)
    log += '\nScaler: ' + str(scaler)
    log += '\n'

    def ravel(mas):
        merged = []
        for l in mas:
            merged.extend(l)
        return merged

    def fill_cross_val(key, fold_nums, mes_amount=500):
        global log
        with open('db/people_sample', 'r') as f:
            people_sample = json.load(f)
        log += ('Comments of each class: ' +
            str(mes_amount if mes_amount != -1 else 'all') + '\n')

        messages = [[] for el in range(fold_nums)]
        mes_class = [[] for el in range(fold_nums)]

        for mas in people_sample[key]:
            mes_amount = mes_amount if mes_amount != -1 else len(mas)
            submas = dict(list(mas.items())[:mes_amount])
            fold_len = len(submas) / fold_nums
        i = 0
        for key in submas.keys():
            messages[int(i // fold_len)].append(key)
            mes_class[int(i // fold_len)].append(submas[key])
            i += 1

        return [np.array(messages), np.array(mes_class)]

    # Проведение кросс-валидации 4:1
    messages, mess_class = fill_cross_val('comments-class', fold_nums, mes_amount)


    estim = 0
    for train_index, test_index in loo:

        # Обучающая и тестирующая выборки
        Com_train, Class_train = ravel(messages[train_index]), ravel(mess_class[train_index])
        Com_test, Class_test = messages[test_index][0], mess_class[test_index][0]


        # Собственные признаки
        add_feat_train = add_feat(ravel(messages[train_index]))
        add_feat_test = add_feat(messages[test_index[0]])

        #     Подсчёт количества слов
        #     Конкатенация признаков
        #     Приведение к нормальному виду

        # Обработка обучающей выборки:
        Com_train = vectorizer.fit_transform(Com_train).toarray()
        Com_train = np.concatenate((Com_train, add_feat_train), axis=1)
        Com_train = scaler.fit_transform(Com_train)

        # Обработка тестирующей выборки
        Com_test = vectorizer.transform(Com_test).toarray()
        Com_test = np.concatenate((Com_test, add_feat_test), axis=1)
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

    print(str((estim / fold_nums) * 100) + ' %')

    # Запись логов в файл
    with open('db/log', 'a') as f:
        f.write(log + str((estim / fold_nums) * 100) + ' %\n\n')
