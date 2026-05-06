from pathlib import Path
import json
from datetime import datetime, timezone


class Storage:
    def __init__(self, archive_path):
        self.path = Path(archive_path)
        self._init_file()

    def _init_file(self):
        if not self.path.exists():
            self.path.write_text("[]")

    def save(self, findings):
        with self.path.open("r") as f:
            archive = json.load(f)

        entry = {
            "scanned_at": datetime.now(timezone.utc).isoformat(),
            "findings": findings,
        }
        archive.append(entry)

        with self.path.open("w") as f:
            json.dump(archive, f, indent=2)
