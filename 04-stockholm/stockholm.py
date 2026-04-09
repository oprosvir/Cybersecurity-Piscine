#!/usr/bin/env python3

import argparse
import os
import sys

VERSION = "1.0.0"
TARGET_DIR = os.path.expanduser("~/infection")
WANNA_CRY_EXTENSIONS = [
    '.123', '.3dm', '.3ds', '.3g2', '.3gp', '.602', '.7z', '.accdb', '.aes', '.ai', '.ARC',
    '.asc', '.asf', '.asm', '.asp', '.avi', '.backup', '.bak', '.bat', '.bmp', '.brd', '.bz2',
    '.c', '.cgm', '.class', '.cmd', '.cpp', '.crt', '.cs', '.csr', '.csv', '.db', '.dbf', '.dch',
    '.der', '.dif', '.dip', '.djvu', '.doc', '.docb', '.docm', '.docx', '.dot', '.dotm', '.dotx',
    '.dwg', '.edb', '.eml', '.fla', '.flv', '.frm', '.gif', '.gpg', '.gz', '.h', '.htm', '.html',
    '.hwp', '.ibd', '.iqy', '.iso', '.jar', '.java', '.jpeg', '.jpg', '.js', '.jsp', '.key', '.lay',
    '.lay6', '.ldf', '.lnk', '.max', '.mdf', '.mdb', '.mkv', '.mml', '.mov', '.mp3', '.mp4', '.mpeg',
    '.mpg', '.msg', '.myd', '.myi', '.nef', '.odb', '.odg', '.odp', '.ods', '.odt', '.onetoc2', '.ost',
    '.otg', '.otp', '.ots', '.ott', '.PAQ', '.pas', '.pdf', '.pem', '.pfx', '.php', '.pl', '.png', '.pot',
    '.potm', '.potx', '.ppam', '.pps', '.ppsm', '.ppsx', '.ppt', '.pptm', '.pptx', '.ps1', '.psd', '.pst',
    '.p12', '.rar', '.raw', '.rb', '.rtf', '.sch', '.sh', '.slk', '.sln', '.snt', '.sql', '.sqlite3',
    '.sqlitedb', '.sldm', '.sldx', '.suo', '.sxc', '.sxd', '.sxm', '.sxw', '.sxi', '.svg', '.stw', '.sxd',
    '.sxi', '.tar', '.tbk', '.tgz', '.tif', '.tiff', '.txt', '.uot', '.uop', '.vb', '.vbs', '.vcd', '.vdi',
    '.vmdk', '.vmx', '.vob', '.vsd', '.vsdx', '.wav', '.wb2', '.wk1', '.wks', '.wma', '.wmv', '.wps', '.xla',
    '.xlc', '.xlm', '.xls', '.xlsb', '.xlsm', '.xlsx', '.xlt', '.xltm', '.xltx', '.xlw', '.xml', '.zip'
]

def parse_arguments():
    parser = argparse.ArgumentParser(description="Stockholm: File encryption simulator")
    parser.add_argument("-v", "--version", action="store_true", help="show version")
    parser.add_argument("-r", "--reverse", metavar="KEY", type=str, help="reverse using key")
    parser.add_argument("-s", "--silent", action="store_true", help="suppress output")
    return parser.parse_args()

def main():
    args = parse_arguments()
    
    if args.version:
        print(f"Stockholm: version {VERSION}")
        return
    
    if not os.path.isdir(TARGET_DIR):
        print(f"Error: {TARGET_DIR} is not a directory or does not exist. Please run 'make' to set up.")
        sys.exit(1)
    
    # TODO: Implement encryption/reverse logic here
    # Use args.reverse for the key, args.silent to control output
    if not args.silent:
        print("Stockholm: Ready to encrypt files in ~/infection")
        if args.reverse:
            print(f"Reversing with key: {args.reverse}")

if __name__ == "__main__":
    main()