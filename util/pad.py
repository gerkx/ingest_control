def pad(num, pad):
    num = str(num)
    while len(num) < pad:
        num = "0" + num
    return num

def two(num):
    num = str(num)
    while len(num) < 2:
        num = "0" + num
    return num

def three(num):
    num = str(num)
    while len(num) < 3:
        num = "0" + num
    return num

def four(num):
    num = str(num)
    while len(num) < 4:
        num = "0" + num
    return num