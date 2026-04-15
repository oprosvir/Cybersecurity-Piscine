#!/usr/bin/env python3
import sys
import re
import argparse
import ipaddress

def error_exit(message):
    print(f"[!] Error: {message}")
    sys.exit(1)
    
def is_valid_ip(ip):
    try:
        ipaddress.IPv4Address(ip)
        return True
    except:
        return False
    
def is_valid_mac(mac):
    mac_pattern = re.compile(r'^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$')
    return bool(mac_pattern.match(mac))
    
def validate_args(args):
    if not is_valid_ip(args.ip_src):
        error_exit("Invalid IP-src format (must be IPv4)")
    if not is_valid_ip(args.ip_target):
        error_exit("Invalid IP-target format (must be IPv4)")
    if not is_valid_mac(args.mac_src):
        error_exit("Invalid MAC-src format")
    if not is_valid_mac(args.mac_target):
        error_exit("Invalid MAC-target format")
    if args.ip_src == args.ip_target or args.mac_src == args.mac_target:
        error_exit("Source and target must be different")
    
def parse_args():
    parser = argparse.ArgumentParser(description="Inquisitor: ARP poisoning and FTP Interception Tool")
    parser.add_argument("ip_src", help="IP of FTP client")
    parser.add_argument("mac_src", help="MAC of FTP client")
    parser.add_argument("ip_target", help="IP of FTP server")
    parser.add_argument("mac_target", help="MAC of FTP server")
    parser.add_argument('-v', '--verbose', action='store_true', help='show all FTP traffic')
    
    args = parser.parse_args()
    
    print(f"[*] Starting Inquisitor: src={args.ip_src} ({args.mac_src}) "
          f"-> target={args.ip_target} ({args.mac_target}), verbose={args.verbose}")
    
    return args

def main():
    try:
        args = parse_args()
        validate_args(args)
        print(f"[*] Poisoning ARP")
        print(f"[*] Sniffing FTP traffic on port 21...")
    except Exception as e:
        error_exit(e)

if __name__ == '__main__':
    main()