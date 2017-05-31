# -*- coding: utf-8 -*-
from vial import render_template
from auto_login import auto_login
import math
import pymysql
import bcrypt


def signup(headers, body, data):
    login = str(data['login']) if 'login' in data else ''
    password = str(data['password']) if 'password' in data else ''
    email = str(data['email']) if 'email' in data else ''
    print '|' + login + '|' + password + '|' + email + '|'
    if (login == '') and (password == '') and (email == ''):
        return render_template('signup.html', body=body, data=data, headers=headers), 200, {}
    elif not login_correct_length(login):
        return render_template('signup.html', body=body, data=data, headers=headers,
                               message='Dlugosc loginu powinna liczyc od 3 do 16 znakow'), 200, {}
    elif not login_correct_chars(login):
        return render_template('signup.html', body=body, data=data, headers=headers,
                               message='Login zawiera nidozwolone znaki'), 200, {}
    elif not login_not_used(login):
        return render_template('signup.html', body=body, data=data, headers=headers,
                               message='Podany login jest juz zajety'), 200, {}
    elif not pass_correct_length(password):
        return render_template('signup.html', body=body, data=data, headers=headers,
                               message='Dlugosc hasla powinna liczyc od 6 do 24 znakow'), 200, {}
    elif not pass_good_entropy(password):
        return render_template('signup.html', body=body, data=data, headers=headers,
                               message='Haslo zbyt proste'), 200, {}
    elif not email_correct_format(email):
        return render_template('signup.html', body=body, data=data, headers=headers,
                               message='Niepoprwany adres email'), 200, {}
    elif not email_not_used(email):
        return render_template('signup.html', body=body, data=data, headers=headers,
                               message='Podany email jest juz zajety'), 200, {}
    add_user(login, password, email)
    return render_template('signup.html', body=body, data=data, headers=headers,
                           message='Poprawne dane'), 200, {}


def add_user(login, password, email):
    salt = bcrypt.gensalt()
    for i in range(3):
        password = bcrypt.hashpw(password, salt)
    conn = pymysql.connect(
        db=auto_login('db_db'),
        user=auto_login('db_user'),
        passwd=auto_login('db_passwd'),
        host=auto_login('db_host'))
    cursor = conn.cursor()
    cursor.execute("INSERT INTO userdata VALUES (%s, %s, %s);", (login, password, email))
    conn.commit()


def pass_good_entropy(password):
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
    if entropy > 50.0:
        return True
    return False


def pass_correct_length(password):
    if 6 <= len(password) <= 24:
        return True
    return False


def login_correct_chars(login):
    for c in login:
        if not (96 < ord(c) < 123) or (64 < ord(c) < 91) or (47 < ord(c) < 58):
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
    cursor.execute("SELECT login FROM userdata WHERE login=%s;", (login,))

    if cursor.fetchone() is None:
        return True
    return False


# To be continued...
def email_correct_format(email):
    if not 6 <= len(email) <= 30:
        return False
    elif email.count('@') != 1:
        return False
    elif email.count('.') == 0:
        return False
    return True


def email_not_used(email):
    conn = pymysql.connect(
        db=auto_login('db_db'),
        user=auto_login('db_user'),
        passwd=auto_login('db_passwd'),
        host=auto_login('db_host'))
    cursor = conn.cursor()
    cursor.execute("SELECT login FROM userdata WHERE email=%s;", (email,))

    if cursor.fetchone() is None:
        return True
    return False
