import pytest
import re
from subprocess import Popen, PIPE
import signal
from time import sleep

import requests
import json
from other import clear

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

#Thsi fixtures registers data and returns necessary info to server tests
@pytest.fixture
def register_data(url):
    r = requests.delete(f"{url}/clear")
    
    #Assert successful registration
    user_1 = {
        'email': 'dogcat@gmail.com',
        'password': "abc123",
        'name_first': "dog",
        'name_last': "cat",
    }
    r = requests.post(f"{url}/auth/register", json=user_1)
    payload = r.json()
    user1_id = payload['u_id']
    user1_token = payload['token']
    
    user_2 = {
        'email': 'catdog@gmail.com',
        'password': "abcdef",
        'name_first': "cat",
        'name_last': "dog",
    }
    r = requests.post(f"{url}/auth/register", json=user_2)
    payload = r.json()
    user2_id = payload['u_id']
    user2_token = payload['token']

    return_dict = {
        'url': url,
        'token1': user1_token,
        'u_id1': user1_id,
        'email1': 'dogcat@gmail.com',
        'token2': user2_token,
        'u_id2': user2_id
    }

    return return_dict

def test_successful_logout(register_data):
    temp_dict = register_data
    url = temp_dict['url']
        
    # Assert successful logout user 1
    r = requests.post(f"{url}/auth/logout", json={'token':temp_dict['token1']})
    payload = r.json()
    assert payload["is_success"] == True
    
    # Assert successful logout user 2
    r = requests.post(f"{url}/auth/logout", json={'token':temp_dict['token2']})
    payload = r.json()
    assert payload["is_success"] == True
    
def test_invalid_logout(register_data):
    temp_dict = register_data
    url = temp_dict['url']
    
    #logout user successfully
    r = requests.post(f"{url}/auth/logout", json={'token':temp_dict['token1']})
    
    # logout should now be invalid as user already logged out
    r = requests.post(f"{url}/auth/logout", json={'token':temp_dict['token1']})
    payload = r.json()
    assert payload["code"] == 400

def test_login(register_data):
    temp_dict = register_data
    url = temp_dict['url']

    #logout user successfully
    r = requests.post(f"{url}/auth/logout", json={'token':temp_dict['token1']})
    
    #Test login with incorrect password
    login_1 = {
        'email': 'dogcat@gmail.com',
        'password': "aaaaaa"
    }
    r = requests.post(f"{url}/auth/login", json=login_1)
    payload = r.json()
    assert payload["code"] == 400
    
    #test successful login
    login_2 = {
        'email': 'dogcat@gmail.com',
        'password': "abc123"
    }
    r = requests.post(f"{url}/auth/login", json=login_2)
    payload = r.json()
    
    #check login successful with logout
    r = requests.post(f"{url}/auth/logout", json={'token':temp_dict['token1']})

def test_invalid_reg(url):
    #RAISE 400 ERRORRRRRtest invalid register (invalid email)
    user_3 = {
        'email':'invalidemail',
        'password':'password',
        'name_first': 'hello',
        'name_last': 'yoo'
    }

    r = requests.post(f"{url}/auth/register", json=user_3)
    payload = r.json()
    assert payload["code"] == 400

def test_reset_and_request(register_data):
    temp_dict = register_data
    url = temp_dict['url']
    
    #register user with valid email
    r = requests.post(f"{url}/auth/register", json={'email': 'exmptmp@gmail.com', 'password': '123456', 'name_first': 'abcd', 'name_last': 'dfghj'})
    
    #request reset successfully
    r = requests.post(f"{url}/auth/passwordreset/request", json={'email':'exmptmp@gmail.com'})
    payload = r.json()
    assert payload == {}

    #incorrect code entered so input error raised when reset tried
    r = requests.post(f"{url}/auth/passwordreset/reset", json={'reset_code':'abcde', 'new_password': "123123"})
    payload = r.json()
    assert payload['code'] == 400
