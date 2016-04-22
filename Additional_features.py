import numpy
import re
from functools import reduce


def foul_find(mas):
    vec = []
    patterns =['^бля[(ть)д]?', 'ху[йиеё]\w+', 'шлюх\w*''сос[ак]\w+', '^[еёeЁ]б[ау]\w*',
              '^[еёeЁ]б[ау]\w*', 'пизд\w+', '[^c]трах[ан]\w+', 'залуп\w*', 'срак[аоу]\w*',
              '\w*дроч\w+', '\w*говн\w+', 'ссан\w+', 'пидр\w*', 'уеб[(ище)ан]\w*']
    patterns = list(map(lambda x: re.compile(x), patterns))
    for comment in mas:
        vec.append(reduce(lambda sum, pat: sum + len(pat.findall(comment.lower())), patterns, 0))
    return [vec]


def punctuation(mas, vec_feat):  # , . ! ? : -
    marks = ['\.', ',', '!', '\?', ':', '-']
    for mark in marks:
        vec = []
        for com in mas:
            vec.append(len(re.findall(mark, com)))
        vec_feat.append(vec)
    return vec_feat



def add_feat(mas):
    vec_feat = foul_find(mas)
    vec_feat = punctuation(mas, vec_feat)
    return numpy.array(vec_feat).T
