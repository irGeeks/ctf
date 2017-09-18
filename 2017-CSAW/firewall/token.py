#!/usr/bin/python

ss = None

def srand(val):
    global ss
    ss = val

def rand():
    global ss
    if ss is None:
        ss = 123459876
    v1 = (16807 * (ss % 0x1F31D) - 2836 * (ss / 0x1F31D))
    ss = v1 + (-(v1 < 0) & 0x7FFFFFFF)
    return ss % 0x80000000

def gen_token():
    srand(0x6D6F6F64)
    token = 0x45544e49
    for i in range(0x100):
        token += rand()
        token &= 0xFFFFFFFF
    return token

print "token:", gen_token()
