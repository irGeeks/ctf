```
root@xored:/tmp# file data.txt.tar.xz 
data.txt.tar.xz: XZ compressed data
root@xored:/tmp# tar xf data.txt.tar.xz 
root@xored:/tmp# file data.txt
data.txt: ASCII text, with very long lines, with no line terminators
root@xored:/tmp# cat data.txt | xxd -r -p > misc315
root@xored:/tmp# file misc315 
misc315: lzip compressed data, version: 1
root@xored:/tmp# lunzip misc315 
root@xored:/tmp# file misc315.out 
misc315.out: POSIX tar archive
root@xored:/tmp# tar xvf misc315.out 
What.exe
root@xored:/tmp# file What.exe 
What.exe: PE32 executable (GUI) Intel 80386, for MS Windows
```

**The file is a Windows Executable file; Protected with VMProtect. After Extracting file resources we found a gif file. We can obtain flag.png by appending gif frames in extracted order.**


```
root@xored:/tmp# convert +append *.gif flag.png
```
flag: bc52fead1ecb908ea9ae98b105809b71