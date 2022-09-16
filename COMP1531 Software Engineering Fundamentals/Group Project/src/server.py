import sys
from json import dumps
from flask import Flask, request, send_from_directory
from flask_cors import CORS
from error import InputError
from auth import auth_login, auth_logout, auth_register, auth_passwordreset_request, auth_passwordreset_reset
from channels import channels_list, channels_listall, channels_create
from channel import channel_invite, channel_details, channel_messages, channel_addowner, channel_removeowner, channel_join, channel_leave
import message 
import other
from user import user_profile, user_profile_setname, user_profile_setemail,user_profile_sethandle, user_profile_uploadphoto
import requests
import os
import standup


def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__, static_url_path='/static/', static_folder='static')
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
   	    raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })

# auth falsk
@APP.route("/auth/login", methods=['POST'])
def login_flask():
    info = request.get_json()
    return dumps(auth_login(info['email'], info['password']))

@APP.route("/auth/logout", methods=['POST'])
def logout_flask():
    info = request.get_json()
    return dumps(auth_logout(info['token']))

@APP.route("/auth/register", methods=['POST'])
def register_flask():
    info = request.get_json()
    return dumps(auth_register(info['email'], info['password'], info['name_first'], info['name_last']))

@APP.route("/auth/passwordreset/request", methods=['POST'])
def reset_request_flask():
    info = request.get_json()
    return dumps(auth_passwordreset_request(info['email']))

@APP.route("/auth/passwordreset/reset", methods=['POST'])
def reset_flask():
    info = request.get_json()
    return dumps(auth_passwordreset_reset(info['reset_code'], info['new_password']))

# channel flask
@APP.route("/channel/invite", methods=['POST'])
def invite_flask():
    info = request.get_json()
    return dumps(channel_invite(info['token'], info['channel_id'], info['u_id']))

@APP.route("/channel/details", methods=['GET'])
def details_flask():
    return dumps(channel_details(request.args.get('token'), request.args.get('channel_id')))

@APP.route("/channel/messages", methods=['GET'])
def messages_flask():
    return dumps(channel_messages(request.args.get('token'), request.args.get('channel_id'), request.args.get('start')))

@APP.route("/channel/addowner", methods=['POST'])
def addowner_flask():
    info = request.get_json()
    return dumps(channel_addowner(info['token'], info['channel_id'], info['u_id']))

@APP.route("/channel/removeowner", methods=['POST'])
def removeowner_flask():
    info = request.get_json()
    return dumps(channel_removeowner(info['token'], info['channel_id'], info['u_id']))

@APP.route("/channel/leave", methods=['POST'])
def leave_flask():
    info = request.get_json()
    return dumps(channel_leave(info['token'], info['channel_id']))

@APP.route("/channel/join", methods=['POST'])
def join_flask():
    info = request.get_json()
    return dumps(channel_join(info['token'], info['channel_id']))

# message flask
@APP.route("/message/send", methods=['POST'])
def send_flask():
    info = request.get_json()
    return dumps(message.message_send(info['token'], info['channel_id'], info['message']))

@APP.route("/message/remove", methods=['DELETE'])
def remove_flask():
    info = request.get_json()
    return dumps(message.message_remove(info['token'], info['message_id']))

@APP.route("/message/edit", methods=['PUT'])
def edit_flask():
    info = request.get_json()
    return dumps(message.message_edit(info['token'], info['message_id'], info['message']))

@APP.route("/message/sendlater", methods=['POST'])
def sendlater_flask():
    info = request.get_json()
    return dumps(message.message_sendlater(info['token'], info['channel_id'], info['message'], info['time_sent']))

@APP.route("/message/react", methods=['POST'])
def react_flask():
    info = request.get_json()
    return dumps(message.message_react(info['token'], info['message_id'], info['react_id']))

@APP.route("/message/unreact", methods=['POST'])
def unreact_flask():
    info = request.get_json()
    return dumps(message.message_unreact(info['token'], info['message_id'], info['react_id']))

@APP.route("/message/pin", methods=['POST'])
def pin_flask():
    info = request.get_json()
    return dumps(message.message_pin(info['token'], info['message_id']))

@APP.route("/message/unpin", methods=['POST'])
def unpin_flask():
    info = request.get_json()
    return dumps(message.message_unpin(info['token'], info['message_id']))

# channels flask
@APP.route("/channels/list", methods=['GET'])
def list_flask():
    return dumps(channels_list(request.args.get('token')))

@APP.route("/channels/listall", methods=['GET'])
def listall_flask():
    return dumps(channels_listall(request.args.get('token')))
    
@APP.route("/channels/create", methods=['POST'])
def create_flask():
    info = request.get_json()
    return dumps(channels_create(info['token'], info['name'], info['is_public']))

# user falsk
@APP.route("/user/profile", methods=['GET'])
def profile_flask():
    return dumps(user_profile(request.args.get('token'), request.args.get('u_id')))

@APP.route("/user/profile/setname", methods=['PUT'])
def setname_flask():
    info = request.get_json()
    return dumps(user_profile_setname(info['token'], info['name_first'], info['name_last']))

@APP.route("/user/profile/setemail", methods=['PUT'])
def setemail_flask():
    info = request.get_json()
    return dumps(user_profile_setemail(info['token'], info['email']))

@APP.route("/user/profile/sethandle", methods=['PUT'])
def sethandle_flask():
    info = request.get_json()
    return dumps(user_profile_sethandle(info['token'], info['handle_str']))

@APP.route("/user/profile/uploadphoto", methods=['POST'])
def upload_flask():
    info = request.get_json()
    return dumps(user_profile_uploadphoto(info['token'], info['img_url'], info['x_start'], info['y_start'], info['x_end'], info['y_end']))

@APP.route('/static/<path:path>')
def send_js(path):
    if (os.path.splitext(path)[-1][1:] != "jpg"):
        raise InputError("Image uploaded is not a JPG")
    else:
         return send_from_directory('', path)

@APP.route("/users/all", methods = ['GET'])
def usersall_flask():
    return dumps(other.users_all(request.args.get('token')))

@APP.route("/admin/userpermission/change", methods = ['POST'])
def permissionchange_flask():
    info = request.get_json()
    return dumps(other.admin_userpermission_change(info['token'], info['u_id'], info['permission_id']))

@APP.route("/standup/start", methods = ['POST'])
def standup_start_flask():
    info = request.get_json()
    return dumps(standup.standup_start(info['token'], info['channel_id'], info['length']))

@APP.route("/standup/active", methods = ['GET'])
def standup_active_flask():
    return dumps(standup.standup_active(request.args.get('token'), request.args.get('channel_id')))

@APP.route("/standup/send", methods = ['POST'])
def standup_send_flask():
    info = request.get_json()
    return dumps(standup.standup_send(info['token'], info['channel_id'], info['message']))

@APP.route("/search", methods = ['GET'])
def search_flask():
    return dumps(other.search(request.args.get('token'), request.args.get('query_str')))

@APP.route("/clear", methods = ['DELETE'])
def clear_flask():
    return dumps(other.clear())

if __name__ == "__main__":
    APP.run(port=0) # Do not edit this port
