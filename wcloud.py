import json
import os
import re

import nltk
from wordcloud import WordCloud


def getting_path():
    path = os.getcwd()
    while re.search('/[^\s/]+$', path).group(0) != '/Demographic_proj':
        path = re.sub('/[^\s/]+$', '', path)
    return path + '/'


def preprocessing(text):
    text = re.sub('^[[\w|]+\], ', '', text)  # Удаляет обращения в начале строки

    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
    text = re.sub('[a-zA-Z]+\.[a-zA-Z-]+', ' ', text)  # Удаляет ссылки

    text = re.sub('<[^>]+>', '', text)  # Удаляет html-теги
    return text


def init():
    with open(getting_path() + 'db/sample', 'r') as f:
        file = json.load(f)

    with open(getting_path() + 'db/stop_words', 'r') as f:
        stop_words = set(f.read().split('\n'))

    def preproc(text):
        tokens1 = set(nltk.tokenize.TweetTokenizer().tokenize(text))
        tokens = tokens1 - stop_words
        return ' '.join(list(tokens))

    text = ''
    for clas in file['comments-class']:
        for pair in clas:
            text += preproc(preprocessing(pair))

    wordcloud = WordCloud(width=1000, height=500, stopwords=stop_words).generate(text)

    wordcloud.to_file(getting_path() + 'UI/db/wcloud.png')

init('sample')

"""
plt.imshow(wordcloud)
plt.axis("off")
plt.show()
"""
