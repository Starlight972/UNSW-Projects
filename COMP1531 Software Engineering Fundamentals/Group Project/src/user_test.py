import auth
import user
import error
import pytest
from other import clear
import hashlib

''' new user registered '''
clear()
user1 = auth.auth_register('rex@gmail.com', '123456', 'REX', 'SUN')
user2 = auth.auth_register('home@gmail.com', '123456', 'Yan', 'Cheng')

''' TEST VALID INPUT '''
def test_profile_show():
    clear()
    user1 = auth.auth_register('rex@gmail.com', '123456', 'REX', 'SUN')
    user2 = auth.auth_register('home@gmail.com', '123456', 'Yan', 'Cheng')
    
    assert user.user_profile(user1['token'], user1['u_id']) == {'user': {'u_id': 1,'email': 'rex@gmail.com','name_first': 'REX','name_last': 'SUN','handle_str': 'REXSUN', 'profile_img_url': None,},}
    assert user.user_profile(user2['token'], user2['u_id']) == {'user': {'u_id': 2,'email': 'home@gmail.com','name_first': 'Yan','name_last': 'Cheng','handle_str': 'YanCheng', 'profile_img_url': None,},}
    with pytest.raises(error.InputError):
        user.user_profile('', '')

def test_profile_setname():
    user.user_profile_setname(user1['token'], 'rex', 'sun')
    assert user.user_profile(user1['token'], user1['u_id']) == {'user': {'u_id': 1,'email': 'rex@gmail.com','name_first': 'rex','name_last': 'sun','handle_str': 'REXSUN', 'profile_img_url': None,},}
    
    user.user_profile_setname(user2['token'], 'yan', 'cheng')
    assert user.user_profile(user2['token'], user2['u_id']) == {'user': {'u_id': 2,'email': 'home@gmail.com','name_first': 'yan','name_last': 'cheng','handle_str': 'YanCheng', 'profile_img_url': None,},}
    
    assert user.user_profile_setname('', 'rex', 'sun') == {}


def test_profile_setemail():
    user.user_profile_setemail(user1['token'], 'abcde@gamil.com')
    assert user.user_profile(user1['token'], user1['u_id']) == {'user': {'u_id': 1,'email': 'abcde@gamil.com','name_first': 'rex','name_last': 'sun','handle_str': 'REXSUN', 'profile_img_url': None,},}

def test_profile_sethandle():
    user.user_profile_sethandle(user1['token'], 'rexsun')
    assert user.user_profile(user1['token'], user1['u_id']) == {'user': {'u_id': 1,'email': 'abcde@gamil.com','name_first': 'rex','name_last': 'sun','handle_str': 'rexsun', 'profile_img_url': None,},}
    
    assert user.user_profile_sethandle('', 'hjads') == {}


''' TEST INVALID INPUT '''
def test_profile_invalid_input():
    with pytest.raises(error.InputError):
        assert user.user_profile(3, user1['u_id'])
        
    with pytest.raises(error.InputError):
        assert user.user_profile('', user1['u_id'])

def test_setname_invalid():
    with pytest.raises(error.InputError):
        assert user.user_profile_setname(user1['token'], '', 'sun')

    with pytest.raises(error.InputError):
        assert user.user_profile_setname(user1['token'], 'rex', '')
        
    with pytest.raises(error.InputError):
        assert user.user_profile_setname(user1['token'], '', '')

def test_setemail_invalid():
    with pytest.raises(error.InputError):
        assert user.user_profile_setemail(user2['token'], 'abcde@gamil.com')
        
    with pytest.raises(error.InputError):
        assert user.user_profile_setemail(user1['token'], 'ankitrai326.com')
        
    with pytest.raises(error.InputError):
        assert user.user_profile_setemail(user1['token'], '')

def test_sethandle_invalid():
    with pytest.raises(error.InputError):
        assert user.user_profile_sethandle(user2['token'], 'rexsun')
        
    with pytest.raises(error.InputError):
        assert user.user_profile_sethandle(user1['token'], 're')

clear()
