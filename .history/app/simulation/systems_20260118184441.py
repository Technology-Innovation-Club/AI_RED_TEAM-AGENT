"""
Infrastructure simulation module.
Simulates servers and operating systems.
No real systems are accessed.
"""

from typing import List, Dict

def simulate_systems() -> List[Dict]:
    """
    Simulate server and system configurations.
    """
    return [
        {
            "hostname": "auth-server",
            "os": "Linux",
            "os_version": "Ubuntu 20.04",
            "role": "authentication",
            "open_ports": [22, 80],
            "services": ["ssh", "http"],
            "config_flags": [
                "default_credentials_enabled"
            ]
        },
        {
            "hostname": "file-server",
            "os": "Windows",
            "os_version": "Windows Server 2016",
            "role": "storage",
            "open_ports": [445],
            "services": ["smb"],
            "config_flags": [
                "legacy_protocol_enabled"
            ]
        }
    ]
git status