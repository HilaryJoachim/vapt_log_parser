import re
from datetime import datetime
from validators.validator import validate_and_prepare
from error_logger import log_error   # ✅ ADD THIS

def parse_windows_registry(block: str):
    try:
        software = None
        version = None

        # Extract Software Name
        name_match = re.search(r'"DisplayName"\s*=\s*"(.+?)"', block)
        if name_match:
            software = name_match.group(1)
        else:
            log_error("windows_registry", block, "Missing DisplayName")
            return None

        # Extract Version
        version_match = re.search(r'"Version"\s*=\s*"(.+?)"', block)
        if version_match:
            version = version_match.group(1)
        else:
            # Version missing is not fatal, but we record it anyway
            log_error("windows_registry", block, "Missing Version (continuing...)")

        log_doc = {
            "timestamp": datetime.utcnow().isoformat(),
            "host": "windows-host",
            "os": "Windows",
            "software": software,
            "version": version,
            "event_type": "registry_modify",
            "message": block.strip(),
            "source": "registry"
        }

        validated = validate_and_prepare(log_doc)
        if validated is None:
            log_error("windows_registry", block, "Schema validation failed")
        return validated

    except Exception as e:
        # Final fallback for unexpected errors
        log_error("windows_registry", block, f"Unexpected error: {str(e)}")
        return None
