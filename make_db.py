import json
import os
import re

import requests


def getting_path():
    path = os.getcwd()
    while re.search('/[^\s/]+$', path).group(0) != '/Demographic_proj':
        path = re.sub('/[^\s/]+$', '', path)
    return path + '/'


class MakingDB:
    def __init__(self):
        self.errors_in_persons = 0
        self.errors_in_comments = 0
        self.people = 0
        self.path = getting_path()

    def get_list_of_comments_id(self, public_id, post_num):  # Возвращаем список id постов
        com_id_list = []
        com_offset = 1  # Не берём первый пост (закреплённый)
        while len(com_id_list) < post_num:
            wall_res = requests.get('http://api.vk.com/method/wall.get', {
                'owner_id': public_id,
                'offset': com_offset,
                'count': post_num if post_num <= 100 else 100,
                'extended': '0'
            }).json()

            if (wall_res.get('response')):
                wall_res = wall_res['response'][1:]
            else:
                print('error')
                return []

            for item in wall_res:
                if len(com_id_list) != post_num:
                    if int(item['comments']['count']):
                        com_id_list.append([item['id'], item['comments']['count']])
                else:
                    break
            com_offset += post_num % 100
            post_num -= 100
        return com_id_list

    def create_new_man(self, people_db, id, text):
        try:
            res = requests.get('http://api.vk.com/method/users.get', {
                'user_ids': id,
                'fields': 'first_name,second_name,sex,bdate,universities,schools,relation,personal,career,military'
            }, timeout=3).json()['response'][0]
            if res.get('bdate') and re.search('\d\d\d\d', res.get('bdate')) and (
                res.get('universities') or res.get('schools')):
                people_db[id] = res
                people_db[id]['user_comments'] = [text]
                print('create new man', id)
        except BaseException:
            print('-----------------error in get persone', id, ':(')
            self.errors_in_persons += 1

    def make_db(self, com_id_list, public_id):
        people_db = {}
        k = 1
        for com in com_id_list:
            print('\n', k, com)
            k += 1
            offset_k = 0
            n = 0
            while com[1] > 0:
                try:
                    comm_get = requests.get('http://api.vk.com/method/wall.getComments', {
                        'owner_id': public_id,
                        'post_id': com[0],
                        'count': com[1] % 100,
                        'offset': 100 * offset_k

                    }, timeout=3).json()['response'][1:]
                    for item in comm_get:
                        print('handling', item['from_id'])
                        self.people += 1
                        if item['from_id'] in people_db:  # Добавляем коммент человека в db, иначе создаём человека)
                            people_db[item['from_id']]['user_comments'].append(item['text'])
                        else:
                            self.create_new_man(people_db, item['from_id'], item['text'])
                except BaseException:
                    print('--------------error in get comments', public_id, ':(')
                    self.errors_in_comments += 1

                offset_k += 1
                com[1] -= 100
                n += 1
        return people_db

    def public_handling(self, public_list, post_amount):
        db = []  # База людей
        for public_id in public_list:
            com_id_list = self.get_list_of_comments_id(public_id, post_amount)  # Список (id) постов в группе
            print('public number', public_id[1:])
            people_db = self.make_db(com_id_list, public_id)  # Словарь {человек: [информация, комменты]}

            for key in people_db.keys():
                people_db[key]['id'] = key
                db.append(people_db[key])
            with open('db/people_db1', 'w') as f:
                json.dump(db, f)

    def comment_handling(self):
        with open(self.path + 'db/people_db1') as f:
            db = json.load(f)  # Все данные о человеке

        sample = {0: [], 1: [], 2: [], 3: []}

        def min_grade(hb):
            grade = 2100
            for univ in hb['universities']:
                if univ.get('graduation'):
                    if univ.get('graduation') < grade:
                        grade = univ.get('graduation')
            if grade == 2000:
                return None
            else:
                return grade

        k = 0
        for hb in db:
            date = int(hb['bdate'][-4:])
            group = None
            k += 1

            if hb['user_comments']:
                if date > 1996 and not hb.get('universities'):
                    group = 1
                elif not hb.get('universities'):
                    group = 2
                elif min_grade(hb):
                    if min_grade(hb) >= 2016:
                        group = 3
                    elif min_grade(hb) < 2016:
                        group = 4
                if group:
                    sample[group - 1].append(hb['user_comments'])

        sample_names = dict(
            school=sample[0],
            no_university=sample[1],
            on_higher_edu=sample[2],
            graduated=sample[3])

        # {'class_name': [comments]}

        ################################################################

        com_class = [{} for el in range(len(sample_names.keys()))]
        names_dic = {}
        k = 0
        for key in sample_names:
            names_dic[k] = key
            for meses in sample_names[key]:
                for mes in meses:
                    com_class[k][mes] = k
            k += 1
        dic = {'comments-class': com_class,
               'class_names': names_dic}

        with open(self.path + 'db/' + self.sample_name, 'w') as f:
            json.dump(dic, f)

    def init(self
             , public_list=open(getting_path() + 'db/public_list', 'r').read().split('\n')
             , comments_amount=200
             , sample_name='sample1'
             ):
        self.public_handling(public_list, comments_amount)
        self.sample_name = sample_name
        print('errors in persons', self.errors_in_persons)
        print('errors in comments', self.errors_in_comments)
        print('number of people', self.people)
        self.comment_handling()

if __name__ == '__main__':
    MakingDB().init(public_list=open('db/public_list', 'r').read().split('\n'), comments_amount=200)
