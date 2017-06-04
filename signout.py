from redirect import redirect
from cookie import disable_cookie


def signout(headers, body, data):
    cookie = str(headers['http-cookie']).replace('sessionid=', '')
    disable_cookie(cookie)
    return redirect(headers=headers, body=body, data=data, message='Signing out')





