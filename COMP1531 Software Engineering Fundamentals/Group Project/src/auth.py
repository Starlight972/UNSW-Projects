from error import InputError, AccessError 
import re
import random
import hashlib
import jwt 
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SECRET = 'ICECREAM'

user_info = {}
num_users = 0
handles_list = []
active_reset_codes = []
letters_digits = 'abcdefghijklmnopqrstuvwqyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'

#Check for a valid email (used provided source in spec for code)
def check_email_syntax(email):
    regex = r"^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
    if re.search(regex, email):
        pass
    else:
        raise InputError("Invalid email entered")

#Assert the given email is registered
def check_email_registered(email):
    for user in user_info.keys():
        if user_info[user].get('email') == email:
            return user_info[user]
    return False   

#Check the password is valid length
def check_pass_len(password):
    if (len(password) < 6):
        raise InputError("Password is too short")

#Assert login credentials are valid
def check_correct_login(email, password):
    #Assert email is registered
    user = check_email_registered(email)

    if not user:
        raise InputError("Email is not registered")

    #If passwords don't match, raise access error
    if user.get('password') != hashlib.sha256(password.encode()).hexdigest():
        raise InputError("Incorrect Password")
    
    #Check if already logged in
    elif user.get('token') != "0":
        raise InputError("Already logged in")
    
    #If not above, login credentials are valid
    else:
        return user

#Generate a unique token
def generate_token(email):
    return jwt.encode({'email': email}, SECRET, algorithm='HS256').decode('utf-8')

#Generate a reset password request code that is 40 characters
def reset_code_gen(email):
    result = ''
    max_len = 40
    i = 0

    while (i < max_len):
        result += random.choice(letters_digits)
        i += 1
    
    new_code = {
        'email': email,
        'code': result
    }
   
    active_reset_codes.append(new_code)
    
    return result

#Generate unique handle
def generate_handle(name_first, name_last):
    if len(str(name_first) + str(name_last)) <= 20:
        handle = name_first + name_last
    else:
        handle = str(name_first + name_last)[0:20]

    #If handle already exists, generate a random number to append to it
    global handles_list
    while handle in handles_list:
        handle = handle[0:16]
        handle = handle + str(random.randint(0, 1000))

    #Once unique, appennd to handles_list and return
    handles_list.append(handle)
    return handle

#Login a user given email and password
def auth_login(email, password):
    #Check email and password are correct and user is not logged in
    user = check_correct_login(email, password)
    
    #Generate a unique token based on their email
    user['token'] = generate_token(email)

    return {
        'u_id': user.get('u_id'),
        'token': user.get('token')
    }

#Logout a user by setting token to 0
def auth_logout(token):
    for user in user_info.keys():
        if user_info[user].get('token') == token:
            user_info[user]['token'] = "0"
            return {
                'is_success': True,
            }

    raise AccessError("Token not logged in")

#Register a new user
def auth_register(email, password, name_first, name_last):
    #Check email entered is valid
    check_email_syntax(email)

    #Check email is not already used by another user
    if check_email_registered(email):
        raise InputError (f"The email {email} is already a user")

    #Assert password is not too short
    check_pass_len(password)
    
    #Generate a unique handle for the user
    handle = generate_handle(name_first, name_last)
    
    #get key name for user_info and add new data
    global num_users
    num_users += 1
    username = "user_" + str(num_users)

    #Set permission of user to member or owner depending on the number of owners
    permission = 2 if num_users > 1 else 1
    
    #add known data to temp dictionary and apped to user_info
    new_user = {
        'email': email,
        'name_first': name_first,
        'name_last': name_last,
        'handle': handle,
        'password': hashlib.sha256(password.encode()).hexdigest(),
        'permissions': permission,
        'u_id': num_users,
        'token': "0"
    }
    user_info[username] = new_user

    #Log the user in and return u_id and token
    return auth_login(email, password)

#Send an email to the user with a code so they can reset their password
#Used youtube https://www.youtube.com/watch?v=YPiHBtddefI&t=107s for source code
def auth_passwordreset_request(email):
    #Assert email is a registered user
    if not check_email_registered(email):
        raise InputError('Email is not registered')
    
    #Set up some variables
    from_email = 'exmptmp@gmail.com'
    password = '1234ABcd'
    message = 'Your code is ' + reset_code_gen(email)

    #Use the MIMEMultipart function to get email components like To, From, Subject
    mail = MIMEMultipart()
    mail['From'] = from_email
    mail['To'] = email
    mail['Subject'] =  'Reset your password'

    #Attach the message as a plain text message to the mail you're sending
    mail.attach(MIMEText(message, 'plain'))

    #Authorise the gmail server to send emails via the temp email (exmptmp@gmail.com)
    #Done by providing crdentials to the server  followed by the details of the mail you're sending
    #Close the server once mail sent and return {} to indicate success
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, password)
    server.sendmail(from_email, email, mail.as_string())
    server.quit()

    return {}

#Change a user's password if they enter a valid code
def auth_passwordreset_reset(reset_code, new_password):
    #Assert password is not too short
    check_pass_len(new_password)
    
    #Check the code exists, and if so reset the user password
    for code in active_reset_codes:
        if code.get('code') == reset_code:
            user = check_email_registered(code.get('email'))
            user['password'] = hashlib.sha256(new_password.encode()).hexdigest()
            active_reset_codes.remove(code)
            return {}
    
    raise InputError("Reset code is not a valid code")
