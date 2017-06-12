# -*- coding: utf-8 -*-
# encoding=utf8

import os
from mimetypes import guess_type

import sys

from vial import to_unicode, to_ascii
from cookie import user_cookie
from redirect import redirect
from auto_login import auto_login
import pymysql


def download(headers, body, data, id=''):
    cookie = str(headers['http-cookie']).replace('sessionid=', '')
    login = user_cookie(cookie)
    if login == '':
        return redirect(headers=headers, body=body, data=data, message='Unauthorized file download request')

    conn = pymysql.connect(
        db=auto_login('db_db'),
        user=auto_login('db_user'),
        passwd=auto_login('db_passwd'),
        host=auto_login('db_host'))
    cursor = conn.cursor()

    cursor.execute("SELECT login, filename from uploads WHERE id=%s", (id,))
    fetch = cursor.fetchone()
    if fetch is None:
        return redirect(headers=headers, body=body, data=data, message='File does no exist')
    if login != str(fetch[0]):
        return redirect(headers=headers, body=body, data=data,
                        message='You do not have permission to download this file')
    file_path = '/uploads/' + login + '/' + str(fetch[1])
    f = open(file_path, 'rb')
    content = to_unicode(f.read())
    content_type = str(guess_type(file_path)[0])
    return content, 200, {'request-method': 'GET',
                          'Content-Description': 'File Transfer',
                          'Content-Type': content_type,
                          'Content-Disposition': 'attachment, filename=' + str(fetch[1]),
                          'Content-Transfer-Encoding': 'binary',
                          'Expires': '0',
                         'Cache-Control': 'must-revalidate, post-check=0, pre-check=0',
                         'Pragma': 'public',
                          'Content-Length': str(os.stat(file_path).st_size)
                          }
