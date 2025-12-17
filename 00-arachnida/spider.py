#!/usr/bin/env python3

import argparse
import os
import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

class Spider:
    IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}

    def __init__(self, save_path, max_depth):
        self.save_path = save_path
        self.max_depth = max_depth
        self.downloaded_images = set()
        self.visited_urls = set()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; Spider/1.0)'
        }

    def run(self, start_url):
       print(f"Starting spider...")
       print(f"Target URL: {start_url}")
       print(f"Save path: {self.save_path}")
       if self.max_depth:
            print(f"Max depth: {self.max_depth}")
       print("-" * 50)

       self.crawl(start_url)

       print("-" * 50)
       print(f"Crawling complete!")
       print(f"Visited {len(self.visited_urls)} pages")
       print(f"Downloaded {len(self.downloaded_images)} images")
    
    def crawl(self, url):
        self.visited_urls.add(url)

        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            html = response.text
            # print(f"html page:\n{html}")

            images = self.parse_image_urls(html)
            # print(f"images:\n{images}")

            for img_url in images:
                self.download_image(img_url, url)

        except requests.exceptions.RequestException as e:
            print(f"Error: Failed to fetch {url}: {e}", file=sys.stderr)
        except Exception as e:
            print(f"Error: Unexpected error processing {url}: {e}", file=sys.stderr)

    def parse_image_urls(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        images = []

        for img in soup.find_all('img'):
            src = img.get('src')
            if src:
                images.append(src)

        return images

    def download_image(self, img_url, base_url):
        absolute_url = urljoin(base_url, img_url)
        
        if not self.is_valid_image_url(absolute_url):
            return
        
        if absolute_url in self.downloaded_images:
            return
        
        try:
            response = requests.get(absolute_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            filename = os.path.basename(urlparse(absolute_url).path)
            filepath = os.path.join(self.save_path, filename)
            counter = 1
            while os.path.exists(filepath):
                name, ext = os.path.splitext(filename)
                filepath = os.path.join(self.save_path, f"{name}_{counter}{ext}")
                counter += 1
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            self.downloaded_images.add(absolute_url)
            print(f"Downloaded: {filename}")
        
        except requests.exceptions.RequestException as e:
            print(f"Error downloading {absolute_url}: {e}", file=sys.stderr)
        except Exception as e:
            print(f"Unexpected error downloading {absolute_url}: {e}", file=sys.stderr)

    def is_valid_image_url(self, url):
        parsed = urlparse(url)
        ext = os.path.splitext(parsed.path)[1].lower()
        return ext in self.IMAGE_EXTENSIONS

def parse_arguments():
    parser = argparse.ArgumentParser(description='Spider: Web Image Scraper')
    parser.add_argument('url', help='URL to download images from')
    parser.add_argument('-r', '--recursive', action='store_true', help='enable recursive downloading')
    parser.add_argument('-l', '--level', type=int, default=None, help='maximum recursion depth (default: 5 when -r is used)')
    parser.add_argument('-p', '--path', default='./data/', help='download path (default: ./data/)')
    return parser.parse_args()

def check_args(args):
    if args.recursive:
        if args.level is None:
            args.level = 5
        elif args.level < 0:
            print("Error: Recursion level must be a non-negative integer.", file=sys.stderr)
            sys.exit(1)
    else:
        if args.level is not None:
            print("Note: Recursion disabled. Ignoring -l flag.")
            print("-" * 50)
        args.level = 0

    if not args.url.startswith(('http://', 'https://')):
        print("Error: URL must start with http:// or https://", file=sys.stderr)
        sys.exit(1)

    # Check and create download path
    if os.path.exists(args.path):
        if not os.path.isdir(args.path):
            print(f"Error: {args.path} exists but is not a directory", file=sys.stderr)
            sys.exit(1)
        if not os.access(args.path, os.W_OK):
            print(f"Error: No write permission for directory {args.path}", file=sys.stderr)
            sys.exit(1)
    else:
        try:
            os.makedirs(args.path, exist_ok=True)
            print(f"Note: Created directory {args.path}")
            print("-" * 50)
        except OSError as e:
            print(f"Error: Cannot create directory {args.path}: {e}", file=sys.stderr)
            sys.exit(1)

def main():
    args = parse_arguments()
    check_args(args)

    spider = Spider(
        save_path=args.path,
        max_depth=args.level
    )

    spider.run(args.url)

    # initialization: save parameters - Done
    # parse page: find images, extract src - Done
    # download and save:
    #       normalize img src links - Done
    #       check for duplicates - Done
    #       handle recursion
    #       download in self.save_path - Done

if __name__ == "__main__":
    main()
