import json
from pathlib import Path

def parse_nvd_file(json_path):
    path = Path(json_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {json_path}")

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Support both formats: CVE_Items (old feed) and vulnerabilities (new feed)
    raw_items = data.get("vulnerabilities", data.get("CVE_Items", []))
    cve_list = []

    for entry in raw_items:
        item = entry.get("cve", entry)

        cve_id = item["id"]
        description = item["descriptions"][0]["value"]

        metrics = item.get("metrics", {}).get("cvssMetricV31", [{}])
        cvss = metrics[0].get("cvssData", {})
        severity = cvss.get("baseSeverity")
        score = cvss.get("baseScore")

        cpes = []
        for config in item.get("configurations", []):
            for node in config.get("nodes", []):
                for c in node.get("cpeMatch", []):
                    if c.get("vulnerable", False):
                        cpes.append(c["criteria"])

        cve_list.append({
            "cve_id": cve_id,
            "description": description,
            "severity": severity,
            "score": score,
            "cpes": cpes
        })

    return cve_list
