#!/usr/bin/env python3

from cryptography.fernet import Fernet
import argparse
import base64
import hashlib
import sys
import os
import qrcode
import time
import hmac

TIME_STEP = 30

def validate(hex_key):
    if len(hex_key) < 64:
        return False
    if not all(c in '0123456789abcdefABCDEF' for c in hex_key):
        return False
    return True

def get_key(salt):
    env_data = os.getenv('USER', '') + '/ft_otp_secret_2025'
    kdf = hashlib.pbkdf2_hmac(
        'sha256',
        env_data.encode(),
        salt,
        100000
    )
    return base64.urlsafe_b64encode(kdf)

def encrypt(hex_key, filename='ft_otp.key'):
    salt = os.urandom(16)
    key = get_key(salt)
    f = Fernet(key)

    token = f.encrypt(hex_key.encode())
    with open(filename, 'wb') as file:
        file.write(salt + token)

    os.chmod(filename, 0o600)
    print(f"Key was successfully saved in {filename}")

def decrypt(filename='ft_otp.key'):
    with open(filename, 'rb') as file:
       data = file.read()

    salt = data[:16]
    token = data[16:]
    
    key = get_key(salt)
    f = Fernet(key)
    return f.decrypt(token).decode()

def generate_qr_code(hex_key):
    key_bytes = bytes.fromhex(hex_key)
    base32_key = base64.b32encode(key_bytes).decode('utf-8').rstrip('=')
    
    uri = f"otpauth://totp/ft_otp?secret={base32_key}&issuer=oprosvir"
    img = qrcode.make(uri)
    img.save("ft_otp_qr.png")
    print("QR code saved as ft_otp_qr.png")

def store_key(filepath):
    try:
        with open(filepath, 'r') as f:
            hex_key = f.read().strip()
        if not validate(hex_key):
            print("Error: key must be at least 64 hexadecimal characters", file=sys.stderr)
            sys.exit(1)

        encrypt(hex_key)
        generate_qr_code(hex_key)
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

def compute_hotp(secret, counter):
    # HOTP implementation from RFC 4226
    key = bytes.fromhex(secret)
    counter_bytes = counter.to_bytes(8, byteorder='big')
    hmac_digest = hmac.new(key, counter_bytes, hashlib.sha1).digest()

    offset = hmac_digest[19] & 0xf
    code = ((hmac_digest[offset] & 0x7f) << 24 |
            (hmac_digest[offset + 1] & 0xff) << 16 |
            (hmac_digest[offset + 2] & 0xff) << 8 |
            (hmac_digest[offset + 3] & 0xff))
    otp = code % 1000000
    return f"{otp:06d}"

def compute_totp(secret):
    # TOTP: C = (T - 0) / 30
    T = int(time.time())
    C = T // TIME_STEP
    return compute_hotp(secret, C)

def generate_otp(keyfile):
    try:
        secret = decrypt(keyfile)
        otp = compute_totp(secret)
        print(otp)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)            

def main():
    parser = argparse.ArgumentParser(
        description='TOTP Generator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
examples:
  %(prog)s -g key.hex           Save hex key to ft_otp.key
  %(prog)s -k ft_otp.key        Generate OTP from key file
        '''
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-g', metavar='hex_key_file', help='Store hex key')
    group.add_argument('-k', metavar='key_file', help='Generate password')
    
    args = parser.parse_args()
    
    if args.g:
        store_key(args.g)
    elif args.k:
        generate_otp(args.k)

if __name__ == '__main__':
    main()