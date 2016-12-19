#!/usr/bin/python

a = "fx1uagMGQQMWOWhyFBxnBUdzN35NPWYHUBQHRmozeEY="
pw = "My_S3cr3t_P@$$W0rD\x00"
print len(pw)
a = a.decode("base64")

b = ""
i = 0
for c in a:
    b += chr(0xff & (ord(c) ^ ord(pw[i % 0x13])))
    i += 1

print "flag:", b
