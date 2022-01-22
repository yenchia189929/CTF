# START

## 解題流程
### 檢查
#### checksec
![image](https://user-images.githubusercontent.com/59916058/150644673-f44ad00e-662f-43ee-9aa2-1108bb6ee805.png)

#### objdump 
```=
start:     file format elf32-i386


Disassembly of section .text:

08048060 <_start>:
 
 # save esp, return value
 8048060:	54                   	push   %esp
 8048061:	68 9d 80 04 08       	push   $0x804809d
 
 # init easx, ebx, ecx, edx to 0
 8048066:	31 c0                	xor    %eax,%eax
 8048068:	31 db                	xor    %ebx,%ebx
 804806a:	31 c9                	xor    %ecx,%ecx
 804806c:	31 d2                	xor    %edx,%edx
 
 # word "Let's start the CTF:""
 804806e:	68 43 54 46 3a       	push   $0x3a465443
 8048073:	68 74 68 65 20       	push   $0x20656874
 8048078:	68 61 72 74 20       	push   $0x20747261
 804807d:	68 73 20 73 74       	push   $0x74732073
 8048082:	68 4c 65 74 27       	push   $0x2774654c
 
 # system call int 80h (write)
 8048087:	89 e1                	mov    %esp,%ecx
 8048089:	b2 14                	mov    $0x14,%dl
 804808b:	b3 01                	mov    $0x1,%bl
 804808d:	b0 04                	mov    $0x4,%al
 804808f:	cd 80                	int    $0x80
 
 # system call int 80h (read)
 8048091:	31 db                	xor    %ebx,%ebx
 8048093:	b2 3c                	mov    $0x3c,%dl
 8048095:	b0 03                	mov    $0x3,%al
 8048097:	cd 80                	int    $0x80
 
 # return
 8048099:	83 c4 14             	add    $0x14,%esp
 804809c:	c3                   	ret

0804809d <_exit>:
 804809d:	5c                   	pop    %esp
 804809e:	31 c0                	xor    %eax,%eax
 80480a0:	40                   	inc    %eax
 80480a1:	cd 80                	int    $0x80
```
### 一步一步走

#### overflow塞shellcode!!!
因為在最一開始checksec的時候就知道他NX沒開，所以我們可以把 shellcode 放在 stack 上面！
- 輸入 0x14 長度把 "lets start the ctf:" 這段字蓋掉 
-  在return那邊蓋成system write的位置 (0x8048087) ，好來印出（獲得）一開始存在最下面的save esp的值 
-  因為 0x8048089 的地方還是有再多 0x14 的大小，所以我要再次塞滿0x14
-  第二次 ret 的地方直接塞 剛剛得到的esp + 0x14 的位置 (要加 0x14 是因為他剛剛)

|offset |init memory |ret 0x8048087後    |
|-------|------------|------------------|
|- 0x20 |let'        |aaaa              |
|- 0x18 |s st        |aaaa              |
|- 0x14 |art         |aaaa              |
|- 0x10 |the         |aaaa              |
|- 0xc  |CTF:        |aaaa              |
|- 0x8  |return      |0x8048087         |
|- 0x4  |save  esp   |用u32(recv(4))接esp| 
|- 0x0  |初esp位置    |aaaa              |
|+ 0x4  |            |aaaa              |
|+ 0x8  |            |aaaa              |
|+ 0xc  |            |aaaa              |
|+ 0x10 |            |getESP + 0x14     |
|+ 0x14 |            |shellcode         |

#### code


## 小知識：Ｄ
### INT 80H
在上面有看到這個東東是什麼呢？
int 0x80是 system call 用的東東，eax是他的opcode，ebx, ecx, edx, esi 等其他的 register 是他的 parameter 。
列出幾個可能常見的 opcode
```
exit      1
fork      2
read      3
write     4
open      5
close     6
waitpid   7
create    8
link      9
unlink    10
execve    11
...
```



