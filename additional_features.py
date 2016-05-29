import re
from functools import reduce

import nltk
import numpy
import pymorphy2

morph = pymorphy2.MorphAnalyzer()
# emoji = re.compile("""[^\w|\s| \. | , | / | < | > | : | ; | \' | \{ | \} | \[ | \] | ! | @ | # | № | \$ | % | \^ | \* | \( | \) | \+ | \- | _ | \= | \? | " | \\\ | « | » | - | … | ~]+""")
patterns =['^бля[(ть)д]?', 'ху[йиеё]\w+', 'шлюх\w*''сос[ак]\w+', '^[еёЕЁ]б[ау]\w*',
              '^[еёeЁ]б[ау]\w*', 'пизд\w+', '[^c]трах[ан]\w+', 'залуп\w*', 'срак[аоу]\w*',
              '\w*дроч\w+', '\w*говн\w+', 'ссан\w+', 'пидр\w*', 'уеб[(ище)ан]\w*']

# Создание массива скомпиленных регулярок на основе массива паттернов
patterns = list(map(lambda x: re.compile(x, re.IGNORECASE), patterns))


# Подсчёт количества матерных слов
def foul(comment):
    # Суммироваине количества матерных слов по каждому паттерну
    return [reduce(lambda sum, pat: sum + len(pat.findall(comment)), patterns, 0) / (len(comment.split()) + 1)]


# Подсчёт количества пунктуационных знаков
def punctuation(tokens):
    marks = {'.': 0, ',': 0, '!': 0, '?': 0, ':': 0, '-': 0, '...': 0, '..': 0}
    for token in tokens:
        for key in marks.keys():
            if key == token:
                marks[key] += 1
    return [marks[key] / len(tokens) if len(tokens) != 0 else 0 for key in sorted(marks.keys())]


# Количество слов с большой буквы
def capital_letter(tokens):
    count = 0
    for word in tokens:
        if word[0].isupper():
            count += 1
    return count / len(tokens) if len(tokens) != 0 else 0


# Количество различных слов
def amount_diff_words(tokens):
    return len(set(tokens)) / len(tokens) if len(tokens) != 0 else 0


def add_feat(mas):
    feat_vec = []
    functions = set()
    for comment in mas:
        tokens = nltk.tokenize.TweetTokenizer().tokenize(comment)
        feats = foul(comment)
        functions.add(str(foul).split()[1])

        feats.extend(punctuation(tokens))
        functions.add(str(punctuation).split()[1])

        feats.append(capital_letter(tokens))
        functions.add(str(capital_letter).split()[1])

        feats.append(amount_diff_words(tokens))
        functions.add(str(amount_diff_words).split()[1])

        feat_vec.append(feats)
    return [numpy.array(feat_vec), functions]
