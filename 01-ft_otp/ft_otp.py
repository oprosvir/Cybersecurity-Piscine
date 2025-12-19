#!/usr/bin/env python3

import argparse
import base64
import sys
import qrcode

def validate(hex_key):
    if len(hex_key) < 64:
        return False
    if not all(c in '0123456789abcdefABCDEF' for c in hex_key):
        return False
    return True

def generate_qr_code(hex_key):
    key_bytes = bytes.fromhex(hex_key)
    base32_key = base64.b32encode(key_bytes).decode('utf-8').rstrip('=')
    
    uri = f"otpauth://totp/ft_otp?secret={base32_key}&issuer=oprosvir"
    img = qrcode.make(uri)
    img.save("ft_otp_qr.png")

def store_key(filepath):
    try:
        with open(filepath, 'r') as f:
            hex_key = f.read().strip()
        if not validate(hex_key):
            print("Error: key must be at least 64 hexadecimal characters", file=sys.stderr)
            sys.exit(1)

        generate_qr_code(hex_key)
        print("QR code saved as ft_otp_qr.png")
        
    except Exception as e:
        print(f"Error: {filepath}: {e}", file=sys.stderr)
        sys.exit(1)

def generate_otp(keyfile):
    print(f"Generate new temporary password {keyfile}")

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