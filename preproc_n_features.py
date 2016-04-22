import json
import time

import nltk
import numpy
from Additional_features import foul_find
from sklearn.preprocessing import MinMaxScaler
from sklearn.cross_validation import LeaveOneOut
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import GaussianNB

Classifier = GaussianNB()
Tokenizer = nltk.tokenize.TweetTokenizer
Scaler = MinMaxScaler((0, 2))
Vectorizer = CountVectorizer(ngram_range=(1, 2), tokenizer=Tokenizer().tokenize)

np = numpy
fold_nums = 5
loo = LeaveOneOut(fold_nums)
mes_amount = 2000

log = ''
log += time.ctime(time.time())
log += '\nClassifier: ' + str(Classifier)
log += '\nVectorizer: ' + str(Vectorizer)
log += '\nTokenizer: ' + str(Tokenizer)
log += '\nScaler: ' + str(Scaler)
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

messages, mess_class = fill_cross_val('comments-class', fold_nums, mes_amount)


estim = 0
for train_index, test_index in loo:

    Com_train, Class_train = ravel(messages[train_index]), ravel(mess_class[train_index])
    Com_test, Class_test = messages[test_index][0], mess_class[test_index][0]

    fouls_train = foul_find(ravel(messages[train_index]))
    fouls_test = foul_find(messages[test_index[0]])


    Com_train = Vectorizer.fit_transform(Com_train).toarray()
    Com_train = np.concatenate((Com_train, fouls_train.T), axis=1)
    Com_train = Scaler.fit_transform(Com_train)

    Com_test = Vectorizer.transform(Com_test).toarray()
    Com_test = np.concatenate((Com_test, fouls_test.T), axis=1)
    Com_test = Scaler.transform(Com_test)


    Classifier.fit(Com_train, Class_train)
    ans = Classifier.predict(Com_test)

    tr = 0
    for i in range(len(ans)):
        if ans[i] == Class_test[i]:
            tr += 1
    estim += tr / len(Class_test)
    print(str((tr / len(Class_test)) * 100) + ' %')

print(str((estim / fold_nums) * 100) + ' %')
log += str((estim / fold_nums) * 100) + ' %\n\n'
with open('db/log', 'a') as f:
    f.write(log)
