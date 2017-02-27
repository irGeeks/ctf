`memo` is a `x86_64` pwn challenge with provided `libc`. `FULL RELRO` and `PIE` is disabled. At start we should provide an username (and password). We can do the following operations:  
1. Insert new memo of size 0x20 up to 4  
2. Edit last memo  
3. View memo by index  
4. Delete memo by index  
5. Change Username and Password you entered before  
  
There is also a two table (array) at `.bss` which keeps memo address and its size (<= 0x20). 
# Vulnerabilities
After analysing each function it can be seen as `memo` has multiple issues:  
1. At `new_message` `0x400C52` if we enter size more than 0x20 we can overflow an heap allocation by `malloc(0x20)` with our size. **and the allocated space won't be placed in memos table**  
2. At `edit_last_message` `0x400DA8` we can leak heap address after editing.  
3. At `view_memo` `0x400E56` index is not checked against negative values although due to casting we can't use this infoleak.  
4. At `change_password` `0x400FF6` there is an off-by-one on entering password which overwrite LSB (Least significant byte) of first (index == 0) memo size.  


As you may noticed we have heap overflow (via using `4` or `1`) but based on size limitation we should trick `fastbins` to own the challenge.  
  
# Exploitation
First of all we need a fastbin free chain. So allocating two chunk both of size 0x20 and then freeing the chunks in **inverse order** gives us a fastbin free chain of size `48` (**0x30**). We can then use `1` vulnerability to overflow the heap and corrupt heap so that free chain last pointer points to our arbitrary address. **But remember we should provide our pointer in such a way that it bypasses the fastbin malloc corruption checks**. To do so we should use an address with having a metadata (address-4) of size `48`. For this case i choose memo table so if i can overwrite pointers in the table i have `infoleak + write-what-where` primitive. As i described earlier we can use password since it is located just behind the table. after overwriting the second pointer in the table and using `view_memo` i have libc leak and stack leak. Due to binary compiled with `FULL RELRO` protection, we can overwrite stack or creating a fake tls_dtors struct (but due to new protection against tls_dtors and issues in some cases i choose option 1). After leaking we can overwrite the second pointer in the table again with stack address and pwn the challenge.  

You can see my [exploit](sol.py) 