import argparse
from urllib.parse import urlparse


def build_parser():
    parser = argparse.ArgumentParser(
        description="Vaccine: Educational SQL injection testing tool",
    )

    parser.add_argument(
        "url",
        help="Target URL, e.g. http://localhost:8000 or http://localhost:8000/search?q=1",
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
        help="Optional POST body override, e.g. 'id=1&name=test'. "
             "If omitted for POST, parameters are discovered from the page's form.",
    )

    parser.add_argument(
        "-H",
        "--header",
        dest="headers",
        action="append",
        default=[],
        help='Extra header, repeatable, e.g. --header "Cookie: session=abc"',
    )

    return parser


def validate_args(args):
    parsed = urlparse(args.url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise ValueError(f"Invalid URL: {args.url}")

    if args.method == "GET" and args.post_data:
        raise ValueError("--data is only valid with POST method (-X POST)")

    if not args.archive_path or not args.archive_path.endswith(".json"):
        raise ValueError("Invalid archive path: must end with .json")


def parse_args():
    parser = build_parser()
    args = parser.parse_args()
    validate_args(args)
    return args
