import math
def entropy_pass(password):
    entropy = 0.0
    charcounter = 0
    smal = 0
    big = 0
    num = 0
    spec = 0
    for c in password:
        charcounter += 1
        if (ord(c) > 96 and ord(c) < 123):
            smal = 1
        elif (ord(c) > 64 and ord(c) < 91):
            big = 1
        elif (ord(c) > 47 and ord(c) < 58):
            num = 1
        else:
            spec = 1
    alpha = smal * 26 + big * 26 + num * 10 + spec * 66
    entropy = charcounter * math.log(alpha if alpha > 0 else 1, 2)
    return entropy