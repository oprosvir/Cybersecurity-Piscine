# Inquisitor: ARP Poisoning and FTP Interception Tool

Python-based network security tool that performs ARP poisoning for man-in-the-middle attacks and intercepts FTP traffic to display file names in real time, with restoration of ARP tables on exit.

## Contents

- `Dockerfile`: Container setup with dependencies
- `docker-compose.yml`: Multi-service setup for FTP testing
- `Makefile`: Build and run automation
- `inquisitor.py` — Main tool implementation
- `README.md`: Documentation and usage guide

## Implementation plan

1. ✅ Set up containerized environment with `Dockerfile` and `docker-compose.yml` for isolated Linux testing, including Python, Scapy, and FTP server/client for validation.

2. ✅ Create `Makefile` to automate building the container, running the tool, and executing test suite without user intervention.

3. Implement argument parsing in `inquisitor.py` for required parameters (**IP-src**, **MAC-src**, **IP-target**, **MAC-target**) and optional verbose flag (`-v`).

4. Add **ARP poisoning** functionality: Send spoofed ARP replies to both source and target hosts to redirect traffic through the attacker machine (full duplex).

5. Implement packet sniffing using *Scapy/libpcap* to capture FTP control channel traffic (**port 21**).

6. Parse intercepted FTP commands (e.g., `RETR`, `STOR`) to extract and display file names in real time; in verbose mode, show all FTP traffic including login details.

7. Handle signal interruption (`CTRL+C`) to restore original ARP table entries by sending corrective ARP replies.

8. Add robust error handling for invalid inputs, network issues, and unexpected failures to ensure the program never stops unexpectedly.

9. Prepare automated test suite: Configure FTP server and client in the container, simulate file transfers, run inquisitor, and verify interception output.

10. Document usage, setup, and testing in `README.md` with examples and security disclaimers.