from core.cli import parse_args
from urllib.parse import urlparse, parse_qsl
from urllib.request import urlopen, Request
from urllib.error import URLError
from html.parser import HTMLParser


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


# ---------------------------------------------------------------------------
# Minimal HTML form parser — stdlib only, no extra deps
# Extracts all <input>, <select>, <textarea> names from the first <form>.
# ---------------------------------------------------------------------------

class _FormParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_form = False
        self.fields  = []   # list of {"name": str, "value": str}

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)

        if tag == "form":
            self.in_form = True

        if not self.in_form:
            return

        if tag in ("input", "textarea", "select"):
            name  = attrs.get("name", "").strip()
            value = attrs.get("value", "").strip()
            itype = attrs.get("type", "text").lower()

            # Skip non-injectable field types
            if name and itype not in ("submit", "button", "image", "file", "hidden", "checkbox", "radio"):
                # Use existing value if present, otherwise seed with "1"
                self.fields.append({"name": name, "value": value or "1"})

    def handle_endtag(self, tag):
        if tag == "form":
            self.in_form = False


def _discover_form_params(url: str, extra_headers: dict) -> list[dict]:
    """
    Fetch the page at `url` and parse the first HTML form for injectable fields.
    Returns a list of {"name": str, "value": str} dicts.
    Raises ValueError if no form fields are found.
    """
    headers = {"User-Agent": "Vaccine/1.0", **extra_headers}
    req = Request(url, headers=headers)

    try:
        with urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8", errors="replace")
    except URLError as e:
        raise ValueError(f"Could not fetch page for parameter discovery: {e}")

    parser = _FormParser()
    parser.feed(html)

    if not parser.fields:
        raise ValueError(
            "No injectable form fields found on the page.\n"
            "Pass parameters explicitly with -d 'param=value' (POST) "
            "or include a query string in the URL (GET)."
        )

    return parser.fields


# ---------------------------------------------------------------------------
# BuildConfig
# ---------------------------------------------------------------------------

class BuildConfig:
    def __init__(self, args):
        self.url          = args.url
        self.method       = args.method
        self.post_data    = args.post_data
        self.archive_path = args.archive_path
        self.headers      = parse_headers(args.headers)
        self.params       = self._resolve_params()

    def _resolve_params(self) -> list[dict]:
        """
        Resolve injectable parameters using a priority fallback chain:

          1. POST + explicit --data    → parse from data string
          2. GET + query string in URL → parse from URL
          3. POST + no --data          → fetch page, parse form fields
          4. GET + no query string     → fetch page, parse form fields
          5. Nothing found             → raise ValueError
        """
        # Priority 1: POST with explicit data
        if self.method == "POST" and self.post_data:
            pairs = parse_qsl(self.post_data, keep_blank_values=True)
            if pairs:
                return [{"name": k, "value": v} for k, v in pairs]

        # Priority 2: GET with query string
        if self.method == "GET":
            parsed = urlparse(self.url)
            pairs  = parse_qsl(parsed.query, keep_blank_values=True)
            if pairs:
                return [{"name": k, "value": v} for k, v in pairs]

        # Priority 3 & 4: auto-discover from page HTML
        print("[~] No parameters provided — discovering form fields from page...")
        return _discover_form_params(self.url, self.headers)

    @classmethod
    def from_cli(cls):
        args = parse_args()
        return cls(args)
