# html_snapshot_diff.py
# Compares saved HTML snapshots to detect structural DOM changes

import os
import difflib
import requests
from datetime import datetime

URL = "https://quotes.toscrape.com/"
SNAPSHOT_DIR = "snapshots"
TODAY = datetime.today().strftime("%Y-%m-%d")
SNAPSHOT_PATH = os.path.join(SNAPSHOT_DIR, f"{TODAY}.html")
PREVIOUS_SNAPSHOT = None

def save_html_snapshot():
    response = requests.get(URL)
    response.raise_for_status()

    os.makedirs(SNAPSHOT_DIR, exist_ok=True)
    with open(SNAPSHOT_PATH, "w", encoding="utf-8") as f:
        f.write(response.text)
    print(f"[+] Saved new HTML snapshot: {SNAPSHOT_PATH}")

def get_previous_snapshot():
    files = sorted(os.listdir(SNAPSHOT_DIR))
    if len(files) < 2:
        print("[!] No previous snapshot to compare.")
        return None
    return os.path.join(SNAPSHOT_DIR, files[-2])

def compare_snapshots(file1, file2):
    with open(file1, encoding="utf-8") as f1, open(file2, encoding="utf-8") as f2:
        html1 = f1.readlines()
        html2 = f2.readlines()

    diff = difflib.unified_diff(html1, html2, fromfile=file1, tofile=file2)
    changes = list(diff)
    if changes:
        print("[!] DOM structure has changed.")
        for line in changes[:20]:  # preview only first 20 lines
            print(line.strip())
    else:
        print("[✓] No DOM changes detected.")

def main():
    save_html_snapshot()
    prev = get_previous_snapshot()
    if prev:
        compare_snapshots(prev, SNAPSHOT_PATH)

if __name__ == "__main__":
    main()