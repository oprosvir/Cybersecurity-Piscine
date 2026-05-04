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
        Scanner(config).run()

    except Exception as e:
        error_exit(e)


if __name__ == '__main__':
    main()
