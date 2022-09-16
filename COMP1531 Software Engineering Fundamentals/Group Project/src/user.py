from error import InputError, AccessError
import auth
import re
import channel
import other
import requests
from PIL import Image
import urllib.request

def check(email):
    # Make a regular expression
    # for validating an Email
    regex = r"^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
    # pass the regular expression
    # and the string in search() method
    if(re.search(regex,email)):
        pass
    else:
        raise InputError("Email entered is not a valid email")
        
    
def user_profile(token, u_id):
    ''' check the given token whether or not is valid '''
    channel.valid_user(token)
    try:
        user = channel.valid_user(int(u_id))
    except AccessError:
        raise InputError

    return {
        'user': {
            'u_id': user.get('u_id'),
            'email': user.get('email'),
            'name_first': user.get('name_first'),
            'name_last': user.get('name_last'),
            'handle_str': user.get('handle'),
            'profile_img_url': user.get('profile_img_url')
        },
    }


def user_profile_setname(token, name_first, name_last):
    ''' check the given token whether or not is valid '''
    for user in auth.user_info.keys():
        user_dict = auth.user_info.get(user)
        if (user_dict['token'] == token):
            if (len(name_first) >= 1 and len(name_first) <= 50):
                user_dict['name_first'] = name_first
            else:
                raise InputError("name_first is not between 1 and 50 characters inclusively in length")
                
            if (len(name_last) >= 1 and len(name_last) <= 50):
                user_dict['name_last'] = name_last
            else:
                raise InputError("name_last is not between 1 and 50 characters inclusively in length")
    return {
    }

def user_profile_setemail(token, email):
    check(email)
    ''' check the given token whether or not is valid '''
    for user in auth.user_info.keys():
        user_dict = auth.user_info.get(user)
        if (user_dict['token'] == token):
            user_dict['email'] = email
        else:
            if (user_dict['email'] == email):
                raise InputError("Email address is already being used")
    return {
    }

def user_profile_sethandle(token, handle_str):
    if (len(handle_str) >= 3 and len(handle_str) <= 20):
        for user in auth.user_info.keys():
            user_dict = auth.user_info.get(user)
            if (user_dict['handle'] == handle_str and user_dict['token'] == token):
                continue
            elif (user_dict['handle'] == handle_str and user_dict['token'] != token):
                raise InputError("handle is already used")
            if (user_dict['handle'] != handle_str and user_dict['token'] == token):
                user_dict['handle'] = handle_str
    else:
        raise InputError("handle_str must be between 3 and 20 characters")
    return {
    }

def user_profile_uploadphoto(token, img_url, x_start, y_start, x_end, y_end):
    user = other.seek_from_token(token)
    img_name = 'static/user_' + str(user.get('u_id')) + 'profile.jpg'
    #check_status(url)
    urllib.request.urlretrieve(img_url, img_name)
    user['profile_img_url'] = img_name

    original = Image.open(user['profile_img_url'])

    width, height = original.size
    print(width, height)
    if (int(x_start) > width or int(y_start) < 0 or int(x_end) > original.size[0] or int(y_end) > original.size[1]):
        raise InputError("Any of x_start, y_start, x_end, y_end are not within the dimensions of the image")
    

    cropped = original.crop((int(x_start), int(y_start), int(x_end) + width, int(y_end) + width))
    cropped.save(user['profile_img_url'])

