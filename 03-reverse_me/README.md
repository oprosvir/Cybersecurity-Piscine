# Reverse Me - Binary Reverse Engineering

A set of three reverse engineering challenges focused on static and dynamic analysis of ELF binaries.

## Contents

- `level1/` - 32-bit PIE binary, simple string comparison
- `level2/` - 32-bit PIE binary, input encoding with `atoi`
- `level3/` - 64-bit PIE binary, switch-based validation

Each level folder contains:
- `levelN` - original binary
- `levelN_patched` - patched binary (bonus)
- `source.c` - reconstructed source
- `disas.md` - disassembly notes
- `password` - recovered password
- `README.md` - step-by-step solution

## Requirements

Recommended tools:
- `file`
- `strings`
- `ltrace`
- `gdb`
- `objdump`
- `readelf`
- `hexedit` (optional)
- `dd`

## Usage

Run a level binary and enter the recovered password:

```bash
./level1
./level2
./level3
```

For detailed walkthroughs and patching steps, see each level README.

## Notes

- All binaries are PIE, so absolute addresses are unreliable; use symbol names, relative offsets, or computed file offsets.
- Patched binaries are provided for the bonus task (accept any password).
- The `password` files contain the correct input for each level.
