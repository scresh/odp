from vial import render_template
from auto_login import auto_login
import smtplib
import uuid
import pymysql


def forget(headers, body, data):
    email = str(data['email']) if 'email' in data else ''
    ip = str(headers['http-x-forwarded-for']) if 'http-x-forwarded-for' in headers else 'PROXY'
    if email == '':
        return render_template('forget.html', body=body, data=data, headers=headers), 200, {}
    send_mail(email, ip)
    return render_template('forget.html', body=body, data=data, headers=headers,
                           message='Jesli podany email jest wlasciwy wiadomosc zostala wyslana'), 200, {}


def send_mail(email, ip):
    token = str(uuid.uuid4().hex)

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
    cursor.execute("SELECT login FROM userdata WHERE email=%s;", (email,))
    login = cursor.fetchone()

    if login is None:
        try:
            msg = 'Hej info,\nZ adresu IP: ' + ip + ' odnotowano nieudana probe resetu hasla'
            server.sendmail(auto_login('mail_user'), auto_login('mail_user'), msg)
            server.quit()
        except Exception:
            server.quit()
        return

    login = str(login)
    login = login.replace("('", "")
    login = login.replace("',)", "")

    cursor.execute("DELETE FROM tokens WHERE login = %s", (login,))
    conn.commit()
    cursor.execute("INSERT INTO tokens VALUES (%s, %s);", (login, token))
    conn.commit()

    msg = 'Hej ' + login + ',\nZ adresu IP: ' + ip + ' zostala wygenerowana prosba o reset hasla\nKliknij w link aby je zresetowac:\nhttps://odprojekt.tk/reset/' + token
    try:
        server.sendmail(auto_login('mail_user'), email, msg)
    except Exception:
        cursor.execute("DELETE FROM tokens WHERE login = %s", (login,))
        conn.commit()
    server.quit()
