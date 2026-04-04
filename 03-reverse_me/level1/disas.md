## Disassembly of main function

```c
Dump of assembler code for function main:
   // prologue
   0x000011c0 <+0>:     push   %ebp
   0x000011c1 <+1>:     mov    %esp,%ebp
   0x000011c3 <+3>:     push   %ebx
   0x000011c4 <+4>:     sub    $0x84,%esp          // allocate 132 bytes on stack

   // PIE trick: get current EIP into ebx
   0x000011ca <+10>:    call   0x11cf <main+15>    // push EIP on stack
   0x000011cf <+15>:    pop    %ebx                // ebx = EIP
   0x000011d0 <+16>:    add    $0x2e31,%ebx        // ebx = 0x11cf + 0x2e31 = 0x4000 (.got.plt base)
   0x000011d6 <+22>:    mov    %ebx,-0x80(%ebp)    // save .got.plt base on stack (restored after each call)
   0x000011d9 <+25>:    movl   $0x0,-0x8(%ebp)     // local var = 0 (unused)

   // copy password from .rodata onto stack (char password[] = "...")
   0x000011e0 <+32>:    mov    -0x1ff8(%ebx),%eax   // read 4 bytes from .rodata (0x4000-0x1ff8=0x2008)
   0x000011e6 <+38>:    mov    %eax,-0x7a(%ebp)     // write bytes 0-3 onto stack
   0x000011e9 <+41>:    mov    -0x1ff4(%ebx),%eax
   0x000011ef <+47>:    mov    %eax,-0x76(%ebp)     // bytes 4-7
   0x000011f2 <+50>:    mov    -0x1ff0(%ebx),%eax
   0x000011f8 <+56>:    mov    %eax,-0x72(%ebp)     // bytes 8-11
   0x000011fb <+59>:    mov    -0x1fec(%ebx),%ax
   0x00001202 <+66>:    mov    %ax,-0x6e(%ebp)      // bytes 12-13 (%ax = 2 bytes), total 14 bytes

   // printf("Please enter key: ")
   0x00001206 <+70>:    lea    -0x1fea(%ebx),%eax   // eax = address of "Please enter key: " in .rodata (0x2016)
   0x0000120c <+76>:    mov    %eax,(%esp)          // arg1 = format string
   0x0000120f <+79>:    call   0x1060 <printf@plt>  // printf("Please enter key: ")
   0x00001214 <+84>:    mov    -0x80(%ebp),%ebx     // restore ebx (may be clobbered by call)

   // scanf("%s", input)
   0x00001217 <+87>:    lea    -0x6c(%ebp),%eax     // eax = address of input buffer
   0x0000121a <+90>:    lea    -0x1fd7(%ebx),%ecx   // ecx = address of "%s" in .rodata
   0x00001220 <+96>:    mov    %ecx,(%esp)          // arg1 = "%s"
   0x00001223 <+99>:    mov    %eax,0x4(%esp)       // arg2 = input buffer
   0x00001227 <+103>:   call   0x1070 <__isoc99_scanf@plt>
   0x0000122c <+108>:   mov    -0x80(%ebp),%ebx     // restore ebx

   // strcmp(input, password)
   0x0000122f <+111>:   lea    -0x6c(%ebp),%ecx     // ecx = input buffer
   0x00001232 <+114>:   lea    -0x7a(%ebp),%edx     // edx = password buffer (on stack)
   0x00001235 <+117>:   mov    %esp,%eax
   0x00001237 <+119>:   mov    %edx,0x4(%eax)       // arg2 = password
   0x0000123a <+122>:   mov    %ecx,(%eax)          // arg1 = input
   0x0000123c <+124>:   call   0x1040 <strcmp@plt>
   0x00001241 <+129>:   cmp    $0x0,%eax            // strcmp returns 0 if equal
   0x00001244 <+132>:   jne    0x1260 <main+160>    // if not equal → jump to fail

   // success
   0x0000124a <+138>:   mov    -0x80(%ebp),%ebx
   0x0000124d <+141>:   lea    -0x1fd4(%ebx),%eax   // address of "Good job.\n"
   0x00001253 <+147>:   mov    %eax,(%esp)
   0x00001256 <+150>:   call   0x1060 <printf@plt>
   0x0000125b <+155>:   jmp    0x1271 <main+177>    // jump to epilogue

   // fail
   0x00001260 <+160>:   mov    -0x80(%ebp),%ebx
   0x00001263 <+163>:   lea    -0x1fc9(%ebx),%eax   // address of "Nope.\n"
   0x00001269 <+169>:   mov    %eax,(%esp)
   0x0000126c <+172>:   call   0x1060 <printf@plt>

   // epilogue
   0x00001271 <+177>:   xor    %eax,%eax    // return 0
   0x00001273 <+179>:   add    $0x84,%esp   // free stack frame
   0x00001279 <+185>:   pop    %ebx         // restore ebx
   0x0000127a <+186>:   pop    %ebp         // restore ebp
   0x0000127b <+187>:   ret
End of assembler dump.
```

## Stack Layout for main function

```
High addresses
+-----------------------------+
| return address (4 bytes)    |
+-----------------------------+  %ebp + 4  (return address from main)
| saved %ebp (4 bytes)        |
+-----------------------------+  %ebp       (old %ebp)
| saved %ebx (4 bytes)        |
+-----------------------------+  %ebp - 4   (saved %ebx)
| unused local var (4 bytes)  |
+-----------------------------+  %ebp - 8   (movl $0x0, -0x8(%ebp))
| input[100] (100 bytes)      |
|   (buffer for scanf)        |
+-----------------------------+  %ebp - 108 (-0x6c(%ebp))
| password[14] (14 bytes)     |
|   (copied from .rodata)     |
+-----------------------------+  %ebp - 122 (-0x7a(%ebp))
| saved GOT base (4 bytes)    |
+-----------------------------+  %ebp - 128 (mov %ebx, -0x80(%ebp))
| rest of stack (up to 0x84)  |
+-----------------------------+  %ebp - 132 (end of frame)
Low addresses
```

