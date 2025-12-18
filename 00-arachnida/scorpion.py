#!/usr/bin/env python3

import argparse
import sys
import os
from PIL import Image
from datetime import datetime

class Scorpion:
    IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif'}
    
    def __init__(self, remove_exif=False):
        self.remove_exif = remove_exif
    
    def run(self, filenames):
        for filename in filenames:
            self.display_metadata(filename)

    def display_metadata(self, filename):
        if not os.path.exists(filename):
            print(f"Error: File not found: {filename}", file=sys.stderr)
            return

        if not os.path.isfile(filename):
            print(f"Error: Not a file: {filename}", file=sys.stderr)
            return

        ext = os.path.splitext(filename)[1].lower()
        if ext not in self.IMAGE_EXTENSIONS:
            print(f"Warning: Unsupported format: {filename}", file=sys.stderr)
            return
        
        print(f"\n{'='*60}")
        print(f"File: {filename}")
        print(f"{'='*60}")

        try:
            with Image.open(filename) as img:
                self.print_basic_metadata(filename, img)
                self.print_exif_data(img)
                
                if self.remove_exif and img.format in ['JPEG', 'TIFF']:
                    self.remove_exif_data(filename, img)
        except Exception as e:
            print(f"  Error reading file info: {e}", file=sys.stderr)

    def print_basic_metadata(self, filename, img):
        stat = os.stat(filename)
        size_mb = os.path.getsize(filename) / (1024 * 1024)
        created = datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
        modified = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')

        print(f"\nFile Information:")
        print(f"  Size: {size_mb:.2f} MB")
        print(f"  Created: {created}")
        print(f"  Modified: {modified}")

        print(f"\nImage Properties:")
        print(f"  Format: {img.format}")
        print(f"  Mode: {img.mode}")
        print(f"  Dimensions: {img.width} x {img.height} pixels")
        if hasattr(img, 'info'):
            dpi = img.info.get('dpi')
            if dpi:
                print(f"  DPI: {dpi}")

    def print_exif_data(self, img):
        if img.format not in ['JPEG', 'TIFF']:
            print(f"\nEXIF Data: Not supported for {img.format} format")
            return
        
        try:
            exif_data = img._getexif()
            if exif_data is None:
                print(f"\nEXIF Data: No EXIF data found")
                return
            
            print(f"\nEXIF Data:")
            for tag, value in exif_data.items():
                tag_name = Image.ExifTags.TAGS.get(tag, f"Unknown ({tag})")
                if isinstance(value, bytes):
                    continue
                print(f"  {tag_name}: {value}")
        except AttributeError:
            print(f"\nEXIF Data: Not available for {img.format} format")
        except Exception as e:
            print(f"\nEXIF Data: Error reading EXIF: {e}")

    def remove_exif_data(self, filename, img):
        try:
            img.save(filename, exif=b'')
            print(f"\nEXIF Data: Removed from {filename}")
        except Exception as e:
            print(f"\nEXIF Data: Error removing EXIF: {e}")

def main():
    parser = argparse.ArgumentParser(description='Scorpion: Image Metadata Extractor')
    parser.add_argument('files', nargs='+', metavar='FILE', help='Image file(s) to analyze')
    parser.add_argument('--remove-exif', action='store_true', help='Remove EXIF data from the image(s)')
    args = parser.parse_args()

    scorpion = Scorpion(remove_exif=args.remove_exif)
    try:
        scorpion.run(args.files)
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        sys.exit(1)

if __name__ == '__main__':
    main()