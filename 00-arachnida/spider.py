#!/usr/bin/env python3

import argparse
import os
import sys

def parse_arguments():
    parser = argparse.ArgumentParser(description='Spider: Web Image Scraper')
    parser.add_argument('url', help='URL to download images from')
    parser.add_argument('-r', '--recursive', action='store_true', help='enable recursive downloading')
    parser.add_argument('-l', '--level', type=int, default=None, help='maximum recursion depth (default: 5 when -r is used)')
    parser.add_argument('-p', '--path', default='./data/', help='download path (default: ./data/)')
    return parser.parse_args()

def check_args(args):
    if args.recursive:
        if args.level is None:
            args.level = 5
        elif args.level < 0:
            print("Error: Recursion level must be a non-negative integer.", file=sys.stderr)
            sys.exit(1)
    else:
        if args.level is not None:
            print("Note: Recursion disabled. Ignoring -l flag.")
        args.level = 0

    if not args.url.startswith(('http://', 'https://')):
        print("Error: URL must start with http:// or https://", file=sys.stderr)
        sys.exit(1)

    # Check and create download path
    if os.path.exists(args.path):
        if not os.path.isdir(args.path):
            print(f"Error: {args.path} exists but is not a directory", file=sys.stderr)
            sys.exit(1)
        if not os.access(args.path, os.W_OK):
            print(f"Error: No write permission for directory {args.path}", file=sys.stderr)
            sys.exit(1)
    else:
        try:
            os.makedirs(args.path, exist_ok=True)
            print(f"Note: Created directory {args.path}")
        except OSError as e:
            print(f"Error: Cannot create directory {args.path}: {e}", file=sys.stderr)
            sys.exit(1)

def main():
    args = parse_arguments()
    check_args(args)

    print(f"Target URL: {args.url}")
    print(f"Recursive: {args.recursive}")
    print(f"Depth Level: {args.level}")
    print(f"Save Path: {args.path}")

    # initialization: save parameters
    # parse page: find images, extract src
    # download and save

if __name__ == "__main__":
    main()
