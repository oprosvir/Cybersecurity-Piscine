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

---

# Scorpion - Image Metadata Extractor

A Python script for extracting and displaying metadata from image files.

## Description

Scorpion analyzes image files and displays comprehensive metadata including file information, image properties, and EXIF data. It supports multiple image formats and can optionally remove EXIF data from images.

## Requirements

- Python 3.6+
- Libraries: `Pillow`

## Usage

Run the script with one or more image files:

```
python3 scorpion.py [OPTIONS] FILE [FILE ...]
```

### Examples

- **Analyze a single image:**
  ```
  python3 scorpion.py image.jpg
  ```

- **Analyze multiple images:**
  ```
  python3 scorpion.py photo1.jpg photo2.png photo3.gif
  ```

- **Remove EXIF data from image(s):**
  ```
  python3 scorpion.py --remove-exif image.jpg
  ```

### Command-Line Arguments

- `FILE`: One or more image files to analyze (required).
- `--remove-exif`: Remove EXIF data from the image(s) (only for JPEG and TIFF formats).

### Supported Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- GIF (.gif)
- BMP (.bmp)
- TIFF (.tiff, .tif)

### Output

The script displays:

**File Information:**
- File size (in MB)
- Creation date
- Modification date

**Image Properties:**
- Format (JPEG, PNG, etc.)
- Color mode (RGB, RGBA, etc.)
- Dimensions (width x height in pixels)
- DPI (if available)

**EXIF Data** (for JPEG and TIFF formats):
- Camera make and model
- Date taken
- GPS coordinates
- Exposure settings
- And other available EXIF tags

## Notes

- EXIF data is only available for JPEG and TIFF formats.
- The `--remove-exif` option modifies the original file, so make backups if needed.
- Unsupported file formats will be skipped with a warning.
