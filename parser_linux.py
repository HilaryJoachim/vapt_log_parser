import re
from datetime import datetime
from validators.validator import validate_and_prepare
from error_logger import log_error

# Patterns
SYSLOG_REGEX = r"^(\w{3})\s+(\d{1,2})\s+(\d\d:\d\d:\d\d)\s+(\S+)\s+(\S+):\s+(.*)$"
SYSLOG_PID_REGEX = r"^(\w{3})\s+(\d{1,2})\s+(\d\d:\d\d:\d\d)\s+(\S+)\s+(\S+)\[(\d+)\]:\s+(.*)$"
SSHD_REGEX = r"^(\w{3})\s+(\d{1,2})\s+(\d\d:\d\d:\d\d)\s+\S+\s+sshd(?:\[\d+\])?:\s+(.*)$"
SUDO_REGEX = r"^(\w{3})\s+(\d{1,2})\s+(\d\d:\d\d:\d\d)\s+\S+\s+sudo(?:\[\d+\])?:\s+(.*)$"


def _convert_to_timestamp(month, day, time):
    year = datetime.now().year
    full = f"{month} {day} {year} {time}"
    return datetime.strptime(full, "%b %d %Y %H:%M:%S").isoformat()


def parse_linux_log(line: str):

    # -------------------------
    # 1️⃣ syslog with PID
    # -------------------------
    match = re.match(SYSLOG_PID_REGEX, line)
    if match:
        month, day, time, host, software, pid, message = match.groups()

        try:
            log_doc = {
                "timestamp": _convert_to_timestamp(month, day, time),
                "host": host,
                "os": "Linux",
                "software": software,
                "version": None,
                "event_type": "process",
                "pid": pid,
                "message": message,
                "source": "syslog",
            }
            return validate_and_prepare(log_doc)
        except Exception as e:
            log_error("linux_syslog", line, str(e))
            return None

    # -------------------------
    # 2️⃣ normal syslog
    # -------------------------
    match = re.match(SYSLOG_REGEX, line)
    if match:
        month, day, time, host, software, message = match.groups()

        try:
            log_doc = {
                "timestamp": _convert_to_timestamp(month, day, time),
                "host": host,
                "os": "Linux",
                "software": software,
                "version": None,
                "event_type": "service_start" if "Started" in message else None,
                "message": message,
                "source": "syslog",
            }
            return validate_and_prepare(log_doc)
        except Exception as e:
            log_error("linux_syslog", line, str(e))
            return None

    # -------------------------
    # 3️⃣ SSHD events
    # -------------------------
    match = re.match(SSHD_REGEX, line)
    if match:
        month, day, time, message = match.groups()

        try:
            log_doc = {
                "timestamp": _convert_to_timestamp(month, day, time),
                "host": "linux-host",
                "os": "Linux",
                "software": "sshd",
                "version": None,
                "event_type": "ssh_auth",
                "message": message,
                "source": "auth",
            }
            return validate_and_prepare(log_doc)
        except Exception as e:
            log_error("linux_syslog", line, str(e))
            return None

    # -------------------------
    # 4️⃣ SUDO events
    # -------------------------
    match = re.match(SUDO_REGEX, line)
    if match:
        month, day, time, message = match.groups()

        try:
            log_doc = {
                "timestamp": _convert_to_timestamp(month, day, time),
                "host": "linux-host",
                "os": "Linux",
                "software": "sudo",
                "version": None,
                "event_type": "privilege_escalation",
                "message": message,
                "source": "auth",
            }
            return validate_and_prepare(log_doc)
        except Exception as e:
            log_error("linux_syslog", line, str(e))
            return None

    # -------------------------
    # No match → LOG IT
    # -------------------------
    log_error("linux_syslog", line, "No matching regex pattern")
    return None
