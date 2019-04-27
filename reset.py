# -*- coding: utf-8 -*-
import binascii
import os
import uuid
from vial import render_template
from params import param_dict
import sqlite3
import math
import bcrypt
from redirect import redirect


def reset(headers, body, data, token=''):
    password = str(data['password']) if 'password' in data else ''
    if token == '':
        token = str(data['token']) if 'token' in data else ''

    if token == '':
        return render_template('templates/reset.html', body=body, data=data, token=token), 200, {}

    if password == '':
        return render_template('templates/reset.html', body=body, data=data,  token=token), 200, {}

    conn = sqlite3.connect(param_dict['db_file'])
    cursor = conn.cursor()
    cursor.execute("SELECT login FROM users WHERE token=?;", (token,))
    login = cursor.fetchone()

    if login is None:
        return render_template('templates/reset.html', body=body, data=data, message='Invalid token', token=token), 200, {}

    elif not pass_correct_length(password):
        return render_template('templates/reset.html', body=body, data=data, headers=headers,
                               message='Password length should be 6-24 characters', token=token), 200, {}
    elif pass_entropy(password) < 50.0:
        return render_template('templates/reset.html', body=body, data=data, headers=headers, token=token,
                               message='Password is too simple. Entropy: ' + str(round(pass_entropy(password), 2))), 200, {}
    salt = bcrypt.gensalt()
    for i in range(3):
        password = bcrypt.hashpw(password, salt)

    login = str(login[0])
    token = str(uuid.UUID(hex=binascii.b2a_hex(os.urandom(16))))

    cursor.execute("UPDATE users SET password=?, token=? WHERE login=?;", (password, token, login))
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
