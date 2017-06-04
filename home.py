# -*- coding: utf-8 -*-
from vial import render_template
import pymysql
from auto_login import auto_login


def home(headers, body, data):
    conn = pymysql.connect(
        db=auto_login('db_db'),
        user=auto_login('db_user'),
        passwd=auto_login('db_passwd'),
        host=auto_login('db_host'))
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, login, time FROM snippets")
    result = cursor.fetchall()

    values = []
    for row in result:
        values.append({'id': str(row[0]), 'name': str(row[1]), 'login': str(row[2]), 'time': str(row[3])})

    return render_template('home.html', body=body, data=data, headers=headers, values=values), 200, {}
