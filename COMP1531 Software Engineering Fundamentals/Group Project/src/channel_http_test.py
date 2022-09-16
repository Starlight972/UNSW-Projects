import pytest
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import requests
import json
from other import clear
import message
import message_data

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

    #create a public channel whose owner is vera
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
        'user3': user3,
        'channel1_id':channel1_id,
    }

    return return_dict

def test_channel_invite(register_data):
    temp_dict = register_data
    BASE_URL = temp_dict['url']

    #test sucessful case
    #invite user2(ruby) into channel
    data = {
        'token': temp_dict['user1']['token'],
        'channel_id': temp_dict['channel1_id'],
        'u_id': temp_dict['user2']['u_id']
    } 
    r = requests.post(f"{BASE_URL}/channel/invite", json=data)
    payload = r.json()
    assert payload == {}

def test_invalid_channel_invite(register_data):
    temp_dict = register_data
    BASE_URL = temp_dict['url']
    
    #test channel_id does not refer to a valid channel
    data = {
        'token': temp_dict['user1']['token'],
        'channel_id': 40,
        'u_id': temp_dict['user2']['u_id']
    }
    r = requests.post(f"{BASE_URL}/channel/invite", json=data)
    payload = r.json()
    assert payload['code'] == 400

    #test u_id does not refer to a valid user
    data = {
        'token': temp_dict['user1']['token'],
        'channel_id': temp_dict['channel1_id'],
        'u_id': 70
    }
    r = requests.post(f"{BASE_URL}/channel/invite", json=data)
    payload = r.json()
    payload['code'] == 400

    #test the authorised user is not a member of the channel
    data = {
        'token': temp_dict['user3']['token'],
        'channel_id': temp_dict['channel1_id'],
        'u_id': temp_dict['user2']['u_id']
    }
    r = requests.post(f"{BASE_URL}/channel/invite", json=data)
    payload = r.json()
    payload['code'] == 400

def test_channel_details(register_data):
    temp_dict = register_data
    BASE_URL = temp_dict['url']
    
    #test successful cases
    data = {
        'token': temp_dict['user1']['token'],
        'channel_id': temp_dict['channel1_id']
    }
    r = requests.get(f"{BASE_URL}/channel/details", params=data)
    payload = r.json()
    details = {
        'name': 'wed15mangoTeam4',
        'owner_members':[
            {
                'u_id': 1,
                'name_first': 'vera',
                'name_last': 'Zhao',
                'profile_img_url': None,
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'name_first': 'vera',
                'name_last': 'Zhao',
                'profile_img_url': None,
            }
        ]
    }
    assert payload == details

def test_invalid_channel_details(register_data):
    temp_dict = register_data
    BASE_URL = temp_dict['url']

    #test Authorised user is not a member of channel with channel_id
    data = {
        'token': temp_dict['user3']['token'],
        'channel_id': temp_dict['channel1_id']
    }
    r = requests.get(f"{BASE_URL}/channel/details", params=data)
    payload = r.json()
    assert payload['code'] == 400

def test_channel_messages(register_data):
    temp_dict = register_data
    BASE_URL = temp_dict['url']

    #send messages into channel (successful)
    message_1 = {
        'token': temp_dict['user1']['token'],
        'channel_id': temp_dict['channel1_id'],
        'message': 'bye'
    }
    r = requests.post(f"{BASE_URL}/message/send", json=message_1)

    message_2 = {
        'token': temp_dict['user1']['token'],
        'channel_id': temp_dict['channel1_id'],
        'message': 'ttyl'
    }
    r = requests.post(f"{BASE_URL}/message/send", json=message_2)
   
    data = {
        'token': temp_dict['user1']['token'],
        'channel_id': temp_dict['channel1_id'],
        'start': 2
    }
    r = requests.get(f"{BASE_URL}/channel/messages", params=data)
    payload = r.json()

    sample_message = {
        'messages': [
            {
                'message_id': 2,
                'u_id': 1,
                'message': 'ttyl',
                'time_created': payload['messages'][0].get('time_created')
            },
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'bye',
                'time_created': payload['messages'][1].get('time_created')
            }
        ],
        'start': 2,
        'end': -1,
    }

    assert payload == sample_message

def test_channel_invalid_messages(register_data):
    temp_dict = register_data
    BASE_URL = temp_dict['url']

    #send message
    data = {
        'token': temp_dict['user1']['token'],
        'channel_id': temp_dict['channel1_id'],
        'message': 'hi everyone'
    }
    r = requests.post(f"{BASE_URL}/message/send", json=data)

    #test start is greater than the total number of messages in the channel
    data = {
        'token': temp_dict['user1']['token'],
        'channel_id': temp_dict['channel1_id'],
        'start': 5
    }
    r = requests.get(f"{BASE_URL}/channel/messages", params=data)
    payload = r.json()
    assert payload['code'] == 400

    #test Authorised user is not a member of channel with channel_id
    data = {
        'token': 'invalidtoken',
        'channel_id': temp_dict['channel1_id'],
        'start': 0
    }
    r = requests.get(f"{BASE_URL}/channel/messages", params=data)
    payload = r.json()
    assert payload['code'] == 400

def test_channel_leave(register_data):
    temp_dict = register_data
    BASE_URL = temp_dict['url']

    #successful case
    data = {
        'token': temp_dict['user1']['token'],
        'channel_id': temp_dict['channel1_id'],
    } 
    r = requests.post(f"{BASE_URL}/channel/leave", json=data)
    payload = r.json()
    assert payload == {}

def test_invalid_channel_leave(register_data):
    temp_dict = register_data
    BASE_URL = temp_dict['url']

    # test if channelID not valid
    data = {
        'token': temp_dict['user1']['token'],
        'channel_id': 40,
    } 
    r = requests.post(f"{BASE_URL}/channel/leave", json=data)
    payload = r.json()
    assert payload['code'] == 400

    # test if authorised user not a member of channel
    data = {
        'token': temp_dict['user3']['token'],
        'channel_id': temp_dict['channel1_id'],
    } 
    r = requests.post(f"{BASE_URL}/channel/leave", json=data)
    payload = r.json()
    assert payload['code'] == 400

def test_channel_join(register_data):
    temp_dict = register_data
    BASE_URL = temp_dict['url']

    # successful case
    data = {
        'token': temp_dict['user3']['token'],
        'channel_id': temp_dict['channel1_id'],
    } 
    r = requests.post(f"{BASE_URL}/channel/join", json=data)
    payload = r.json()
    assert payload == {}

def test_invalid_channel_join(register_data):
    temp_dict = register_data
    BASE_URL = temp_dict['url']

    # test if channelID not valid
    data = {
        'token': temp_dict['user1']['token'],
        'channel_id': 40,
    } 
    r = requests.post(f"{BASE_URL}/channel/join", json=data)
    payload = r.json()
    assert payload['code'] == 400

    #Create a private channel
    channel2_data = {
        'token': temp_dict['user1']['token'],
        'name': 'private channel',
        'is_public': False
    }
    r = requests.post(f"{BASE_URL}/channels/create", json=channel2_data)
    payload = r.json()
    channel2_id = payload['channel_id']
    
    # test user join if the channel is private
    data = {
        'token': temp_dict['user2']['token'],
        'channel_id': channel2_id,
    } 
    r = requests.post(f"{BASE_URL}/channel/join", json=data)
    payload = r.json()
    assert payload['code'] == 400

def test_channel_owner_valid(register_data):
    #Setup, register users
    temp_dict = register_data
    BASE_URL = temp_dict['url']
    
    #Allow user2 to join channel
    data = {
        'token': temp_dict['user2']['token'],
        'channel_id': temp_dict['channel1_id'],
    } 
    r = requests.post(f"{BASE_URL}/channel/join", json=data)
    
    #test for successful addowner case
    data = {
        'token': temp_dict['user1']['token'],
        'channel_id': temp_dict['channel1_id'],
        'u_id': temp_dict['user2']['u_id']
    }
    r = requests.post(f"{BASE_URL}/channel/addowner", json=data)
    payload = r.json()
    assert payload == {}

    #test for sucessful removeoner case
    '''data = {
        'token': temp_dict['user1']['token'],
        'channel_id': temp_dict['channel1_id'],
        'u_id': temp_dict['user2']['u_id']
    }
    r = requests.post(f"{BASE_URL}/channel/removeowner", json=data)
    payload = r.json()
    assert payload == {}'''

def test_channel_owner_invalid(register_data):
    #Setup, register users
    temp_dict = register_data
    BASE_URL = temp_dict['url']

    #user is already the owner of the channel
    data = {
        'token': temp_dict['user1']['token'],
        'channel_id':temp_dict['channel1_id'],
        'u_id': temp_dict['user1']['u_id']
    }
    r = requests.post(f"{BASE_URL}/channel/addowner", json=data)
    payload = r.json()
    assert payload['code'] == 400
    
    #token is not a member of the channel
    data = {
        'token': temp_dict['user2']['token'],
        'channel_id':temp_dict['channel1_id'],
        'u_id': temp_dict['user2']['u_id']
    }
    r = requests.post(f"{BASE_URL}/channel/addowner", json=data)
    payload = r.json()
    assert payload['code'] == 400

    #user2 isnt the owner, she cant be removed
    data = {
        'token': temp_dict['user1']['token'],
        'channel_id': temp_dict['channel1_id'],
        'u_id': temp_dict['user2']['u_id']
    }
    r = requests.post(f"{BASE_URL}/channel/removeowner", json=data)
    payload = r.json()
    assert payload['code'] == 400
