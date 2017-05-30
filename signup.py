# -*- coding: utf-8 -*-
from entropy_pass import entropy_pass
from vial import render_template


def signup(headers, body, data):
    login = str(data['login']) if 'login' in data else ''
    password = str(data['password']) if 'password' in data else ''
    email = str(data['email']) if 'email' in data else ''
    if (login == '') or (password == '') or (email == ''):
        return render_template('signup.html', body=body, data=data, headers=headers), 200, {}
    elif entropy_pass(password) < 50.0:
        return render_template('signin.html', body=body, data=data, headers=headers, message='Hasło zbyt proste'), 200, {}
    return render_template('signup.html', body=body, data=data, headers=headers), 200, {}
