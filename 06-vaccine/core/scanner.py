from core.requester import Requester
from core.storage import Storage

class Scanner:
    def __init__(self, config):
        self.config = config
        self.requester = Requester(
            headers=config.headers
        )
        self.storage = Storage(config.archive_path)
        
    def test_connection(self):
        self.requester.send(self.config.method, self.config.url)
        