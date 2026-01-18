"""
Infrastructure simulation module.
Simulates Wi-Fi and network environments.
No real networking is performed.
"""

from typing import List, Dict

def simulate_networks() -> List[Dict]:
    """
    Simulate Wi-Fi networks and network configurations.
    """
    return [
        {
            "ssid": "CampusNet",
            "encryption": "WPA2",
            "hidden": False,
            "signal_strength": 78,
            "auth_policy": "pre_shared_key",
            "misconfigurations": [
                "weak_passphrase_policy"
            ]
        },
        {
            "ssid": "Guest_WiFi",
            "encryption": "OPEN",
            "hidden": False,
            "signal_strength": 65,
            "auth_policy": "none",
            "misconfigurations": [
                "no_encryption"
            ]
        }
    ]
