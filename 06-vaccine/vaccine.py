#!/usr/bin/env python3
from core.cli import parse_args, validate_args
import sys
import json
import os

def error_exit(message):
    print(f"[!] Error: {message}")
    sys.exit(1)

def init_archive(path):
    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump([], f)

def main():
    try:
        args = parse_args()
        validate_args(args)
        init_archive(args.archive_path)

        print("URL    :", args.url)
        print("Output :", args.archive_path)
        print("Method :", args.method)
        if args.post_data:
            print("Data   :", args.post_data)

    except Exception as e:
        error_exit(e)

if __name__ == '__main__':
    main()