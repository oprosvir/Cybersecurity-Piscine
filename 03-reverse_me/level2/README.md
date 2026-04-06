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

## 2. Overall Logic Summary

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