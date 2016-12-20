## Pretty Slim

Opening the file in Winhex/Notepad, it seems like a Zip file.
We changed the first byte to `P` (PK header) and extracted it but it seemed to be corrupted!!  More changes are needed to fix it.
We had no time to fix it manually and we wanted the bonus points badly.
The `DiskInternals ZIP Repair` did it right and by extracting it we got another file with string `KGB in Kremlin28` in header

KGB archiver?
We should fix the header again

```
$ unzip slim_fix.zip 
Archive:  slim_fix.zip
This Zip file has been recovered!
 extracting: flaggggg    

$ stat /tmp/1 | grep Size
  Size: 8626         Blocks: 8          IO Block: 4096   regular file
  
$ kgb 1.kgb /tmp/1
/tmp/1                           0KB -> 0KB
0KB -> 0KB w 0.01s. (112.53% czas: 29 KB/s)

$ hexdump -C 1.kgb| head -2
00000000  4b 47 42 5f 61 72 63 68  20 2d 33 0d 0a 38 36 32  |KGB_arch -3..862|
00000010  36 09 2f 74 6d 70 2f 31  0d 0a 1a 0c 00 82 4a c5  |6./tmp/1......J.|

$ stat flaggggg | grep Size
  Size: 359         Blocks: 8          IO Block: 4096   regular file
  
$ hexdump -C flaggggg| head -2
00000000  4b 47 42 20 69 6e 20 4b  72 65 6d 6c 69 6e 32 38  |KGB in Kremlin28|
00000010  09 66 6c 61 67 67 67 67  67 0d 0a 1a 0c 00 7b 00  |.flaggggg.....{.|
```

KGB is not so sensitive to size of file in it's header (inner file size before decompress)
we put that 359 and it worked, nor we should bruteforce it

```
$ vbindiff flaggggg flaggggg_fixed_kgb 
flaggggg                                                                        
0000 0000: 4B 47 42 20 69 6E 20 4B  72 65 6D 6C 69 6E 32 38  KGB in K remlin28
[...]
flaggggg_fixed_kgb                                                              
0000 0000: 4B 47 42 5F 61 72 63 68  20 2D 33 0D 0A 33 35 39  KGB_arch  -3..359
[...]

$ file flaggggg_fixed_kgb 
flaggggg_fixed_kgb: KGB Archiver file with compression level 3

$ kgb flaggggg_fixed_kgb 
Extracting archive KGB_arch -3 flaggggg_fixed_kgb ...
         0KB flaggggg: different: offset 0, archive=137 file=75
0KB -> 0KB w 0.01s. (100.00% czas: 44 KB/s)

$ rm flaggggg; kgb flaggggg_fixed_kgb
Extracting archive KGB_arch -3 flaggggg_fixed_kgb ...
         0KB flaggggg: extracted
0KB -> 0KB w 0.01s. (100.00% czas: 37 KB/s)

$ file flaggggg
flaggggg: PNG image data, 111 x 111, 1-bit grayscale, non-interlaced
```

![flaggggg.png](flaggggg.png)