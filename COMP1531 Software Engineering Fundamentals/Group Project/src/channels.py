from error import InputError, AccessError
import auth
import channel
num_channels = 0
channels_dict = {}

'''Helper Functions'''
'''Generate a key to append to channels dict'''
def Generate_key():
    global num_channels
    num_channels += 1
    return "channel_" + str(num_channels)

'''Validate details entered'''
def validate_details(token, name):
    #Assert proposed name is not too long
    if len(name) > 20:
        raise InputError(f"Name {name} is too long")
    
    #Assert tokn is a valid user
    for user in auth.user_info:
        if (auth.user_info[user].get(token) == token):
            return True

    #raise AccessError(f"Token {token} is not valid")

'''Main Functions'''
'''Generate list of channels that the token is part of'''
def channels_list(token):
    '''Get the U_id'''
    user = channel.valid_user(token)
    channels_list = []
    for curr_channel in channels_dict:
        for member in channels_dict[curr_channel]['members']['all_members']:
            print(user.get('u_id'))
            if member.get('u_id') == user.get('u_id'):
                details = {
                    'channel_id':channels_dict[curr_channel].get('channel_id'),
                    'name': channels_dict[curr_channel].get('name'),
                }
                channels_list.append(details)

    return {'channels': channels_list,}
  
'''Generate list of public channels that the token is not part of'''
def channels_listall(token):
    '''Get the U_id'''
    user = channel.valid_user(token)

    channels_list = []
    for curr_channel in channels_dict:
        channel_members = channels_dict[curr_channel]['members'].get('all_members')
        if channels_dict[curr_channel]['is_public'] and {'u_id': user.get('u_id')} not in channel_members:
            details = {
                'channel_id':channels_dict[curr_channel].get('channel_id'),
                'name': channels_dict[curr_channel].get('name'),
            }
            channels_list.append(details)
        
    return {'channels': channels_list,}

'''Creat a new cahnnel'''
def channels_create(token, name, is_public):
    '''Get the u_id'''
    user = channel.valid_user(token)
    
    '''Check token and name are suitable'''
    validate_details(token, name)

    ''' create a channel dictionary with details and a key for it'''
    key = Generate_key()
    new_channel = {
        'name': name,
        'is_public': is_public,
        'channel_id': num_channels,
        'members': {
            'owner': [{'u_id': int(user.get('u_id'))}, ],
            'all_members': [{'u_id': int(user.get('u_id'))}, ],
        },
        'message': [],
        'standup': 0,
        'standup_message': '',
    }

    '''push channel dictionary into channels dictionary under a key'''
    channels_dict[key] = new_channel
    
    return {'channel_id': num_channels}
    
