# -*- coding: utf-8 -*-
from vial import render_template
from auto_login import auto_login
from datetime import datetime
import datetime as dt
import pymysql
import bcrypt


def signin(headers, body, data):
    login = str(data['login']) if 'login' in data else ''
    password = str(data['password']) if 'password' in data else ''
    if (login == '') or (password == ''):
        return render_template('signin.html', body=body, data=data, headers=headers), 200, {}
    elif allow_signin(login, headers):
        if authentication(login, password):
            add_log(headers, data, True)
            return render_template('signin.html', body=body, data=data, headers=headers,
                                   message='Pooprawne dane'), 200, {}
        add_log(headers, data, False)
        return render_template('signin.html', body=body, data=data, headers=headers,
                               message='Niepoprawne dane'), 200, {}
    add_log(headers, data, False)
    return render_template('signin.html', body=body, data=data, headers=headers, message='Ban na IP'), 200, {}


def allow_signin(login, headers):
    ip = str(headers['http-x-forwarded-for']) if 'http-x-forwarded-for' in headers else 'PROXY'
    conn = pymysql.connect(
        db=auto_login('db_db'),
        user=auto_login('db_user'),
        passwd=auto_login('db_passwd'),
        host=auto_login('db_host'))
    cursor = conn.cursor()
    cursor.execute("SELECT success, time FROM logs WHERE ip=%s AND login=%s ORDER BY time DESC LIMIT 10;", (ip, login))
    cursor_length = 0
    last_login = ''
    for result in cursor:
        cursor_length = cursor_length + 1
        if str(result)[1] == '1':
            return True
        if cursor_length == 1:
            last_login = str(result)
    if cursor_length < 10:
        return True

    last_login = last_login.replace('(0, datetime.datetime(', '')
    last_login = last_login.replace('))', '')
    last_login = last_login.replace(',', '')
    allow_after = datetime.strptime(last_login, "%Y %m %d %H %M %S") + dt.timedelta(minutes=15)
    if dt.datetime.now() > allow_after:
        return True
    return False


def add_log(headers, data, success=False):
    login = str(data['login']) if 'login' in data else '-'
    ip = str(headers['http-x-forwarded-for']) if 'http-x-forwarded-for' in headers else 'PROXY'
    date_time = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = pymysql.connect(
        db=auto_login('db_db'),
        user=auto_login('db_user'),
        passwd=auto_login('db_passwd'),
        host=auto_login('db_host'))
    cursor = conn.cursor()
    if success:
        cursor.execute("INSERT INTO logs VALUES (%s, %s, TRUE, %s);", (login, ip, date_time))
    else:
        cursor.execute("INSERT INTO logs VALUES (%s, %s, FALSE, %s);", (login, ip, date_time))
    conn.commit()


def authentication(login, password):
    conn = pymysql.connect(
        db=auto_login('db_db'),
        user=auto_login('db_user'),
        passwd=auto_login('db_passwd'),
        host=auto_login('db_host'))
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM userdata WHERE login=%s;", (login,))
    dbhash = cursor.fetchone()

    if dbhash is None:
        for i in range(3):
            bcrypt.hashpw('wrong data delay', bcrypt.gensalt())
        return False
    dbhash = str(dbhash)[2:62]
    salt = dbhash[0:29]
    hash = password

    for i in range(3):
        hash = bcrypt.hashpw(hash, salt)

    if hash == dbhash:
        return True
    return False
