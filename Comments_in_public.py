import requests
import json

public_id = int(input())
comments_num = int(input())

def get_comments_id(public_id, comments_num):
    com_id_list = []
    com_offset = 2
    while len(com_id_list) < comments_num:
        wall_get_comm = 'http://api.vk.com/method/wall.get'
        wall_res = requests.get(wall_get_comm, {
            'owner_id': public_id,
            'offset': com_offset,
            'count': comments_num,
            'extended': '0'
        }).json()['response'][1:]
        com_offset += comments_num

        for item in wall_res:
            if len(com_id_list) != comments_num:
                if int(item['comments']['count']):
                    com_id_list.append([item['id'], item['comments']['count']])
            else:
                break
    return com_id_list


def create_new_man(people_db, id, text):
    res = requests.get('http://api.vk.com/method/users.get', {
        'user_ids': id,
        'fields': 'first_name,second_name,sex,bdate,city,country,education,personal,relation'
    }).json()['response'][0]
    if res['sex'] != 0 and res.get('bdate'):
        people_db[id] = res
        people_db[id]['user_comments'] = [text]


def make_db(com_id_list,public_id):
    people_db = {}
    k = 1
    for com in com_id_list:
        print(k, com)
        k += 1
        offset_k = 0
        while com[1] > 0:
            comm_get = requests.get('http://api.vk.com/method/wall.getComments', {
                'owner_id': public_id,
                'post_id': com[0],
                'count': com[1] % 100,
                'offset': 100 * offset_k

            }).json()['response'][1:]
            for item in comm_get:
                if item['from_id'] in people_db:
                    people_db[item['from_id']]['user_comments'].append(item['text'])
                else:
                    create_new_man(people_db, item['from_id'], item['text'])
            offset_k += 1
            com[1] -= 100
            print(people_db, '\n')
    return people_db

com_id_list = get_comments_id(public_id, comments_num)

people_db = make_db(com_id_list, public_id)

db = []
for key in people_db.keys():
    people_db[key]['id'] = key
    db.append(people_db[key])

with open('db/people_db_'+str(public_id)+'_'+str(comments_num), 'w', encoding='utf-8') as f:
    json.dump(db, f, sort_keys=True)

