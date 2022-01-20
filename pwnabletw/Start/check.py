#!usr/bin/python

from pwn import *

f = open("str", 'wb')

s = p32(0x3a465443) + p32(0x20656874) + p32(0x20747261) + p32(0x74732073) + p32(0x2774654c)

f.write(s)
f.close()






