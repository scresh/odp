# -*- coding: utf-8 -*-
import uuid
import OpenSSL
from vial import render_template
from auto_login import auto_login
import pymysql
import math
import bcrypt
from redirect import redirect


def reset(headers, body, data, token=''):
    password = str(data['password']) if 'password' in data else ''
    if token == '':
        token = str(data['token']) if 'token' in data else ''

    if token == '':
        return render_template('html/reset.html', body=body, data=data, token=token), 200, {}

    if password == '':
        return render_template('html/reset.html', body=body, data=data,  token=token), 200, {}

    conn = pymysql.connect(
        db=auto_login('db_db'),
        user=auto_login('db_user'),
        passwd=auto_login('db_passwd'),
        host=auto_login('db_host'))
    cursor = conn.cursor()
    cursor.execute("SELECT login FROM users WHERE token=%s;", (token,))
    login = cursor.fetchone()

    if login is None:
        return render_template('html/reset.html', body=body, data=data, message='Invalid token', token=token), 200, {}

    elif not pass_correct_length(password):
        return render_template('html/reset.html', body=body, data=data, headers=headers,
                               message='Password length should be 6-24 characters', token=token), 200, {}
    elif pass_entropy(password) < 50.0:
        return render_template('html/reset.html', body=body, data=data, headers=headers, token=token,
                               message='Password is too simple. Entropy: ' + str(round(pass_entropy(password), 2))), 200, {}
    salt = bcrypt.gensalt()
    for i in range(3):
        password = bcrypt.hashpw(password, salt)

    login = str(login[0])
    token = str(uuid.UUID(bytes=OpenSSL.rand.bytes(16)).hex)

    cursor.execute("UPDATE users SET password=%s, token=%s WHERE login=%s;", (password, token, login))
    conn.commit()
    return redirect(headers=headers, body=body, data=data, message='Password has been successfully changed.')


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
