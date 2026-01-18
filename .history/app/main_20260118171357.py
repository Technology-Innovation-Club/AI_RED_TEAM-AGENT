   """
Telemetry and logging module.
Records simulation events in a safe, offline manner.
"""

import json
from datetime import datetime
from pathlib import Path

LOG_FILE = Path("app/data/system_logs.json")

def log_event(component: str, message: str):
    """
    Log a telemetry event.
    """
    event = {
        "timestamp": datetime.utcnow().isoformat(),
        "component": component,
        "message": message
    }

    if LOG_FILE.exists():
        data = json.loads(LOG_FILE.read_text())
    else:
        data = {"events": []}

    data["events"].append(event)
    LOG_FILE.write_text(json.dumps(data, indent=2))
 