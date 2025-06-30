import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os
import argparse

visited_urls = set()
allowed_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')
recursive = False
max_depth = 5 
target_folder = 'data'

def scrape_images(url, depth, download_path):
    if recursive == True:
        if depth > max_depth or url in visited_urls:
            return
        visited_urls.add(url)

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        os.makedirs(download_path, exist_ok=True)

        # Download images
        for img in soup.find_all('img', src=True):
            img_url = urljoin(url, img['src'])
            if is_valid_image(img_url):
                download_image(img_url, download_path)

        if recursive == True:
            # Find and recursively follow links
            for link in soup.find_all('a', href=True):
                next_url = urljoin(url, link['href'])
                if urlparse(next_url).netloc == urlparse(url).netloc:  # stay in domain
                    scrape_images(next_url, depth + 1, download_path)

    except Exception as e:
        print(f"Failed to scrape {url}: {e}")

def download_image(img_url, download_path):
    try:
        image_name = img_url.split('/')[-1]
        path = os.path.join(download_path, image_name)
        r = requests.get(img_url, timeout=5)
        with open(path, 'wb') as f:
            f.write(r.content)
        print(f"Succesfully downloaded: {img_url}")
    except Exception as e:
        print(f"Failed to download: {img_url}: {e}")

# if valid url it returns the link else it returns false
def is_valid_image(url):
    return url.lower().endswith(allowed_extensions)

# Start scraping
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description="Script that scrapes images from a given website"
        )
    parser.add_argument("-r", required=False, type=bool)
    parser.add_argument("-l", required=False, type=int, help="Enter maximum recursive depth")
    parser.add_argument("-p", required=False, type=str, help="Enter download path")
    parser.add_argument("url", type=str, help="Enter url")
    args = parser.parse_args()

    if args.r:
        recursive = args.r
    if args.l:
        max_depth = args.l
    if args.p:
        target_folder = args.p
    url = args.url[4:]

# Start scraping 
# Command example mac/linux: python3 spider.py -r=true -l=1 -p=images url=https://www.codam.nl
# Command example windows: python spider.py -r=true -l=1 -p=images url=https://www.codam.nl
scrape_images(url, 0, target_folder)
