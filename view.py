# -*- coding: utf-8 -*-
from vial import render_template
from auto_login import auto_login
import pymysql


def view(headers, body, data, snippet_id='0'):
    try:
        snippet_id = int(snippet_id)
    except:
        snippet_id = 0

    print str(snippet_id)

    conn = pymysql.connect(
        db=auto_login('db_db'),
        user=auto_login('db_user'),
        passwd=auto_login('db_passwd'),
        host=auto_login('db_host'))
    cursor = conn.cursor()
    cursor.execute("SELECT login FROM snippets WHERE id=%s;", (snippet_id,))
    login = cursor.fetchone()

    if login is None:
        return render_template('view.html', body=body, data=data, message='Snippet does not exist'), 200, {}
    file_path = 'snippets/' + str(snippet_id) + '.snippet'
    try:
        f = open(file_path, 'r')
        snippet = f.read()
        f.close()
        return render_template('view.html', body=body, data=data, snippet=snippet), 200, {}
    except:
        return render_template('view.html', body=body, data=data, message='Snippet does not exist'), 200, {}
