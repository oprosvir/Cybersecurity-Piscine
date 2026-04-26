#!/usr/bin/env python3
from core.cli import parse_args, validate_args, Config
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

        config = Config(args)

        print("URL    :", config.url)
        print("Method :", config.method)
        print("Output :", config.archive_path)
        if config.post_data:
            print("Data   :", config.post_data)

        print(f"\n[*] Found {len(config.params)} parameter(s) to test:")
        for p in config.params:
            print(f"    - {p['name']} = {p['value']}")

    except Exception as e:
        error_exit(e)

if __name__ == '__main__':
    main()