from flask import Flask, render_template, request, redirect
from pathlib import Path
import sys, os

# Allow importing backend files (main.py, db/)
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import main                                      # ⬅ keep main.py imports untouched
from cve.cve_fetcher import download_full_cve_feed
from db.mongo_client import get_mongo_client

app = Flask(__name__)

# Upload directory
UPLOAD_DIR = Path(__file__).resolve().parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_log():
    file = request.files["logfile"]
    if not file:
        return redirect("/")

    filepath = UPLOAD_DIR / file.filename
    file.save(filepath)

    # Run backend log parser from Week 1
    main.process_log_file(str(filepath))

    return render_template(
        "results.html",
        message=f"Log processed successfully: {file.filename}"
    )


@app.route("/view_logs")
def view_logs():
    db = get_mongo_client()["vapt_db"]
    records = list(db.normalized_logs.find().sort("_id", -1).limit(25))
    return render_template("results.html", logs=records)


@app.route("/sync_cve")
def sync_cve():
    path = download_full_cve_feed()  # Week 2 (NVD sync)
    return render_template(
        "results.html",
        message=f"CVE Database synced successfully: {path}"
    )

@app.route("/view_errors")
def view_errors():
    log_file = Path(__file__).resolve().parent.parent / "error_reports.log"

    if not log_file.exists():
        return render_template("results.html", message="No errors recorded yet.")

    with open(log_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    return render_template("results.html", errors=lines)



if __name__ == "__main__":
    app.run(debug=True, port=5000)
