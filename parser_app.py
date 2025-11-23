import re
from validators.validator import validate_and_prepare

APP_LOG_REGEX = r"^(.+?)\s+\|\s+(.+?)\s+\|\s+(.+?)\s+\|\s+(.*)$"

def parse_app_log(line: str):
    match = re.match(APP_LOG_REGEX, line)
    if not match:
        return None

    timestamp, software, event_type, message = match.groups()

    log_doc = {
        "timestamp": timestamp,
        "host": "Application-Host",
        "os": "Unknown",
        "software": software,
        "version": None,
        "event_type": event_type.lower(),
        "message": message,
        "source": "application",
    }

    return validate_and_prepare(log_doc)
