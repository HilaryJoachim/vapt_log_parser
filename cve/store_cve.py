from cve.cve_parser import parse_nvd_file
from cve.db_cve import save_cve_item

def load_cve_feed(json_path):
    print(f"📥 Reading CVE feed: {json_path}")

    items = parse_nvd_file(json_path)

    print(f"📦 Parsed {len(items)} CVE items. Saving into DB...")

    saved = 0
    for cve in items:
        save_cve_item(cve)
        saved += 1

    print(f"✅ Saved {saved} CVE entries successfully!")


# -------- MAIN ENTRY POINT (important!) --------
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("❌ Missing argument: JSON file path")
        sys.exit(1)

    json_path = sys.argv[1]
    load_cve_feed(json_path)
