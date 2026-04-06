# Level 2

## 1. Binary Analysis

The binary is an ELF 32-bit LSB PIE executable. Using GDB, we inspect the available functions:

```bash
$ gdb ./level2
(gdb) info functions
...
0x00001220  no
0x00001260  xd
0x000012a0  ok
0x000012d0  main
0x00001490  xxd
0x000014d0  n
0x00001500  xxxd
0x00001540  ww
0x000015b0  xyxxd
```

Only `ok`, `no`, and `main` are relevant to the program logic. The other functions are distractions that print text and do not affect the password check.

```bash
(gdb) disas main
(gdb) disas no
(gdb) disas ok
```

Strings are stored in `.rodata` and accessed relative to the GOT base. For example:

```bash
(gdb) print /x 0x7000-0x42e5
$4 = 0x2d1b
(gdb) x/s 0x2d1b
0x2d1b: "Please enter key: "
```

## 2. Password Validation Logic

- The program expects input starting with `'00'`, followed by groups of 3 digits (e.g., `"00100102"`).
- It builds an output string starting with `'d'`.
- Then for each 3-digit group starting from index 2, it converts the group with `atoi()` and writes the low byte of the result as a character.
- The final reconstructed string is compared with the hardcoded string `"delabere"`.
- If they match, the program prints `Good job.`; otherwise, it prints `Nope.`

Therefore, the final input should start with `00`. The program itself sets `'d'` at the beginning, so we only need to encode the remaining part: `"elabere"`.

- `e` = `101`
- `l` = `108`
- `a` = `097`
- `b` = `098`
- `e` = `101`
- `r` = `114`
- `e` = `101`

So the input is: `'00'` (prefix) + `'101'` + `'108'` + `'097'` + `'098'` + `'101'` + `'114'` + `'101'`.

```
00101108097098101114101
```

## Bonus: Patching to Accept Any Password

The bonus goal here is to make the program call `ok()` regardless of input. To accept any input, we need to patch 3 checks: 2 `no()` calls before the loop, and the final `strcmp` check.

First inspect the binary to confirm the exact bytes:

```bash
objdump -d ./level2
```

| Check           | Address          | Opcode | What to patch |
| --------------- | ---------------- | ------ | ------------- |
| `input[1] != '0'` | `0x1340` - `call no` | `e8 db fe ff ff` | `nop` x5 |
| `input[0] != '0'` | `0x1359` - `call no` | `e8 c2 fe ff ff` | `nop` x5 |
| `strcmp != 0`     | `0x146d` - `jne`     | `0f 85 0d 00 00 00` | `nop` x6 |

### Patch with `dd`

```bash
cp level2 level2_patched

# input[1] check: 0x1340 = 4928
printf '\x90\x90\x90\x90\x90' | dd of=./level2_patched bs=1 seek=4928 conv=notrunc

# input[0] check: 0x1359 = 4953
printf '\x90\x90\x90\x90\x90' | dd of=./level2_patched bs=1 seek=4953 conv=notrunc

# strcmp jne (6 bytes): 0x146d = 5229
printf '\x90\x90\x90\x90\x90\x90' | dd of=./level2_patched bs=1 seek=5229 conv=notrunc
```

Verify the patches:

```bash
objdump -d ./level2_patched | grep -A3 "1340:\|1359:\|146d:"
```

Test the patched binary:

```bash
echo "anything" | ./level2_patched
# Good job.

echo "xyz" | ./level2_patched
# Good job.
```