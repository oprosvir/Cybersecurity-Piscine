from core.requester import Requester
from core.storage import Storage


class Scanner:
    def __init__(self, config):
        self.config = config
        self.requester = Requester(headers=config.headers)
        self.storage = Storage(config.archive_path)

    def run(self):
        print(f"\n[*] Target  : {self.config.url}")
        print(f"[*] Method  : {self.config.method}")
        print(f"[*] Params  : {[p['name'] for p in self.config.params]}\n")

        response = self.requester.send(self.config)
        print(
            f"[*] Response: {response.status_code} | "
            f"len={len(response.text)} | "
            f"time={response.elapsed.total_seconds():.2f}s | "
            f"final={response.url}\n"
        )