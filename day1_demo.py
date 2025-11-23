# this file has sample logs which i used this sample logs to test if my mongodb is receining data correct
from db import insert_log, get_all_logs

sample_log = {
    "timestamp": "2025-11-10 14:00:00",
    "host": "ServerX",
    "os": "Ubuntu",
    "software": "Apache",
    "version": "2.4.29",
    "event_type": "service_start",
    "message": "Started Apache/2.4.29 (Ubuntu)",
    "source": "syslog"
}

insert_log(sample_log)
logs = get_all_logs()
print("Inserted logs:", logs)
