import json
import requests

URL = "http://127.0.0.1:8000/register-api/"

def get_data(id = None):
    data = {}
    if id is not None:
        data = {'id':id}
    json_data = json.dumps(data)
    r = requests.get(url=URL, data=json_data)
    data =  r.json()
    print(data)

get_data(4)

def post_data():
    data = {
        'name':'kishor sir',
        'email':'kishor@gmail.com',
        'password':'321',
        'mobile':5432,
    }
    json_data = json.dumps(data)
    r = requests.post(url=URL, data=json_data)
    data =  r.json()
    print(data)

# post_data()

def update_data():
    data = {
        'id': 2,
        'name':'ashu',
        'email':'ashu@gmail.com',
        'password':'321',
        'mobile':5432,
    }
    json_data = json.dumps(data)
    r = requests.put(url=URL, data=json_data)
    data =  r.json()
    print(data)

# update_data()

def delete_data():
    data = {'id':6}
    json_data = json.dumps(data)
    print(data)
    r = requests.delete(url=URL, data=json_data)
    res = r.json()
    print(res)

# delete_data()