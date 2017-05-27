from entropy_pass import entropy_pass

def proper_pass(password):
    if len(password) < 6:
        return 'Hasło musi składać się z co najmniej 6 znaków'
    elif len(password) > 16:
        return 'Hasło nie może być dłuższe niż 16 znaków'
    elif entropy_pass(password) < 57.0:
        return 'Zbyt mała entropia hasła: ' + str(entropy_pass(password))
    
    return 'Correct'