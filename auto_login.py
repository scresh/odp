def auto_login(parameter):
    if parameter == 'db_file':
        return 'database.db'
    elif parameter == 'mail_user':
        return 'mail.bot@gmail.com'
    elif parameter == 'mail_passwd':
        return 'ExamplePassword1234'
    elif parameter == 'mail_smtp':
        return 'smtp.gmail.com'
    elif parameter == 'mail_port':
        return 587
    return
