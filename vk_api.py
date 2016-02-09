import requests

user_get  = 'http://api.vk.com/method/users.get'
res = requests.get(user_get, {
    'user_ids': '12306049',
    'fields': 'photo_id,sex,bdate'}
)

print(res.json()['response'][0])
