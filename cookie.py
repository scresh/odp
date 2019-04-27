from auto_login import auto_login
from datetime import datetime
import datetime as dt
import sqlite3


def user_cookie(cookie):
    if cookie == '':
        return ''
    conn = sqlite3.connect(auto_login('db_file'))
    cursor = conn.cursor()
    cursor.execute("SELECT login, expires FROM users WHERE cookie=?;", (cookie,))
    data = cursor.fetchone()

    if data is not None:
        if datetime.strptime(str(data[1]).split('.')[0], "%Y-%m-%d %H:%M:%S") > dt.datetime.now():
            return str(data[0])
    return ''


def token_cookie(cookie):
    if cookie == '':
        return ''
    conn = sqlite3.connect(auto_login('db_file'))
    cursor = conn.cursor()
    cursor.execute("SELECT token, expires FROM users WHERE cookie=?;", (cookie,))
    data = cursor.fetchone()

    if data is not None:
        if datetime.strptime(str(data[1]).split('.')[0], "%Y-%m-%d %H:%M:%S") > dt.datetime.now():
            return str(data[0])
    return ''


def tk_pass(token, cookie):
    if token == '' or cookie == '':
        return ''
    conn = sqlite3.connect(auto_login('db_file'))
    cursor = conn.cursor()
    cursor.execute("SELECT password, cookie, expires FROM users WHERE token=?;", (token,))
    data = cursor.fetchone()

    if data is not None:
        if cookie == str(data[1]) and datetime.strptime(str(data[2].split('.')[0]), "%Y-%m-%d %H:%M:%S") > dt.datetime.now():
            return str(data[0])
    return ''


def tk_login(token, cookie):
    if token == '' or cookie == '':
        return ''
    conn = sqlite3.connect(auto_login('db_file'))
    cursor = conn.cursor()
    cursor.execute("SELECT login, cookie, expires FROM users WHERE token=?;", (token,))
    data = cursor.fetchone()

    if data is not None:
        if cookie == str(data[1]) and datetime.strptime(str(data[2]).split('.')[0], "%Y-%m-%d %H:%M:%S") > dt.datetime.now():
            return str(data[0])
    return ''


def tk_login(token, cookie):
    if token == '' or cookie == '':
        return ''
    conn = sqlite3.connect(auto_login('db_file'))
    cursor = conn.cursor()
    cursor.execute("SELECT login, cookie, expires FROM users WHERE token=?;", (token,))
    data = cursor.fetchone()

    if data is not None:
        if cookie == str(data[1]) and datetime.strptime(str(data[2]).split('.')[0], "%Y-%m-%d %H:%M:%S") > dt.datetime.now():
            return str(data[0])
    return ''


def update_cookie(cookie, expires, login):
    conn = sqlite3.connect(auto_login('db_file'))
    cursor = conn.cursor()
    expires = str(expires)
    cursor.execute("UPDATE users SET cookie=?, expires=? WHERE login=?;", (cookie, expires, login))
    conn.commit()


def disable_cookie(cookie):
    conn = sqlite3.connect(auto_login('db_file'))
    cursor = conn.cursor()
    expires = str(dt.datetime.utcnow())
    cursor.execute("UPDATE users SET expires=? WHERE cookie=?;", (expires, cookie))
    conn.commit()
