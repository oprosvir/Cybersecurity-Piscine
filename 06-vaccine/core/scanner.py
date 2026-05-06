from core.requester import Requester
from core.storage import Storage
from core.payloads import (
    ENGINE_SIGNATURES,
    ERROR_PAYLOADS,
)
import re

SUPPORTED_ENGINES = list(ENGINE_SIGNATURES.keys())


def detect_engine(body):
    for engine, patterns in ENGINE_SIGNATURES.items():
        for pattern in patterns:
            if re.search(pattern, body, re.IGNORECASE):
                return engine
    return None


class Scanner:
    def __init__(self, config):
        self.config = config
        self.requester = Requester(headers=config.headers)
        self.storage = Storage(config.archive_path)
        self.findings = []

    def run(self):
        print(f"\n[*] Target : {self.config.url} ({self.config.method})")
        print(f"[*] Params : {[p['name'] for p in self.config.params]}\n")

        print(f"[*] Engines to test: {SUPPORTED_ENGINES}\n")

        baseline = {p["name"]: p["value"] for p in self.config.params}
        for param in self.config.params:
            self._test_param(param, baseline)

        if self.findings:
            self.storage.save(self.findings)
            print(f"[+] Results saved to: '{self.config.archive_path}'")
        else:
            print("[-] No SQL injection vulnerabilities detected.")

    def _test_param(self, param, baseline):
        for method, test_fn in [
            ("error",   self._test_error),
            ("boolean", self._test_boolean),
            ("time",    self._test_time),
        ]:
            engine = test_fn(param, baseline)
            if engine:
                print(f"[+] '{param['name']}' vulnerable -> {engine} ({method}-based)")
                self.findings.append(
                    {
                        "url": self.config.url,
                        "method": self.config.method,
                        "params": baseline,
                        "vulnerable": param["name"],
                        "type": f"{method}-based",
                        "engine": engine,
                    }
                )
                return

    def _test_error(self, param, baseline):
        for payload in ERROR_PAYLOADS:
            test_params = baseline.copy()
            test_params[param["name"]] = payload
            response = self.requester.send(self.config, test_params)
            engine = detect_engine(response.text)
            if engine:
                return engine
        return None

    def _test_boolean(self, param, baseline):
        pass
        return None

    def _test_time(self, param, baseline):
        pass
        return None
