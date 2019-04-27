# -*- coding: utf-8 -*-
# encoding=utf8

import os
from mimetypes import guess_type
from vial import to_unicode
from cookie import user_cookie
from redirect import redirect
from params import param_dict
import sqlite3


def download(headers, body, data, file_id=''):
    cookie = str(headers['http-cookie']).replace('sessionid=', '')
    login = user_cookie(cookie)
    if login == '':
        return redirect(headers=headers, body=body, data=data, message='Unauthorized file download request')

    conn = sqlite3.connect(param_dict['db_file'])
    cursor = conn.cursor()

    cursor.execute("SELECT login, filename from uploads WHERE id=?", (file_id,))
    fetch = cursor.fetchone()
    if fetch is None:
        return redirect(headers=headers, body=body, data=data, message='File does no exist')
    if login != str(fetch[0]):
        return redirect(headers=headers, body=body, data=data,
                        message='You do not have permission to download this file')
    file_path = 'uploads/' + login + '/' + str(fetch[1])
    f = open(file_path, 'rb')

    content = str(to_unicode(f.read())).encode()
    content_type = str(guess_type(file_path)[0])
    return content, 200, {'request-method': 'GET',
                          'Content-Description': 'File Transfer',
                          'Content-Type': content_type,
                          'Content-Disposition': 'attachment; filename="' + str(fetch[1]) + '"',
                          'Content-Transfer-Encoding': 'binary',
                          'Expires': '0',
                          'Cache-Control': 'must-revalidate',
                          'Pragma': 'public',
                          'Content-Length': str(os.stat(file_path).st_size)}
