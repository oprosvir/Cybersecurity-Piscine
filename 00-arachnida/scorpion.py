#!/usr/bin/env python3

import argparse
import sys

class Scorpion:
    IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}
    
    def run(self, filenames):
        for filename in filenames:
            print(f"\n{'='*60}")
            print(f"File: {filename}")
            print(f"\n{'='*60}")

def main():
    parser = argparse.ArgumentParser(description='Scorpion: Image Metadata Extractor')
    parser.add_argument('files', nargs='+', metavar='FILE', help='Image file(s) to analyze')
    args = parser.parse_args()

    scorpion = Scorpion()
    try:
        scorpion.run(args.files)
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        sys.exit(1)

if __name__ == '__main__':
    main()

# TODO:
#       - check file exists, extension
#       - import lib to read metadata
#       - open file/parse metadata/print