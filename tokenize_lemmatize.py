import re

import pymorphy2


def lemma_text(text):
    morph = pymorphy2.MorphAnalyzer()
    with open ('db/stop_word_dic', 'r') as f:
        stop_words = f.read().split('\n')

    if (re.match('\w+, ?', text)):
        text = text[re.match('\w+, ?', text).end():]  # Удаляет обращения в начале строки
    text = re.sub('\S+\.[\S-]+', '', text)  # Удаляет ссылки
    text = re.sub('<[^>]+>', '', text)  #  Удаляет html-теги

    vec_norm_words = [morph.parse(word)[0].normal_form for word in re.findall('[a-zA-Zа-яА-Я]+-?[a-zA-Zа-яА-Я]*', text)]

    text = []
    for el in vec_norm_words:
        if el not in stop_words:
            text.append(el)
    return text
