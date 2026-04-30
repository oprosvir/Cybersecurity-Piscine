# Vaccine: SQL Injection Detection Tool

Educational SQL injection testing tool designed for authorized lab environments. The project is focused on understanding and identifying filtering errors in data input.

## Usage
```sh
./vaccine [-o FILE] [-X METHOD] [--data DATA] [--header KEY:VALUE] URL
```

**Options**
- `URL` : Target URL to test (e.g., `http://localhost:8080/item?id=1`).
- `-o`, `--output` : Archive file path (default: `vaccine_archive.json`).
- `-X`, `--method` : HTTP method to use (`GET` or `POST`, default: `GET`).
- `-d`, `--data` : POST body data (e.g., `'id=1&name=test'`).
- `-H`, `--header` : Extra header, repeatable (e.g., `--header "User-Agent: Vaccine/1.0"`).

## Project structure

```
vaccine/
├── vaccine.py              # Main entry point: orchestrates the scan
├── core/
│   ├── cli.py              # Argument parsing and validation
│   ├── config.py           # Build config object from CLI input
│   ├── requester.py        # HTTP request sender
│   ├── scanner.py          # Scan workflow and vulnerability checks
│   └── storage.py          # Archive file initialization
└── README.md
```

## Requirements
```sh
pip3 install requests
```

## Legal notice
**Disclaimer:** This tool is for educational purposes only. Use only on systems you are explicitly authorized to test. Unauthorized access or testing of systems is illegal and unethical.