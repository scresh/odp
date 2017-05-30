from datetime import datetime
import datetime as dt
import pymysql


def allow_signin(login, headers):
    ip = str(headers['http-x-forwarded-for']) if 'http-x-forwarded-for' in headers else 'PROXY'
    conn = pymysql.connect(
        db='odp',
        user='odp',
        passwd='qqq',
        host='localhost')
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
