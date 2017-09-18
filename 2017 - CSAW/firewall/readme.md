# FIREWALL

firewall was a pwn challenge prepared to run under windows (POSIX support).
First of all we enable *Unix-subsystem* in the windows features which can be accessed from CP->Programs->Turn on ...(Please make sure you have Enterprise or Ultimate version of win!).
Then we need [this file](https://download.microsoft.com/download/6/2/1/6214608E-1A46-43DA-BEF4-B1A575F7CD26/Utilities%20and%20SDK%20for%20Subsystem%20for%20UNIX-based%20Applications_AMD64.exe) to run and then debug the exe.

##Analysing:

After reading the binary we can summerize the tasks:

1. The binary first loads flag in the memory and init some space and a menu table and a MAGIC (`0xFEE15BAD`) in the `0x40E960`. (So the goal seems to be reading flag from memory.)
2. After creating a token, we should authenticate with valid token to enter the system.
3. We can select 8 menu to:  
	1. Create new firewall rule (create_rule:`0x401d00`)
	2. Edit a firewall rule (edit_rule:`0x401e60`)
	3. Delete a firewall rule (delete_rule:`0x401fd0`)
	4. Print a firewall rule	(print_rule:`0x402080`)
	5. List all firewall rules (list_rules:`0x4021a0`)
	6. Check some MAGIC (with `0xFACADE`) and print flag if it is correct! (print_flag:`0x402240`)
	7. help
	8. Exit

Size of each rule is `29` and we can create up to `16` rules.  
`[byte:enable | char[20]:name | int:port | char[4]:type`  

[token.py](token.py) generates valid token (Also you can read it from memory).

## vuln #1

In `edit_rule` we can overflow `name` of a rule to overflow into next rule and overwriting 2 bytes of it. **Please note MAGIC and flag are located just after 16 rules**
At first glance it seems we should create 16 rules and overflow last rule to MAGIC and overwrite to use menu #6 and get the flag. After some time we deduce we cant do such a thing. since first we can write 2 bytes and the due to using fgets in reading type a null byte will be written after 2 bytes!  

## vuln #2

In all functions you can select `rule_index = 0`. So after subtracting by `1` we can underflow the rules and leak or overwrite 28 bytes behind of rules. As i told before we have a menu table which is located exactly before rules array!. So we can overwrite the table and write flag addr and after printing menu we can leak the flag :).


## Exploiting 

The menu table is located at `0x0041294C`.  
flag is at `0x00412B31`.  

In `0x40E960` menu table filled with menu strings at `0x0040F130` (8 addresses).  

Due to randomization we can use `print_rule` with `idx = 0` to leak address of one menu string and then calculate address of flag. (After running the code on remote i noticed there's no randomization (fork?) anyway we need the address to locate flag for the first time). Based on my analysis using leakage flag offset is `0x00412B31 - 0x0040F168 = 0x39c9`.  
Then we can use `edit_rule` with `idx = 0` to overwrite the table with address of flag and leak the flag.

The flag is `flag{w3_f3ll_pr3tty_f4r_d0wn_th3_w1nd0ws_r4bb1t_h0le_huh}`.

You can see full exploit [here](firewall_sol.py).