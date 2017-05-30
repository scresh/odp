import datetime
import pymysql

def add_log(headers, login, succes=False):
    ip = str(headers['http-x-forwarded-for']) if 'http-x-forwarded-for' in headers else 'PROXY'
    date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print date_time
    conn = pymysql.connect(
        db='odp',
        user='odp',
        passwd='qqq',
        host='localhost')
    cursor = conn.cursor()
    if(succes):
        cursor.execute("INSERT INTO logs VALUES (%s, %s, TRUE, %s);", (login, ip, date_time))
    else:
        cursor.execute("INSERT INTO logs VALUES (%s, %s, FALSE, %s);", (login, ip, date_time))
    conn.commit()