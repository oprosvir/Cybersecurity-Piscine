#!/usr/bin/env python3
from core.config import BuildConfig
from core.scanner import Scanner
import sys


def error_exit(message):
    print(f"[!] Error: {message}")
    sys.exit(1)


def main():
    try:
        config = BuildConfig.from_cli()

        print("URL    :", config.url)
        print("Method :", config.method)
        print("Output :", config.archive_path)
        if config.post_data:
            print("Data   :", config.post_data)

        print(f"\n[*] Found {len(config.params)} parameter(s) to test:")
        for p in config.params:
            print(f"    - {p['name']} = {p['value']}")

        scanner = Scanner(config)
        scanner.run()

    except Exception as e:
        error_exit(e)


if __name__ == '__main__':
    main()
