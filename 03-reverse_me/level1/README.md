# Level 1

## 1. Binary analysis

```bash
$ file level1
level1: ELF 32-bit LSB pie executable, Intel 80386, version 1 (SYSV),
dynamically linked, interpreter /lib/ld-linux.so.2, not stripped
```

| Field | Meaning |
|---|---|
| `ELF 32-bit` | Linux binary format, x86 architecture (32-bit registers: eax, esp...) |
| `LSB` | little-endian byte order |
| `PIE` | loaded at random address (ASLR) — raw address breakpoints won't work |
| `dynamically linked` | uses shared libraries (libc: strcmp, printf, scanf) |
| `not stripped` | debug symbols kept — function names visible in GDB |

## 2. Finding the password with ltrace

`ltrace` intercepts library calls and prints their arguments at runtime:

```bash
$ ltrace ./level1
printf("Please enter key: ")          = 18
scanf("%s", buf)   → input: AAAA
strcmp("AAAA", "__stack_check")        = -1
printf("Nope.\n")                      = 6
```

The second argument to `strcmp` is the secret password: **`__stack_check`**

```bash
$ echo "__stack_check" | ./level1
Please enter key: Good job.
```

## 3. Stack analysis (GDB + disassembly)

From `disassemble main`, we can map the stack frame layout:

```
ebp          ← frame base
ebp-0x04     ← saved ebx (push %ebx)
ebp-0x08     ← unused local var = 0
...
ebp-0x6c     ← input buffer (scanf writes here)   ← buf[0]
...
ebp-0x7a     ← password buffer (14 bytes, copied from .rodata)
ebp-0x80     ← saved ebx (GOT/data base for PIE)
esp          ← ebp - 0x84 (132 bytes allocated)
```

Input buffer size:
```bash
(gdb) print 0x6c - 0x08
$1 = 100 # bytes
```

We can also read strings directly from memory by computing their addresses.
The password is copied FROM `.rodata` `[ebx - 0x1ff8]` INTO `[ebp - 0x7a]`:
```c
0x000011ca <+10>:    call   0x11cf <main+15>
0x000011cf <+15>:    pop    %ebx
0x000011d0 <+16>:    add    $0x2e31,%ebx    // ebx = 0x11cf + 0x2e31 = 0x4000
0x000011e0 <+32>:    mov    -0x1ff8(%ebx),%eax  // 0x4000 - 0x1ff8 = 0x2008
0x000011e6 <+38>:    mov    %eax,-0x7a(%ebp)
```
```bash
(gdb) x/s 0x2008
0x2008: "__stack_check"
```

The same approach works for any string — compute `ebx - offset` to get the address:

```c
0x00001206 <+70>:    lea    -0x1fea(%ebx),%eax  // 0x4000 - 0x1fea = 0x2016
```
```bash
(gdb) x/s 0x2016
0x2016: "Please enter key: "
```

## Bonus: Patching to Accept Any Password

To make the program accept any password instead of the correct `"__stack_check"`, we modify the password check logic in the binary file. Instead of checking for a match and jumping to `"Nope"` on mismatch, we force the program to always proceed to the `"Good job."` message.

### Analysis of Check Logic
From the disassembler (`objdump -d ./level1`), we see the key part in the `main` function:
```c
123c: e8 ff fd ff ff       call   10a0 <strcmp@plt>  // Call strcmp to compare input password with "__stack_check"
1241: 83 f8 00             cmp    $0x0,%eax          // Compare strcmp result with 0 (0 means match)
1244: 0f 85 16 00 00 00    jne    1260 <main+0xa0>   // If not equal to 0, jump to "Nope"
124a: e8 41 fd ff ff       call   1090 <printf@plt>  // Print "Good job."
```

- `strcmp` returns 0 if strings are equal.
- `cmp $0x0, %eax` checks if the result is 0.
- `jne` (jump if not equal) jumps to failure if the password is incorrect.

### Patching Method
We replace the `jne` instruction (6 bytes: `0f 85 16 00 00 00`) with 6 NOP instructions (`90 90 90 90 90 90`). This means the program will always continue execution to `printf("Good job.")`, regardless of the comparison result.

- NOP (No Operation) is an empty instruction that does nothing.
- Replacing the conditional jump with NOP makes the program ignore the condition and always execute the success code.
- This does not change other parts of the program, only the check logic.

### Finding the file offset

To patch a file we need the byte position of the instruction. `readelf -S` gives us section addresses:

```bash
readelf -S ./level1 | grep ".text"
# [14] .text  PROGBITS  00001090  001090  0001ec  00  AX  0  0  16
#                       ^^^^^^^^  ^^^^^^
#                       vaddr     file offset
```

Since `vaddr == file offset` for `.text` (both `0x1090`), the file offset of any instruction equals its address directly:

```
jne is at vaddr 0x1244  ->  file offset 0x1244 = 4676 decimal
```

### Commands

```bash
# Copy the original file
cp level1 level1_patched

# Replace jne with NOP
printf '\x90\x90\x90\x90\x90\x90' | dd of=level1_patched bs=1 seek=4676 conv=notrunc

# Test
echo "wrongpassword" | ./level1_patched  # Should output "Good job."
./level1_patched  # Enter any password
```

**Alternative**: use `hexedit` for visual editing — navigate to offset `0x1244`,
replace `0f 85 16 00 00 00` with `90 90 90 90 90 90`, save with `Ctrl+X`.

```bash
hexedit level1_patched
00001234   86 89 E0 89  50 04 89 08  E8 FF FD FF  FF 83 F8 00  -> 90 90 90 90  ....P...............
00001248   90 90 <- 8B 5D  80 8D 83 2C  E0 FF FF 89  04 24 E8 05  FE FF FF E9  ...]...,.....$......
```

### Tools used

- **`objdump -d`** — disassembles the binary, showing each instruction as: address / hex bytes / mnemonic / operands.

- **`readelf -S`** — prints the ELF section table. Each row shows a section name, its virtual address (where it loads in RAM), and its file offset (position in the file). Used to confirm that `vaddr == file offset` for `.text`, so the instruction address equals its position in the file.

- **`dd`** — low-level copy utility that writes data directly to a specific byte position in a file. Flags used: `bs=1` (work byte by byte), `seek=4676` (start writing at byte 4676), `conv=notrunc` (do not truncate the file — only overwrite the target bytes).

- **`hexedit`** — interactive hex editor for visual byte editing. Navigate to offset `0x1244`, replace `0f 85 16 00 00 00` with `90 90 90 90 90 90`, save with `Ctrl+X`.

- **`0x90`** — the opcode for `NOP` (No Operation) in x86. The CPU reads it and does nothing, then moves to the next instruction. Six NOPs replace the 6-byte `jne`, effectively removing the conditional jump.

- **`LD_PRELOAD`** — environment variable that forces Linux to load a custom `.so` before libc, allowing functions like `strcmp` to be overridden at runtime without modifying the binary. Prohibited by the task — the patch must be permanent and inside the file itself.
