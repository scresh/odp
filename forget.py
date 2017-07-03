# -*- coding: utf-8 -*-
from vial import render_template
from auto_login import auto_login
import smtplib
import uuid
import pymysql
import OpenSSL


def forget(headers, body, data):
    email = str(data['email']) if 'email' in data else ''
    ip = str(headers['http-x-forwarded-for']) if 'http-x-forwarded-for' in headers else 'PROXY'
    if email == '':
        return render_template('templates/forget.html', body=body, data=data, headers=headers), 200, {}
    if not email_correct_format(email):
        return render_template('templates/forget.html', body=body, data=data, headers=headers,
                               message='Email address is in an invalid format'), 200, {}
    send_mail(email, ip)
    return render_template('templates/forget.html', body=body, data=data, headers=headers,
                           message='A reset password link has been sent to you via email'), 200, {}


def email_correct_format(email):
    if not 6 <= len(email) <= 30:
        return False
    elif email.count('@') != 1 or not (0 < email.index('@') < (len(email) - 4)):
        return False
    elif email.count('.') == 0:
        return False
    for c in email:
        if not ((96 < ord(c) < 123) or (63 < ord(c) < 91) or (47 < ord(c) < 58) or ord(c) == 46):
            return False
    return True


def send_mail(email, ip):
    server = smtplib.SMTP(auto_login('mail_smtp'), auto_login('mail_port'))
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(auto_login('mail_user'), auto_login('mail_passwd'))

    conn = pymysql.connect(
        db=auto_login('db_db'),
        user=auto_login('db_user'),
        passwd=auto_login('db_passwd'),
        host=auto_login('db_host'))
    cursor = conn.cursor()
    cursor.execute("SELECT login, token FROM users WHERE email=%s;", (email,))
    fetch = cursor.fetchone()

    if fetch is None:
        msg = 'Hi info,\nA incorrect request to reset password was noticed from IP: ' + ip
        server.sendmail(auto_login('mail_user'), auto_login('mail_user'), msg)
        server.quit()
        return

    login = fetch[0]

    login = str(login)
    token = str(fetch[1])

    msg = 'Hi ' + login + ',\nWe have received a request to reset your password from IP: ' + ip + '\nPlease confirm: https://odprojekt.tk/reset/' + token
    server.sendmail(auto_login('mail_user'), email, msg)
    server.quit()
