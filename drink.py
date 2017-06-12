# -*- coding: utf-8 -*-
from vial import Vial
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
from upload import upload
from download import download

routes = {
    '/': home,
    '/signin': signin,
    '/signup': signup,
    '/forget': forget,
    '/redirect': redirect,
    '/signout': signout,

    '/upload': upload,
    '/upload/': upload,
    '/upload/{token}': upload,

    '/reset': reset,
    '/reset/': reset,
    '/reset/{token}': reset,

    '/view': view,
    '/view/': view,
    '/view/{snippet_id}': view,

    '/add': add,
    '/add/': add,
    '/add/{token}': add,

    '/change': change,
    '/change/': change,
    '/change/{token}': change,

    '/download': download,
    '/download/': download,
    '/download/{id}': download,

}

app = Vial(routes, prefix='', static='/static').wsgi_app()
