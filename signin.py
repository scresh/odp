# -*- coding: utf-8 -*-
from redirect import redirect
from vial import render_template
from auto_login import auto_login
from datetime import datetime
import datetime as dt
import pymysql
import bcrypt
import uuid
import OpenSSL


def signin(headers, body, data):
    login = str(data['login']) if 'login' in data else ''
    password = str(data['password']) if 'password' in data else ''
    cookie = str(headers['http-cookie']).replace('sessionid=', '')
    if (login == '') or (password == ''):
        if whose_cookie(cookie) != '':
            return redirect(headers=headers, body=body, data=data, message='You are arleady signed in')
        return render_template('html/signin.html', body=body, data=data, headers=headers), 200, {}
    elif allow_signin(login, headers):
        if authentication(login, password):
            cookie = str(uuid.UUID(bytes=OpenSSL.rand.bytes(16)).hex)
            expires = (dt.datetime.utcnow() + dt.timedelta(days=1))
            update_cookie(cookie, expires, login)
            expires = expires.strftime("%a, %d %b %Y %H:%M:%S GMT")
            cookie = 'sessionid=' + cookie + '; expires=' + expires + "; secure"
            add_log(headers, data, True)
            return render_template('html/redirect.html', body=body, data=data, headers=headers,
                                   message='Successfully signed in'), 200, {'Set-Cookie': cookie}
        add_log(headers, data, False)
        return render_template('html/signin.html', body=body, data=data, headers=headers,
                               message='Niepoprawne dane'), 200, {}
    add_log(headers, data, False)
    return render_template('html/signin.html', body=body, data=data, headers=headers, message='Ban na IP'), 200, {}


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
    cursor.execute("SELECT password FROM users WHERE login=%s;", (login,))
    dbhash = cursor.fetchone()

    if dbhash is None:
        for i in range(3):
            bcrypt.hashpw('wrong data delay', bcrypt.gensalt())
        return False
    dbhash = str(dbhash[0])
    salt = dbhash[0:29]
    hash = password

    for i in range(3):
        hash = bcrypt.hashpw(hash, salt)

    if hash == dbhash:
        return True
    return False


def whose_cookie(cookie):
    if cookie == '':
        return ''
    conn = pymysql.connect(
        db=auto_login('db_db'),
        user=auto_login('db_user'),
        passwd=auto_login('db_passwd'),
        host=auto_login('db_host'))
    cursor = conn.cursor()
    cursor.execute("SELECT login, expires FROM users WHERE cookie=%s;", (cookie,))
    data = cursor.fetchone()

    if data is not None:
        if datetime.strptime(str(data[1]), "%Y-%m-%d %H:%M:%S") > dt.datetime.now():
            return str(data[0])
    return ''

def update_cookie(cookie, expires, login):
    conn = pymysql.connect(
        db=auto_login('db_db'),
        user=auto_login('db_user'),
        passwd=auto_login('db_passwd'),
        host=auto_login('db_host'))
    cursor = conn.cursor()
    expires = str(expires)
    cursor.execute("UPDATE users SET cookie=%s, expires=%s WHERE login=%s;", (cookie, expires, login))

    conn.commit()