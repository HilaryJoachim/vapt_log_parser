import re
from validators.validator import validate_and_prepare
from error_logger import log_error    # ✅ MUST ADD THIS

EVENT_REGEX = r"EventID=(\d+)\s+User=(\S+)\s+Time=([\w:\-T]+)\s+Message=\"(.+)\""

def parse_windows_event(line: str):
    try:
        match = re.match(EVENT_REGEX, line)
        if not match:
            log_error("windows_event", line, "Regex mismatch")
            return None

        event_id, user, timestamp, message = match.groups()

        log_doc = {
            "timestamp": timestamp,
            "host": "windows-host",
            "os": "Windows",
            "software": "WindowsEventLog",
            "version": None,
            "event_type": f"event_{event_id}",
            "user": user,
            "message": message,
            "source": "event_log"
        }

        validated = validate_and_prepare(log_doc)
        if validated is None:
            log_error("windows_event", line, "Schema validation failed")

        return validated

    except Exception as e:
        log_error("windows_event", line, f"Unexpected error: {str(e)}")
        return None
