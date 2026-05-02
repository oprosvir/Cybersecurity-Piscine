# Vaccine

An educational SQL injection testing tool built for the 42 Cybersecurity Piscine.

> ⚠️ Only use this tool against systems you own or have explicit permission to test.

---

## How it works

Vaccine automatically discovers injectable parameters from a target URL, detects the database engine, and runs a battery of SQL injection tests. On a confirmed vulnerable parameter it extracts database names, table names, column names, and a full data dump.

**Injection methods supported:** error-based, union-based, boolean-based, time-based (blind)

**Database engines supported:** MySQL, SQLite, PostgreSQL, Microsoft SQL Server

---

## Usage

```bash
python3 vaccine.py [options] URL
```

### Options

| Flag | Description | Default |
|---|---|---|
| `URL` | Target URL | required |
| `-X METHOD` | HTTP method: `GET` or `POST` | `GET` |
| `-o FILE` | Output archive file (must end in `.json`) | `vaccine_archive.json` |
| `-d DATA` | POST body override, e.g. `id=1&name=test` | auto-discovered |
| `-H HEADER` | Extra request header, repeatable | — |

### Parameter discovery

You do **not** need to specify parameters manually. Vaccine will:
1. Parse query parameters directly from the URL (GET with query string)
2. Fetch the page and extract form fields automatically (POST or GET without query string)
3. Raise an error only if no parameters can be found at all

You can still override this with `-d` for POST if needed.

---

## Examples

```bash
# GET — parameters parsed from URL
python3 vaccine.py "http://localhost:8000/item?id=1"

# POST — form fields auto-discovered from the page
python3 vaccine.py http://localhost:8000 -X POST

# POST with explicit data override
python3 vaccine.py http://localhost:8000 -X POST -d "username=admin&password=test"

# Custom output file + extra header
python3 vaccine.py http://localhost:8000 -X POST -o scan.json -H "Cookie: session=abc"

# Altoro Mutual (public legal test target)
python3 vaccine.py "https://demo.testfire.net/login.jsp" -X POST
```

---

## Test targets

### Local — Docker (SQLite injection playground)

```bash
# Start the vulnerable container on port 8000
make test

# Run the scanner against it
make run ARGS="http://localhost:8000 -X POST"

# Stop the container when done
make stop
```

### Remote — Altoro Mutual

[Altoro Mutual](https://demo.testfire.net) is a deliberately vulnerable banking demo maintained by IBM for security testing.

```bash
python3 vaccine.py "https://demo.testfire.net/login.jsp" -X POST
```

---

## Project structure

```
06-vaccine/
├── vaccine.py              # Entry point
├── Makefile                # run / test / stop rules
├── README.md
└── core/
    ├── cli.py              # Argument parsing and validation
    ├── config.py           # Config object + parameter discovery
    ├── requester.py        # HTTP client
    ├── fingerprint.py      # DB engine detection
    ├── payloads.py         # Payload library (error/union/boolean/time)
    ├── scanner.py          # Injection loop + data extraction
    └── storage.py          # JSON archive
```

---

## Requirements

```bash
pip3 install requests
```

All other dependencies are Python stdlib.

---

## Output format

Results are saved to the archive JSON file (default: `vaccine_archive.json`).
Each scan appends a new entry:

```json
[
  {
    "scanned_at": "2026-05-02T10:00:00+00:00",
    "findings": [
      {
        "param": "username",
        "payload": "' AND 1=1-- -",
        "method": "boolean",
        "engine": "mysql",
        "data": {
          "version": "8.0.32",
          "current_db": "app",
          "databases": "information_schema|app",
          "tables": "users|products",
          "columns": { "users": "id|username|password" },
          "dump": { "users": "1|admin|secret" }
        }
      }
    ]
  }
]
```

---

## Legal notice

**Disclaimer:** This tool is for educational purposes only. Only use it on systems you own or are explicitly authorized to test. Unauthorized access or testing of systems is illegal and unethical.
