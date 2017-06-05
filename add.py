# -*- coding: utf-8 -*-
from vial import render_template
from auto_login import auto_login
import datetime as dt
from cookie import whose_cookie
from redirect import redirect
import pymysql


def add(headers, body, data):
    cookie = str(headers['http-cookie']).replace('sessionid=', '')
    login = whose_cookie(cookie)
    if login == '':
        return redirect(headers=headers, body=body, data=data, message='You must be signed-in to be able to add snippets')
    snippet = str(data['snippet']) if 'snippet' in data else ''
    title = str(data['title']) if 'title' in data else ''

    if (snippet == '') or (title == ''):
        return render_template('html/add.html', body=body, data=data, headers=headers), 200, {}
    elif len(title) > 60:
        return render_template('html/add.html', body=body, data=data, headers=headers,
                               message='Title length should not be longer than 60 characters'), 200, {}
    elif len(snippet) > 6000:
        return render_template('html/add.html', body=body, data=data, headers=headers,
                               message='Snippet length should not be longer than 6000 characters'), 200, {}
    add_snippet(title, snippet, login)
    return redirect(headers=headers, body=body, data=data, message='Your snippet has been successfully added.')


def add_snippet(title, snippet_content, login):
    conn = pymysql.connect(
        db=auto_login('db_db'),
        user=auto_login('db_user'),
        passwd=auto_login('db_passwd'),
        host=auto_login('db_host'))
    cursor = conn.cursor()
    cursor.execute("SELECT id, time FROM snippets ORDER BY id DESC LIMIT 1;")
    id = int(cursor.fetchone()[0])+1
    date_time = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO snippets VALUES (%s, %s, %s, %s);", (title, id, login, date_time))
    conn.commit()
    snippet_path = 'static/snippets/' + str(id) + '.snippet'
    snippet_file = open(snippet_path, 'w+')
    snippet_file.write(snippet_content)
    snippet_file.close()
