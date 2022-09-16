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

    #create channels
    channel1_data = {
        'token': user1['token'],
        'name': 'wed15mangoTeam4',
        'is_public': True,
        'is_active': False,
        'time_finished': ','
    }
    r = requests.post(f"{url}/channels/create", json=channel1_data)
    payload = r.json()
    channel1_id = payload['channel_id']

    channel1_data = {
        'token': user2['token'],
        'name': 'wed15mangoTeam5',
        'is_public': True,
        'is_active': True,
        'time_finished': '',
    }
    r = requests.post(f"{url}/channels/create", json=channel1_data)
    payload = r.json()
    channel2_id = payload['channel_id']

    return_dict = {
        'url': url,
        'user1': user1,
        'user2': user2,
        'channel1_id': channel1_id,
        'channel2_id': channel2_id
    }

    return return_dict

def test_start_invalid_token(register_data):
    temp_dict = register_data
    url = temp_dict['url']
   
    #invalid token
    data = {
        'token': 'invalidtoken',
        'channel_id': temp_dict['channel1_id'],
        'length' : 3
    }

    r = requests.post(f"{url}/standup/start", json=data)
    payload = r.json()
    print(payload)
    assert payload['code'] == 400  

def test_start_invalid_channelid(register_data):
    temp_dict = register_data
    url = temp_dict['url']
   
    #invalid channel_id
    data = {
        'token': temp_dict['user1']['token'],
        'channel_id': temp_dict['channel1_id'] + 10000,
        'length' : 3
    }

    r = requests.post(f"{url}/standup/start", json=data)
    payload = r.json()
    assert payload['code'] == 400

def test_start_already_active(register_data):
    temp_dict = register_data
    url = temp_dict['url']
   
    #already a standup is running in channel2
    data = {
        'token': temp_dict['user2']['token'],
        'channel_id': temp_dict['channel2_id'],
        'length' : 3
    }
    requests.post(f"{url}/standup/start", json=data)

    r = requests.post(f"{url}/standup/start", json=data)
    payload = r.json()
    assert payload['code'] == 400  

def test_active_invalid_channelid(register_data):
    temp_dict = register_data
    url = temp_dict['url']
   
    #invalid channel_id
    data = {
        'token': temp_dict['user2']['token'],
        'channel_id': temp_dict['channel2_id'] + 10000
    }

    r = requests.get(f"{url}/standup/active", params=data)
    payload = r.json()
    assert payload['code'] == 400              

def test_send_invalid_channelid(register_data):
    temp_dict = register_data
    url = temp_dict['url']
   
    #invalid channel_id
    data = {
        'token': temp_dict['user2']['token'],
        'channel_id': temp_dict['channel2_id'] + 10000,
        'message' : 'hello world'
    }

    r = requests.post(f"{url}/standup/send", json=data)
    payload = r.json()
    assert payload['code'] == 400

def test_send_long_messages(register_data):
    temp_dict = register_data
    url = temp_dict['url']
   
    #too long message
    data = {
        'token': temp_dict['user2']['token'],
        'channel_id': temp_dict['channel2_id'],
        'message' : 'hello world'*1000
    }

    r = requests.post(f"{url}/standup/send", json=data)
    payload = r.json()
    assert payload['code'] == 400          

def test_send_non_active(register_data):
    temp_dict = register_data
    url = temp_dict['url']
   
    #no standup is runnning in channel1
    data = {
        'token': temp_dict['user1']['token'],
        'channel_id': temp_dict['channel1_id'],
        'message' : 'hello world',
    }

    r = requests.post(f"{url}/standup/send", json=data)
    payload = r.json()
    assert payload['code'] == 400   