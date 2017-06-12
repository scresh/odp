import uuid

from vial import render_template
from cookie import tk_login
from redirect import redirect
from auto_login import auto_login
import pymysql
import OpenSSL
import datetime as dt


def upload(headers, body, data, token=''):
    cookie = str(headers['http-cookie']).replace('sessionid=', '')
    if token == '':
        token = str(data['token']) if 'token' in data else ''
    login = tk_login(token, cookie)
    print '|' + cookie + '|' + token + '|'
    file_name = data['upload'].filename if 'upload' in data else ''
    if login == '':
        return redirect(headers=headers, body=body, data=data, message='Unauthorized file upload request')
    if len(file_name) > 60:
        return render_template('html/upload.html', headers=headers, body=body, data=data, message='File name is too long', token=token), 200, {}

    if body != '' and file_name != '':
        new_file = open('uploads/' + login + '/' + file_name, 'wb')
        new_file.write(data['upload'].value)
        new_file.close()
        token = str(uuid.UUID(bytes=OpenSSL.rand.bytes(16)).hex)
        date_time = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn = pymysql.connect(
            db=auto_login('db_db'),
            user=auto_login('db_user'),
            passwd=auto_login('db_passwd'),
            host=auto_login('db_host'))
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM uploads ORDER BY id DESC LIMIT 1;")
        id = int(cursor.fetchone()[0]) + 1

        cursor.execute("SELECT login FROM uploads WHERE login=%s AND filename=%s", (login, file_name))
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO uploads VALUES (%s, %s, %s, %s);", (file_name, id, login, date_time))
        else:
            cursor.execute("UPDATE uploads SET time=%s WHERE login=%s AND filename=%s;", (date_time, login, file_name))
        conn.commit()
        cursor.execute("UPDATE users SET token=%s WHERE login=%s;", (token, login))
        conn.commit()
        return redirect(headers=headers, body=body, data=data, message='Your file has been successfully uploaded')

    return render_template('html/upload.html', headers=headers, body=body, data=data, token=token), 200, {}

