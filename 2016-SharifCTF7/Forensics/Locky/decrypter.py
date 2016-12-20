#!/usr/bin/python 


from Crypto.PublicKey import RSA
import sys
rsa = RSA.importKey(open("privkey.pem").read())

msg = open(sys.argv[1]).read()
for i in xrange(13):
    msg = rsa.decrypt(msg)
    with open("{}_{}.txt".format(sys.argv[1], i), "wb") as f:
        f.write(msg)
