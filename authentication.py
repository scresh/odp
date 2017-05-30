import bcrypt
import pymysql


def authentication(login, password):
    conn = pymysql.connect(
        db='odp',
        user='odp',
        passwd='qqq',
        host='localhost')
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM userdata WHERE login=%s;", (login,))
    dbhash = cursor.fetchone()

    if dbhash is None:
        for i in range(3):
            bcrypt.hashpw('wrong data delay', bcrypt.gensalt())
        return False
    dbhash = str(dbhash)[2:62]
    salt = dbhash[0:29]
    hash = password

    for i in range(3):
        hash = bcrypt.hashpw(hash, salt)

    if hash == dbhash:
        return True
    return False

