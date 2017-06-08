from auto_login import auto_login
from datetime import datetime
import datetime as dt
import pymysql


def user_cookie(cookie):
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


def token_cookie(cookie):
    if cookie == '':
        return ''
    conn = pymysql.connect(
        db=auto_login('db_db'),
        user=auto_login('db_user'),
        passwd=auto_login('db_passwd'),
        host=auto_login('db_host'))
    cursor = conn.cursor()
    cursor.execute("SELECT token, expires FROM users WHERE cookie=%s;", (cookie,))
    data = cursor.fetchone()

    if data is not None:
        if datetime.strptime(str(data[1]), "%Y-%m-%d %H:%M:%S") > dt.datetime.now():
            return str(data[0])
    return ''


def tk_pass(token, cookie):
    if token == '' or cookie == '':
        return ''
    conn = pymysql.connect(
        db=auto_login('db_db'),
        user=auto_login('db_user'),
        passwd=auto_login('db_passwd'),
        host=auto_login('db_host'))
    cursor = conn.cursor()
    cursor.execute("SELECT password, cookie, expires FROM users WHERE token=%s;", (token,))
    data = cursor.fetchone()

    if data is not None:
        if cookie == str(data[1]) and datetime.strptime(str(data[2]), "%Y-%m-%d %H:%M:%S") > dt.datetime.now():
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


def disable_cookie(cookie):
    conn = pymysql.connect(
        db=auto_login('db_db'),
        user=auto_login('db_user'),
        passwd=auto_login('db_passwd'),
        host=auto_login('db_host'))
    cursor = conn.cursor()
    expires = str(dt.datetime.utcnow())
    cursor.execute("UPDATE users SET expires=%s WHERE cookie=%s;", (expires, cookie))
    conn.commit()
