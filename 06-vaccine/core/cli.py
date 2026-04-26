import argparse
from urllib.parse import urlparse, parse_qsl

def parse_args():
    parser = argparse.ArgumentParser( 
        description="Vaccine: Educational SQL injection testing tool",
    )

    parser.add_argument(
        "url",
        help="Target URL to test, e.g. http://localhost:8080/item?id=1",
    )

    parser.add_argument(
        "-o",
        "--output",
        dest="archive_path",
        default="vaccine_archive.json",
        help="Archive file path (default: vaccine_archive.json)",
    )

    parser.add_argument(
        "-X",
        "--method",
        dest="method",
        default="GET",
        choices=["GET", "POST"],
        help="HTTP method to use (default: GET)",
    )

    parser.add_argument(
        "-d",
        "--data",
        dest="post_data",
        default=None,
        help="POST body, e.g., 'id=1&name=test'",
    )

    return parser.parse_args()

def validate_args(args):
    parsed = urlparse(args.url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise ValueError(f"Invalid URL: {args.url}")
    
    if args.method == "GET" and args.post_data:
        raise ValueError("Data parameter is only valid with POST method")
    
    if args.method == "GET" and not parsed.query:
        raise ValueError("GET testing requires at least one query parameter, e.g. ?id=1")
    
    if args.method == "POST" and not args.post_data:
        raise ValueError("POST method requires --data with at least one parameter")
    
    if not args.archive_path or not args.archive_path.endswith('.json'):
        raise ValueError("Invalid archive path: must end with .json")

class Config:
    def __init__(self, args):
        self.url = args.url
        self.method = args.method
        self.post_data = args.post_data
        self.archive_path = args.archive_path
        self.params = self._extract_params()

    def _extract_params(self):
        if self.method == "GET":
            parsed = urlparse(self.url)
            pairs = parse_qsl(parsed.query, keep_blank_values=True)
        else:
            pairs = parse_qsl(self.post_data, keep_blank_values=True)
        return [{"name": k, "value": v} for k, v in pairs]
