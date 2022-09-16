import pytest
import auth
import channel
import channels
import message
from standup import standup_start, standup_active, standup_send
from error import InputError, AccessError
from other import clear
import time


#NOTE FOR TESTS: These tests may fail with slight difference in time if the time on the right 
# of the assert is calculated a second after the time on the left. I believe the logic of the 
#functions are correct, but if a failure occurs that is likely the cause due to the nature
#of the returns.

''' new user registered '''
@pytest.fixture
def register_data():
    clear()

    user1 = auth.auth_register('derek123@gmail.com', '123456', 'derek', 'dong')
    user2 = auth.auth_register('rex123@gmail.com', '123456', 'rex', 'sun')

    #might probably add new keys'is_active' and 'time_finish' in the channel_dict,
    #the last true/false represent the value of 'is_active'
    mychannel = channels.channels_create(user1['token'], 'wed15mangoTeam4', True)
    mychannel2 = channels.channels_create(user2['token'], 'wed15mangoTeam5', True)

    return_dict = {
        'user_1': user1,
        'user_2': user2,
        'channel_1': mychannel,  
        'channel_2': mychannel2,
    }
    return return_dict

#we assume any length as if it's smaller than 1000 characters is valid
#tests for start
#invalid user
def test_invalid_token(register_data):
    temp_dict = register_data

    valid_token = temp_dict['user_1']['token']
    invalid_token = valid_token + 'xx'

    valid_channel_id = temp_dict['channel_1']['channel_id']

    with pytest.raises(InputError):
        standup_start(invalid_token, valid_channel_id, 10)

#Non member tries to strat a standup
def test_invalid_member_start(register_data):
    temp_dict = register_data

    valid_token = temp_dict['user_2']['token']

    valid_channel_id = temp_dict['channel_1']['channel_id']

    with pytest.raises(AccessError):
        standup_start(valid_token, valid_channel_id, 10)

#invalid_channelID
def test_invalid_channelid(register_data):
    temp_dict = register_data

    valid_token = temp_dict['user_1']['token']
    valid_channel_id = temp_dict['channel_1']['channel_id']
    invalid_channelid = valid_channel_id + 100

    with pytest.raises(InputError):
        standup_start(valid_token, invalid_channelid, 10)

#Non member tries to check if theres a standup
def test_invalid_member_active(register_data):
    temp_dict = register_data

    valid_token = temp_dict['user_2']['token']

    valid_channel_id = temp_dict['channel_1']['channel_id']

    with pytest.raises(AccessError):
        standup_active(valid_token, valid_channel_id)

#An active standup is currently running in this channel
def test_active_standup(register_data):
    temp_dict = register_data

    valid_token = temp_dict['user_2']['token']
    valid_channel_id = temp_dict['channel_2']['channel_id']
    #Start a standup. 
    #since there is already an active standup runnning in channel_2, it should raise inputerror
    standup_start(valid_token, valid_channel_id, 10)
    with pytest.raises(InputError):
        standup_start(valid_token, valid_channel_id, 10)

#test case for successful standup_start.
def test_successful_start(register_data):
    temp_dict = register_data

    valid_token = temp_dict['user_1']['token']
    valid_channel_id = temp_dict['channel_1']['channel_id']    
    length = 5
    # weshould return time_finished, and its an integer

    assert standup_start(valid_token, valid_channel_id, length) == {'time_finish': message.change_timestamp() + length}
    time.sleep(length)
#test for standup_active
#invalid user
def test_active_invalid_token(register_data):
    temp_dict = register_data

    valid_token = temp_dict['user_1']['token']
    invalid_token = valid_token + 'x'

    valid_channel_id = temp_dict['channel_1']['channel_id']

    with pytest.raises(InputError):
        standup_active(invalid_token, valid_channel_id)

#invalid channel_id
def test_active_invalid_channelid(register_data):
    temp_dict = register_data

    valid_token = temp_dict['user_1']['token']
    valid_channel_id = temp_dict['channel_1']['channel_id']
    invalid_channelid = valid_channel_id + 2

    with pytest.raises(InputError):
        standup_start(valid_token, invalid_channelid, 15)

#test for successful case
def test_successful_active(register_data):
    temp_dict = register_data

    valid_token = temp_dict['user_1']['token']
    valid_channel_id = temp_dict['channel_1']['channel_id']   
    length = 10 
    standup_start(valid_token, valid_channel_id, length)
    
    #should return time_finish, and is_active
    assert standup_active(valid_token, valid_channel_id) == {'is_active': True, 'time_finish': message.change_timestamp() + length}

#test for standup_send

#assume a valid message
Valid_message = 'hello world'
#invalid user
def test_send_invalid_user(register_data):
    temp_dict = register_data

    valid_token = temp_dict['user_2']['token']
    valid_channel_id = temp_dict['channel_1']['channel_id']
    #it should raise acesserror since the message was sent to channel_1 and user_2 isnt a member
    with pytest.raises(AccessError):
        standup_send(valid_token, valid_channel_id, Valid_message)

#invalid channel_id
def test_send_invalid_channelid(register_data):
    temp_dict = register_data

    valid_token = temp_dict['user_2']['token']
    valid_channel_id = temp_dict['channel_2']['channel_id']  
    invalid_channelid = valid_channel_id + 10

    with pytest.raises(InputError):
        standup_send(valid_token, invalid_channelid, Valid_message)

#An active standup is not currently running in this channel
def test_send_non_active(register_data):
    temp_dict = register_data

    valid_token = temp_dict['user_1']['token']
    valid_channel_id = temp_dict['channel_1']['channel_id']  

    #since 'is_active' for channel1 is False, it should raise inputerror then
    with pytest.raises(InputError):
        standup_send(valid_token, valid_channel_id, Valid_message)

#test for successful cases
def test_send_success(register_data):
    temp_dict = register_data

    valid_token = temp_dict['user_2']['token']
    valid_channel_id = temp_dict['channel_2']['channel_id']
    length = 10

    standup_start(valid_token, valid_channel_id, length)
    assert standup_send(valid_token, valid_channel_id, Valid_message) == {}
    time.sleep(length)


