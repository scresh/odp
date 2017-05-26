# -*- coding: utf-8 -*-
from vial import Vial, render_template
from authentication import authentication

def signin(headers, body, data):
    login =  str(data['login']) if 'login' in data else ''
    password = str(data['password']) if 'password' in data else ''
    email = str(data['email']) if 'email' in data else ''
    if (login == '') and (password == '') and (email == ''):
        return render_template('signup.html', body=body, data=data, headers=headers), 200, {}
    elif(authentication(login, password)):
        return render_template('signin.html', body=body, data=data, headers=headers, message='Pooprawne dane'), 200, {}
    return render_template('signin.html', body=body, data=data, headers=headers, message='Niepoprawne dane'), 200, {}