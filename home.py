# -*- coding: utf-8 -*-
from vial import render_template
import sqlite3
from params import param_dict
from cookie import token_cookie, user_cookie


def home(headers, body, data):
    cookie = str(headers['http-cookie']).replace('sessionid=', '')
    token = token_cookie(cookie)
    login = user_cookie(cookie)

    conn = sqlite3.connect(param_dict['db_file'])
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, login, time FROM snippets ORDER BY time DESC ")
    snippets_result = cursor.fetchall()
    snippets_values = []
    for row in snippets_result:
        snippets_values.append({'id': str(row[0]), 'name': str(row[1]), 'login': str(row[2]), 'time': str(row[3])})

    cursor.execute("SELECT filename, id, login, time FROM uploads WHERE login=? ORDER BY time DESC ", (login,))
    uploads_result = cursor.fetchall()
    uploads_values = []
    for row in uploads_result:
        uploads_values.append({'filename': str(row[0]), 'id': str(row[1]), 'login': str(row[2]), 'time': str(row[3])})

    cursor.execute("SELECT ip FROM logs WHERE login=? AND success=1 ORDER BY time DESC LIMIT 2", (login,))
    fetch = cursor.fetchall()
    if login != '':
        if len(fetch) >= 2:
            if str(fetch[0][0]) != str(fetch[1][0]):
                return render_template('templates/signed.html', body=body, data=data, headers=headers, snippets_values=snippets_values, uploads_values=uploads_values, token=token,
                                   message='New login location detected. IP: ' + str(fetch[1][0])), 200, {}
        return render_template('templates/signed.html', body=body, data=data, headers=headers, snippets_values=snippets_values, uploads_values=uploads_values,  token=token), 200, {}
    return render_template('templates/unsigned.html', body=body, data=data, headers=headers, snippets_values=snippets_values), 200, {}

