# -*- coding: utf-8 -*-
import binascii
import os
import uuid
import sqlite3

from auto_login import auto_login
from vial import render_template
import math
import bcrypt
from redirect import redirect
from cookie import tk_pass


def change(headers, body, data, token=''):
    cookie = str(headers['http-cookie']).replace('sessionid=', '')
    current = str(data['current']) if 'current' in data else ''
    password1 = str(data['password1']) if 'password1' in data else ''
    password2 = str(data['password2']) if 'password2' in data else ''
    if token == '':
        token = str(data['token']) if 'token' in data else ''
    db_password = tk_pass(token, cookie)
    if current == '' or password1 == '' or password2 == '':
        return render_template('templates/change.html', body=body, data=data, token=token), 200, {}
    elif db_password == '':
        return redirect(headers=headers, body=body, data=data, message='Unauthorized password change request')
    salt = db_password[0:29]
    for i in range(3):
        current = bcrypt.hashpw(current, salt)

    if current != db_password:
        return render_template('templates/change.html', body=body, data=data, token=token, message='Current password is incorrect'), 200, {}
    elif password1 != password2:
        return render_template('templates/change.html', body=body, data=data, token=token, message='Passwords must be identical'), 200, {}
    elif not pass_correct_length(password1):
        return render_template('templates/change.html', body=body, data=data,  token=token, message='New password length should be 6-24 characters'), 200, {}
    elif pass_entropy(password1) < 50.0:
        return render_template('templates/change.html', body=body, data=data, token=token, message='New password is too simple. Entropy: ' + str(round(pass_entropy(password1), 2))), 200, {}
    salt = bcrypt.gensalt()
    for i in range(3):
        password1 = bcrypt.hashpw(password1, salt)
    new_token = str(uuid.UUID(hex=binascii.b2a_hex(os.urandom(16))))

    conn = sqlite3.connect(auto_login('db_file'))
    cursor = conn.cursor()

    cursor.execute("UPDATE users SET password=?, token=? WHERE token=?;", (password1, new_token, token))
    conn.commit()
    return redirect(headers=headers, body=body, data=data, message='Password has been successfully changed')


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
