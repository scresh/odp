# -*- coding: utf-8 -*-
import binascii
import os

from redirect import redirect
from vial import render_template
from cookie import user_cookie, update_cookie
from auto_login import auto_login
from datetime import datetime
import datetime as dt
import sqlite3
import bcrypt
import uuid


def signin(headers, body, data):
    login = str(data['login']) if 'login' in data else ''
    password = str(data['password']) if 'password' in data else ''
    cookie = str(headers['http-cookie']).replace('sessionid=', '')
    if (login == '') or (password == ''):
        if user_cookie(cookie) != '':
            return redirect(headers=headers, body=body, data=data, message='You are arleady signed in')
        return render_template('templates/signin.html', body=body, data=data, headers=headers), 200, {}
    elif allow_signin(login, headers):
        if authentication(login, password):
            cookie = str(uuid.UUID(hex=binascii.b2a_hex(os.urandom(16))))
            expires = (dt.datetime.utcnow() + dt.timedelta(days=1))
            update_cookie(cookie, expires, login)
            expires = expires.strftime("%a, %d %b %Y %H:%M:%S GMT")
            cookie = 'sessionid=' + cookie + '; expires=' + expires + "; secure"
            add_log(headers, data, True)
            return render_template('templates/redirect.html', body=body, data=data, headers=headers,
                                   message='Successfully signed in'), 200, {'Set-Cookie': cookie}
        add_log(headers, data, False)
        return render_template('templates/signin.html', body=body, data=data, headers=headers,
                               message='Invalid Login Credentials'), 200, {}
    add_log(headers, data, False)
    return render_template('templates/signin.html', body=body, data=data, headers=headers, message='Too many login failures from your newtwork'), 200, {}


def allow_signin(login, headers):
    ip = str(headers['http-x-forwarded-for']) if 'http-x-forwarded-for' in headers else 'PROXY'
    conn = sqlite3.connect(auto_login('db_file'))
    cursor = conn.cursor()
    cursor.execute("SELECT success, time FROM logs WHERE ip=? AND login=? ORDER BY time DESC LIMIT 10;", (ip, login))
    cursor_length = 0
    last_login = ''
    for result in cursor.fetchall():
        cursor_length += 1
        if str(result[0]) == '1':
            return True
        if cursor_length == 1:
            last_login = str(result[1])
    if cursor_length < 10:
        return True

    allow_after = datetime.strptime(last_login, "%Y-%m-%d %H:%M:%S") + dt.timedelta(minutes=15)
    if dt.datetime.now() > allow_after:
        return True
    return False


def add_log(headers, data, success=False):
    login = str(data['login']) if 'login' in data else '-'
    ip = str(headers['http-x-forwarded-for']) if 'http-x-forwarded-for' in headers else 'PROXY'
    date_time = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect(auto_login('db_file'))
    cursor = conn.cursor()
    if success:
        cursor.execute("INSERT INTO logs VALUES (?, ?, 1, ?);", (login, ip, date_time))
    else:
        cursor.execute("INSERT INTO logs VALUES (?, ?, 0, ?);", (login, ip, date_time))
    conn.commit()


def authentication(login, password):
    conn = sqlite3.connect(auto_login('db_file'))
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE login=?;", (login,))
    dbhash = cursor.fetchone()

    if dbhash is None:
        dbhash = '$2b$12$c/d7ZeuRgBPXvlktF7OH3uUF3DQFyq5FJnqmzbvKWMA6Et.e7Knrm'
        salt = dbhash[0:29]
        hash = password
        for i in range(3):
            hash = bcrypt.hashpw(hash, salt)
        return False

    dbhash = str(dbhash[0])
    salt = dbhash[0:29]
    hash = password

    for i in range(3):
        hash = bcrypt.hashpw(hash, salt)

    if hash == dbhash:
        return True
    return False
