import pytest
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import requests
import json
from other import clear
import message
import auth

# Use this fixture to get the URL of the server. It starts the server for you,
# so you don't need to.
@pytest.fixture
def url():
    url_re = re.compile(r' \* Running on ([^ ]*)')
    server = Popen(["python3", "src/server.py"], stderr=PIPE, stdout=PIPE)
    line = server.stderr.readline()
    local_url = url_re.match(line.decode())
    if local_url:
        yield local_url.group(1)
        # Terminate the server
        server.send_signal(signal.SIGINT)
        waited = 0
        while server.poll() is None and waited < 5:
            sleep(0.1)
            waited += 0.1
        if server.poll() is None:
            server.kill()
    else:
        server.kill()
        raise Exception("Couldn't get URL from local server")

@pytest.fixture
def register_data(url):
    r = requests.delete(f"{url}/clear")
    
    #Assert successful registration
    user1 = {
        'email': 'derek123@gmail.com',
        'password': '123456',
        'name_first': 'derek',
        'name_last': 'dong'
    }
    r = requests.post(f"{url}/auth/register", json=user1)
    user1 = r.json()
    
    user2 = {
        'email': 'rex@gmail.com',
        'password': '123456',
        'name_first': 'REX',
        'name_last': 'SUN'
    }
    r = requests.post(f"{url}/auth/register", json=user2)
    user2 = r.json()

    #create a channel
    channel1_data = {
        'token': user1['token'],
        'name': 'wed15mangoTeam4',
        'is_public': True
    }
    r = requests.post(f"{url}/channels/create", json=channel1_data)
    payload = r.json()
    channel1_id = payload['channel_id']

    return_dict = {
        'url': url,
        'user1': user1,
        'user2': user2,
        'channel1_id': channel1_id
    }

    return return_dict

def test_users_all(register_data):
    temp_dict = register_data
    url = temp_dict['url']
    
    #test Accesserror with invalid token
    r = requests.get(f"{url}/users/all", params={'token':'invalidtoken'})
    payload = r.json()
    assert payload['code'] == 400

    #tests for successful cases
    r = requests.get(f"{url}/users/all", params={'token': temp_dict['user1']['token']})
    payload = r.json()
    assert payload['users'] ==  [{'u_id': temp_dict['user1']['u_id'], 'email': 'derek123@gmail.com','name_first': 'derek','name_last': 'dong', 'profile_img_url': None,}, {'u_id': temp_dict['user2']['u_id'], 'email': 'rex@gmail.com','name_first': 'REX','name_last': 'SUN', 'profile_img_url': None,}]    
    
def test_invalid_search(register_data):
    temp_dict = register_data
    url = temp_dict['url']
    
    #invalid token
    data = {
        'token': 'invalidtoken',
        'query': 'hi everyone'
    }

    r = requests.get(f"{url}/search", params=data)
    payload = r.json()
    assert payload['code'] == 400    

def test_valid_search(register_data):
    temp_dict = register_data
    url = temp_dict['url']
    
    #tests for successful cases
    data1 = {
        'token': temp_dict['user1']['token'],
        'channel_id': temp_dict['channel1_id'],
        'message': 'hi everyone'
    }
    
    r = requests.post(f"{url}/message/send", json=data1)
    payload = r.json()
    message1_id = payload['message_id']


    #search for with a substrying "every" 
    data = {
        'token': temp_dict['user1']['token'],
        'query_str': 'every'
    }

    r = requests.get(f"{url}/search", params=data)
    payload = r.json()

    result = {
        'messages':[ 
            {
            'message': 'hi everyone',
            'message_id': message1_id,
            'u_id': temp_dict['user1']['u_id'],
            'time_created': payload['messages'][0].get('time_created'),
            },
        ]
    }
    assert payload == result

def test_invalid_search2(register_data):
    temp_dict = register_data
    url = temp_dict['url']
       
    #user2 cant search messages in channels since he isn't member
    data = {
        'token': temp_dict['user2']['token'],
        'query': 'every'
    }
    r = requests.get(f"{url}/search", params=data)
    payload = r.json()
    assert payload == {'messages': []}
    
    #search for non existing message
    data = {
        'token': temp_dict['user1']['token'],
        'query': 'python'
    }
    r = requests.get(f"{url}/search", params=data)
    payload = r.json()
    assert payload == {'messages': []}

def test_permission(register_data):
    temp_dict = register_data
    url = temp_dict['url']
    
    #test user permission
    #successful permission change case
    data = {
        'token': temp_dict['user1']['token'],
        'u_id': temp_dict['user2']['u_id'],
        'permission_id': '1'
    }
    r = requests.post(f"{url}/admin/userpermission/change", json=data)
    payload = r.json()
    assert payload == {}

def test_invalid_permission(register_data):
    temp_dict = register_data
    url = temp_dict['url']
    
    #already owner
    data = {
        'token': temp_dict['user1']['token'],
        'u_id': temp_dict['user1']['u_id'],
        'permission_id': '1'
    }
    r = requests.post(f"{url}/admin/userpermission/change", json=data)
    payload = r.json()
    assert payload == {}

    #invalid permission id
    data = {
        'token': temp_dict['user1']['token'],
        'u_id': temp_dict['user2']['u_id'],
        'permission_id': 'abc'
    }
    r = requests.post(f"{url}/admin/userpermission/change", json=data)
    payload = r.json()
    print (payload)
    assert payload['code'] == 400