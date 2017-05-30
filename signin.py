# -*- coding: utf-8 -*-
from vial import Vial, render_template
from authentication import authentication
from add_log import add_log
from allow_signin import allow_signin


def signin(headers, body, data):
    login = str(data['login']) if 'login' in data else ''
    password = str(data['password']) if 'password' in data else ''
    if (login == '') or (password == ''):
        return render_template('signin.html', body=body, data=data, headers=headers), 200, {}
    elif allow_signin(login, headers):
        if (authentication(login, password)):
            add_log(headers, data, True)
            return render_template('signin.html', body=body, data=data, headers=headers, message='Pooprawne dane'), 200, {}
        add_log(headers, data, False)
        return render_template('signin.html', body=body, data=data, headers=headers, message='Niepoprawne dane'), 200, {}
    add_log(headers, data, False)
    return render_template('signin.html', body=body, data=data, headers=headers, message='Ban na IP'), 200, {}
