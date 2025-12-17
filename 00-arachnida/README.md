# Spider - Web Image Scraper

A Python script for recursively downloading images from websites.

## Description

Spider crawls web pages, extracts image URLs from `<img>` tags, and can be extended to download them. It supports recursive crawling with depth limits and custom save paths.

## Requirements

- Python 3.6+
- Libraries: `requests`, `beautifulsoup4`

## Installation

1.  **Create a virtual environment:**
```
   python3 -m venv venv
   source venv/bin/activate
```

2. **Install dependencies:**
```
   pip install -r requirements.txt
```

3. **Deactivate the virtual environment:**
```
   deactivate
```

## Usage

Run the script with the target URL and optional flags:

```
python3 spider.py [OPTIONS] URL
```

### Examples

- **Basic usage (download from a single page):**
  ```
  python3 spider.py https://example.com
  ```

- **Recursive crawling with depth 3:**
  ```
  python3 spider.py -r -l 3 https://example.com
  ```

- **Save to custom path:**
  ```
  python3 spider.py -p /path/to/save https://example.com
  ```

- **Full example:**
  ```
  python3 spider.py -r -l 5 -p ./images https://example.com
  ```

### Command-Line Arguments

- `URL`: The target website URL (must start with `http://` or `https://`).
- `-r, --recursive`: Enable recursive downloading (follow links to other pages).
- `-l N, --level N`: Maximum recursion depth (default: 5 when recursive; ignored otherwise).
- `-p PATH, --path PATH`: Directory to save images (default: `./data/`; created if not exists).

### Output

- Prints crawling progress, found image URLs, and completion status.
- Errors are logged to stderr.

## Notes

- Ensure the target site allows scraping (check `robots.txt`).
- For large sites, use depth limits to avoid overloading servers.
