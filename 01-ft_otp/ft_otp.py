#!/usr/bin/env python3

import argparse

def main():
    parser = argparse.ArgumentParser(description='TOTP Generator')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-g', metavar='hex_key_file', help='Store hex key')
    group.add_argument('-k', metavar='key_file', help='Generate password')
    
    args = parser.parse_args()
    
    if args.g:
        print(f"Store hexadecimal key {args.g}")
    elif args.k:
        print(f"Generate new temporary password {args.k}")

if __name__ == '__main__':
    main()