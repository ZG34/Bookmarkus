import re


def password_check(password):
    pw = password
    # copied from a website. as I understand, the ?= portion is specifying the following chars as required.
    # first portion being at least 1 lower a-z char and so on, with the end curly brackets specifying min and max length
    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
    rg_compile = re.compile(reg)
    match = re.search(rg_compile, pw)

    if match:
        print("good password")
        return True
    else:
        print("bad password")
        return False
