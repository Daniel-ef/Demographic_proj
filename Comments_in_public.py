import json
import requests
import time

with open('db/public_list', 'r') as f:
    public_list = f.read().split('\n') # Список групп в виде -номер


def get_list_of_comments_id(public_id, comments_num):  # Возвращаем список id постов
    com_id_list = []
    com_offset = 1  # Не берём первый пост (закреплённый)
    while len(com_id_list) < comments_num:
        wall_res = requests.get('http://api.vk.com/method/wall.get', {
            'owner_id': public_id,
            'offset': com_offset,
            'count': comments_num % 100,
            'extended': '0'
        }).json()

        if (wall_res.get('response')):
            wall_res = wall_res['response'][1:]
        else:
            print('error')
            return []

        for item in wall_res:
            if len(com_id_list) != comments_num:
                if int(item['comments']['count']):
                    com_id_list.append([item['id'], item['comments']['count']])
            else:
                break
        com_offset += comments_num % 100
        comments_num -= 100
    return com_id_list


def create_new_man(people_db, id, text):
    global errors_in_persons
    try:
        res = requests.get('http://api.vk.com/method/users.get',{
            'user_ids': id,
            'fields': 'first_name,second_name,sex,bdate,universities,schools,relation,personal,career,military'
        }, timeout=3).json()['response'][0]
        if res.get('universities') or res.get('schools'):
            people_db[id] = res
            people_db[id]['user_comments'] = [text]
            print('create new man', id)
    except BaseException:
        print('-----------------error in get persone', id, ':(')
        errors_in_persons += 1


def make_db(com_id_list, public_id):
    global errors_in_comments
    global people
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
                    people += 1
                    if item['from_id'] in people_db:  # Добавляем коммент человека в db, иначе создаём человека)
                        people_db[item['from_id']]['user_comments'].append(item['text'])
                    else:
                        create_new_man(people_db, item['from_id'], item['text'])
            except BaseException:
                print('--------------error in get comments', public_id, ':(')
                errors_in_comments += 1

            offset_k += 1
            com[1] -= 100
            n += 1
    return people_db


def public_handling(public_list):
    comments_amount = 30
    db = []  # База людей
    for public_id in public_list:
        com_id_list = get_list_of_comments_id(public_id, comments_amount)  # Список (id) постов в группе
        print('public number', public_id[1:])
        people_db = make_db(com_id_list, public_id)  # Словарь {человек: [информация, комменты]}

        for key in people_db.keys():
            people_db[key]['id'] = key
            db.append(people_db[key])

    with open('db/people_db', 'w') as f:
        json.dump(db, f)

errors_in_persons = 0
errors_in_comments = 0
people = 0
public_handling(public_list)
print('errors in persons', errors_in_persons)
print('errors in comments', errors_in_comments)
print('number of people', people)
