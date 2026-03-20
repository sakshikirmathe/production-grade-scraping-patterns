# delta_detection.py
# Compares current and previous CSVs to detect new, removed, or changed records

import pandas as pd
from deepdiff import DeepDiff

PREVIOUS_FILE = "quotes_output.csv"
CURRENT_FILE = "quotes_output_new.csv"  # This would be from latest scrape

def load_csv(path):
    return pd.read_csv(path).fillna("").sort_values(by=["text", "author"]).reset_index(drop=True)

def detect_changes(prev_df, curr_df):
    prev_records = prev_df.to_dict(orient="records")
    curr_records = curr_df.to_dict(orient="records")

    diff = DeepDiff(prev_records, curr_records, ignore_order=True)

    added = diff.get("iterable_item_added", {})
    removed = diff.get("iterable_item_removed", {})
    modified = diff.get("values_changed", {})

    print("\n[+] 🔄 Delta Tracking Report")

    if added:
        print(f"\n🆕 Added ({len(added)}):")
        for _, item in added.items():
            print(f" - {item}")

    if removed:
        print(f"\n🗑️ Removed ({len(removed)}):")
        for _, item in removed.items():
            print(f" - {item}")

    if modified:
        print(f"\n✏️ Modified ({len(modified)} fields):")
        for path, change in modified.items():
            print(f" - {path}: {change['old_value']} → {change['new_value']}")

    if not (added or removed or modified):
        print("\n✅ No changes detected.")

def main():
    try:
        prev_df = load_csv(PREVIOUS_FILE)
        curr_df = load_csv(CURRENT_FILE)
        detect_changes(prev_df, curr_df)
    except FileNotFoundError as e:
        print(f"[!] Missing file: {e}")

if __name__ == "__main__":
    main()