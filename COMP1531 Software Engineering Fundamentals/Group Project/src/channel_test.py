import pytest
import auth
import message

import channel
import channels
from error import InputError, AccessError
from other import clear

#from global_data import user_dict, channels.channels_dict
#a new user is registered
@pytest.fixture
def register_data():
    clear()

    owner = auth.auth_register("vera123@gmail.com", "123456", "vera", "Zhao")
    user1 = auth.auth_register("ruby123@gmail.com", "123456", "ruby", "Shao")
    user2 = auth.auth_register("rex123@gmail.com", "123456", "rex", "Sun")
    user3 = auth.auth_register("derek123@gmail.com", "123456", "derek", "Dong")
    user4 = auth.auth_register("isha123@gmail.com", "123456", "isha", "Shroff")
    user5 = auth.auth_register("luy123@gmail.com", "123456", "luy", "Xie")

    #a new public channel is created
    #assume 1 is public and 0 is private
    mychannel = channels.channels_create(owner['token'], 'wed15mangoTeam4', True)
    channel_id = mychannel.get('channel_id')

    #a new private channel is created
    private_channel1 = channels.channels_create(user2['token'], 'private channel', False)
    channel_id2 = private_channel1.get('channel_id')

    private_channel2 = channels.channels_create(user3['token'], 'private channel', False)
    channel_id3 = private_channel2.get('channel_id')

    channel.channel_invite(owner['token'], channel_id, user1['u_id'])
    channel.channel_invite(owner['token'], channel_id, user2['u_id'])
    channel.channel_invite(owner['token'], channel_id, user3['u_id'])

    return_dict = {
        'owner': owner,
        'user_1': user1,
        'user_2': user2,
        'user_3': user3,
        'user_4': user4,
        'user_5': user5,  
        'channel_id': channel_id,   
        'channel_id2': channel_id2,   
        'channel_id3': channel_id3,
    }

    return return_dict

#======test channel.channel_invite==========
#succseeful case    
def test_channel_invite(register_data):
    temp_dict = register_data
    assert channel.channel_invite(temp_dict['owner']['token'], temp_dict['channel_id'], temp_dict['user_5']['u_id']) == {}

#test input error
#test channel_id does not refer to a valid channel
def test_channel_invite_invalid_channel(register_data):
    temp_dict = register_data
    with pytest.raises(InputError):
        assert channel.channel_invite(temp_dict['owner']['token'], 4, temp_dict['user_5']['u_id'])

#test u_id does not refer to a valid user
def test_channel_invite_invalid_user(register_data):
    temp_dict = register_data
    with pytest.raises(InputError):
        assert channel.channel_invite(temp_dict['owner']['token'], temp_dict['channel_id'], 7)

#test AccessError
#test the authorised user is not already a member of the channel
def test_channel_invite_not_a_member(register_data):
    temp_dict = register_data
    with pytest.raises(AccessError):
        assert channel.channel_invite(temp_dict['user_4']['token'], temp_dict['channel_id'], temp_dict['user_5']['u_id'])

#test u_id is already a member in channel
def test_channel_invite_already_a_member(register_data):
    temp_dict = register_data
    with pytest.raises(AccessError):
        assert channel.channel_invite(temp_dict['owner']['token'], temp_dict['channel_id'], temp_dict['user_2']['u_id'])

#===========test channel.channel_details=============
#test successful cases
def test_channel_details(register_data):
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

            },
            {
                'u_id': 2,
                'name_first': 'ruby',
                'name_last': 'Shao',
                'profile_img_url': None,
            },
            {
                'u_id': 3,
                'name_first': 'rex',
                'name_last': 'Sun',
                'profile_img_url': None,
            },
            {
                'u_id': 4,
                'name_first': 'derek',
                'name_last': 'Dong',
                'profile_img_url': None,
            },
        ],
    }
    temp_dict = register_data
    assert channel.channel_details(temp_dict['owner']['token'], temp_dict['channel_id']) == details

#test Access error
#test Authorised user is not a member of channel with channel_id
def test_channel_details_not_a_member(register_data):
    temp_dict = register_data
    with pytest.raises(AccessError):
        assert channel.channel_details(temp_dict['user_4']['token'], temp_dict['channel_id'])

#==========test channel.channel_messages===========
#test successful cases
def test_channel_messages(register_data):
    temp_dict = register_data
    
    message.message_send(temp_dict['owner']['token'], temp_dict['channel_id'], 'have a good time')
    message.message_send(temp_dict['owner']['token'], temp_dict['channel_id'], 'ttyl')

    #Get messages in channel one so we can get times for first and second message
    messages = channel.find_messages(temp_dict['channel_id'])
    
    sample_message = {
        'messages': [
            {
                'message_id': 2,
                'u_id': 1,
                'message': 'ttyl',
                'time_created': messages[1].get('time_created')
            },
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'have a good time',
                'time_created': messages[0].get('time_created')
            }
        ],
        'start': 2,
        'end': -1,
    }
    assert channel.channel_messages(temp_dict['owner']['token'], temp_dict['channel_id'], 2) == sample_message

#test start is greater than the total number of messages in the channel

def test_channel_messages_bigger_start(register_data):
    temp_dict = register_data
    with pytest.raises(InputError):
        assert channel.channel_messages(temp_dict['owner']['token'], temp_dict['channel_id'], 5)

#test access error
#test Authorised user is not a member of channel with channel_id
def test_channel_messages_not_a_member(register_data):
    temp_dict = register_data
    with pytest.raises(AccessError):
        assert channel.channel_messages(temp_dict['user_4']['token'], temp_dict['channel_id'], 0)

#=========test channel.channel_leave==========
#successful case
def test_channel_leave(register_data):
    temp_dict = register_data
    assert channel.channel_leave(temp_dict['user_2']['token'], temp_dict['channel_id']) == {}

#if owner want to leave channel
def test_channel_owner_leave(register_data):
    temp_dict = register_data
    channel.channel_invite(temp_dict['user_2']['token'], temp_dict['channel_id2'], temp_dict['user_1']['u_id'])
    assert channel.channel_leave(temp_dict['user_2']['token'], temp_dict['channel_id2']) == {}

#if last member wants to leave
def test_channel_last_owner(register_data):
    temp_dict = register_data
    assert channel.channel_leave(temp_dict['user_2']['token'], temp_dict['channel_id2']) == {}

# AccessError
# test if authorised user not a member of channel
def test_channel_leave_not_an_member(register_data):
    temp_dict = register_data
    with pytest.raises(AccessError):
        channel.channel_leave(temp_dict['user_4']['token'], temp_dict['channel_id'])

#==============test channel.channel_join================
# successful case
# no InputError and AccessError
def test_channel_join(register_data):
    temp_dict = register_data
    assert channel.channel_join(temp_dict['user_4']['token'], temp_dict['channel_id']) == {}

#Raises error as user is already a member
def test_channel_join_already_member(register_data):
    temp_dict = register_data
    with pytest.raises (InputError):
        channel.channel_join(temp_dict['owner']['token'], temp_dict['channel_id'])

# AccessError
# test if the channel is private
def test_channel_join_private_channel(register_data):
    temp_dict = register_data
    with pytest.raises(AccessError):
        assert channel.channel_join(temp_dict['user_2']['token'], temp_dict['channel_id3'])

#=============================ADD/REMOVE OWNER TESTS=========================#
#instead of treating the parameter as the simple num, just put the key on it,
#so that later can be readable and easier to change it

# successful case
def test_channel_addowner(register_data):
    temp_dict = register_data
    # let user1 to join the public channel created by owner.
    assert channel.channel_addowner(temp_dict['owner']['token'], temp_dict['channel_id'], temp_dict['user_1']['u_id']) == {}

def test_channel_addowner_already_owner(register_data):
    temp_dict = register_data
    # let user1 to join the public channel created by owner. 
    # fails cuz user is already the channel owner(creator)
    channel.channel_addowner(temp_dict['owner']['token'], temp_dict['channel_id'], temp_dict['user_1']['u_id'])
    with pytest.raises(InputError):
        channel.channel_addowner(temp_dict['user_1']['token'], temp_dict['channel_id'], temp_dict['user_1']['u_id'])

def test_channel_addowner_not_owner(register_data):
    temp_dict = register_data
    # let user1 to join the public channel created by owner.
    with pytest.raises(AccessError):
        channel.channel_addowner(temp_dict['user_3']['token'], temp_dict['channel_id'], temp_dict['user_3']['u_id'])

#successful case
def test_channel_removeowner(register_data):
    temp_dict = register_data
    # let user1 to join the public channel created by owner
    # then being the owner added by the orinal owner(Vera).
    channel.channel_addowner(temp_dict['owner']['token'], temp_dict['channel_id'], temp_dict['user_1']['u_id'])
    assert channel.channel_removeowner(temp_dict['user_1']['token'], temp_dict['channel_id'], temp_dict['user_1']['u_id']) == {} 

# fails since user1 is not the owner of the channel
def test_channel_removeowner_not_owner(register_data):
    temp_dict = register_data
    
    with pytest.raises(AccessError):
        channel.channel_removeowner(temp_dict['owner']['token'], temp_dict['channel_id'], temp_dict['user_2']['u_id'])

# fails since user1 is not a member of the channel
def test_channel_removeowner_not_member(register_data):
    temp_dict = register_data
    channel.channel_leave(temp_dict['user_1']['token'], temp_dict['channel_id'])
    with pytest.raises(AccessError):
        channel.channel_removeowner(temp_dict['owner']['token'], temp_dict['channel_id'], temp_dict['user_1']['u_id'])

def test_channel_removeowner_wrong_owner(register_data):
    temp_dict = register_data
    channel.channel_addowner(temp_dict['owner']['token'], temp_dict['channel_id'], temp_dict['user_3']['u_id'])
    # fails since user2 is not the owner of the channel,
    # so without any authority to remove other member
    with pytest.raises(AccessError):
        channel.channel_removeowner(temp_dict['user_2']['token'], temp_dict['channel_id'], temp_dict['user_3']['u_id']) 
        # the case is about when the authorised user is not an owner,
        # so cant remove other owner

#should be more specific cases for tests, especially for the remove one
# extra cases:
# case1: there is only 1 member in the channel(the owner herself),
# so she can't be removed by herself
def test_channel_removeowner_specific_case1(register_data):
    temp_dict = register_data
    with pytest.raises(AccessError):
        channel.channel_removeowner(temp_dict['user_1']['token'], temp_dict['channel_id'], temp_dict['user_1']['u_id'])

# case2: since the user1 havent joined the channel(not a member for the channel at all)
def test_channel_removeowner_specific_case2(register_data):
    temp_dict = register_data
    with pytest.raises(AccessError):
        channel.channel_removeowner(temp_dict['user_1']['token'], temp_dict['channel_id'], temp_dict['user_3']['u_id'])


clear()

