import time
import threading
import other
import channel
import message
import channels
from error import AccessError, InputError
import datetime

standup_mess = []

def standup_start(token, channel_id, length):
    #Check token and channel id are valid
    other.seek_from_token(token)
    this_channel = channel.is_a_valid_channel(channel_id)

    #Check token is a member
    if not channel.is_a_member(channel_id, token):
        raise AccessError('user is not a member of this channel')
    
    #Assert there is not already a standup
    if standup_active(token, channel_id)['is_active']:
        raise InputError("An avtive standup is currently running in this channel")

    #Use datetime to calculate time now + length, assign to standup property in dict
    time_finish = message.change_timestamp() + int(length)
    this_channel['standup'] = time_finish
    
    t = threading.Timer(length, send_final, args=(standup_mess, token, channel_id))
    t.start()

    return{
        'time_finish': time_finish
    }

def standup_active(token, channel_id):
    #Assert user and channel are valid, and token is a member
    other.seek_from_token(token)
    this_channel = channel.is_a_valid_channel(channel_id)
    if not channel.is_a_member(channel_id, token):
        raise AccessError('user is not a member of this channel')  

    #Check status of the standup and return accordingly
    is_active = False if this_channel.get('standup') == 0 else True
    time_finish = None if this_channel.get('standup') == 0 else this_channel.get('standup')
    
    return{
        'is_active': is_active,
        'time_finish': time_finish
    }

def standup_send(token, channel_id, message):
    #Assert user and channel are valid, get user handle
    this_channel = channel.is_a_valid_channel(channel_id)
    user = other.seek_from_token(token)
    handle = user.get('handle')

    #Assert token is a member of the channel
    if not channel.is_a_member(channel_id, token):
        raise AccessError('user is not a member of this channel')
 
    #If there is no active standup, raise Input Error
    if this_channel.get('standup') == 0:
        raise InputError("There is currently no standup")

    standup_mess.append(f"{handle}: {message}\n")
    #it should be sth like this?or we basically do some append things like channels_dict[channel_id]['message_queue'].append(message)
    #this_channel['standup_message'] += f'{handle}: {message}\n'

    print(this_channel.get('standup_message'))
    return {}

def send_final(standup_mess, token, channel_id):
    final_msg = ''
    for msg in standup_mess:
        final_msg += msg

    message.message_send(token, channel_id, final_msg)
