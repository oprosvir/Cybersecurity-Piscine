# ---------------------------------------------------------------------------
# Payload library
#
# Supported injection types:  union | error | boolean | time
# Supported DB engines:       mysql | sqlite | postgresql | mssql
# ---------------------------------------------------------------------------

# ── Error-based type ───────────────────────────────────────────────────────

# Strings that break SQL syntax when injected into a query

ERROR_PAYLOADS = ["'", '"', "')", '")', "';", '";', "\\"]

# Regex patterns that appear in error messages

ENGINE_SIGNATURES = {
    "mysql": [
        r"You have an error in your SQL syntax",
        r"MySQL server version",
        r"mysql_fetch_",
        r"valid MySQL result",
    ],
    "sqlite": [
        r"SQLite/JDBCDriver",
        r"SQLite\.Exception",
        r"System\.Data\.SQLite\.SQLiteException",
        r"unrecognized token",
        r"SQLite error",
    ],
    "postgresql": [
        r"PostgreSQL.*ERROR",
        r"pg_query\(\)",
        r"valid PostgreSQL result",
    ],
    "mssql": [
        r"Microsoft SQL Native Client error",
        r"Unclosed quotation mark",
        r"SQLServer JDBC Driver",
    ],
}
