import re
import pymorphy2
morph = pymorphy2.MorphAnalyzer()

with open ('db/stop_word_dic', 'r') as f:
    stop_words = f.read().split('\n')

with open('db/text_for_test', 'r') as f:
    text = f.read()
text = text[re.match('\w+, ?', text).end():]  # Удаляет обращения в начале строки
text = re.sub('\S+\.\w+', '', text)  # Удаляет ссылки
text = re.sub('<[^>]+>', '', text)  #  Удаляет html-теги

dic_norm_words = [morph.parse(word)[0].normal_form for word in re.findall('[a-zA-Zа-яА-Я]+-?[a-zA-Zа-яА-Я]*', text)]

for el in dic_norm_words:
    if el not in stop_words:
        print(el, end='\n')
