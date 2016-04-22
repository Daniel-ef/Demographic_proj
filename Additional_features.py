import numpy
import re


def fouls_num(comment):
    k = 0
    k += len(re.findall('^бля[(ть)д]?', comment))
    k += len(re.findall('ху[йие]\w+', comment))
    k += len(re.findall('шлюх\w*', comment))
    k += len(re.findall('сос[ак]\w+', comment))
    k += len(re.findall('^[еёeЁ]б[ау]\w*', comment))
    k += len(re.findall('пизд\w+', comment))
    k += len(re.findall('[^c]трах[ан]\w+', comment))
    k += len(re.findall('залуп\w*', comment))
    k += len(re.findall('срак[аоу]\w*', comment))
    k += len(re.findall('\w*дроч\w+', comment))
    k += len(re.findall('\w*говн\w+', comment))
    k += len(re.findall('ссан\w+', comment))
    k += len(re.findall('пидр\w*', comment))
    k += len(re.findall('уеб[(ище)ан]\w*', comment))
    return k


def foul_find(mas):
    vec = []
    for comment in mas:
        vec.append(fouls_num(comment))
    return numpy.array([vec])


