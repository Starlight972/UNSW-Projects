import pytest
from error import InputError, AccessError
from other import clear
from auth import auth_register, user_info
from channels import channels_create, channels_dict
from message import message_send, message_remove, message_edit, message_sendlater, message_react, message_unreact, message_pin, message_unpin
from channel import channel_invite
import message_data
from datetime import datetime
from pytz import timezone as tz
import time

#register some users
@pytest.fixture
def register_data():
    clear()

    owner = auth_register("vera123@gmail.com", "123456", "vera", "Zhao")
    user1 = auth_register("ruby123@gmail.com", "123456", "ruby", "Shao")
    user2 = auth_register("rex123@gmail.com", "123456", "rex", "Sun")
    user3 = auth_register("derek123@gmail.com", "123456", "derek", "Dong")
    user4 = auth_register("isha123@gmail.com", "123456", "isha", "Shroff")
    user5 = auth_register("luy123@gmail.com", "123456", "luy", "Xie")

    #a new public channel is created
    #assume 1 is public and 0, is private
    mychannel = channels_create(owner['token'], 'wed15mangoTeam4', True)
    channel_id = mychannel.get('channel_id')

    mychannel2 = channels_create(owner['token'], 'channel2', True)
    channel2_id = mychannel2.get('channel_id')
    
    channel_invite(owner['token'], channel_id, user1['u_id'])
    channel_invite(owner['token'], channel_id, user2['u_id'])
    channel_invite(owner['token'], channel_id, user3['u_id'])
    channel_invite(owner['token'], channel_id, user4['u_id'])

    return_dict = {
        'owner': owner,
        'user_1': user1,
        'user_2': user2,
        'user_3': user3,
        'user_4': user4,
        'user_5': user5,  
        'channel_id': channel_id,
        'channel2_id': channel2_id,  
        'message1_id': 0,
        'message2_id': 0,
        'message3_id': 0,
        'message4_id': 0 
    }

    return return_dict
#=============test message_send=========
#test successful case
def test_message_send(register_data):
    temp_data = register_data
    
    return_id = message_send(temp_data['owner']['token'], temp_data['channel_id'], 'hi everyone')
    global message1_id
    message1_id = return_id['message_id']
    assert message1_id == 1

    return_id = message_send(temp_data['owner']['token'], temp_data['channel_id'], 'nice to see u')
    global message2_id
    message2_id = return_id['message_id']
    assert message2_id == 2

    return_id = message_send(temp_data['owner']['token'], temp_data['channel_id'], 'have a good time')
    global message3_id
    message3_id = return_id['message_id']
    assert message3_id == 3

    return_id = message_send(temp_data['owner']['token'], temp_data['channel_id'], 'ttyl')
    global message4_id
    message4_id = return_id['message_id']
    assert message4_id == 4

#Input Error
#check if message is more than 1000 characters
def test_message_send_long_message(register_data):
    temp_data = register_data
    with pytest.raises(InputError):
        message_send(temp_data['owner']['token'], temp_data['channel_id'], 'aaa' * 1000)

#check invalid channel id
def test_message_send_invalid_channel(register_data):
    temp_data = register_data
    with pytest.raises(InputError):
        message_send(temp_data['owner']['token'], 4, 'hi everyone')

#Access Error
#check the authorised user has not joined the channel they are trying to post to
def test_message_send_not_an_member(register_data):
    temp_data = register_data
    with pytest.raises(AccessError):
        message_send(temp_data['user_5']['token'], temp_data['channel_id'], 'hi everyone') 

#=============test message_remove==========
#test successful case
def test_message_remove(register_data):
    temp_data = register_data
    message_send(temp_data['owner']['token'], temp_data['channel_id'], 'hi everyone')
    assert message_remove(temp_data['owner']['token'], message1_id) == {}

#Input Error
#test Message (based on ID) no longer exists
def test_message_remove_no_message(register_data):
    temp_data = register_data
    with pytest.raises(InputError):
        message_remove(temp_data['owner']['token'], message1_id)

#test invalid token
def test_message_remove_invalid_token():
    with pytest.raises(InputError):
        message_remove('invalidtoken', message2_id)

#Access Error
'''
test Message with message_id was not sent by the authorised user making this request and 
also not the owner of that channel
'''
def test_message_remove_user_without_permission(register_data):
    temp_data = register_data
    
    message_send(temp_data['owner']['token'], temp_data['channel_id'], 'hi everyone')
    message2 = message_send(temp_data['owner']['token'], temp_data['channel_id'], 'nice to see u')

    with pytest.raises(AccessError):
        message_remove(temp_data['user_1']['token'], message2.get('message_id'))

#============test message_edit=======
#test successful test
def test_message_edit(register_data):
    temp_data = register_data
    message1 = message_send(temp_data['owner']['token'], temp_data['channel_id'], 'have a good time')
    assert message_edit(temp_data['owner']['token'], message1.get('message_id'), 'I am the owner of this channel') == {}

#test message = ''
def test_message_edit_empty_message(register_data):
    temp_data = register_data
    message1 = message_send(temp_data['owner']['token'], temp_data['channel_id'], 'have a good time')
    assert message_edit(temp_data['owner']['token'], message1.get('message_id'), '') == {}

#Input Error
#test invalid token
def test_message_edit_invalid_token(register_data):
    temp_data = register_data
    message1 = message_send(temp_data['owner']['token'], temp_data['channel_id'], 'have a good time')
    with pytest.raises(InputError):
        message_edit('invalidtoken', message1.get('message_id'), 'hello')

#check if message is more than 1000 characters
def test_message_edit_long_message(register_data):
    temp_data = register_data
    with pytest.raises(InputError):
        message_edit(temp_data['owner']['token'], message2_id, 'aaa' * 1000)

#Access Error
'''
test Message with message_id was not sent by the authorised user making this request and 
also not the owner of that channel
'''
def test_message_edit_user_without_permission(register_data):
    temp_data = register_data
    message1 = message_send(temp_data['owner']['token'], temp_data['channel_id'], 'hi everyone')

    with pytest.raises(AccessError):
        message_edit(temp_data['user_1']['token'], message1.get('message_id'), 'hello')

#============test message_sendlater=======
#test successful case
def test_message_sendlater(register_data):
    temp_data = register_data
    #dt = datetime.now()
    
    au_tz = tz('Australia/Sydney')
    timestamp = au_tz.localize(datetime.now())
    timestamp = time.mktime(timestamp.timetuple()) + 5

    #timestamp = dt.replace(tzinfo=timezone.utc).timestamp() + 5
    message6 = message_sendlater(temp_data['owner']['token'], temp_data['channel_id'], 'just test', timestamp)
    assert message6.get('message_id') == 1

#Input Error
#test Channel ID is not a valid channel
def test_message_sendlater_invalid_channel(register_data):
    temp_data = register_data
    #dt = datetime(2020, 12, 25, 12, 30)
    #timestamp = dt.replace(tzinfo=timezone.utc).timestamp()

    au_tz = tz('Australia/Sydney')
    timestamp = au_tz.localize(datetime(2020, 12, 25, 12, 30))
    timestamp = time.mktime(timestamp.timetuple())
    
    with pytest.raises(InputError):
        message_sendlater(temp_data['owner']['token'], 100, 'just test', timestamp)

#test Message is more than 1000 characters
def test_message_sendlater_long_message(register_data):
    temp_data = register_data
    # dt = datetime(2020, 12, 25, 12, 30)
    # timestamp = dt.replace(tzinfo=timezone.utc).timestamp()

    au_tz = tz('Australia/Sydney')
    timestamp = au_tz.localize(datetime(2020, 12, 25, 12, 30))
    timestamp = time.mktime(timestamp.timetuple())
        
    with pytest.raises(InputError):
        message_sendlater(temp_data['owner']['token'], temp_data['channel_id'], 'aaa' * 1000, timestamp)

#test Time sent is a time in the past
def test_message_sendlater_past_time(register_data):
    temp_data = register_data
    # dt = datetime(2020, 1, 1, 13)
    # timestamp = dt.replace(tzinfo=timezone.utc).timestamp()

    au_tz = tz('Australia/Sydney')
    timestamp = au_tz.localize(datetime(2020, 1, 1, 13))
    timestamp = time.mktime(timestamp.timetuple())
    
    with pytest.raises(InputError):
        message_sendlater(temp_data['owner']['token'], temp_data['channel_id'], 'just test', timestamp)

#Access Error
#test the authorised user has not joined the channel they are trying to post to
def test_message_sendlater_not_a_member(register_data):
    temp_data = register_data
    # dt = datetime(2020, 12, 25, 12, 30)
    # timestamp = dt.replace(tzinfo=timezone.utc).timestamp()

    au_tz = tz('Australia/Sydney')
    timestamp = au_tz.localize(datetime(2020, 12, 25, 12, 30))
    timestamp = time.mktime(timestamp.timetuple())
    
    with pytest.raises(AccessError):
        message_sendlater(temp_data['user_5']['token'], temp_data['channel_id'], 'just test', timestamp)

#============test message_react=======
#test successful case
def test_message_react(register_data):
    temp_data = register_data
    message6 = message_send(temp_data['owner']['token'], temp_data['channel_id'], 'just test')
    assert message_react(temp_data['owner']['token'], message6.get('message_id'), 1) == {}

#Input Error
#test message_id is not a valid message within a channel that the authorised user has joined
def test_message_react_invalid_message(register_data):
    temp_data = register_data
    message6 = message_send(temp_data['owner']['token'], temp_data['channel2_id'], 'just test')
    with pytest.raises(InputError):
        message_react(temp_data['user_2']['token'], message6.get('message_id'), 1)

#test react_id is not a valid React ID. The only valid react ID the frontend has is 1
def test_message_react_invalid_react_id(register_data):
    temp_data = register_data
    message6 = message_send(temp_data['owner']['token'], temp_data['channel_id'], 'just test')
    with pytest.raises(InputError):
        message_react(temp_data['owner']['token'], message6.get('message_id'), 2)

#test Message with ID message_id already contains an active React with ID react_id from the authorised user
def test_message_react_repeat_react_by_message_sender(register_data):
    temp_data = register_data
    message6 = message_send(temp_data['owner']['token'], temp_data['channel_id'], 'just test')
    message_react(temp_data['owner']['token'], message6.get('message_id'), 1)
    with pytest.raises(InputError):
        message_react(temp_data['owner']['token'], message6.get('message_id'), 1)

def test_message_react_repeat_react_by_other_user(register_data):
    temp_data = register_data
    message6 = message_send(temp_data['owner']['token'], temp_data['channel_id'], 'just test')
    message_react(temp_data['user_2']['token'], message6.get('message_id'), 1)
    with pytest.raises(InputError):
        message_react(temp_data['user_2']['token'], message6.get('message_id'), 1)

#============test message_unreact=========
#test successful case
def test_message_unreact_by_message_sender(register_data):
    temp_data = register_data
    message6 = message_send(temp_data['owner']['token'], temp_data['channel_id'], 'just test')
    message_react(temp_data['owner']['token'], message6.get('message_id'), 1)
    assert message_unreact(temp_data['owner']['token'], message6.get('message_id'), 1) == {}

def test_message_unreact_by_other_user(register_data):
    temp_data = register_data
    message6 = message_send(temp_data['owner']['token'], temp_data['channel_id'], 'just test')
    message_react(temp_data['user_2']['token'], message6.get('message_id'), 1)
    assert message_unreact(temp_data['user_2']['token'], message6.get('message_id'), 1) == {}
#Input Error
#test message_id is not a valid message within a channel that the authorised user has joined
def test_message_unreact_invalid_message(register_data):
    temp_data = register_data
    with pytest.raises(InputError):
        message_unreact(temp_data['owner']['token'], 100, 1)

#test react_id is not a valid React ID
def test_message_unreact_invalid_react_id(register_data):
    temp_data = register_data
    message6 = message_send(temp_data['owner']['token'], temp_data['channel_id'], 'just test')
    message_react(temp_data['owner']['token'], message6.get('message_id'), 1)
    with pytest.raises(InputError):
        message_unreact(temp_data['owner']['token'], message6.get('message_id'), 2)

#test Message with ID message_id does not contain an active React with ID react_id
def test_message_unreact_no_active_react_by_message_sender(register_data):
    temp_data = register_data
    message6 = message_send(temp_data['owner']['token'], temp_data['channel_id'], 'just test')
    with pytest.raises(InputError):
        message_unreact(temp_data['owner']['token'], message6.get('message_id'), 1)

def test_message_unreact_no_active_react_by_other_user(register_data):
    temp_data = register_data
    message6 = message_send(temp_data['owner']['token'], temp_data['channel_id'], 'just test')
    with pytest.raises(InputError):
        message_unreact(temp_data['user_2']['token'], message6.get('message_id'), 1)

#=========test message_pin=======
#test successful case
def test_message_pin(register_data):
    temp_data = register_data
    message6 = message_send(temp_data['owner']['token'], temp_data['channel_id'], 'just test')
    assert message_pin(temp_data['owner']['token'], message6.get('message_id')) == {}

#Input Error
#test message_id is not a valid message
def test_message_pin_invalid_message(register_data):
    temp_data = register_data
    with pytest.raises(InputError):
        message_pin(temp_data['owner']['token'], 100)

#test Message with ID message_id is already pinned
def test_message_pin_already_pin(register_data):
    temp_data = register_data
    message6 = message_send(temp_data['owner']['token'], temp_data['channel_id'], 'just test')
    message_pin(temp_data['owner']['token'], message6.get('message_id'))
    with pytest.raises(InputError):
        message_pin(temp_data['owner']['token'], message6.get('message_id'))

#Access Error
#test The authorised user is not a member of the channel that the message is within
def test_message_pin_not_a_member(register_data):
    temp_data = register_data
    message6 = message_send(temp_data['owner']['token'], temp_data['channel_id'], 'just test')
    with pytest.raises(AccessError):
        message_pin(temp_data['user_5']['token'], message6.get('message_id'))

#The authorised user is not an owner
def test_message_pin_not_owner(register_data):
    temp_data = register_data
    message6 = message_send(temp_data['owner']['token'], temp_data['channel_id'], 'just test')
    with pytest.raises(AccessError):
        message_pin(temp_data['user_2']['token'], message6.get('message_id'))

#==========test message_unpin========
#test successful case
def test_message_unpin(register_data):
    temp_data = register_data
    message6 = message_send(temp_data['owner']['token'], temp_data['channel_id'], 'just test')
    message_pin(temp_data['owner']['token'], message6.get('message_id'))
    assert message_unpin(temp_data['owner']['token'], message6.get('message_id')) == {}

#Input Error
#test message_id is not a valid message
def test_message_unpin_invalid_message(register_data):
    temp_data = register_data
    message6 = message_send(temp_data['owner']['token'], temp_data['channel_id'], 'just test')
    message_pin(temp_data['owner']['token'], message6.get('message_id'))
    with pytest.raises(InputError):
        message_unpin(temp_data['owner']['token'], 100)

#test Message with ID message_id is already unpinned
def test_message_unpin_already_unpin(register_data):
    temp_data = register_data
    message6 = message_send(temp_data['owner']['token'], temp_data['channel_id'], 'just test')
    message_pin(temp_data['owner']['token'], message6.get('message_id'))
    message_unpin(temp_data['owner']['token'], message6.get('message_id'))
    with pytest.raises(InputError):
        message_unpin(temp_data['owner']['token'], message6.get('message_id'))

#Access Error
#test The authorised user is not a member of the channel that the message is within
def test_message_unpin_not_a_member(register_data):
    temp_data = register_data
    message6 = message_send(temp_data['owner']['token'], temp_data['channel_id'], 'just test')
    message_pin(temp_data['owner']['token'], message6.get('message_id'))
    with pytest.raises(AccessError):
        message_unpin(temp_data['user_5']['token'], message6.get('message_id'))

#test The authorised user is not an owner
def test_message_unpin_not_owner(register_data):
    temp_data = register_data
    message6 = message_send(temp_data['owner']['token'], temp_data['channel_id'], 'just test')
    message_pin(temp_data['owner']['token'], message6.get('message_id'))
    with pytest.raises(AccessError):
        message_unpin(temp_data['user_2']['token'], message6.get('message_id'))
clear()

