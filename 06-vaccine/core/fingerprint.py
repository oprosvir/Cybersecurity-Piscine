#!/usr/bin/env python3
from core.payloads import DB_FINGERPRINTS, SUPPORTED_ENGINES

# ---------------------------------------------------------------------------
# DB engine fingerprinting for Vaccine
#
# Strategy (in order):
#   1. Passive  — scan the baseline response body/headers for known DB strings
#   2. Active   — send a deliberate syntax error (') and scan the error response
#
# Returns the detected engine name (str) or None if unknown.
# ---------------------------------------------------------------------------

# Probe payloads that trigger verbose error messages
_PROBE_PAYLOADS = ["'", "''", "\\", "1'"]


def _scan_body(text: str) -> str | None:
    """Return the first matching engine whose fingerprint appears in text."""
    text_lower = text.lower()
    for engine, signatures in DB_FINGERPRINTS.items():
        for sig in signatures:
            if sig.lower() in text_lower:
                return engine
    return None


def _scan_headers(headers: dict) -> str | None:
    """Check response headers (e.g. X-Powered-By, Server) for DB hints."""
    combined = " ".join(headers.values()).lower()
    hints = {
        "mysql":      ["mysql", "mariadb"],
        "postgresql": ["postgresql", "postgres"],
        "mssql":      ["microsoft-iis", "asp.net"],
        "sqlite":     ["sqlite"],
    }
    for engine, keywords in hints.items():
        if any(k in combined for k in keywords):
            return engine
    return None


def fingerprint(requester, method: str, url: str,
                params: list[dict], post_data: str | None) -> str | None:
    """
    Try to identify the DB engine.

    Steps:
      1. Send the original (unmodified) request — check baseline body + headers.
      2. For each parameter, inject each probe payload — check error response.
      3. If still unknown, return None (scanner will test all engines).

    Args:
        requester:  Requester instance
        method:     "GET" or "POST"
        url:        target URL
        params:     list of {"name": str, "value": str}
        post_data:  raw POST body string or None

    Returns:
        Engine name string or None.
    """

    # -- Step 1: passive scan of baseline response ---------------------------
    try:
        baseline = requester.send(method, url)
        detected = _scan_headers(baseline["headers"])
        if detected:
            print(f"[~] DB engine detected from headers: {detected}")
            return detected

        detected = _scan_body(baseline["body"])
        if detected:
            print(f"[~] DB engine detected from baseline response: {detected}")
            return detected
    except RuntimeError:
        pass  # baseline failed; proceed to active probing

    # -- Step 2: active probing — inject syntax errors -----------------------
    for param in params:
        for probe in _PROBE_PAYLOADS:
            injected_value = param["value"] + probe

            try:
                if method == "GET":
                    probe_params = {
                        p["name"]: (injected_value if p["name"] == param["name"] else p["value"])
                        for p in params
                    }
                    response = requester.send(method, url, params=probe_params)
                else:
                    from urllib.parse import urlencode
                    probe_data = {
                        p["name"]: (injected_value if p["name"] == param["name"] else p["value"])
                        for p in params
                    }
                    response = requester.send(method, url, data=urlencode(probe_data))

                detected = _scan_body(response["body"])
                if detected:
                    print(f"[~] DB engine detected via active probe on param '{param['name']}': {detected}")
                    return detected

            except RuntimeError:
                continue  # network error on this probe; try next

    # -- Step 3: unknown -----------------------------------------------------
    print("[~] Could not detect DB engine — will test all supported engines")
    return None


def fingerprint_or_all(requester, method: str, url: str,
                       params: list[dict], post_data: str | None) -> list[str]:
    """
    Convenience wrapper used by scanner.py.
    Returns a list of engines to test:
      - [detected_engine]  if fingerprinting succeeded
      - SUPPORTED_ENGINES  if unknown (test everything)
    """
    engine = fingerprint(requester, method, url, params, post_data)
    return [engine] if engine else list(SUPPORTED_ENGINES)
