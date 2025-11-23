from pathlib import Path
import requests, json
from datetime import datetime

def download_full_cve_feed():
    project_root = Path(__file__).resolve().parents[1]
    cve_dir = project_root / "cve_data"
    cve_dir.mkdir(parents=True, exist_ok=True)   # 🔥 creates folder always

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M")
    target_file = cve_dir / f"cve_full_{timestamp}.json"

    print("📥 Downloading FULL NVD CVE dataset...")
    url = "https://services.nvd.nist.gov/rest/json/cves/2.0?resultsPerPage=2000"
    response = requests.get(url)
    response.raise_for_status()

    with open(target_file, "w", encoding="utf-8") as f:
        f.write(json.dumps(response.json(), indent=2))

    print(f"✔ Saved full feed: {target_file}")
    return target_file


if __name__ == "__main__":
    download_full_cve_feed()
