import pytest
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import requests
import json
from other import clear

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
    #Clear any existing data
    r = requests.delete(f"{url}/clear")

    #register 4 users
    user1_data = {
        'email': "vera123@gmail.com",
        'password': "123456",
        'name_first': "vera",
        'name_last': "Zhao"
    }
    r = requests.post(f"{url}/auth/register", json=user1_data)
    user1 = r.json()

    user2_data = {
        'email': "ruby123@gmail.com",
        'password': "123456",
        'name_first': "ruby",
        'name_last': "Shao"
    }
    r = requests.post(f"{url}/auth/register", json=user2_data)
    user2 = r.json()

    # valid channel create
    channel_1 = {
        'name': 'Channel_1',
        'is_public': False,
        'token': user1['token']
    }
    r = requests.post(f"{url}/channels/create", json=channel_1)
    payload = r.json()
    channel1_id = payload['channel_id']
    
    channel_2 = {
        'name': 'Channel_2',
        'is_public': True,
        'token': user1['token']
    }
    r = requests.post(f"{url}/channels/create", json=channel_2)
    payload = r.json()
    channel2_id = payload['channel_id']
    
    channel_3 = {
        'name': 'Channel_3',
        'is_public': True,
        'token': user2['token']
    }
    r = requests.post(f"{url}/channels/create", json=channel_3)
    payload = r.json()
    channel3_id = payload['channel_id']
    
    return_dict = {
        'url': url,
        'user1': user1,
        'user2': user2,
        'channel1_id':channel1_id,
        'channel2_id':channel2_id,
        'channel3_id':channel3_id,
    }

    return return_dict

def test_list(register_data):
    temp_dict = register_data
    url = temp_dict['url']
    
    r = requests.get(f"{url}/channels/list", params={'token': temp_dict['user2']['token']})
    payload = r.json()
    assert payload['channels'] == [{'channel_id': 3,'name':'Channel_3',}]
    
    r = requests.get(f"{url}/channels/list", params={'token': temp_dict['user1']['token']})
    payload = r.json()
    assert payload['channels'] == [{'channel_id': 1, 'name': 'Channel_1'}, {'channel_id': 2, 'name': 'Channel_2'}]

def test_listall(register_data):
    temp_dict = register_data
    url = temp_dict['url']
    
    r = requests.get(f"{url}/channels/listall", params={'token': temp_dict['user1']['token']})
    payload = r.json()
    assert payload['channels'] == [{'channel_id': 3,'name':'Channel_3',}]

def test_create_invalid(register_data):
    temp_dict = register_data
    url = temp_dict['url']
    
    # Nothing created under unexist token
    channel_5 = {
        'name': 'Channel_5',
        'is_public': False,
        'token': '5'
    }
    r = requests.post(f"{url}/channels/create", json=channel_5)
    payload = r.json()
    assert payload['code'] == 400
    