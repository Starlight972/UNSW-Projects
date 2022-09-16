from auth import auth_login, auth_register, auth_logout, user_info, auth_passwordreset_request, auth_passwordreset_reset
import pytest
from error import InputError, AccessError
from other import clear

@pytest.fixture
def register_data():
    clear()

    valid_reg_data = {
        'valid_1': {
            'email': 'dogcat@gmail.com',
            'password': "abc123", 
            'name_first': "dog"*4, 
            'name_last': "cat"*4,
            'u_id':"",
            'token':""
        },
        'valid_2': {
            'email': 'catdog@gmail.com',
            'password': "abcdef", 
            'name_first': "cat", 
            'name_last': "dog",
            'u_id':"",
            'token':""
        },
        'valid_3': {
            'email': 'wed15mango@gmail.com',
            'password': "123456", 
            'name_first': "cat", 
            'name_last': "dog",
            'u_id':"",
            'token':""
        }, 
        'valid_4': {
            'email': "validemail1@gmail.com",
            'password': "abcde123", 
            'name_first': "cat-ab", 
            'name_last': "dog ab",
            'u_id':"",
            'token':""
        }, 
        'valid_5': {
            'email': "validemail2@gmail.com",
            'password': "abcde123", 
            'name_first': "cat ab", 
            'name_last': "dog-ab",
            'u_id':"",
            'token':""
        } 
    }
    #register user 1
    result = auth_register(valid_reg_data['valid_1']['email'], valid_reg_data['valid_1']['password'], valid_reg_data['valid_1']['name_first'], valid_reg_data['valid_1']['name_last'])
    valid_reg_data['valid_1']['u_id'] = result['u_id']
    valid_reg_data['valid_1']['token'] = result['token']

    #register user 2
    result = auth_register(valid_reg_data['valid_2']['email'], valid_reg_data['valid_2']['password'], valid_reg_data['valid_2']['name_first'], valid_reg_data['valid_2']['name_last'])
    valid_reg_data['valid_2']['u_id'] = result['u_id']
    valid_reg_data['valid_2']['token'] = result['token']

    #register user 3
    result = auth_register(valid_reg_data['valid_3']['email'], valid_reg_data['valid_3']['password'], valid_reg_data['valid_3']['name_first'], valid_reg_data['valid_3']['name_last'])
    valid_reg_data['valid_3']['u_id'] = result['u_id']
    valid_reg_data['valid_3']['token'] = result['token']

    #Registers with hyphenated first and last names
    result = auth_register(valid_reg_data['valid_4']['email'], valid_reg_data['valid_4']['password'], valid_reg_data['valid_4']['name_first'], valid_reg_data['valid_4']['name_last'])
    valid_reg_data['valid_4']['u_id'] = result['u_id']
    valid_reg_data['valid_4']['token'] = result['token']

    result = auth_register(valid_reg_data['valid_5']['email'], valid_reg_data['valid_5']['password'], valid_reg_data['valid_5']['name_first'], valid_reg_data['valid_5']['name_last'])
    valid_reg_data['valid_5']['u_id'] = result['u_id']
    valid_reg_data['valid_5']['token'] = result['token']

    return valid_reg_data

#If all logins/registers successful, logouts should all pass
def test_logout_valid(register_data):
    temp_dict = register_data
    for user in temp_dict:
        assert auth_logout(temp_dict[user]['token']) == {'is_success': True}

#If register is valid, logout should be successful
def test_Invalid_logout(register_data): 
    temp_dict = register_data      
    assert auth_logout(temp_dict['valid_1']['token']) == {'is_success': True}

    #Test unsucccessful case as well, because token is no longr valid
    with pytest.raises(AccessError):
        auth_logout(temp_dict['valid_1']['token'])    

#Login after logout
def test_relogin(register_data):
    temp_dict = register_data
    auth_logout(temp_dict['valid_1']['token']) == {'is_success': True}
    auth_login("dogcat@gmail.com", "abc123")

#If registers valid, should raise error
def test_already_logged_in():
    with pytest.raises(InputError):
        auth_login("catdog@gmail.com", "abcdef")

# Login with incorrect password
def test_login_wrong_password(register_data):
    temp_dict = register_data
    auth_logout(temp_dict['valid_1']['token']) == {'is_success': True}
    with pytest.raises(InputError):
        auth_login("dogcat@gmail.com", "abcde")

#Test email addresses which are invalid
def test_register_invalid_email():
    #Invalid email address
    with pytest.raises(InputError):
        auth_register("dogcatgmail.com", "abcde123", "North", "West")

     #nothing in domain
    with pytest.raises(InputError):
        auth_register("nodomain@", "abcde123", "North", "West")
    
    #email already registered
    with pytest.raises(InputError):
        auth_register("dogcat@gmail.com", "abcde123", "North", "West")

    #no email provided
    with pytest.raises(InputError):
        auth_register("", "abcde123", "North", "West")

#Test names which are invalid
def test_register_invalid_names():
    #First name empty
    with pytest.raises(InputError):
        auth_register("Team4mango.com", "abcde123", " ", "West")

    #First name too long
    with pytest.raises(InputError):
        auth_register("Team4mango.com", "abcde123", "abcde"*11, "West")
    
    #Last name empty
    with pytest.raises(InputError):
        auth_register("Team4mango.com", "abcde123", "North", " ")
    
    #Last name too long
    with pytest.raises(InputError):
        auth_register("Team4mango.com", "abcde123", "North", "abcde"*11)

#password too short
def test_register_invalid_password():
    with pytest.raises(InputError):
        auth_register("Team4mango.com", "abcd", "North", "abcde")

#test login with unrgeisterd email
def test_unregistered():
    with pytest.raises(InputError):
        auth_login("unregistereemail@gmail.com", "123456")

#Test a valid reset request sent
def test_valid_reset_req(register_data):
    temp_dict = register_data
    assert auth_passwordreset_request(temp_dict['valid_1']['email']) == {}

#Should raise Input Error as email is not a valid email
def test_invalid_reset_req():
    with pytest.raises(InputError):
        auth_passwordreset_request('abcde')

#Should raise Input Error as code is not valid 
def test_invalid_reset_code():
    with pytest.raises(InputError):
        auth_passwordreset_reset('abcde', '123456')

#Should raise Input Error as password is too short
def test_invalid_reset_pass():
    with pytest.raises(InputError):
        auth_passwordreset_reset('abcde', '12')

#ensure data from tests is gone for next files
clear()