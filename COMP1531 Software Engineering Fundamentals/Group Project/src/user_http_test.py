import pytest
import re
from subprocess import Popen, PIPE
import signal
import hashlib
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
    r = requests.delete(f"{url}/clear")
    
    #Assert successful registration
   # register users
    user1 = {
        'email': 'rex@gmail.com',
        'password': '123456',
        'name_first': 'REX',
        'name_last': 'SUN'
    }
    r = requests.post(f"{url}/auth/register", json=user1)
    user1 = r.json()
    
    user2 = {
        'email': 'home@gmail.com',
        'password': '123456',
        'name_first': 'Yan',
        'name_last': 'Cheng'
    }
    r = requests.post(f"{url}/auth/register", json=user2)
    user2 = r.json()

    #setup a profile
    profile_1 = {
        'u_id': user1['u_id'],
        'token': user1['token']
    }
    return_dict = {
        'url': url,
        'user1': user1,
        'user2': user2,
        'profile1': profile_1
    }

    return return_dict

def test_valid_prof(register_data):
    temp_dict = register_data
    url = temp_dict['url']

    # show vaild profile
   
    r = requests.get(f"{url}/user/profile", params=temp_dict['profile1'])
    payload = r.json()
    assert payload['user'] == {'u_id': 1, 'email': 'rex@gmail.com', 'name_first': 'REX', 'name_last': 'SUN', 'handle_str': 'REXSUN', 'profile_img_url': None,}

def test_invalid_prof(register_data):
    temp_dict = register_data
    url = temp_dict['url']

    #Result in Input error as u_id is not valid
    profile_2 = {
        'u_id': 1234,
        'token': temp_dict['user2']['token']
    }
    r = requests.get(f"{url}/user/profile", params=profile_2)
    payload = r.json()

    assert payload['code'] == 400

    
def test_valid_setname(register_data):
    temp_dict = register_data
    url = temp_dict['url']

    # update name under valid input
    set_1 = {
        'token': temp_dict['user1']['token'],
        'name_first': 'rex',
        'name_last': 'sun'
    }
    r = requests.put(f"{url}/user/profile/setname", json=set_1)
    r = requests.get(f"{url}/user/profile", params=temp_dict['profile1'])
    payload = r.json()
    assert payload['user'] == {'u_id': 1, 'email': 'rex@gmail.com', 'name_first': 'rex', 'name_last': 'sun', 'handle_str': 'REXSUN', 'profile_img_url': None,}
    
def test_invalid_setname(register_data):
    temp_dict = register_data
    url = temp_dict['url']

    # update name under invalid input
    set_2 = {
        'token': temp_dict['user1']['token'],
        'name_first': '',
        'name_last': ''
    }
    r = requests.put(f"{url}/user/profile/setname", json=set_2)
    r = requests.get(f"{url}/user/profile", params=temp_dict['profile1'])
    payload = r.json()
    assert payload['user'] == {'u_id': 1, 'email': 'rex@gmail.com', 'name_first': 'REX', 'name_last': 'SUN', 'handle_str': 'REXSUN', 'profile_img_url': None,}

def test_valid_setemail(register_data):
    temp_dict = register_data
    url = temp_dict['url']

    set_3 = {
        'token': temp_dict['user1']['token'],
        'email': 'abcde@gamil.com',
    }
    r = requests.put(f"{url}/user/profile/setemail", json=set_3)
    r = requests.get(f"{url}/user/profile", params=temp_dict['profile1'])
    payload = r.json()
    assert payload['user'] == {'u_id': 1, 'email': 'abcde@gamil.com', 'name_first': 'REX', 'name_last': 'SUN', 'handle_str': 'REXSUN', 'profile_img_url': None,}

def test_invalid_email(register_data):
    temp_dict = register_data
    url = temp_dict['url']

    # update email under invalid input
    set_4 = {
        'token': temp_dict['user2']['token'],
        'email': 'abcdegamil.com',
    }
    r = requests.put(f"{url}/user/profile/setemail", json=set_4)
    r = requests.get(f"{url}/user/profile", params={'token': temp_dict['user2']['token'], 'u_id': temp_dict['user2']['u_id']})
    payload = r.json()
    assert payload['user'] == {'u_id': 2, 'email': 'home@gmail.com', 'name_first': 'Yan', 'name_last': 'Cheng', 'handle_str': 'YanCheng', 'profile_img_url': None,}

def test_valid_handle(register_data):
    temp_dict = register_data
    url = temp_dict['url']

    # update handle under valid input
    set_5 = {
        'token': temp_dict['user1']['token'],
        'handle': 'rexsun',
    }
    r = requests.put(f"{url}/user/profile/sethandle", json=set_5)
    r = requests.get(f"{url}/user/profile", params=temp_dict['profile1'])
    payload = r.json()
    assert payload['user'] == {'u_id': 1, 'email': 'rex@gmail.com', 'name_first': 'REX', 'name_last': 'SUN', 'handle_str': 'REXSUN', 'profile_img_url': None,}
    
def test_invalid_handle(register_data):
    temp_dict = register_data
    url = temp_dict['url']

    # update handle under invalid input
    set_6 = {
        'token': temp_dict['user1']['token'],
        'handle': 're',
    }
    r = requests.put(f"{url}/user/profile/sethandle", json=set_6)
    r = requests.get(f"{url}/user/profile", params=temp_dict['profile1'])
    payload = r.json()
    assert payload['user'] == {'u_id': 1, 'email': 'rex@gmail.com', 'name_first': 'REX', 'name_last': 'SUN', 'handle_str': 'REXSUN', 'profile_img_url': None,}

def test_valid_photoupload(register_data):
    temp_dict = register_data
    url = temp_dict['url']
    set_8 = {
        'token': temp_dict['user1']['token'],
        'img_url': 'http://m.imeitou.com/uploads/allimg/190221/3-1Z221113343.jpg',
        'x_start': 0,
        'y_start': 0,
        'x_end': 100,
        'y_end': 100,
    }
    r = requests.post(f"{url}/user/profile/uploadphoto", json=set_8)
    r = requests.get(f"{url}/user/profile", params=temp_dict['profile1'])
    payload = r.json()
    assert payload['user'] == {'u_id': 1, 'email': 'rex@gmail.com', 'name_first': 'REX', 'name_last': 'SUN', 'handle_str': 'REXSUN', 'profile_img_url': 'static/user_1profile.jpg',}
