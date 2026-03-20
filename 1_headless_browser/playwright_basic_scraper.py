# playwright_basic_scraper.py
# Scrapes product titles, prices, and availability from books.toscrape.com using Playwright in headless mode

from playwright.sync_api import sync_playwright
import csv

BASE_URL = "https://books.toscrape.com/"
OUTPUT_FILE = "books_output.csv"

def scrape_books(page):
    page.goto(BASE_URL)
    page.wait_for_selector(".product_pod")
    
    books = page.query_selector_all(".product_pod")
    data = []

    for book in books:
        title = book.query_selector("h3 a").get_attribute("title")
        price = book.query_selector(".price_color").inner_text()
        availability = book.query_selector(".availability").inner_text().strip()
        data.append({
            "title": title,
            "price": price,
            "availability": availability
        })

    return data

def save_to_csv(records):
    with open(OUTPUT_FILE, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["title", "price", "availability"])
        writer.writeheader()
        writer.writerows(records)

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        records = scrape_books(page)
        save_to_csv(records)
        print(f"Scraped {len(records)} books.")
        browser.close()

if __name__ == "__main__":
    main()