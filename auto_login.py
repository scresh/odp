def auto_login(parameter):
    if parameter == 'db_db':
        return 'database_name'
    elif parameter == 'db_user':
        return 'root'
    elif parameter == 'db_passwd':
        return 'ExamplePassword1234'
    elif parameter == 'db_host':
        return 'localhost'
    elif parameter == 'mail_user':
        return 'mail.bot@gmail.com'
    elif parameter == 'mail_passwd':
        return 'ExamplePassword1234'
    elif parameter == 'mail_smtp':
        return 'smtp.gmail.com'
    elif parameter == 'mail_port':
        return 587
    return
