# Stockholm: Ransomware Simulator

Stockholm is a Python-based simulator of ransomware behavior, designed for educational purposes in cybersecurity. It encrypts files in the `~/infection` directory using modern cryptography (Argon2id key derivation + Fernet symmetric encryption), mimicking WannaCry's file selection and extension appending (`.ft`).

**Warning:** This is a simulation tool. Do not run it on real data or systems. Use only in controlled environments for learning.

## Features

- **File Encryption:** Encrypts files with extensions matching WannaCry's list (e.g., `.docx`, `.jpg`, `.pdf`).
- **Reversible:** Supports decryption with the same key.
- **Secure Key Derivation:** Uses Argon2id (memory-hard function) to derive keys from passwords.

## Installation

```bash
make all
```

This will:
- Install required dependencies (`cryptography`, `argon2-cffi`)
- Make the script executable
- Create `~/infection/` and populate it with test files

## Usage

### Encrypt files in `~/infection/`

```bash
./stockholm.py <key>
```

### Decrypt files in `~/infection/`

```bash
./stockholm.py -r <key>
```

### Options

| Flag | Long | Description |
|------|------|-------------|
| `-r KEY` | `--reverse KEY` | Decrypt files using the provided key |
| `-s` | `--silent` | Suppress all output |
| `-v` | `--version` | Show version |
| `-h` | `--help` | Show help message |

## Encryption

- Algorithm: **Fernet** (AES-128-CBC + HMAC-SHA256) — authenticated symmetric encryption
- Key derivation: **Argon2id** (memory-hard KDF, OWASP recommended, RFC 9106)
  - `time_cost=2`, `memory_cost=19456` (19 MB), `parallelism=1`
- Per-file random salt (16 bytes) embedded in file header
- Encrypted files are renamed with `.ft` extension

## Clean up

```bash
make clean
```

Removes `~/infection/` directory entirely.