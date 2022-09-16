import pytest
import auth
import channel
import channels
import message
import user
from error import InputError, AccessError
from other import clear, users_all, search, seek_from_token, admin_userpermission_change

''' new user registered '''
@pytest.fixture
def register_data():
    clear()

    user1 = auth.auth_register('derek123@gmail.com', '123456', 'derek', 'dong')
    user2 = auth.auth_register('rex123@gmail.com', '123456', 'rex', 'sun')

    mychannel = channels.channels_create(user1['token'], 'wed15mangoTeam4', True)
    mychannel2 = channels.channels_create(user2['token'], 'wed15mangoTeam5', True)

    return_dict = {
        'user_1': user1,
        'user_2': user2,
        'channel_1': mychannel,   
        'channel_2': mychannel2,
    }
    return return_dict

#tests for users_all
def test_invalid_token():
    #create invalid token for test
    invalid_token = "abcdef"
    with pytest.raises(AccessError):
        users_all(invalid_token)

#since successful cases are tested in user_test.py already, just add supplementary case for invalid one
def test_successful_users(register_data):
    temp_dict = register_data

    with pytest.raises(AccessError):
        users_all('')
   
    assert users_all(temp_dict['user_1']['token']) == {'users': [{ 'u_id': temp_dict['user_1']['u_id'], 'email': 'derek123@gmail.com','name_first': 'derek','name_last': 'dong', 'profile_img_url': None,}, {'u_id': temp_dict['user_2']['u_id'], 'email': 'rex123@gmail.com','name_first': 'rex','name_last': 'sun', 'profile_img_url': None,}],}

#tests for search
#invalid user
def test_token_invalid(register_data):
    temp_dict = register_data
    
    valid_token = temp_dict['user_1']['token']
    
    invalid_token = valid_token + 'x'
    temp_dict['channel_1']['channel_id'] = temp_dict['channel_1']['channel_id']

    message.message_send(valid_token, temp_dict['channel_1']['channel_id'], 'hi everyone')
    
    with pytest.raises(AccessError):
        search(invalid_token, 'hi everyone')

#assert first registered user has owner permissions
def test_permission_original(register_data):
    temp_dict = register_data
    
    owner = seek_from_token(temp_dict['user_1']['token'])
    user = seek_from_token(temp_dict['user_2']['token'])

    assert owner['permissions'] == 1
    assert user['permissions'] == 2

#check if permission_change function is successful
def test_permission_change(register_data):
    temp_dict = register_data
    
    admin_userpermission_change(temp_dict['user_1']['token'], temp_dict['user_2']['u_id'], '1')

    user = seek_from_token(temp_dict['user_2']['token'])

    assert user['permissions'] == 1

#check invalid permission id raises arror
def test_permission_invalid_permission(register_data):
    temp_dict = register_data
    
    with pytest.raises(InputError):
        admin_userpermission_change(temp_dict['user_1']['token'], temp_dict['user_2']['u_id'], 'abcde')

def test_permission_invalid_users(register_data):
    temp_dict = register_data
    
    #user isn't valid
    with pytest.raises(InputError):
        admin_userpermission_change(temp_dict['user_1']['token'], "abcde", '1')
    
    #token isnt_owner
    with pytest.raises(AccessError):
        admin_userpermission_change(temp_dict['user_2']['token'], temp_dict['user_2']['u_id'], '1')

#cant search for long message with more than 1000 characters
def test_long_message(register_data):
    temp_dict = register_data

    channel.channel_join(temp_dict['user_1']['token'], temp_dict['channel_2']['channel_id'])

    assert search(temp_dict['user_1']['token'], 'aaa' * 1000) == {'messages': []}
    assert search(temp_dict['user_1']['token'], '') == {'messages': []}

#tests for successful cases
#search all the message string containing in the channel which user belongs to
def test_all_messages(register_data):
    temp_dict = register_data
   
    channel.channel_join(temp_dict['user_1']['token'], temp_dict['channel_2']['channel_id'])

    message_info1 = message.message_send(temp_dict['user_1']['token'], temp_dict['channel_1']['channel_id'], 'hi everyone')
    message_id1 = message_info1['message_id']

    message_info2 = message.message_send(temp_dict['user_2']['token'], temp_dict['channel_2']['channel_id'], 'hello everyone')
    message_id2 = message_info2['message_id']
   
    messages1 = channel.find_messages(temp_dict['channel_1']['channel_id'])
    messages2 = channel.find_messages(temp_dict['channel_2']['channel_id'])

    assert search(temp_dict['user_1']['token'], 'every') == {
        'messages':[
            {
                'message_id': message_id1,
                'u_id': temp_dict['user_1']['u_id'],
                'message': 'hi everyone',
                'time_created': messages1[0].get('time_created'),
            },
            {
                'message_id': message_id2,
                'u_id': temp_dict['user_2']['u_id'],
                'message': 'hello everyone',
                'time_created': messages2[0].get('time_created'),
            }
        ]
    }

    assert search(temp_dict['user_1']['token'], 'hi') =={
        'messages':[
            {
                'message_id': message_id1,
                'u_id': temp_dict['user_1']['u_id'],
                'message': 'hi everyone',
                'time_created': messages1[0].get('time_created'),
            }
        ]        
    }

#cant search for messages in channel which user isnt belong to
def test_part_of_some_channel(register_data):
    temp_dict = register_data

    channel.channel_join(temp_dict['user_1']['token'], temp_dict['channel_2']['channel_id'])

    message.message_send(temp_dict['user_1']['token'], temp_dict['channel_1']['channel_id'], 'hi everyone')

    message_info2 = message.message_send(temp_dict['user_2']['token'], temp_dict['channel_2']['channel_id'], 'hello everyone')
    message_id2 = message_info2['message_id']

    messages = channel.find_messages(temp_dict['channel_2']['channel_id'])

    assert search(temp_dict['user_2']['token'], 'every') == {
        'messages':[
            {
                'message_id': message_id2,
                'u_id': temp_dict['user_2']['u_id'],
                'message': 'hello everyone',
                'time_created': messages[0].get('time_created'),
            }
        ]
    }

#cant search for messages when user isnt belong to the channel
def test_not_part_of_channel(register_data):
    temp_dict = register_data

    channel.channel_join(temp_dict['user_1']['token'], temp_dict['channel_2']['channel_id'])
    channel.channel_addowner(temp_dict['user_2']['token'], temp_dict['channel_2']['channel_id'], temp_dict['user_1']['u_id'])
    channel.channel_leave(temp_dict['user_2']['token'], temp_dict['channel_2']['channel_id'])
    
    message.message_send(temp_dict['user_1']['token'], temp_dict['channel_1']['channel_id'], 'hi everyone')

    message.message_send(temp_dict['user_1']['token'], temp_dict['channel_2']['channel_id'], 'hello everyone')

    assert search(temp_dict['user_2']['token'], 'every') == {
        'messages':[]
    }

#it will return nothing if the message doesnt exsit
def test_no_exsiting_message(register_data):
    temp_dict = register_data

    channel.channel_join(temp_dict['user_1']['token'], temp_dict['channel_2']['channel_id'])

    message.message_send(temp_dict['user_1']['token'], temp_dict['channel_1']['channel_id'], 'hi everyone')

    message.message_send(temp_dict['user_2']['token'], temp_dict['channel_2']['channel_id'], 'hello everyone')

    assert search(temp_dict['user_1']['token'], 'python') == {
        'messages':[]
    }    

clear()