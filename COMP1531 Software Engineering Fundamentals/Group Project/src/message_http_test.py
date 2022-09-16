import pytest
import re
from subprocess import Popen, PIPE
import signal
from time import sleep

import requests
import json
from other import clear
from datetime import datetime
from pytz import timezone as tz
import time

# Use this fixture to get the URL of the server. 
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

    user3_data = {
        'email': "rex123@gmail.com",
        'password': "123456",
        'name_first': "rex",
        'name_last': "Sun"
    }
    r = requests.post(f"{url}/auth/register", json=user3_data)
    user3 = r.json()

    user4_data = {
        'email': "derek123@gmail.com",
        'password': "123456",
        'name_first': "derek",
        'name_last': "Dong"
    }
    r = requests.post(f"{url}/auth/register", json=user4_data)
    user4 = r.json()

    #create a public channel whose owner is vera
    channel1_data = {
        'token': user1['token'],
        'name': 'wed15mangoTeam4',
        'is_public': True
    }
    r = requests.post(f"{url}/channels/create", json=channel1_data)
    payload = r.json()
    channel1_id = payload['channel_id']

    # send messages
    data = {
        'token': user1['token'],
        'channel_id': channel1_id,
        'message': 'hi everyone'
    }
    r = requests.post(f"{url}/message/send", json=data)
    payload = r.json()
    message1_id = payload['message_id']

    data = {
        'token': user1['token'],
        'channel_id': channel1_id,
        'message': 'nice to see u'
    }
    r = requests.post(f"{url}/message/send", json=data)
    payload = r.json()
    message2_id = payload['message_id']

    return_dict = {
        'url': url,
        'user1': user1,
        'user2': user2,
        'user3': user3,
        'user4': user4,
        'channel1_id':channel1_id,
        'message1_id': message1_id,
        'message2_id': message2_id
    }

    return return_dict

def test_invalid_message_send(register_data):
    temp_dict = register_data
    BASE_URL = temp_dict['url']

    #check if message is more than 1000 characters
    data = {
        'token': temp_dict['user1']['token'],
        'channel_id': temp_dict['channel1_id'],
        'message': 'aaa' * 1000
    }
    r = requests.post(f"{BASE_URL}/message/send", json=data)
    payload = r.json()
    assert payload['code'] == 400

    #check invalid channel id
    data = {
        'token': temp_dict['user1']['token'],
        'channel_id': 40,
        'message': 'hi everyone'
    }
    r = requests.post(f"{BASE_URL}/message/send", json=data)
    payload = r.json()
    assert payload['code'] == 400

    #check the authorised user has not joined the channel they are trying to post to
    data = {
        'token': temp_dict['user2']['token'],
        'channel_id': temp_dict['channel1_id'],
        'message': 'hi everyone'
    }
    r = requests.post(f"{BASE_URL}/message/send", json=data)
    payload = r.json()
    assert payload['code'] == 400

def test_message_remove(register_data):
    temp_dict = register_data
    BASE_URL = temp_dict['url']

    #test successful case
    data = {
        'token': temp_dict['user1']['token'],
        'message_id': temp_dict['message1_id']
    }
    r = requests.delete(f"{BASE_URL}/message/remove", json=data)
    payload = r.json()
    assert payload == {}

def test_invalid_remove(register_data):
    temp_dict = register_data
    BASE_URL = temp_dict['url']

    #remove message with id 1
    data = {
        'token': temp_dict['user1']['token'],
        'message_id': temp_dict['message1_id']
    }
    r = requests.delete(f"{BASE_URL}/message/remove", json=data)
    
    #if Message no longer exists
    data = {
        'token': temp_dict['user1']['token'],
        'message_id': temp_dict['message1_id'],
    }
    r = requests.delete(f"{BASE_URL}/message/remove", json=data)
    payload = r.json()
    assert payload['code'] == 400

    #Message was not sent by the authorised user or owner
    data = {
        'token': temp_dict['user2']['token'],
        'message_id': temp_dict['message1_id'],
    }

    r = requests.delete(f"{BASE_URL}/message/remove", json=data)
    payload = r.json()
    assert payload['code'] == 400

def test_message_edit(register_data):
    temp_dict = register_data
    BASE_URL = temp_dict['url']

    #test successful test
    data = {
        'token': temp_dict['user1']['token'],
        'message_id': temp_dict['message2_id'],
        'message': 'I am the owner of this channel'
    }
    r = requests.put(f"{BASE_URL}/message/edit", json=data)
    payload = r.json()
    assert payload == {}

def test_invalid_edit(register_data):
    temp_dict = register_data
    BASE_URL = temp_dict['url']

    #test invalid token
    data = {
        'token': 'invalidtoken',
        'message_id': temp_dict['message2_id'],
        'message': 'nice to see u'
    }
    r = requests.put(f"{BASE_URL}/message/edit", json=data)
    payload = r.json()
    assert payload['code'] == 400

#============test message_sendlater=======
def test_message_sendlater(register_data):
    temp_dict = register_data
    BASE_URL = temp_dict['url']

    #test successful case
    au_tz = tz('Australia/Sydney')
    timestamp = au_tz.localize(datetime.now())
    timestamp = time.mktime(timestamp.timetuple()) + 5

    data = {
        'token': temp_dict['user1']['token'],
        'channel_id': temp_dict['channel1_id'],
        'message': 'just test',
        'time_sent': timestamp,
    }
    r = requests.post(f"{BASE_URL}/message/sendlater", json=data)
    payload = r.json()
    send = {
        'message_id': 3
    }
    assert payload == send

    #test Channel ID is not a valid channel
    au_tz = tz('Australia/Sydney')
    timestamp = au_tz.localize(datetime(2020, 12, 25, 12, 30))
    timestamp = time.mktime(timestamp.timetuple()) + 5    
    data = {
        'token': temp_dict['user1']['token'],
        'channel_id': 100,
        'message': 'just test',
        'time_sent': timestamp,
    }
    r = requests.post(f"{BASE_URL}/message/sendlater", json=data)
    payload = r.json()
    assert payload['code'] == 400

    #test Message is more than 1000 characters
    data = {
        'token': temp_dict['user1']['token'],
        'channel_id': temp_dict['channel1_id'],
        'message': 'aaa' * 1000,
        'time_sent': timestamp,
    }
    r = requests.post(f"{BASE_URL}/message/sendlater", json=data)
    payload = r.json()
    assert payload['code'] == 400

    #test Time sent is a time in the past
    au_tz = tz('Australia/Sydney')
    timestamp = au_tz.localize(datetime(2020, 1, 1, 13))
    timestamp = time.mktime(timestamp.timetuple()) + 5    
    
    data = {
        'token': temp_dict['user1']['token'],
        'channel_id': temp_dict['channel1_id'],
        'message': 'just test',
        'time_sent': timestamp,
    }
    r = requests.post(f"{BASE_URL}/message/sendlater", json=data)
    payload = r.json()
    assert payload['code'] == 400

    #test the authorised user has not joined the channel they are trying to post to
    au_tz = tz('Australia/Sydney')
    timestamp = au_tz.localize(datetime(2020, 12, 25, 12, 30))
    timestamp = time.mktime(timestamp.timetuple()) + 5        
    
    data = {
        'token': temp_dict['user4']['token'],
        'channel_id': temp_dict['channel1_id'],
        'message': 'just test',
        'time_sent': timestamp,
    }
    r = requests.post(f"{BASE_URL}/message/sendlater", json=data)
    payload = r.json()
    assert payload['code'] == 400

#============test message_react=======
def test_message_react(register_data):
    temp_dict = register_data
    BASE_URL = temp_dict['url']

    #successful case
    data = {
        'token': temp_dict['user1']['token'],
        'message_id': temp_dict['message1_id'],
        'react_id': 1,
    }
    r = requests.post(f"{BASE_URL}/message/react", json=data)
    payload = r.json()
    assert payload == {}

    #test message_id is not a valid message within a channel that the authorised user has joined
    data = {
        'token': temp_dict['user1']['token'],
        'message_id': 100,
        'react_id': 1,
    }
    r = requests.post(f"{BASE_URL}/message/react", json=data)
    payload = r.json()
    assert payload['code'] == 400

    #test react_id is not a valid React ID. The only valid react ID the frontend has is 1

    data = {
        'token': temp_dict['user1']['token'],
        'message_id': temp_dict['message1_id'],
        'react_id': 2,
    }
    r = requests.post(f"{BASE_URL}/message/react", json=data)
    payload = r.json()
    assert payload['code'] == 400

    #test Message with ID message_id already contains an active React with ID react_id from the authorised user
    
    data = {
        'token': temp_dict['user1']['token'],
        'message_id': temp_dict['message1_id'],
        'react_id': 1,
    }
    r = requests.post(f"{BASE_URL}/message/react", json=data)
    payload = r.json()
    assert payload['code'] == 400

#============test message_unreact=========
def test_message_unreact(register_data):
    temp_dict = register_data
    BASE_URL = temp_dict['url']

    #test successful case

    data = {
        'token': temp_dict['user1']['token'],
        'message_id': temp_dict['message1_id'],
        'react_id': 1,
    }
    r = requests.post(f"{BASE_URL}/message/react", json=data)
    r = requests.post(f"{BASE_URL}/message/unreact", json=data)
    payload = r.json()
    assert payload == {}

    #test message_id is not a valid message within a channel that the authorised user has joined
    data = {
        'token': temp_dict['user1']['token'],
        'message_id': 100,
        'react_id': 1,
    }
    r = requests.post(f"{BASE_URL}/message/unreact", json=data)
    payload = r.json()
    assert payload['code'] == 400

    #test react_id is not a valid React ID
    data = {
        'token': temp_dict['user1']['token'],
        'message_id': temp_dict['message1_id'],
        'react_id': 2,
    }
    r = requests.post(f"{BASE_URL}/message/unreact", json=data)
    payload = r.json()
    assert payload['code'] == 400


    #test Message with ID message_id does not contain an active React with ID react_id
    data = {
        'token': temp_dict['user1']['token'],
        'message_id': temp_dict['message1_id'],
        'react_id': 1,
    }
    r = requests.post(f"{BASE_URL}/message/unreact", json=data)
    payload = r.json()
    assert payload['code'] == 400

#=========test message_pin=======
def test_message_pin(register_data):
    temp_dict = register_data
    BASE_URL = temp_dict['url']

    #test successful case
    data = {
        'token': temp_dict['user1']['token'],
        'message_id': temp_dict['message1_id'],
    }
    r = requests.post(f"{BASE_URL}/message/pin", json=data)
    payload = r.json()
    assert payload == {}

    #test message_id is not a valid message
    data = {
        'token': temp_dict['user1']['token'],
        'message_id': 100,
    }
    r = requests.post(f"{BASE_URL}/message/pin", json=data)
    payload = r.json()
    assert payload['code'] == 400

    #test Message with ID message_id is already pinned
    data = {
        'token': temp_dict['user1']['token'],
        'message_id': temp_dict['message1_id'],
    }
    r = requests.post(f"{BASE_URL}/message/pin", json=data)
    payload = r.json()
    assert payload['code'] == 400

    #test The authorised user is not a member of the channel that the message is within
    data = {
        'token': temp_dict['user4']['token'],
        'message_id': temp_dict['message1_id'],
    }
    r = requests.post(f"{BASE_URL}/message/pin", json=data)
    payload = r.json()
    assert payload['code'] == 400

    #The authorised user is not an owner

    data = {
        'token': temp_dict['user1']['token'],
        'channel_id': temp_dict['channel1_id'],
        'u_id': temp_dict['user2']['u_id']
    }
    r = requests.post(f"{BASE_URL}/channel/invite", json=data)

    data = {
        'token': temp_dict['user2']['token'],
        'message_id': temp_dict['message1_id']
    }
    r = requests.post(f"{BASE_URL}/message/pin", json=data)
    payload = r.json()
    assert payload['code'] == 400

#==========test message_unpin========
def test_message_unpin(register_data): 
    temp_dict = register_data
    BASE_URL = temp_dict['url']

    #test successful case
    data = {
        'token': temp_dict['user1']['token'],
        'message_id': temp_dict['message1_id']
    }
    r = requests.post(f"{BASE_URL}/message/pin", json=data)

    data = {
        'token': temp_dict['user1']['token'],
        'message_id': temp_dict['message1_id']
    }
    r = requests.post(f"{BASE_URL}/message/unpin", json=data)
    payload = r.json()
    assert payload == {}

    #test message_id is not a valid message
    data = {
        'token': temp_dict['user1']['token'],
        'message_id': 100,
    }
    r = requests.post(f"{BASE_URL}/message/unpin", json=data)
    payload = r.json()
    assert payload['code'] == 400

    #test Message with ID message_id is already unpinned
    data = {
        'token': temp_dict['user1']['token'],
        'message_id': temp_dict['message1_id']
    }
    r = requests.post(f"{BASE_URL}/message/unpin", json=data)
    payload = r.json()
    assert payload['code'] == 400

    #test The authorised user is not a member of the channel that the message is within
    data = {
        'token': temp_dict['user4']['token'],
        'message_id': temp_dict['message1_id']
    }
    r = requests.post(f"{BASE_URL}/message/unpin", json=data)
    payload = r.json()
    assert payload['code'] == 400

    data = {
        'token': temp_dict['user1']['token'],
        'channel_id': temp_dict['channel1_id'],
        'u_id': temp_dict['user2']['u_id']
    }
    r = requests.post(f"{BASE_URL}/channel/invite", json=data)

    #The authorised user is not an owner
    data = {
        'token': temp_dict['user2']['token'],
        'message_id': temp_dict['message1_id']
    }
    r = requests.post(f"{BASE_URL}/message/unpin", json=data)
    payload = r.json()
    assert payload['code'] == 400