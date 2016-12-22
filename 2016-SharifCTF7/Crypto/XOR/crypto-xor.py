#!/usr/bin/env python3

# Hint: Flag starts with "SharifCTF{", and ends with "}".

# from secret import p_small_prime, q_small_prime, r, key, flag
# flag = flag * r

# def encrypt(msg, p, q, r, key):
# 	enc = []
# 	for i in range(len(msg)):
# 		enc += 
# 	return bytes(enc)

# with open('enc', 'wb') as f:
# 	f.write(encrypt(flag, p_small_prime, q_small_prime, r, key))

#
#r=7

#!/usr/bin/env python3

# Hint: Flag starts with "SharifCTF{", and ends with "}".


def attack(enc,p,q,kl):
	if (q**2 - 6*q + 6)<=0:return False
	flag="SharifCTF{" + '?'*32 + "}"
	xks=[]*kl
	for i in range(kl):
		xks.append([])
	for i,c in enumerate(enc):
		xks[(7*i)%kl].append( (i%43,c^(i%p)) )
	key=[-1]*kl
	for i in range(kl):
		k=-1
		for f,xk in xks[i]:
			if flag[f]!='?':
				nk=xk^pow(long(ord(flag[f])),q,q**2 - 6*q + 6)
				if k!=-1 and k!=nk:
					return False
				k=nk
			elif k!=-1:
				ok=False
				for pf in range(48,58)+range(97,103):
					if xk^pow(pf,q,q**2 - 6*q + 6)==k:
						ok=True
						break
				if not ok:
					return False
		if k!=-1:
			key[i]=k
	print key
	return True	


	return True
def isprime(x):
	for i in range(2,x):
		if x%i==0:return False
	return True
def small_prime(mi,ma):
	if mi<2:mi=2
	small_prime=[]
	for p in range(mi,ma):
		if isprime(p):
			small_prime.append(p)
	return small_prime

p_list=small_prime(2,400)
q_list=small_prime(2,500)

enc=map(ord,open('enc', 'rb').read())

############## PHASE 1 ###################
# for kl in range(2,500):
# 	for p in p_list:
# 		for q in q_list:
# 			if attack(enc,p,q,kl):
# 				print ">>>>>>>>>",p,q,kl

############## PHASE 2 ###################

r=7
key=[239L, 84L, 245L, 143L, 95L, 81L, 203L, 177L, 30L, 225L, 241L]
p=251
q=19
flag=[]

rev={}
for i in range(48,58)+range(97,103):
	x=pow(i,q,q**2 - 6*q + 6)
	if x not in rev:
		rev[x]=[i]
	else:
		rev[x].append(i)

str=""
for i in range(43):
	x=(enc[i] ^ (i%p) ^ key[r*i % len(key)])%(q**2 - 6*q + 6)
	if x not in rev :
		str+='?'
	else:
		str+=chr(rev[x][0])
print str

#SharifCTF{6494889069126bb688b8755815a8d672}