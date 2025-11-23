import datetime
import os

ERROR_LOG_FILE = "error_reports.log"

def log_error(source: str, line: str, error: str):
    """Record errors for debugging."""
    
    timestamp = datetime.datetime.utcnow().isoformat()

    entry = (
        f"[{timestamp}] [SOURCE: {source}] "
        f"[ERROR: {error}] "
        f"LINE: {line}\n"
    )

    # Write to log file
    with open(ERROR_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry)

    # Optional: show on console
    print(f"⚠ Logged error → {error}")
