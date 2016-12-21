#!/usr/bin/python
"""
SharifCTF{10ED2D76BCC417D9C48BE67F6790AF70}
"""
import gmpy2
from Crypto.Util.number import *
from Crypto.Cipher import AES
from fractions import gcd

nn=[]
for i,x in enumerate(map(int,tuple(open('enc.txt', 'r')))):
	nn.append(x-1-i)

q=nn[2]-nn[1]
for i in range(len(nn)):
	for j in range(i+1,len(nn)):
		q=gcd(q,abs(nn[j]-nn[i]))
print "q:",q
rand=nn[0]%q
print "rand:",rand

f=(q-1)/2
#f=(a-d)(a+d)=a^2-d^2
d=1
while 2*d<10**8:
	a2=f+d**2
	if gmpy2.is_square(a2):
		a=gmpy2.isqrt(a2)
		break
	d+=1
print "d:",d
p1,p2=a-d,a+d
print "p1:",p1
print "p2:",p2

c=""
for i,x in enumerate(nn):
	l = (x-rand)/(q*(rand+i))
	c+= '1' if pow(l,p1*2,q)==1 else '0' 
print c

c = hex(int(c, 2))[2:-1].decode("hex")

key = long_to_bytes(rand)
IV = key[16:32]
mode = AES.MODE_CBC
aes = AES.new(key[:16], mode, IV=IV)

print "flag:", aes.decrypt(c)