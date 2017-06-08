# -*- coding: utf-8 -*-
from vial import Vial, render_template
from signin import signin
from signup import signup
from forget import forget
from reset import reset
from view import view
from home import home
from redirect import redirect
from signout import signout
from add import add
from change import change


def index(headers, body, data):
    return 'Hello', 200, {}


def hello(headers, body, data, name):
    return 'Howdy ' + name, 200, {}


def upload(headers, body, data):
    return render_template('upload.html', body=body, data=data), 200, {}


routes = {
    '/': home,
    '/hello/{name}': hello,
    '/upload': upload,
    '/signin': signin,
    '/signup': signup,
    '/forget': forget,
    '/reset/{token}': reset,
    '/reset': reset,
    '/view/{snippet_id}': view,
    '/redirect': redirect,
    '/signout': signout,
    '/add': add,
    '/change': change,
    '/change/{token}': change,

}

app = Vial(routes, prefix='', static='/static').wsgi_app()
