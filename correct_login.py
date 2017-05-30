import pymysql


def correct_chars(login):
    for c in login:
        if not (96 < ord(c) < 123) or (64 < ord(c) < 91) or (47 < ord(c) < 58):
            return False
    return True


def correct_length(login):
    if 6 < len(login) < 24:
        return True
    return False


def not_used(login):
    conn = pymysql.connect(
        db='odp',
        user='odp',
        passwd='qqq',
        host='localhost')
    cursor = conn.cursor()
    cursor.execute("SELECT login FROM userdata WHERE login=%s;", (login, ))

    if cursor.fetchall() is None:
        return False
    return True

