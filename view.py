# -*- coding: utf-8 -*-
from vial import render_template
from redirect import redirect
import sqlite3


def view(headers, body, data, snippet_id='0'):
    try:
        snippet_id = int(snippet_id)
    except Exception:
        snippet_id = 0

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT login FROM snippets WHERE id=?;', (snippet_id, ))
    login = cursor.fetchone()

    if login is None:
        return redirect(headers=headers, body=body, data=data, message='Snippet does not exist')
    snippet_path = 'static/snippets/' + str(snippet_id) + '.snippet'
    return render_template('templates/view.html', body=body, data=data, snippet_path=snippet_path), 200, {}
