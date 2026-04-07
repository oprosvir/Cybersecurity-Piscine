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

This binary is 64-bit PIE, so all strings are addressed using **RIP-relative** `lea` instructions. This allows the code to work independently of where it is loaded in memory. Each string address is resolved as: `string_addr = address_of_next_instruction + offset`.

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

## 2. Password Validation Logic

The overall structure mirrors level2, with three key differences: the prefix is `"42"` instead of `"00"`, the initial buffer character is `'*'` (`42`) instead of `'d'`, and the `strcmp` result is dispatched through a **switch table** instead of a single `jne`.

The program:
- Reads input with `scanf("%23s", input)`
- Verifies `input[0] == '4'` and `input[1] == '2'`
- Initializes `out[0] = '*'`, then decodes groups of 3 digits from `input[2:]` via `atoi()` into `out[1:]`
- Compares the result against `"********"` (8 asterisks)

Since `out[0]` is already `'*'`, we need to encode 7 more `'*'` characters. `'*'` is ASCII `42`, so `atoi("042")` = 42, which gives us `'*'`.

So the remaining 7 groups are all `042`.

```
42042042042042042042042
```

## Bonus: Patching to Accept Any Password

First identify the patch targets with objdump:

```bash
objdump -d ./level3
```

| Check             | Address  | Opcode           | Bytes | Patch     |
| ----------------- | -------- | ---------------- | ----- | --------- |
| `input[1] != '2'` | `0x1376` | `e8 65 ff ff ff` | 5     | `nop` x5  |
| `input[0] != '4'` | `0x138c` | `e8 4f ff ff ff` | 5     | `nop` x5  |

The `strcmp` dispatch is trickier here than in level2 - instead of a single `jne`, the compiler emitted a **switch chain**.

Instead of patching the switch at all, we will patch `strcmp` call itself — replace it with `xor %eax,%eax` to force return value 0, then the switch naturally falls through to `case 0` -> success:

```bash
1475:       e8 f6 fb ff ff          call   1070 <strcmp@plt>
```

Replace with `31 c0 90 90 90` (xor %eax,%eax + 3 nops):
```bash
printf '\x31\xc0\x90\x90\x90' | dd of=./level3_patched bs=1 seek=5237 conv=notrunc
```

Now `cmp_result` is always `0`, the switch hits `case 0`, and `____syscall_malloc` is always called. No need to touch the switch chain at all.

### Patch with `dd`

```bash
cp level3 level3_patched

# input[1] != '2': 0x1376 = 4982 
printf '\x90\x90\x90\x90\x90' | dd of=./level3_patched bs=1 seek=4982 conv=notrunc

# input[0] != '4': 0x138c = 5004
printf '\x90\x90\x90\x90\x90' | dd of=./level3_patched bs=1 seek=5004 conv=notrunc

# strcmp always return 0 (xor %eax,%eax + nop x3): 0x1475 = 5237
printf '\x31\xc0\x90\x90\x90' | dd of=./level3_patched bs=1 seek=5237 conv=notrunc
```

Verify the patches:

```bash
objdump -d ./level3_patched | grep -A2 "1376:\|138c:\|1475:"
```

Test the patched binary:

```bash
./level3_patched  # Enter any password
# Good job.
```