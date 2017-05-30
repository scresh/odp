import datetime
import pymysql


def add_log(headers, data, success=False):
    login = str(data['login']) if 'login' in data else '-'
    ip = str(headers['http-x-forwarded-for']) if 'http-x-forwarded-for' in headers else 'PROXY'
    date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = pymysql.connect(
        db='odp',
        user='odp',
        passwd='qqq',
        host='localhost')
    cursor = conn.cursor()
    if success:
        cursor.execute("INSERT INTO logs VALUES (%s, %s, TRUE, %s);", (login, ip, date_time))
    else:
        cursor.execute("INSERT INTO logs VALUES (%s, %s, FALSE, %s);", (login, ip, date_time))
    conn.commit()
