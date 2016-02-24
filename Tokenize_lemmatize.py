import re
import pymorphy2
morph = pymorphy2.MorphAnalyzer()

with open ('db/stop_word_dic', 'r') as f:
    stop_words = f.read().split('\n')
with open('db/text_for_test', 'r') as f:
    dic_norm_words = [morph.parse(word)[0].normal_form for word in re.findall('[а-яА-Я]+-?[а-яА-Я]*', f.read())]

for el in dic_norm_words:
    if el not in stop_words:
        print(el, end='\n')
