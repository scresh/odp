from vial import render_template


def redirect(headers, body, data, message='Page not found'):
    return render_template('templates/redirect.html', body=body, data=data, headers=headers, message=message), 200, {}
