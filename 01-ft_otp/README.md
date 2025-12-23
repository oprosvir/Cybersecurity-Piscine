# ft_otp - TOTP Generator

Time-based One-Time Password (TOTP) generator implementation based on RFC 6238 and RFC 4226.

## Description

ft_otp is a command-line tool that generates temporary passwords (OTP) that change every 30 seconds. This is the same technology used by Google Authenticator, Authy, and other two-factor authentication apps.

## Installation

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

Or manually:
```bash
pip install cryptography qrcode pillow
```

### 2. Make executable

```bash
chmod +x ft_otp.py
```

## Examples

### Complete workflow

```bash
# 1. Generate random hex key
python3 -c "import secrets; import sys; sys.stdout.write(secrets.token_hex(32))" > key.hex

# 2. Store and encrypt the key
./ft_otp.py -g key.hex

# 3. Generate OTP code
./ft_otp.py -k ft_otp.key
836492

# 4. Wait 30 seconds and generate again
./ft_otp.py -k ft_otp.key
123518
```

## How it works

### Encryption

The key is encrypted before storage using:
- **Fernet** (symmetric encryption: AES-128-CBC + HMAC-SHA256)
- **PBKDF2** (key derivation from environment variables)
- **Salt** (16 random bytes, stored with encrypted data)

**Key derivation:**
```
encryption_key = PBKDF2(
    password = $USER + "/ft_otp_secret_2025",
    salt = random_16_bytes,
    iterations = 100,000,
    hash = SHA256
)
```

### TOTP Algorithm (RFC 6238)

```
TOTP = HOTP(K, C)

where:
  K = secret key
  C = ⌊(T - T0) / X⌋
  T = current Unix time
  T0 = 0 (epoch)
  X = 30 seconds (time step)
```

### HOTP Algorithm (RFC 4226)

```
1. Generate HMAC-SHA1(K, C)
2. Extract 4 bytes using dynamic truncation
3. Convert to 6-digit code: truncated % 1,000,000
```

## Testing

### Verify against oathtool

```bash
# Install oathtool
sudo apt-get install oathtool

# Compare outputs
oathtool --totp $(cat key.hex)
./ft_otp.py -k ft_otp.key

# Both should output the same 6-digit code
```

## Bonus Features

### QR Code Generation

When storing a key with `-g`, a QR code is automatically generated in TOTP URI format:

```
otpauth://totp/ft_otp?secret=BASE32_SECRET&issuer=oprosvir
```

This QR code can be scanned by:
- Google Authenticator
- Authy
- Microsoft Authenticator
- Any TOTP-compatible app

## Security Considerations

### File Permissions

Encrypted key file is automatically set to `600` (read/write for owner only):
```bash
ls -la ft_otp.key
```

### Limitations

- Encryption key based on `$USER` environment variable
- If `ft_otp.key` is copied to another user/system, it won't decrypt

## References

- [RFC 6238 - TOTP: Time-Based One-Time Password Algorithm](https://datatracker.ietf.org/doc/html/rfc6238)
- [RFC 4226 - HOTP: An HMAC-Based One-Time Password Algorithm](https://datatracker.ietf.org/doc/html/rfc4226)
