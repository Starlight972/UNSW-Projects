import auth
import channels
import error
import pytest
from other import clear

''' new user registered '''
@pytest.fixture
def register_data():
    clear()
    user1 = auth.auth_register('rex@gmail.com', '123456', 'REX', 'SUN')
    user2 = auth.auth_register('home@gmail.com', '123456', 'Yan', 'Cheng')
    user3 = auth.auth_register('newsouthwales@gmail.com', '123456', 'Sydney', 'Australia')
    user4 = auth.auth_register('yancheng@gmail.com', '123456', 'Jiangsu', 'China')
    
    return_dict = {
        'user_1': user1,
        'user_2': user2,
        'user_3': user3,
        'user_4': user4
    }

    return return_dict

''' TEST VALID INPUT '''
''' Test list under same token '''
def test_list_same_token(register_data):
    temp_dict = register_data
    channels.channels_create(temp_dict['user_1']['token'], 'My Channel', False)
    channels.channels_create(temp_dict['user_1']['token'], 'My Channel', False)
    assert channels.channels_list(temp_dict['user_1']['token']) == {'channels': [{'channel_id': 1, 'name': 'My Channel',},{'channel_id': 2, 'name': 'My Channel',} ],}

''' Test list under different token '''
def test_list_diff_token(register_data):
    temp_dict = register_data
    channels.channels_create(temp_dict['user_1']['token'], 'My Channel', False)
    channels.channels_create(temp_dict['user_2']['token'], 'My Channel', False)
    assert channels.channels_list(temp_dict['user_1']['token']) == {'channels': [{'channel_id': 1, 'name': 'My Channel'}]}
    assert channels.channels_list(temp_dict['user_2']['token']) == {'channels': [{'channel_id': 2, 'name': 'My Channel',}],}

''' Test no channels under token '''
def test_no_list(register_data):
    temp_dict = register_data
    channels.channels_create(temp_dict['user_3']['token'], 'My Channel', True)
    assert channels.channels_list(temp_dict['user_3']['token']) == {'channels': [{'channel_id': 1, 'name': 'My Channel'}]}
    assert channels.channels_list(temp_dict['user_4']['token']) == {'channels': []}

''' TEST VALID LISTALL '''
''' Test function work '''
def test_channels_listall(register_data):
    temp_dict = register_data
    channels.channels_create(temp_dict['user_1']['token'], 'My Channel', True)
    channels.channels_create(temp_dict['user_1']['token'], 'My Channel', True)
    
    #Should show all public channels for user2 and none for ser 1 (because he created)
    assert channels.channels_listall(temp_dict['user_2']['token']) == {'channels': [{'channel_id': 1, 'name': 'My Channel',},{'channel_id': 2, 'name': 'My Channel',} ],}
    assert channels.channels_listall(temp_dict['user_1']['token']) == {'channels': []}

''' Test no channels under given token '''
def test_no_listall(register_data):
    temp_dict = register_data
    assert channels.channels_listall(temp_dict['user_4']['token']) == {'channels': []}

''' TEST VALID INPUT '''
def test_channels_create(register_data):
    temp_dict = register_data
    assert channels.channels_create(temp_dict['user_1']['token'], 'My Channel', True) == {'channel_id': 1,}
    assert channels.channels_create(temp_dict['user_1']['token'], 'My Channel', False) == {'channel_id': 2,}
    
''' TEST INVALID INPUT '''
''' Token is not registered '''
def test_create_failed():
    with pytest.raises(error.InputError):
        channels.channels_create(15, 'My Channel', False)

''' InputError test about too long name '''
def test_invalid_create(register_data):
    temp_dict = register_data
    with pytest.raises(error.InputError):
        channels.channels_create(temp_dict['user_1']['token'], 'kjsadkabjkasjhaskhasdjk', 'False')

''' Clear all data and reset to initial state '''
clear()