import os
import sys
from datetime import datetime
from error_logger import log_error
from db import save_log

# ------- IMPORT PARSERS -------
from parser_linux import parse_linux_log
from parser_windows_registry import parse_windows_registry
from parser_windows_event import parse_windows_event
from parser_app import parse_app_log

# -------- IMPORT DB ----------
from db import save_log


# ==============================================================================
# 1️⃣ AUTO-DETECT LOG TYPE
# ==============================================================================
def detect_log_type(line: str):
    line = line.strip()

    if not line:
        return None

    # Application logs → contain pipe separators
    if " | " in line:
        return "app"

    # Windows Event logs → EventID=xx
    if "EventID" in line or "SourceName" in line:
        return "windows_event"

    # Windows Registry logs → look like key/value pairs
    if '"' in line and "=" in line:
        return "windows_registry"

    # Linux syslog → typical format "Jan 12 11:00:00 ..."
    return "linux"


# ==============================================================================
# 2️⃣ PARSING DISPATCHER
# ==============================================================================
def dispatch_parser(log_type: str, line: str):
    if log_type == "linux":
        return parse_linux_log(line)
    if log_type == "app":
        return parse_app_log(line)
    if log_type == "windows_registry":
        return parse_windows_registry(line)
    if log_type == "windows_event":
        return parse_windows_event(line)

    return None


# ==============================================================================
# 3️⃣ MAIN LOG PROCESSOR
# ==============================================================================
def process_log_file(filepath: str):
    print(f"➡️ Processing → {filepath}")

    success = 0
    errors = 0

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            for line in file:
                stripped = line.strip()
                if not stripped:
                    continue

                log_type = detect_log_type(stripped)

                if not log_type:
                    log_error(filepath, stripped, "Unknown log type")
                    errors += 1
                    continue

                try:
                    parsed = dispatch_parser(log_type, stripped)

                    if parsed:
                        save_log(parsed)
                        success += 1
                    else:
                        log_error(filepath, stripped, "Parser returned None")
                        errors += 1

                except Exception as exc:
                    log_error(filepath, stripped, f"Exception in parser: {exc}")
                    errors += 1

    except Exception as e:
        print(f"❌ ERROR reading {filepath}: {e}")
        return

    print(f"    ✔ Saved: {success}  |  ❌ Errors: {errors}")


# ==============================================================================
# 4️⃣ ENTRY POINT — AUTOMATICALLY SCAN sample_logs/
# ==============================================================================
def main():
    LOG_DIR = "sample_logs"

    if not os.path.exists(LOG_DIR):
        print(f"❌ ERROR: Folder '{LOG_DIR}' not found!")
        sys.exit(1)

    print("\n📥 Collecting logs...\n")

    log_files = [f for f in os.listdir(LOG_DIR) if f.endswith(".txt")]

    if not log_files:
        print("❌ No log files found in sample_logs/")
        sys.exit(0)

    # Show discovered files
    for f in log_files:
        print(f"📄 Found → {f}")

    print("\n📌 START PROCESSING...\n")

    # Process all discovered log files
    for f in log_files:
        process_log_file(os.path.join(LOG_DIR, f))

    print("\n🎉 DONE — All logs parsed and saved.\n")


# ==============================================================================
# RUN
# ==============================================================================
if __name__ == "__main__":
    main()
