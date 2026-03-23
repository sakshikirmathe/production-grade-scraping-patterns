# rotating_session_scraper.py
# Rotates proxies and user-agents to reduce detection risk while scraping

import requests
from bs4 import BeautifulSoup
import random
import time
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

# Toggle mode
USE_PUBLIC_PROXIES = True  # set to False for Bright Data mode

# Sample user-agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (X11; Linux x86_64)",
]

# Example public proxies (demo only — unstable)
PUBLIC_PROXIES = [
    "http://103.174.81.7:8080",
    "http://185.199.228.90:7492",
    "http://8.219.97.248:80",
]

# Bright Data proxy example (requires paid account + whitelisted IP)
BRIGHT_DATA_PROXY = {
    "http": "http://user:pass@brd.superproxy.io:22225",
    "https": "http://user:pass@brd.superproxy.io:22225",
}

TARGET_URL = "https://quotes.toscrape.com/page/1/"

def get_proxy():
    if USE_PUBLIC_PROXIES:
        return {"http": random.choice(PUBLIC_PROXIES), "https": random.choice(PUBLIC_PROXIES)}
    else:
        return BRIGHT_DATA_PROXY

def get_headers():
    return {"User-Agent": random.choice(USER_AGENTS)}

def fetch_with_rotation(url):
    if not USE_PUBLIC_PROXIES:
        logging.info("Using direct connection (no proxy)")
        proxy = None
    else:
        proxy = get_proxy()

    try:
        headers = get_headers()
        response = requests.get(url, headers=headers, proxies=proxy, timeout=8)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        logging.warning(f"Request failed: {e}")
        return None

def parse_quotes(html):
    soup = BeautifulSoup(html, "html.parser")
    quotes = soup.select(".quote")
    return [q.select_one(".text").text.strip() for q in quotes]

def main():
    html = fetch_with_rotation(TARGET_URL)
    if html:
        quotes = parse_quotes(html)
        logging.info(f"✅ Extracted {len(quotes)} quotes.")
    else:
        logging.error("Failed to scrape target page.")

if __name__ == "__main__":
    main()