## Snake
We were given a 32-bit executable VMProtected file. Debugging VMProtected is difficult and OllyDbg was detected and after wasting a lot of time on debugging ‘snake.exe', I was frustrated. 

I double checked the file and found this string: 

`Number of foods= number of used bytes in windows drive.`

I hadn't noticed it before, I don't know why but I couldn't solve my problem with OllyDbg and other debuggers stuck on protections inside VMProtect so I decided to debug my VMWare with WinDbg and it was just another pain in the neck, because it was detected too, therefore I thought maybe I had to hook some API , but my friend suggested API Monitor's breakpoint feature. I tried it and it was very straightforward.
'Snake.exe' uses ‘RtlDosPathNameToNtPathName_U' to get Windows directory path and ‘NtQueryVolumeInformationFile' to calculate Windows drive size, so I tried to change ‘RtlDosPathNameToNtPathName_U' path to another drive with API Monitor and the rounds changed, before trying to write any code I changed it to a non-existent drive and ta-da-...! 

Problem solved without any further ado.

![scr1.png](scr1.png)

Seems easy, right? :D