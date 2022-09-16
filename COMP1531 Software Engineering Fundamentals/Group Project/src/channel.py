from error import InputError, AccessError
import auth
import channels
import message_data

#===================help fuction=========================
#check whether a channel_id is a valid channel
#if is valid return the index value of that channel, otherwise return False
def is_a_valid_channel(channel_id):
    for channel in channels.channels_dict:
        if channels.channels_dict[channel]['channel_id'] == int(channel_id):
            return channels.channels_dict[channel]
           
    raise InputError(f"Channel id {channel_id} is not valid")

#check a channel is public
def is_channel_public(channel_id):
    this_channel = is_a_valid_channel(channel_id)
    if this_channel.get('is_public') == True:
        return True

    return False

#check whether a u_id is a valid user
#if is a valid user return index value of that user, otherwise return False
def valid_user(id):
    for user in auth.user_info:
        this_user = auth.user_info.get(user)
        if this_user.get('token') == id or this_user.get('u_id') == id:
            return this_user
      
    raise InputError(f"user {id} is not a valid user")

#is a member return True, otherwise return False
def is_a_member(channel_id, token):
    '''Get the u_id'''
    user = valid_user(token)
    
    this_channel = is_a_valid_channel(channel_id)
    if {'u_id': user.get('u_id')} in this_channel['members']['all_members']:
        return True
    
    return False

#check token is an owner of a channel
def is_an_owner(token,channel_id):
    '''Get the u_id'''
    user = valid_user(token)
    
    #Get corret channel and its members
    this_channel = is_a_valid_channel(channel_id)
    owners = this_channel['members'].get('owner')

    if {'u_id': user.get('u_id')} in owners:
        return owners       
    
    return False

#find and all messages sent in channel_id
def find_messages(channel_id):
    messages = []
    for curr_message in message_data.all_messages:
        if message_data.all_messages[curr_message].get('channel_id') == channel_id:
            messages.append(message_data.all_messages[curr_message])

    return messages

#Delete channel if removing last member
def delete_channel(channel_id):
    this_channel = is_a_valid_channel(channel_id)
    del this_channel

#For cases where there's only one owner/member left in the channel
def last_owner(channel_owners, channel_members, channel_id, owner_token):
    #if theres more members, append a member to be the owner
    '''Get the u_id'''
    user = valid_user(owner_token)
    
    if (len(channel_members) > 1):
        for member in channel_members:
            if member.get('u_id') != user.get('u_id'):
                channel_owners.append({'u_id': member.get('u_id')})
                break
    else:
        delete_channel(channel_id)   

#===========================================
def channel_invite(token, channel_id, u_id):
    #input erroe
    #check channel_id refers to a valid channel
    this_channel = is_a_valid_channel(channel_id)
    
    #check u_id refers to a valid user
    member = valid_user(int(u_id))
    valid_user(token)

    #access error - Assert authorised member is a member of the channel
    if not is_a_member(channel_id, token):
        raise AccessError(f"Token {token} is not a member in channel {channel_id}")

    #Assert u_id is already not a member in channel
    if is_a_member(channel_id, member['token']):
        raise AccessError(f"User {member['u_id']} is already a member in channel {channel_id}")

    #add member's token into channels_dic
    channel_members = this_channel['members'].get('all_members')
    channel_members.append({'u_id' : member.get('u_id')})

    return {}

def channel_details(token, channel_id):
    #input error - check Channel ID is a valid channel
    this_channel = is_a_valid_channel(channel_id)

    #access error - check Authorised user is a member of channel with channel_id
    if not is_a_member(channel_id, token):
        raise AccessError(f"Token {token} is not a member in channel {channel_id}")

    this_channel_owners = this_channel['members'].get('owner')
    this_channel_members = this_channel['members'].get('all_members')
        
    #intislize a details dictionary to return
    details = {
        'name': this_channel.get('name'),
        'owner_members': [],
        'all_members': []
    }
    
    #put owner_members into details
    for owner in this_channel_owners:
        curr_user = valid_user(int(owner.get('u_id'))) 
        details['owner_members'].append({'u_id': curr_user.get('u_id'), 'name_first': curr_user.get('name_first'), 'name_last': curr_user.get('name_last'), 'profile_img_url': curr_user.get('profile_img_url')})
    
    #put all_members into details
    for member in this_channel_members:
        curr_user =valid_user(int(member.get('u_id'))) 
        details['all_members'].append({'u_id': curr_user.get('u_id'), 'name_first': curr_user.get('name_first'), 'name_last': curr_user.get('name_last'), 'profile_img_url': curr_user.get('profile_img_url')})
    
    return details

def channel_messages(token, channel_id, start):
    #input error - check Channel ID is a valid channel
    this_channel = is_a_valid_channel(int(channel_id))
    
    #access error - assert Authorised user is a member of channel with channel_id
    if not is_a_member(int(channel_id), token):
        raise AccessError(f"{token} is not a member in channel {channel_id}")

    #Find messages in channel and add to channels_dict
    this_channel['message'] = find_messages(int(channel_id))
    num_messages = len(this_channel['message'])
    
    #check start is greater than the total number of messages in the channel
    if int(start) > num_messages:
        raise InputError(f"{start} is greater than the total numbers of messages {num_messages} in the channel {channel_id}")
    
    #put messages into return_message_dict
    message_list = this_channel['message']
    message_list.reverse()
    max_num_messages = 50
    
    #initiliaze messages and by default, assume there are greater then 50 messages
    return_message_dict = {
        'messages': [],
        'start':int(start),
        'end': int(start) + max_num_messages,
    }
    
    #If there are less then 50 messages
    if int(start) + max_num_messages > num_messages:
        max_num_messages = num_messages - int(start)
        return_message_dict['end'] = -1
    
    for message in this_channel['message']:
        return_message_dict['messages'].append({'message_id': message.get('message_id'), 'u_id': message.get('u_id'), 'message': message.get('message'), 'time_created': message.get('time_created')})

    return return_message_dict

def channel_leave(token, channel_id):
    # check channel id is valid or not 
    this_channel = is_a_valid_channel(channel_id)
    user = valid_user(token)

    #check token is a valid user and in channel
    leaver = valid_user(token)
    if not is_a_member(channel_id, token):
        raise AccessError(f"{token} is not a member in channel {channel_id}")
    
    channel_owners = is_an_owner(token, channel_id)
    channel_members = this_channel['members'].get('all_members')
    
    #If leaver is not an owner    
    if not channel_owners:
        #delete the user in all_members list
        for member in channel_members:
            if member.get('u_id') == user.get('u_id'):
                channel_members.remove(member)
    
    #if leaver is the owner, pass in the owner details to remove_owner function
    else:
        channel_removeowner(leaver['token'], channel_id, leaver['u_id'])
        channel_members.remove({'u_id': leaver.get('u_id')})

        
    return {}

def channel_join(token, channel_id):
    #Assert token and channel_id are valid
    this_channel = is_a_valid_channel(channel_id)
    user = valid_user(token)

    # assert token is not already a member if the channel
    if is_a_member(channel_id, token):
        raise InputError(f"{token} is already a member in channel {channel_id}")

    # check the channel is public or not
    if not is_channel_public(channel_id):
        raise AccessError('Channel is not public')

    #Join channel
    this_channel['members']['all_members'].append({'u_id': user.get('u_id')})
    
    return {}

def channel_addowner(token, channel_id, u_id):
    #input error - check Channel ID is a valid channel
    this_channel = is_a_valid_channel(channel_id)

    #check u_id is a valid user
    to_add = valid_user(int(u_id))

    #Assert token is owner and u_id is not owner
    if not is_an_owner(token, channel_id):
        raise AccessError(f"{token} is not an owner in channel {channel_id}")
    
    if is_an_owner(to_add.get('token'), channel_id):
        raise InputError(f"{u_id} is already an owner of channel {channel_id}")
    
    #Add the u_id as owner
    this_channel['members']['owner'].append({'u_id': to_add.get('u_id')})
   
    return {}

def channel_removeowner(token, channel_id, u_id):
    #input error - check Channel ID is a valid channel
    this_channel = is_a_valid_channel(channel_id)
    token_remove = valid_user(int(u_id))
    
    channel_owners = is_an_owner(token, channel_id)
    channel_members = this_channel['members'].get('all_members')
    
    #Assert token and u_id are owners and u_id is a member
    if not channel_owners:
        raise AccessError(f"{token} is not an owner")
    
    if not is_a_member(channel_id, token_remove.get('u_id')):
        raise AccessError(f"{token_remove.get('u_id')} is not a member")

    if not is_an_owner(token_remove.get('u_id'), channel_id):
        raise AccessError(f"{token_remove.get('u_id')} is not an owner")
    
    #If removing last owner
    if len(channel_owners) == 1:
        last_owner(channel_owners, channel_members, channel_id, token)         
    
    #Remove the specified owner   
    for owner in channel_owners:
        if owner.get('u_id') == token_remove.get('u_id'):
            channel_owners.remove({'u_id': token_remove.get('u_id')})
   
    return {}