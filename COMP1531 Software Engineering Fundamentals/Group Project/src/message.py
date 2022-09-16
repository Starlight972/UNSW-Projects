from error import InputError, AccessError
import channel
from datetime import datetime
import message_data
import time
from pytz import timezone as tz

num_message = 0
mess_count = 0

#=========help function=======
def change_timestamp():
    au_tz = tz('Australia/Sydney')
    loc_time = au_tz.localize(datetime.now())
    loc_time = time.mktime(loc_time.timetuple())

    return loc_time
'''
find if the message_id is existing, if exists return channel_id, if not return -1
'''
def message_exsits(message_id):
    for i in message_data.all_messages.keys():
        curr = message_data.all_messages.get(i)
        if curr.get('message_id') == int(message_id):
            return curr.get('channel_id')
    return -1

'''
if message is sent by that token, return True, otherwise return -1
'''
def check_message_sender(token, message_id):
    for i in message_data.all_messages.keys():
        curr = message_data.all_messages.get(i)
        if curr.get('message_id') == int(message_id):
            if curr.get('token') == token:
                return True
    return -1

'''
check if message_id is a valid message within a channel that the user has joined
'''
def user_and_message_in_same_channel(token, message_id):
    #check message is valid
    if message_exsits(message_id) != -1:
        channel_id = message_exsits(message_id)
        if channel.is_a_member(channel_id, token) == True:
            return True
        else:
            raise InputError('not a member in that channel')
    else:
        raise InputError('message id ' + str(message_id) + ' is not existing')

def is_react(token, message_id):
    '''Get the coresponding u_id of token'''
    user = channel.valid_user(token)
    uid = user.get('u_id')

    #find message info of message id
    for i in message_data.all_messages.keys():
        curr = message_data.all_messages.get(i)
        if curr.get('message_id') == int(message_id):
            break

    #find reacts info
    react_dic = curr.get('reacts')

    if uid == curr.get('u_id'):
        if react_dic['is_this_user_reacted'] == True:
            raise InputError('message has already reacted by message sender')
    else:
        react_ids = react_dic['u_ids']
        for u in react_ids:
            if u == uid:
                raise InputError('message has already reacted by that user')
    return uid

def is_unreact(token, message_id):
    '''Get the coresponding u_id of token'''
    user = channel.valid_user(token)
    uid = user.get('u_id')

    #find message info of message id
    for i in message_data.all_messages.keys():
        curr = message_data.all_messages.get(i)
        if curr.get('message_id') == int(message_id):
            break

    #find reacts info
    react_dic = curr.get('reacts')

    if uid == curr.get('u_id'):
        if react_dic['is_this_user_reacted'] == False:
            raise InputError('message has already unreacted by message sender')
    else:
        react_ids = react_dic['u_ids']
        for u in react_ids:
            if u == uid:
                return uid
        raise InputError('message has already unreacted by that user')        
    return uid
def is_pin(message_id):
    #find message info of message id
    for i in message_data.all_messages.keys():
        curr = message_data.all_messages.get(i)
        if curr.get('message_id') == int(message_id):
            break
    
    if curr['is_pinned'] == True:
        raise InputError('message has already pinned')
    else:
        return True

def is_unpin(message_id):
    #find message info of message id
    for i in message_data.all_messages.keys():
        curr = message_data.all_messages.get(i)
        if curr.get('message_id') == int(message_id):
            break
    
    if curr['is_pinned'] == False:
        raise InputError('message has already unpinned')
    else:
        return True
#=========================
def message_send(token, channel_id, message):
    #Input error - check if message is more than 1000 characters
    if len(message) > 1000:
        raise InputError('messages are too long')
    
    #check invalid channel id
    channel.is_a_valid_channel(int(channel_id))
    
    #Access Error - assert authorised is a member of the channel
    if not channel.is_a_member(int(channel_id), token):
        raise AccessError(token + 'is not a member in channel' + str(channel_id))

    time = change_timestamp()
    global mess_count
    mess_count += 1
    global num_message
    num_message += 1
    new_message = {
        'token': token,
        'message_id': mess_count,
        'message': message,
        'time_created': time,
        'channel_id': int(channel_id),
        'u_id': channel.valid_user(token)['u_id'],
        'reacts': {
            'react_id': 0,
            'u_ids': [],
            'is_this_user_reacted': False
        },
        #assume False represents not pinned, True represents pinned
        'is_pinned': False
    }

    message_name = 'message_' + str(mess_count)
    message_data.all_messages[message_name] = new_message
    return {'message_id': new_message['message_id'],}

def message_remove(token, message_id):
    #Input Error
    #Message (based on ID) no longer exists
    if message_exsits(message_id) == -1:
        raise InputError('message id ' + str(message_id) + ' is not existing')

    #Assert token is a valid user
    channel.valid_user(token)
    
    '''
    test Message with message_id was not sent by the authorised user making this request and 
    also not the owner of that channel
    '''
    channel_id = message_exsits(message_id)
    sender = check_message_sender(token, message_id) 
    owner = channel.is_an_owner(token, channel_id)
    if sender == -1 and not owner:
        raise AccessError('user is neither an owner nor the message sender')

    #remove that message from message_data.all_messages
    for i in message_data.all_messages.keys():
        curr = message_data.all_messages.get(i)
        if curr.get('message_id') == message_id:
            del message_data.all_messages[i]
            break
    global num_message
    num_message = num_message - 1
    return {
    }

def message_edit(token, message_id, message):
    #Input Error
    #test invalid token
    channel.valid_user(token)
    
    #check if message is more than 1000 characters
    if len(message) > 1000:
        raise InputError('messages are too long')

    #Access Error
    '''
    test Message with message_id was not sent by the authorised user making this request and 
    also not the owner of that channel
    '''
    channel_id = message_exsits(message_id)
    sender = check_message_sender(token, message_id) 
    owner = channel.is_an_owner(token, channel_id)
    if sender == -1 and not owner:
        raise AccessError('user is neither an owner nor the message sender')
    
    #if message is empty, just remove that message
    if len(message) == 0:
        message_remove(token, message_id)
    time = change_timestamp()
    temp_id = channel.valid_user(token)['u_id']
    for i in message_data.all_messages.keys():
        curr = message_data.all_messages.get(i)
        if curr.get('message_id') == message_id:
            curr['message'] = message
            curr['u_id'] = temp_id
            curr['time_created'] = time
            break

    return {}

def message_sendlater(token, channel_id, message, time_sent):
    #Input Error
    #check Channel ID is not a valid channel
    channel.is_a_valid_channel(int(channel_id))

    #check Message is more than 1000 characters
    if len(message) > 1000:
        raise InputError('messages are too long')
    
    #check Time sent is a time in the past
    time_now = change_timestamp()
    if time_now > time_sent:
        raise InputError('can not set the sending time before now')

    #Access Error
    #check the authorised user has not joined the channel they are trying to post to
    if not channel.is_a_member(int(channel_id), token):
        raise AccessError(token + 'is not a member in channel' + str(channel_id))
    
    sec = time_sent - time_now
    time.sleep(sec)
    return message_send(token, channel_id, message)
    

def message_react(token, message_id, react_id):
    #Input Error
    #check message_id is not a valid message within a channel that the authorised user has joined
    user_and_message_in_same_channel(token, message_id)

    #check react_id is not a valid React ID.
    if react_id != 1:
        raise InputError('Invalid react id')
    
    #check Message with ID message_id already contains an active React with ID react_id from the authorised user
    uid = is_react(token, message_id)

    #find message info of message id
    for i in message_data.all_messages.keys():
        curr_mess = message_data.all_messages.get(i)
        if curr_mess.get('message_id') == int(message_id):
            break

    #find reacts info
    react_dic = curr_mess.get('reacts')
    react_dic['react_id'] = 1
    if uid == curr_mess.get('u_id'):
        react_dic['is_this_user_reacted'] = True
    else:
        react_dic['u_ids'].append(uid)

    return {}

def message_unreact(token, message_id, react_id):
    #Input Error
    #check message_id is not a valid message within a channel that the authorised user has joined
    user_and_message_in_same_channel(token, message_id)

    #check react_id is not a valid React ID.
    if react_id != 1:
        raise InputError('Invalid react id')

    #check Message with ID message_id already contains an active React with ID react_id from the authorised user
    uid = is_unreact(token, message_id)

    #find message info of message id
    for i in message_data.all_messages.keys():
        curr_mess = message_data.all_messages.get(i)
        if curr_mess.get('message_id') == int(message_id):
            break
    
    #find reacts info
    react_dic = curr_mess.get('reacts')
    react_dic['react_id'] = 1    

    if uid == curr_mess.get('u_id'):
        react_dic['is_this_user_reacted'] = False
    else:
        react_ids = react_dic.get('u_ids')
        for i in range(len(react_ids)):
            if react_ids[i] == int(uid):
                del react_ids[i]

    return {}

def message_pin(token, message_id):
    #Input Error
    #check message_id is not a valid message
    if message_exsits(message_id) == -1:
        raise InputError('message id ' + str(message_id) + ' is not existing')
    
    #check Message with ID message_id is already pinned
    is_pin(message_id)

    #Access Error
    #check The authorised user is not a member of the channel that the message is within
    channel_id = message_exsits(message_id)
    if channel.is_a_member(channel_id, token) == False:
        raise AccessError('not a member in that channel')

    #check The authorised user is not an owner
    if channel.is_an_owner(token, channel_id) == False:
        raise AccessError('not an owner in that channel')

    #find message info of message id
    for i in message_data.all_messages.keys():
        curr_mess = message_data.all_messages.get(i)
        if curr_mess.get('message_id') == int(message_id):
            break

    curr_mess['is_pinned'] = True
    return {}

def message_unpin(token, message_id):
    #Input Error
    #check message_id is not a valid message
    if message_exsits(message_id) == -1:
        raise InputError('message id ' + str(message_id) + ' is not existing')
    
    #check Message with ID message_id is already unpinned
    is_unpin(message_id)

    #Access Error
    #check The authorised user is not a member of the channel that the message is within
    channel_id = message_exsits(message_id)
    if channel.is_a_member(channel_id, token) == False:
        raise AccessError('not a member in that channel')

    #check The authorised user is not an owner
    if channel.is_an_owner(token, channel_id) == False:
        raise AccessError('not an owner in that channel')

    #find message info of message id
    for i in message_data.all_messages.keys():
        curr_mess = message_data.all_messages.get(i)
        if curr_mess.get('message_id') == int(message_id):
            break

    curr_mess['is_pinned'] = False

    return {}

