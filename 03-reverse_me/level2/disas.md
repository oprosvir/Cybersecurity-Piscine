## Disassembly of level2

```c
// ok
   0x000012a0 <+0>:     push   %ebp
   0x000012a1 <+1>:     mov    %esp,%ebp
   0x000012a3 <+3>:     push   %ebx
   0x000012a4 <+4>:     push   %eax
   0x000012a5 <+5>:     call   0x12aa <ok+10>
   0x000012aa <+10>:    pop    %ebx
   0x000012ab <+11>:    add    $0x5d56,%ebx        // base address: 0x7000

   0x000012b1 <+17>:    lea    -0x42ef(%ebx),%eax  // 0x2d11: "Good job."
   0x000012b7 <+23>:    mov    %eax,(%esp)
   0x000012ba <+26>:    call   0x1080 <puts@plt>   // puts("Good job.")
   0x000012bf <+31>:    add    $0x4,%esp           // clear stack
   0x000012c2 <+34>:    pop    %ebx
   0x000012c3 <+35>:    pop    %ebp
   0x000012c4 <+36>:    ret

// no
   0x00001220 <+0>:     push   %ebp
   0x00001221 <+1>:     mov    %esp,%ebp
   0x00001223 <+3>:     push   %ebx
   0x00001224 <+4>:     sub    $0x14,%esp          // 20 bytes
   0x00001227 <+7>:     call   0x122c <no+12>
   0x0000122c <+12>:    pop    %ebx
   0x0000122d <+13>:    add    $0x5dd4,%ebx        // base address: 0x7000
   0x00001233 <+19>:    mov    %ebx,-0x8(%ebp)

   0x00001236 <+22>:    lea    -0x4ff8(%ebx),%eax  // 0x2008: "Nope."
   0x0000123c <+28>:    mov    %eax,(%esp)
   0x0000123f <+31>:    call   0x1080 <puts@plt>   // puts("Nope.")
   0x00001244 <+36>:    mov    -0x8(%ebp),%ebx     // restore base address
   0x00001247 <+39>:    movl   $0x1,(%esp)         // put '1' on stack
   0x0000124e <+46>:    call   0x1090 <exit@plt>   // exit(1)

// main

   // prologue and setup
   0x000012d0 <+0>:     push   %ebp
   0x000012d1 <+1>:     mov    %esp,%ebp
   0x000012d3 <+3>:     push   %ebx
   0x000012d4 <+4>:     sub    $0x54,%esp             // allocate 84 bytes on stack
   0x000012d7 <+7>:     call   0x12dc <main+12>
   0x000012dc <+12>:    pop    %ebx
   0x000012dd <+13>:    add    $0x5d24,%ebx           // compute base address: 0x12dc + 0x5d24 = 0x7000
   0x000012e3 <+19>:    mov    %ebx,-0x40(%ebp)       // ebp-64
   0x000012e6 <+22>:    movl   $0x0,-0x8(%ebp)        // ebp-8 = 0

   // printf("Please enter key: ");
   0x000012ed <+29>:    lea    -0x42e5(%ebx),%eax
   0x000012f3 <+35>:    mov    %eax,(%esp)
   0x000012f6 <+38>:    call   0x1060 <printf@plt>
   0x000012fb <+43>:    mov    -0x40(%ebp),%ebx

   // read user input
   0x000012fe <+46>:    lea    -0x35(%ebp),%eax
   0x00001301 <+49>:    lea    -0x42d2(%ebx),%ecx
   0x00001307 <+55>:    mov    %ecx,(%esp)            // arg1 = "%23s"
   0x0000130a <+58>:    mov    %eax,0x4(%esp)         // arg2 = input buffer
   0x0000130e <+62>:    call   0x10c0 <__isoc99_scanf@plt>  // return value in %eax

   // validate scanf success
   0x00001313 <+67>:    mov    %eax,-0xc(%ebp)        // ebp-12 = scanf result
   0x00001316 <+70>:    mov    $0x1,%eax
   0x0000131b <+75>:    cmp    -0xc(%ebp),%eax        // result == 1 ?
   0x0000131e <+78>:    je     0x132c <main+92>       // success
   0x00001324 <+84>:    mov    -0x40(%ebp),%ebx
   0x00001327 <+87>:    call   0x1220 <no>            // fail (exit)

   // validate second character of input
   0x0000132c <+92>:    movsbl -0x34(%ebp),%ecx       // input[1]
   0x00001330 <+96>:    mov    $0x30,%eax             // ASCII '0'
   0x00001335 <+101>:   cmp    %ecx,%eax
   0x00001337 <+103>:   je     0x1345 <main+117>      // success
   0x0000133d <+109>:   mov    -0x40(%ebp),%ebx
   0x00001340 <+112>:   call   0x1220 <no>            // fail

   // validate first character of input
   0x00001345 <+117>:   movsbl -0x35(%ebp),%ecx       // input[0]
   0x00001349 <+121>:   mov    $0x30,%eax             // ASCII '0'
   0x0000134e <+126>:   cmp    %ecx,%eax
   0x00001350 <+128>:   je     0x135e <main+142>      // success
   0x00001356 <+134>:   mov    -0x40(%ebp),%ebx
   0x00001359 <+137>:   call   0x1220 <no>            // fail
   0x0000135e <+142>:   mov    -0x40(%ebp),%ebx       // restore base address

   // flush stdin
   0x00001361 <+145>:   mov    -0xc(%ebx),%eax        // load a pointer (stdin address)
   0x00001367 <+151>:   mov    (%eax),%eax            // %eax = stdin
   0x00001369 <+153>:   mov    -0xc(%ebx),%ecx        // redundant
   0x0000136f <+159>:   mov    %eax,(%esp)
   0x00001372 <+162>:   call   0x1070 <fflush@plt>
   0x00001377 <+167>:   mov    -0x40(%ebp),%ebx

   // initialize transformation buffer
   0x0000137a <+170>:   lea    -0x1d(%ebp),%eax
   0x0000137d <+173>:   xor    %ecx,%ecx              // ecx = 0
   0x0000137f <+175>:   mov    %eax,(%esp)            // arg1 = &out
   0x00001382 <+178>:   movl   $0x0,0x4(%esp)         // arg2 = 0 (value)
   0x0000138a <+186>:   movl   $0x9,0x8(%esp)         // arg3 = 9 (size)
   0x00001392 <+194>:   call   0x10b0 <memset@plt>    // memset(out, 0, 9)

   0x00001397 <+199>:   movb   $0x64,-0x1d(%ebp)      // out[0] = 'd'
   0x0000139b <+203>:   movb   $0x0,-0x36(%ebp)       // temp[3] = '\0'
   0x0000139f <+207>:   movl   $0x2,-0x14(%ebp)       // counter i = 2 (read "00+")
   0x000013a6 <+214>:   movl   $0x1,-0x10(%ebp)       // counter j = 1 (write "d+")

   // main processing loop
   0x000013ad <+221>:   mov    -0x40(%ebp),%ebx
   0x000013b0 <+224>:   lea    -0x1d(%ebp),%ecx       // %ecx = &out
   0x000013b3 <+227>:   mov    %esp,%eax
   0x000013b5 <+229>:   mov    %ecx,(%eax)
   0x000013b7 <+231>:   call   0x10a0 <strlen@plt>    // strlen(out), result in %eax
   0x000013bc <+236>:   mov    %eax,%ecx
   0x000013be <+238>:   xor    %eax,%eax              // clear %eax
   0x000013c0 <+240>:   cmp    $0x8,%ecx              // strlen(out) == 8 ?
   0x000013c3 <+243>:   mov    %al,-0x41(%ebp)        // flag
   0x000013c6 <+246>:   jae    0x13ee <main+286>      // jump if strlen(out) >= 8

   0x000013cc <+252>:   mov    -0x40(%ebp),%ebx
   0x000013cf <+255>:   mov    -0x14(%ebp),%eax       // eax = i
   0x000013d2 <+258>:   mov    %eax,-0x48(%ebp)       // tmp_i
   0x000013d5 <+261>:   lea    -0x35(%ebp),%ecx
   0x000013d8 <+264>:   mov    %esp,%eax
   0x000013da <+266>:   mov    %ecx,(%eax)
   0x000013dc <+268>:   call   0x10a0 <strlen@plt>    // strlen(input), result in %eax
   0x000013e1 <+273>:   mov    %eax,%ecx
   0x000013e3 <+275>:   mov    -0x48(%ebp),%eax
   0x000013e6 <+278>:   cmp    %ecx,%eax              // cmp i & input_length
   0x000013e8 <+280>:   setb   %al                    // al = 1 if i < input_length
   0x000013eb <+283>:   mov    %al,-0x41(%ebp)        // flag = %al (1 or 0)

   // exit condition (i > input_length && )
   0x000013ee <+286>:   mov    -0x41(%ebp),%al
   0x000013f1 <+289>:   test   $0x1,%al               // flag != 0 ?
   0x000013f3 <+291>:   jne    0x13fe <main+302>      // jump to loop body
   0x000013f9 <+297>:   jmp    0x144a <main+378>      // exit loop

   // loop body
   0x000013fe <+302>:   mov    -0x40(%ebp),%ebx
   0x00001401 <+305>:   mov    -0x14(%ebp),%eax       // eax = i
   0x00001404 <+308>:   mov    -0x35(%ebp,%eax,1),%al // al = input[i]
   0x00001408 <+312>:   mov    %al,-0x39(%ebp)        // temp[0] = input[i]

   0x0000140b <+315>:   mov    -0x14(%ebp),%eax       // eax = i
   0x0000140e <+318>:   mov    -0x34(%ebp,%eax,1),%al // input[i+1] (-0x34 = -0x35 + 1)
   0x00001412 <+322>:   mov    %al,-0x38(%ebp)        // temp[1] = input[i+1]

   0x00001415 <+325>:   mov    -0x14(%ebp),%eax       // eax = i
   0x00001418 <+328>:   mov    -0x33(%ebp,%eax,1),%al // input[i+2]
   0x0000141c <+332>:   mov    %al,-0x37(%ebp)        // temp[2] = input[i+2]

   0x0000141f <+335>:   lea    -0x39(%ebp),%eax       // eax = &temp
   0x00001422 <+338>:   mov    %eax,(%esp)
   0x00001425 <+341>:   call   0x10d0 <atoi@plt>      // atoi(tmp)
   0x0000142a <+346>:   mov    %al,%cl
   0x0000142c <+348>:   mov    -0x10(%ebp),%eax       // eax = j
   0x0000142f <+351>:   mov    %cl,-0x1d(%ebp,%eax,1) // out[j] = char(atoi)

   0x00001433 <+355>:   mov    -0x14(%ebp),%eax
   0x00001436 <+358>:   add    $0x3,%eax              // i + 3
   0x00001439 <+361>:   mov    %eax,-0x14(%ebp)

   0x0000143c <+364>:   mov    -0x10(%ebp),%eax
   0x0000143f <+367>:   add    $0x1,%eax              // j + 1
   0x00001442 <+370>:   mov    %eax,-0x10(%ebp)
   0x00001445 <+373>:   jmp    0x13ad <main+221>      // jump to loop start

   // finish string and compare
   0x0000144a <+378>:   mov    -0x40(%ebp),%ebx
   0x0000144d <+381>:   mov    -0x10(%ebp),%eax       // eax = j
   0x00001450 <+384>:   movb   $0x0,-0x1d(%ebp,%eax,1)   // out[j] = '\0'

   0x00001455 <+389>:   lea    -0x1d(%ebp),%ecx       // ecx = &out
   0x00001458 <+392>:   lea    -0x42cd(%ebx),%edx     // 0x2d33: "delabere"
   0x0000145e <+398>:   mov    %esp,%eax
   0x00001460 <+400>:   mov    %edx,0x4(%eax)         // arg2 = edx
   0x00001463 <+403>:   mov    %ecx,(%eax)            // arg1 = ecx
   0x00001465 <+405>:   call   0x1040 <strcmp@plt>    // strcmp(out, "delabere")
   0x0000146a <+410>:   cmp    $0x0,%eax
   0x0000146d <+413>:   jne    0x1480 <main+432>      // fail (not equal)

   0x00001473 <+419>:   mov    -0x40(%ebp),%ebx
   0x00001476 <+422>:   call   0x12a0 <ok>            // success (equal)
   0x0000147b <+427>:   jmp    0x1488 <main+440>

   0x00001480 <+432>:   mov    -0x40(%ebp),%ebx
   0x00001483 <+435>:   call   0x1220 <no>

   // epilogue
   0x00001488 <+440>:   xor    %eax,%eax              // return 0
   0x0000148a <+442>:   add    $0x54,%esp             // restore sctack pointer
   0x0000148d <+445>:   pop    %ebx
   0x0000148e <+446>:   pop    %ebp
   0x0000148f <+447>:   ret
```

## Stack Layout for main function

```
High addresses
+-----------------------------+
| return address (4 bytes)    |
+-----------------------------+  %ebp + 4
| saved %ebp (4 bytes)        |
+-----------------------------+  %ebp
| saved %ebx (4 bytes)        |
+-----------------------------+  %ebp - 4
| unused local var (4 bytes)  |
+-----------------------------+  %ebp - 8   (movl $0x0, -0x8(%ebp))
| scan_result  (4 bytes)      |
+-----------------------------+  %ebp - 12  (-0xc(%ebp))
| j counter (4 bytes)         |
+-----------------------------+  %ebp - 16  (-0x10(%ebp))
| i counter (4 bytes)         |
+-----------------------------+  %ebp - 20  (-0x14(%ebp))
| out[9]                      |
+-----------------------------+  %ebp - 29  (-0x1d(%ebp))
| input[24]                   |
+-----------------------------+  %ebp - 53  (-0x35(%ebp))
| temp[3] = '\0'              |
+-----------------------------+  %ebp - 54  (-0x36(%ebp))
| temp[2]                     |
+-----------------------------+  %ebp - 55  (-0x37(%ebp))
| temp[1]                     |
+-----------------------------+  %ebp - 56  (-0x38(%ebp))
| temp[0]                     |
+-----------------------------+  %ebp - 57  (-0x39(%ebp))
|             ...             |
+-----------------------------+  %ebp - 60
| saved GOT base (4 bytes)    |
+-----------------------------+  %ebp - 64  (-0x40(%ebp))
| flag (1 byte)               |
+-----------------------------+  %ebp - 65  (-0x41(%ebp))
|             ...             |
+-----------------------------+  %ebp - 68
| tmp_i (4 bytes)             |
+-----------------------------+  %ebp - 72  (-0x48(%ebp))
|             ...             |
+-----------------------------+  %ebp - 84  (-0x54(%ebp))
Low addresses
```
