import json
from pathlib import Path
            
class Storage:
    def __init__(self, archive_path):
        self.path = Path(archive_path)
        self._init_file()
        
    def _init_file(self):
        if not self.path.exists():
            with self.path.open("w") as f:
                json.dump([], f)
    