# -*- coding: utf-8 -*-
from vial import render_template
from auto_login import auto_login
import datetime as dt
import math
import pymysql
import bcrypt
import uuid
import OpenSSL
import os


def signup(headers, body, data):
    login = str(data['login']) if 'login' in data else ''
    password = str(data['password']) if 'password' in data else ''
    email = str(data['email']) if 'email' in data else ''
    if (login == '') and (password == '') and (email == ''):
        return render_template('templates/signup.html', body=body, data=data, headers=headers), 200, {}
    elif not login_correct_length(login):
        return render_template('templates/signup.html', body=body, data=data, headers=headers,
                               message='Username length should be 3-16 characters'), 200, {}
    elif not login_correct_chars(login):
        return render_template('templates/signup.html', body=body, data=data, headers=headers,
                               message='Username contains invalid characters'), 200, {}
    elif not login_not_used(login):
        return render_template('templates/signup.html', body=body, data=data, headers=headers,
                               message='Username is already in use'), 200, {}
    elif not pass_correct_length(password):
        return render_template('templates/signup.html', body=body, data=data, headers=headers,
                               message='Password length should be 6-24 characters'), 200, {}
    elif pass_entropy(password) < 50.0:
        return render_template('templates/signup.html', body=body, data=data, headers=headers,
                               message='Password is too simple. Entropy: ' + str(round(pass_entropy(password), 2))), 200, {}
    elif not email_correct_format(email):
        return render_template('templates/signup.html', body=body, data=data, headers=headers,
                               message='Email address is in an invalid format'), 200, {}
    elif not email_not_used(email):
        return render_template('templates/signup.html', body=body, data=data, headers=headers,
                               message='Email address is already in use'), 200, {}
    cookie = str(uuid.UUID(bytes=OpenSSL.rand.bytes(16)).hex)
    expires = (dt.datetime.utcnow() + dt.timedelta(days=1))
    token = str(uuid.UUID(bytes=OpenSSL.rand.bytes(16)).hex)
    add_user(login, password, email, cookie, expires.strftime("%Y-%m-%d %H:%M:%S"), token)
    expires = expires.strftime("%a, %d %b %Y %H:%M:%S GMT")
    cookie = 'sessionid=' + cookie + '; expires=' + expires + "; secure"
    return render_template('templates/redirect.html', body=body, data=data, headers=headers,
                           message='Successfully signed up'), 200, {'Set-Cookie': cookie}


def add_user(login, password, email, cookie, expires, token):
    salt = bcrypt.gensalt()
    for i in range(3):
        password = bcrypt.hashpw(password, salt)
    conn = pymysql.connect(
        db=auto_login('db_db'),
        user=auto_login('db_user'),
        passwd=auto_login('db_passwd'),
        host=auto_login('db_host'))
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users VALUES (%s, %s, %s, %s, %s, %s);", (login, password, email, cookie, expires, token))
    os.mkdir('uploads/'+login)
    conn.commit()


def pass_entropy(password):
    small = big = num = spec = 0
    for c in password:
        if 96 < ord(c) < 123:
            small = 1
        elif 64 < ord(c) < 91:
            big = 1
        elif 47 < ord(c) < 58:
            num = 1
        else:
            spec = 1
    alpha = small * 26 + big * 26 + num * 10 + spec * 66
    entropy = len(password) * math.log(alpha if alpha > 0 else 1, 2)
    return entropy


def pass_correct_length(password):
    if 6 <= len(password) <= 24:
        return True
    return False


def login_correct_chars(login):
    for c in login:
        if not ((96 < ord(c) < 123) or (64 < ord(c) < 91) or (47 < ord(c) < 58)):
            return False
    return True


def login_correct_length(login):
    if 3 <= len(login) <= 16:
        return True
    return False


def login_not_used(login):
    conn = pymysql.connect(
        db=auto_login('db_db'),
        user=auto_login('db_user'),
        passwd=auto_login('db_passwd'),
        host=auto_login('db_host'))
    cursor = conn.cursor()
    cursor.execute("SELECT login FROM users WHERE login=%s;", (login,))

    if cursor.fetchone() is None:
        return True
    return False


def email_correct_format(email):
    if not 6 <= len(email) <= 30:
        return False
    elif email.count('@') != 1 or not (0 < email.index('@') < (len(email) - 4)):
        return False
    elif email.count('.') == 0:
        return False
    for c in email:
        if not ((96 < ord(c) < 123) or (63 < ord(c) < 91) or (47 < ord(c) < 58) or ord(c) == 46):
            return False
    return True


def email_not_used(email):
    conn = pymysql.connect(
        db=auto_login('db_db'),
        user=auto_login('db_user'),
        passwd=auto_login('db_passwd'),
        host=auto_login('db_host'))
    cursor = conn.cursor()
    cursor.execute("SELECT login FROM users WHERE email=%s;", (email,))

    if cursor.fetchone() is None:
        return True
    return False
