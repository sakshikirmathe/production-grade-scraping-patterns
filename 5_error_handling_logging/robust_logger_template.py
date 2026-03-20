# robust_logger_template.py
# Logging + exception handling structure for stable scraping

import logging
import requests
from bs4 import BeautifulSoup
import time

# Setup logging
logging.basicConfig(
    filename="scraper.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
console.setFormatter(formatter)
logging.getLogger("").addHandler(console)

BASE_URL = "https://quotes.toscrape.com/page/{}/"

def fetch_page(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch {url} | {e}")
        return None

def parse_quotes(html):
    try:
        soup = BeautifulSoup(html, "html.parser")
        quotes = soup.select(".quote")
        return [q.select_one(".text").text.strip() for q in quotes]
    except Exception as e:
        logging.warning(f"Failed to parse quotes | {e}")
        return []

def main():
    for page_num in range(1, 6):
        url = BASE_URL.format(page_num)
        logging.info(f"Scraping page {page_num}: {url}")
        
        html = fetch_page(url)
        if not html:
            logging.warning(f"Skipping page {page_num} due to fetch failure")
            continue
        
        quotes = parse_quotes(html)
        if quotes:
            logging.info(f"Extracted {len(quotes)} quotes from page {page_num}")
        else:
            logging.warning(f"No quotes found on page {page_num}")

        time.sleep(1)  # polite delay

    logging.info("Scraping job completed.")

if __name__ == "__main__":
    main()