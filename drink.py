# -*- coding: utf-8 -*-
from vial import Vial, render_template
from signin import signin
from signup import signup


def index(headers, body, data):
    return 'Hello', 200, {}


def hello(headers, body, data, name):
    return 'Howdy ' + name, 200, {}


def upload(headers, body, data):
    return render_template('upload.html', body=body, data=data), 200, {}


routes = {
    '/': index,
    '/hello/{name}': hello,
    '/upload': upload,
    '/signin': signin,
    '/signup': signup,
    # '/forget': forget,
}

app = Vial(routes, prefix='', static='/static').wsgi_app()