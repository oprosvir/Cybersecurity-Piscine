# Level 3

## 1. Binary Analysis

```bash
$ file level3  
level3: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=26a7c615f73fac182924d75acbfbe7363560cdb2, for GNU/Linux 3.2.0, not stripped
```

The binary is an ELF 64-bit LSB PIE executable. This means:
- calling convention uses registers `rdi`, `rsi`, `rdx`, `rcx`, `r8`, `r9` for arguments instead of the stack
- the stack base pointer is `rbp` instead of `ebp`
- pointers are 8 bytes wide instead of 4

Using GDB, we inspect the available functions:

```bash
...
0x00000000000011c0  wt
0x00000000000011e0  nice
0x0000000000001200  try
0x0000000000001220  but
0x0000000000001240  this
0x0000000000001260  it
0x0000000000001280  not
0x00000000000012a0  that
0x00000000000012c0  easy
0x00000000000012e0  ___syscall_malloc
0x0000000000001300  ____syscall_malloc
0x0000000000001320  main
```

The functions `wt`, `nice`, `try`, `but`, `this`, `it`, `not`, `that`, and `easy` appear to be distractions. The relevant functions are `main`, `___syscall_malloc`, and `____syscall_malloc`. Despite their names suggesting memory allocation, these are custom functions that contain the actual validation logic - their names are chosen to mislead.

```bash
(gdb) disas main
(gdb) disas ___syscall_malloc
(gdb) disas ____syscall_malloc
```

This binary is 64-bit PIE, so all strings are addressed using **RIP-relative** `lea` instructions. Each string address is resolved as: `string_addr = address_of_next_instruction + offset`.

| Instruction address | RIP (next instr) | Offset   | Resolved addr | Usage                        |
| ------------------- | ---------------- | -------- | ------------- | ---------------------------- |
| `0x12e4`            | `0x12eb`         | `+0xd48` | `0x2033`      | `___syscall_malloc` message  |
| `0x1304`            | `0x130b`         | `+0xd2e` | `0x2039`      | `____syscall_malloc` message |
| `0x132f`            | `0x1336`         | `+0xd0d` | `0x2043`      | `printf` prompt              |
| `0x1341`            | `0x1348`         | `+0xd0e` | `0x2056`      | `scanf` format string        |
| `0x146a`            | `0x1471`         | `+0xb93` | `0x2004`      | `strcmp` target password     |

To inspect them all at once:
```bash
objdump -s -j .rodata ./level3

./level3:     file format elf64-x86-64

Contents of section .rodata:
 2000 01000200 2a2a2a2a 2a2a2a2a 006e6963  ....********.nic
 2010 65007472 79006275 74007468 69730069  e.try.but.this.i
 2020 74006e6f 742e0074 6861742e 00656173  t.not..that..eas
 2030 792e004e 6f70652e 00476f6f 64206a6f  y..Nope..Good jo
 2040 622e0050 6c656173 6520656e 74657220  b..Please enter 
 2050 6b65793a 20002532 337300             key: .%23s. 
```