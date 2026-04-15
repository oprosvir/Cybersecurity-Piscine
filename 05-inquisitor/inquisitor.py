import sys

def error_exit(message):
    print(f"[!] Error: {message}")
    sys.exit(1)

def main():
    try:
        print(f"[*] Poisoning ARP")
        print(f"[*] Sniffing FTP traffic on port 21...")
    except Exception as e:
        error_exit(e)

if __name__ == '__main__':
    main()