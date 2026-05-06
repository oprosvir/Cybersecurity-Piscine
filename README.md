# Cybersecurity Piscine

42 School cybersecurity piscine — a series of progressively complex security projects.

<img src="_assets/42-cybersec-piscine.png" alt="Cybersecurity Piscine" width="800">

## Projects

| # | Project | Description | Score |
|---|---------|-------------|-------|
| 00 | [arachnida](00-arachnida/) | `spider` — recursive web image scraper; `scorpion` — EXIF metadata viewer/remover | `116/100` |
| 01 | [ft_otp](01-ft_otp/) | TOTP (Time-based One-Time Password) generator per RFC 6238 | `117/100` |
| 02 | [ft_onion](02-ft_onion/) | Tor hidden service with nginx and SSH, deployed via Docker | `125/100` |
| 03 | [reverse_me](03-reverse_me/) | Reverse engineering of three ELF binaries (32/64-bit PIE) | `125/100` |
| 04 | [stockholm](04-stockholm/) | WannaCry-inspired ransomware simulator with Argon2id + Fernet encryption | `100/100` |
| 05 | [inquisitor](05-inquisitor/) | ARP poisoning tool for MITM interception of FTP traffic | `125/100` |
| 06 | [vaccine](06-vaccine/) | SQL injection tester (error/union/boolean/time-based, multi-DB) | `125/100` |

## Topics Covered

| Topic | Projects |
|-------|----------|
| OSINT / web scraping | 00 |
| Cryptography (TOTP, HMAC, Argon2id, Fernet) | 01, 04 |
| Anonymity networks (Tor, .onion) | 02 |
| Reverse engineering (static/dynamic analysis, GDB, patching) | 03 |
| Malware simulation (ransomware) | 04 |
| Network attacks (ARP spoofing, MITM) | 05 |
| Web vulnerabilities (SQLi) | 06 |

## Tools & Techniques

`gdb` `objdump` `ltrace` `strings` `readelf` — binary analysis  
`scapy` — packet crafting and ARP manipulation  
`requests` + `beautifulsoup4` — web scraping  
`cryptography` `argon2-cffi` — encryption and key derivation  
`docker` / `docker-compose` — isolated environments  
`tor` + `nginx` — hidden service stack  
SQL injection: error-based · union-based · boolean-based · time-based (blind)
