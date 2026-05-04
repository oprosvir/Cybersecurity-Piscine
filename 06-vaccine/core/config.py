from core.cli import parse_args
from urllib.parse import urlparse, urlunparse, parse_qsl


def parse_headers(raw_headers):
    headers = {}

    for raw in raw_headers:
        if ":" not in raw:
            raise ValueError(f"Invalid header format: {raw!r}. Use 'Key: Value'.")

        key, value = raw.split(":", 1)
        key = key.strip()
        value = value.strip()

        if not key:
            raise ValueError(f"Invalid header name in: {raw!r}")

        headers[key] = value

    return headers


class BuildConfig:
    def __init__(self, args):
        self.url = args.url
        self.method = args.method
        self.archive_path = args.archive_path
        self.params = self._extract_params(args.post_data)
        self.headers = parse_headers(args.headers)

    def _extract_params(self, post_data):
        if self.method == "GET":
            parsed = urlparse(self.url)
            self.url = urlunparse(
                (parsed.scheme, parsed.netloc, parsed.path, "", "", "")
            )
            pairs = parse_qsl(parsed.query, keep_blank_values=True)
        else:
            pairs = parse_qsl(post_data, keep_blank_values=True)
        return [{"name": k, "value": v} for k, v in pairs]

    @classmethod
    def from_cli(cls):
        args = parse_args()
        return cls(args)
