import re
from functools import reduce

import nltk
import numpy


# Подсчёт количества матерных слов
def foul(comment):
    vec = []
    patterns =['^бля[(ть)д]?', 'ху[йиеё]\w+', 'шлюх\w*''сос[ак]\w+', '^[еёЕЁ]б[ау]\w*',
              '^[еёeЁ]б[ау]\w*', 'пизд\w+', '[^c]трах[ан]\w+', 'залуп\w*', 'срак[аоу]\w*',
              '\w*дроч\w+', '\w*говн\w+', 'ссан\w+', 'пидр\w*', 'уеб[(ище)ан]\w*']
    # Создание массива скомпиленных регулярок на основе массива паттернов
    patterns = list(map(lambda x: re.compile(x, re.IGNORECASE), patterns))
    # Суммироваине количества матерных слов по каждому паттерну
    return [reduce(lambda sum, pat: sum + len(pat.findall(comment)), patterns, 0) / (len(comment.split()) + 1)]


# Подсчёт количества пунктуационных знаков
def punctuation(comment):
    marks = ['\.', ',', '!', '\?', ':', '-']
    vec = [len(re.findall(mark, comment)) for mark in marks]
    return vec


# Количество слов с большой буквы
def capital_letter(comment):
    comment = nltk.tokenize.TweetTokenizer().tokenize(comment)
    count = 0
    for word in comment:
        if word[0].isupper():
            count += 1
    return count / len(comment) if len(comment) != 0 else 0


# Количество слов
def word_len(comment):
    vec = nltk.tokenize.TweetTokenizer().tokenize(comment)
    lenght = 0
    count = 0
    for el in vec:
        if re.search('\w+', el):
            lenght += len(el)
            count += 1
    return lenght / count if count != 0 else 0


# Количество различных слов
def amount_diff_words(comment):
    comment = nltk.tokenize.TweetTokenizer().tokenize(comment)
    return len(set(comment)) / len(comment) if len(comment) != 0 else 0

# TODO: Служебные слова, междометия (ах, да ладно, ну)
# TODO: pos-tagging (nltk, pymorphy)


def add_feat(mas):
    feat_vec = []
    for comment in mas:
        feats = foul(comment)
        feats.extend(punctuation(comment))
        feats.append(capital_letter(comment))
        feats.append(word_len(comment))
        feats.append(amount_diff_words(comment))
        feat_vec.append(feats)
    return numpy.array(feat_vec)
