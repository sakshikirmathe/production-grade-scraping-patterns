# scroll_paginated_scraper.py
# Scrapes JS-rendered paginated quotes using Playwright with proper waits

from playwright.sync_api import sync_playwright
import time
import csv

BASE_URL = "https://quotes.toscrape.com/js/page/{}/"
OUTPUT_FILE = "quotes_output.csv"

def extract_quotes_from_page(page):
    quotes = page.query_selector_all(".quote")
    results = []

    for quote in quotes:
        try:
            text = quote.query_selector(".text").inner_text()
            author = quote.query_selector(".author").inner_text()
            results.append({"text": text, "author": author})
        except:
            continue  # skip any failed quote blocks

    return results

def main():
    all_quotes = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # set True when stable
        page = browser.new_page()

        page_num = 1
        while True:
            url = BASE_URL.format(page_num)
            print(f"[+] Visiting Page {page_num}: {url}")
            page.goto(url)
            page.wait_for_load_state("networkidle")  # wait for JS rendering
            time.sleep(1.5)  # allow DOM to fully populate

            try:
                page.wait_for_selector(".quote", timeout=8000)
            except:
                print(f"[!] No quotes found on page {page_num}. Ending.")
                break

            quotes = extract_quotes_from_page(page)
            if not quotes:
                print("[!] Page loaded but no quote blocks found. Ending.")
                break

            all_quotes.extend(quotes)
            print(f"[✓] Extracted {len(quotes)} quotes from page {page_num}")
            page_num += 1
            time.sleep(1)  # polite delay

        browser.close()

    # Save to CSV
    with open(OUTPUT_FILE, "w", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["text", "author"])
        writer.writeheader()
        writer.writerows(all_quotes)

    print(f"\n[✓] Total quotes scraped: {len(all_quotes)}")

if __name__ == "__main__":
    main()