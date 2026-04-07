## Disassembly of level3

```c
// ___syscall_malloc (failure)
   0x12e0 <+0>:     push   %rbp                    // save caller's base pointer
   0x12e1 <+1>:     mov    %rsp,%rbp               // Set up stack frame
   0x12e4 <+4>:     lea    0xd48(%rip),%rdi        # 0x2033  // Load address of "Nope." string
   0x12eb <+11>:    call   0x1030 <puts@plt>       // Print the string
   0x12f0 <+16>:    mov    $0x1,%edi               // Exit code 1 (failure)
   0x12f5 <+21>:    call   0x10b0 <exit@plt>       // Exit program

// ____syscall_malloc (success)
   0x1300 <+0>:     push   %rbp
   0x1301 <+1>:     mov    %rsp,%rbp
   0x1304 <+4>:     lea    0xd2e(%rip),%rdi        # 0x2039  // "Good job."
   0x130b <+11>:    call   0x1030 <puts@plt>
   0x1310 <+16>:    pop    %rbp                    // Restore base pointer
   0x1311 <+17>:    ret                            // Return to caller

// main
   // stack setup and prompt
   0x1320 <+0>:     push   %rbp
   0x1321 <+1>:     mov    %rsp,%rbp
   0x1324 <+4>:     sub    $0x60,%rsp              // allocate 96 bytes of locals
   0x1328 <+8>:     movl   $0x0,-0x4(%rbp)         // unused = 0
   0x132f <+15>:    lea    0xd0d(%rip),%rdi        # 0x2043 // "Please enter key: "
   0x1336 <+22>:    mov    $0x0,%al                // no float args
   0x1338 <+24>:    call   0x1050 <printf@plt>

   // read input and validate scanf return
   0x133d <+29>:    lea    -0x40(%rbp),%rsi        // rsi = &input[0]
   0x1341 <+33>:    lea    0xd0e(%rip),%rdi        # 0x2056  // "%23s"
   0x1348 <+40>:    mov    $0x0,%al                // no float args
   0x134a <+42>:    call   0x10a0 <__isoc99_scanf@plt>  // Read input (up to 23 chars)
   0x134f <+47>:    mov    %eax,-0x8(%rbp)         // scanf_ret = eax
   0x1352 <+50>:    mov    $0x1,%eax
   0x1357 <+55>:    cmp    -0x8(%rbp),%eax         // scanf_ret == 1 ?
   0x135a <+58>:    je     0x1365 <main+69>        // yes -> continue
   0x1360 <+64>:    call   0x12e0 <___syscall_malloc>  // no -> fail

   // prefix checks: input must start with "42"
   0x1365 <+69>:    movsbl -0x3f(%rbp),%ecx        // ecx = (int)input[1]
   0x1369 <+73>:    mov    $0x32,%eax              // '2' (ASCII 50)
   0x136e <+78>:    cmp    %ecx,%eax
   0x1370 <+80>:    je     0x137b <main+91>        // pass
   0x1376 <+86>:    call   0x12e0 <___syscall_malloc>  // fail

   0x137b <+91>:    movsbl -0x40(%rbp),%ecx        // ecx = (int)input[0]
   0x137f <+95>:    mov    $0x34,%eax              // '4' (ASCII 52)
   0x1384 <+100>:   cmp    %ecx,%eax
   0x1386 <+102>:   je     0x1391 <main+113>       // pass
   0x138c <+108>:   call   0x12e0 <___syscall_malloc>  // fail

   // buffer initialization
   0x1391 <+113>:   mov    0x2c48(%rip),%rax        # 0x3fe0  // stdin pointer
   0x1398 <+120>:   mov    (%rax),%rdi             // dereference to get FILE* for stdin
   0x139b <+123>:   call   0x1080 <fflush@plt>     // flush stdin

   0x13a0 <+128>:   lea    -0x21(%rbp),%rdi        // rdi = &out[0]
   0x13a4 <+132>:   xor    %esi,%esi               // fill byte = 0
   0x13a6 <+134>:   mov    $0x9,%edx               // n = 9
   0x13ab <+139>:   call   0x1060 <memset@plt>     // memset(out, 0, 9)

   0x13b0 <+144>:   movb   $0x2a,-0x21(%rbp)       // out[0] = '*'  (42)
   0x13b4 <+148>:   movb   $0x0,-0x41(%rbp)        // temp[3] = '\0'
   0x13b8 <+152>:   movq   $0x2,-0x18(%rbp)        // in_idx  = 2  (skip "42" prefix)
   0x13c0 <+160>:   movl   $0x1,-0xc(%rbp)         // out_idx = 1  (out[0] already set to '*')

   // decoding loop: loop condition is checked at the top each iteration
   // --- loop top ---
   0x13c7 <+167>:   lea    -0x21(%rbp),%rdi        // rdi = &out
   0x13cb <+171>:   call   0x1040 <strlen@plt>     // strlen(out)
   0x13d0 <+176>:   mov    %rax,%rcx
   0x13d3 <+179>:   xor    %eax,%eax
   0x13d5 <+181>:   cmp    $0x8,%rcx               // Compare length with 8
   0x13d9 <+185>:   mov    %al,-0x45(%rbp)         // Store comparison result (0 or 1)
   0x13dc <+188>:   jae    0x1403 <main+227>       // If length >= 8, jump

   // strlen(out) < 8: check in_idx < strlen(input)
   0x13e2 <+194>:   mov    -0x18(%rbp),%rax        // Load current index
   0x13e6 <+198>:   mov    %rax,-0x50(%rbp)        // temp copy in_idx
   0x13ea <+202>:   lea    -0x40(%rbp),%rdi
   0x13ee <+206>:   call   0x1040 <strlen@plt>     // rcx = strlen(input)
   0x13f3 <+211>:   mov    %rax,%rcx
   0x13f6 <+214>:   mov    -0x50(%rbp),%rax
   0x13fa <+218>:   cmp    %rcx,%rax               // in_idx < strlen(input) ?
   0x13fd <+221>:   setb   %al                     // al = 1 if in_idx < strlen(input)
   0x1400 <+224>:   mov    %al,-0x45(%rbp)         // loop_cond = al

   // --- loop condition check ---
   0x1403 <+227>:   mov    -0x45(%rbp),%al
   0x1406 <+230>:   test   $0x1,%al                // Test if bit 0 is set
   0x1408 <+232>:   jne    0x1413 <main+243>       // If true, continue processing
   0x140e <+238>:   jmp    0x1461 <main+321>       // Else, jump to end
   // The loop continues as long as both: strlen(out) < 8 — output buffer not yet full, in_idx < strlen(input) — there are still input chars to consume

   // loop body
   // Read 3 chars from input[in_idx..in_idx+2] into temp
   0x1413 <+243>:   mov    -0x18(%rbp),%rax        // Load current index
   0x1417 <+247>:   mov    -0x40(%rbp,%rax,1),%al  // Load char from input[index]
   0x141b <+251>:   mov    %al,-0x44(%rbp)         // temp[0] = input[in_idx]

   0x141e <+254>:   mov    -0x18(%rbp),%rax        // Load index
   0x1422 <+258>:   mov    -0x3f(%rbp,%rax,1),%al  // Load char from input[index+1]
   0x1426 <+262>:   mov    %al,-0x43(%rbp)         // temp[1] = input[in_idx+1]

   0x1429 <+265>:   mov    -0x18(%rbp),%rax        // Load index
   0x142d <+269>:   mov    -0x3e(%rbp,%rax,1),%al  // Load char from input[index+2]
   0x1431 <+273>:   mov    %al,-0x42(%rbp)         // temp[2] = input[in_idx+2]

   0x1434 <+276>:   lea    -0x44(%rbp),%rdi        // rdi = &temp[0]
   0x1438 <+280>:   call   0x1090 <atoi@plt>       // eax = atoi(triplet)
   0x143d <+285>:   mov    %al,%cl                 // cl  = low byte of result

   0x143f <+287>:   movslq -0xc(%rbp),%rax         // rax = (int64)out_idx
   0x1443 <+291>:   mov    %cl,-0x21(%rbp,%rax,1)  // out[out_idx] = (char)atoi(triplet)

   // advance both indices
   0x1447 <+295>:   mov    -0x18(%rbp),%rax
   0x144b <+299>:   add    $0x3,%rax
   0x144f <+303>:   mov    %rax,-0x18(%rbp)        // in_idx  += 3

   0x1453 <+307>:   mov    -0xc(%rbp),%eax
   0x1456 <+310>:   add    $0x1,%eax
   0x1459 <+313>:   mov    %eax,-0xc(%rbp)         // out_idx += 1

   0x145c <+316>:   jmp    0x13c7 <main+167>       // Loop back to check length
   // Each iteration consumes 3 characters from input and writes 1 decoded byte into the output buffer

   // null-terminate and strcmp
   0x1461 <+321>:   movslq -0xc(%rbp),%rax
   0x1465 <+325>:   movb   $0x0,-0x21(%rbp,%rax,1)  // out[out_idx] = '\0'  (null-terminate)

   0x146a <+330>:   lea    0xb93(%rip),%rsi        # 0x2004 // "********"
   0x1471 <+337>:   lea    -0x21(%rbp),%rdi        // rdi = out
   0x1475 <+341>:   call   0x1070 <strcmp@plt>
   0x147a <+346>:   mov    %eax,-0x10(%rbp)        // cmp_result = strcmp(out, target)

   // switch dispatch on strcmp result
   0x147d <+349>:   mov    -0x10(%rbp),%eax        // cmp_result
   0x1480 <+352>:   mov    %eax,-0x54(%rbp)        // switch_val = cmp_result

   // switch (cmp_result) {
   // case -2:
   0x1483 <+355>:   sub    $0xfffffffe,%eax        // cmp_result - (-2)
   0x1486 <+358>:   je     0x1536 <main+534>       // if == -2, fail
   0x148c <+364>:   jmp    0x1491 <main+369>
   
   // case -1:
   0x1491 <+369>:   mov    -0x54(%rbp),%eax
   0x1494 <+372>:   sub    $0xffffffff,%eax        // cmp_result - (-1)
   0x1497 <+375>:   je     0x152c <main+524>       // if == -1, fail
   0x149d <+381>:   jmp    0x14a2 <main+386>
   
   // case 0:
   0x14a2 <+386>:   mov    -0x54(%rbp),%eax
   0x14a5 <+389>:   test   %eax,%eax               // cmp_result == 0 ?
   0x14a7 <+391>:   je     0x155e <main+574>       // if == 0, success
   0x14ad <+397>:   jmp    0x14b2 <main+402>
   
   // case 1:
   0x14b2 <+402>:   mov    -0x54(%rbp),%eax
   0x14b5 <+405>:   sub    $0x1,%eax               // cmp_result - 1
   0x14b8 <+408>:   je     0x1518 <main+504>       // if == 1, fail
   0x14be <+414>:   jmp    0x14c3 <main+419>
   
   // case 2:
   0x14c3 <+419>:   mov    -0x54(%rbp),%eax
   0x14c6 <+422>:   sub    $0x2,%eax               // cmp_result - 2
   0x14c9 <+425>:   je     0x1522 <main+514>       // if == 2, fail
   0x14cf <+431>:   jmp    0x14d4 <main+436>
   
   // case 3:
   0x14d4 <+436>:   mov    -0x54(%rbp),%eax
   0x14d7 <+439>:   sub    $0x3,%eax               // cmp_result - 3
   0x14da <+442>:   je     0x1540 <main+544>       // if == 3, fail
   0x14e0 <+448>:   jmp    0x14e5 <main+453>
   
   // case 4:
   0x14e5 <+453>:   mov    -0x54(%rbp),%eax
   0x14e8 <+456>:   sub    $0x4,%eax               // cmp_result - 4
   0x14eb <+459>:   je     0x154a <main+554>       // if == 4, fail
   0x14f1 <+465>:   jmp    0x14f6 <main+470>
   
   // case 5:
   0x14f6 <+470>:   mov    -0x54(%rbp),%eax
   0x14f9 <+473>:   sub    $0x5,%eax               // cmp_result - 5
   0x14fc <+476>:   je     0x1554 <main+564>       // if == 5, fail
   0x1502 <+482>:   jmp    0x1507 <main+487>
   
   // case 115:
   0x1507 <+487>:   mov    -0x54(%rbp),%eax
   0x150a <+490>:   sub    $0x73,%eax              // cmp_result - 115
   0x150d <+493>:   je     0x1568 <main+584>       // if == 115, fail
   0x1513 <+499>:   jmp    0x1572 <main+594>       // default: fail
   
   // fail branches for each case
   0x1518 <+504>:   call   0x12e0 <___syscall_malloc>  // fail for case 1
   0x151d <+509>:   jmp    0x1577 <main+599>

   0x1522 <+514>:   call   0x12e0 <___syscall_malloc>  // fail for case 2
   0x1527 <+519>:   jmp    0x1577 <main+599>

   0x152c <+524>:   call   0x12e0 <___syscall_malloc>  // fail for case -1
   0x1531 <+529>:   jmp    0x1577 <main+599>

   0x1536 <+534>:   call   0x12e0 <___syscall_malloc>  // fail for case -2
   0x153b <+539>:   jmp    0x1577 <main+599>

   0x1540 <+544>:   call   0x12e0 <___syscall_malloc>  // fail for case 3
   0x1545 <+549>:   jmp    0x1577 <main+599>

   0x154a <+554>:   call   0x12e0 <___syscall_malloc>  // fail for case 4
   0x154f <+559>:   jmp    0x1577 <main+599>

   0x1554 <+564>:   call   0x12e0 <___syscall_malloc>  // fail for case 5
   0x1559 <+569>:   jmp    0x1577 <main+599>

   0x155e <+574>:   call   0x1300 <____syscall_malloc>  // success for case 0
   0x1563 <+579>:   jmp    0x1577 <main+599>

   0x1568 <+584>:   call   0x12e0 <___syscall_malloc>  // fail for case 115
   0x156d <+589>:   jmp    0x1577 <main+599>

   0x1572 <+594>:   call   0x12e0 <___syscall_malloc>  // default fail
   0x1577 <+599>:   jmp    0x1577 <main+599>
   // }

   0x1577 <+599>:   xor    %eax,%eax   // return 0
   0x1579 <+601>:   add    $0x60,%rsp
   0x157d <+605>:   pop    %rbp
   0x157e <+606>:   ret
```

- `movb`: move byte (8-bit data)
- `movl`: move long (32-bit data)
- `movq`: move quad (64-bit data)
- `mov`: move (size inferred from operands, usually 32/64-bit)
- `movslq`: move with sign extension from 32-bit to 64-bit
- `movsbl`: move with sign extension from 8-bit to 32-bit

## Stack Layout for main function

```
+-----------------------------+
| saved %rip (8 bytes)        |
+-----------------------------+  %ebp + 8    (return address)
| saved %rbp (8 bytes)        |
+-----------------------------+  %rbp
| int    unused = 0 (4 bytes) |
+-----------------------------+  %rbp - 4    (-0x4(%rbp))
| int    scanf_ret (4 bytes)  |
+-----------------------------+  %rbp - 8    (-0x8(%rbp))
| int    out_idx (4 bytes)    |
+-----------------------------+  %rbp - 12   (-0xc(%rbp))
| int    cmp_result (4 bytes) |
+-----------------------------+  %rbp - 16   (-0x10(%rbp))
| long   in_idx (8 bytes)     |
+-----------------------------+  %rbp - 24   (-0x18(%rbp))
| char   out[9]               |
+-----------------------------+  %rbp - 33   (-0x21(%rbp))
| char   input[31]            |
+-----------------------------+  %rbp - 64   (-0x40(%rbp))
| char   temp[3] = '\0'       |
+-----------------------------+  %rbp - 65   (-0x41(%rbp))
| char   temp[3]              |
+-----------------------------+  %rbp - 68   (-0x44(%rbp))
| bool   loop_cond (1 byte)    |
+-----------------------------+  %rbp - 69   (-0x45(%rbp))
| long in_idx_saved (8 bytes) |
+-----------------------------+  %rbp - 80   (-0x50(%rbp))
| int    switch_val (4 bytes) |
+-----------------------------+  %rbp - 84   (-0x54(%rbp))
|             ...             |
+-----------------------------+  %rbp - 96   (-0x60(%ebp))  (end of frame)
```
