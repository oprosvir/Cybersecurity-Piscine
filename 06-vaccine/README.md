# Vaccine

An educational SQL injection testing tool built for the 42 Cybersecurity Piscine.

> ⚠️ Only use this tool against systems you own or have explicit permission to test.

---

## How it works

Vaccine takes a target URL, extracts the injectable parameters, and runs a battery of SQL injection tests. On a confirmed vulnerable parameter it identifies the database engine and extracts database names, table names, column names, and a full data dump.

**Injection methods:** error-based, union-based, boolean-based, time-based (blind)

**Database engines:** MySQL, SQLite, PostgreSQL, Microsoft SQL Server

---

## Install

```bash
pip3 install requests
```

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
| `-o FILE` | Output archive (must end in `.json`) | `vaccine_archive.json` |
| `-d DATA` | POST body, e.g. `uid=admin&passw=test` | — |
| `-H HEADER` | Extra request header, repeatable | — |

---

## Examples

```bash
# GET — parameters in the URL query string
python3 vaccine.py "http://192.168.56.105/?page=member&id=1&Submit=Submit"

# POST — body passed with -d
python3 vaccine.py http://localhost:8000 -X POST -d "search=1"

# Custom output file
python3 vaccine.py "http://192.168.56.105/?page=member&id=1&Submit=Submit" -o results.json

# Extra header (e.g. session cookie)
python3 vaccine.py http://localhost:8000 -X POST -d "search=1" -H "Cookie: session=abc"

# Altoro Mutual — public legal test target
python3 vaccine.py https://demo.testfire.net/doLogin -X POST -d "uid=admin&passw=test&btnSubmit=Login"
```

---

## Test targets

### Local — Docker (SQLite injection playground)

```bash
# Start the vulnerable container on port 8000
make up

# Run all test cases
make test

# Stop the container
make down
```

### Darkly (42 school VM)

```bash
# SQL injection — member search
python3 vaccine.py "http://192.168.56.105/?page=member&id=1&Submit=Submit"

# SQL injection — image search
python3 vaccine.py "http://192.168.56.105/index.php?page=searchimg&id=3&Submit=Submit"
```

### Altoro Mutual (demo.testfire.net)

Public legal test target. The login form POSTs to `/doLogin`:

```bash
python3 vaccine.py https://demo.testfire.net/doLogin -X POST -d "uid=admin&passw=test&btnSubmit=Login"
```

---

## Output format

Results are saved to the archive file (default: `vaccine_archive.json`). Each scan appends one entry:

```json
[
  {
    "scanned_at": "2026-05-04T10:00:00+00:00",
    "findings": [
      {
        "param": "id",
        "payload": "' OR 1=1-- -",
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

## Project structure

```
06-vaccine/
├── vaccine.py          # Entry point
├── Makefile            # up / test / down rules
├── README.md
└── core/
    ├── cli.py          # Argument parsing and validation
    ├── config.py       # Config object and parameter extraction
    ├── requester.py    # HTTP client wrapper
    ├── scanner.py      # Injection loop and data extraction
    └── storage.py      # JSON archive
```

---

## Legal notice

This tool is for educational purposes only. Only use it on systems you own or are explicitly authorized to test. Unauthorized testing is illegal.
