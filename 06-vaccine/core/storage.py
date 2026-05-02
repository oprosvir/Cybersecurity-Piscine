import json
from pathlib import Path
from datetime import datetime, timezone


class Storage:
    def __init__(self, archive_path):
        self.path = Path(archive_path)
        self._init_file()

    def _init_file(self):
        if not self.path.exists():
            with self.path.open("w") as f:
                json.dump([], f)

    def save(self, findings: list):
        """
        Append a new scan entry to the archive JSON file.

        Entry structure:
        {
            "scanned_at": "<ISO 8601 timestamp>",
            "findings": [ ...finding dicts from scanner... ]
        }
        """
        with self.path.open("r") as f:
            archive = json.load(f)

        entry = {
            "scanned_at": datetime.now(timezone.utc).isoformat(),
            "findings": findings,
        }
        archive.append(entry)

        with self.path.open("w") as f:
            json.dump(archive, f, indent=2)
