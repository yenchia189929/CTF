#!/usr/bin/python3
from pwn import *

s = asm(shellcraft.i386.linux.sh())
print(s)


