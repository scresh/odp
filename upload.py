import binascii
import os
import sqlite3
import uuid

from vial import render_template
from cookie import tk_login
from redirect import redirect
from auto_login import auto_login
import pymysql
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
        return render_template('templates/upload.html', headers=headers, body=body, data=data, message='File name is too long', token=token), 200, {}

    if body != '' and file_name != '':
        new_file = open('uploads/' + login + '/' + file_name, 'wb')
        new_file.write(data['upload'].value)
        new_file.close()
        token = str(uuid.UUID(hex=binascii.b2a_hex(os.urandom(16))))
        date_time = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn = sqlite3.connect(auto_login('db_file'))
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM uploads ORDER BY id DESC LIMIT 1;")
        fetch = cursor.fetchone()
        file_id = (int(fetch[0]) + 1) if fetch is not None else 0
        cursor.execute("SELECT login FROM uploads WHERE login=? AND filename=?", (login, file_name))
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO uploads VALUES (?, ?, ?, ?);", (file_id, login, file_name, date_time))
        else:
            cursor.execute("UPDATE uploads SET time=? WHERE login=? AND filename=?;", (date_time, login, file_name))
        conn.commit()
        cursor.execute("UPDATE users SET token=? WHERE login=?;", (token, login))
        conn.commit()
        return render_template('templates/upload.html', headers=headers, body=body, data=data, token=token), 200, {}

    return render_template('templates/upload.html', headers=headers, body=body, data=data, token=token), 200, {}

