import auth
import channels
import message
import message_data
import channel
from error import AccessError, InputError

permissions = [1, 2]

#===================help fuction=========================
#with giving a valid u_id, return all the info about the user
def seek_from_uid(u_id):
    for user in auth.user_info:
        if auth.user_info[user]['u_id'] == u_id:
            return auth.user_info[user]
    return None

#with giving a valid token, return all the infor about the user
def seek_from_token(token):
    for user in auth.user_info:
        if auth.user_info[user]['token'] == token:
            return auth.user_info[user]
    return None
#===========================================

def clear():
    #Reset auth.py data
    auth.user_info = {}
    auth.id_val = 0
    auth.num_users = 0
    auth.handles_list = []
   
    #reset channels.py data
    channels.channels_dict = {}
    channels.num_channels = 0
    channels.count = 0

    #reset message.py data
    message_data.all_messages = {}
    message.num_message = 0
    message.mess_count = 0
   
def users_all(token):
    users_list = []
    if seek_from_token(token) != None:
        for user in auth.user_info:
            user_dict = auth.user_info.get(user)
            print(user_dict)
            return_dict = {
                'u_id': user_dict.get('u_id'),
                'email': user_dict.get('email'),
                'name_first': user_dict.get('name_first'),
                'name_last': user_dict.get('name_last'),
                'profile_img_url': user_dict.get('profile_img_url')

            }
            users_list.append(return_dict)
    else:
        raise AccessError
    
    return {'users': users_list}

def admin_userpermission_change(token, u_id, permission_id):
    if not permission_id.isnumeric() or int(permission_id) not in permissions:
        raise InputError(f"permission_id {permission_id} does not refer to a valid permission.")

    user = seek_from_uid(u_id)
    if user == None:
        raise InputError("User with u_id is not valid")
   
    changer = seek_from_token(token)
       
    # according to spec,flockr users have 2 permission: 1 for owners, 2 for members
    if changer['permissions'] != 1:
        raise AccessError('The authorised user is not an owner')

    for user in auth.user_info:
        if auth.user_info[user]['u_id'] == u_id:
            auth.user_info[user]['permissions'] =  int(permission_id)
    
    return {}    

def search(token, query_str):
    found_list = []
    user = seek_from_token(token)
    if user == None:
        raise AccessError
    
    for single_channel in channels.channels_dict:
        member_list = channels.channels_dict[single_channel]['members']['all_members']
       
        for member in member_list:
            if member['u_id'] == user.get('u_id'):
                messages = channel.channel_messages(token, channels.channels_dict[single_channel]['channel_id'], 0)
                for single_message in messages['messages']:
                    if query_str in single_message['message']:
                        found_list.append(single_message)
    

    return {'messages': found_list}
