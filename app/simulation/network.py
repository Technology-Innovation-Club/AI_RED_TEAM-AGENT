<<<<<<< HEAD
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
=======
"""
Simulated Wi-Fi network infrastructure.

This module is responsible ONLY for modeling wireless network
topology and configuration in a safe, offline, and ethical manner.

No attack logic is implemented here.
"""

from app.core.telemetry import log


def simulate_networks(
    enable_rogue_ap: bool = True,
    insecure_defaults: bool = True
):
    """
    Simulates a Wi-Fi network environment.

    Args:
        enable_rogue_ap (bool): Whether to include a rogue access point.
        insecure_defaults (bool): Whether to introduce common misconfigurations.

    Returns:
        list: A list of simulated Wi-Fi network configurations.
    """

    log("Simulating Wi-Fi network topology")

    networks = []

    # -------------------------------------------------
    # Open Wi-Fi Network
    # -------------------------------------------------
    open_wifi = {
        "id": "wifi_open_guest",
        "type": "wifi",
        "role": "guest_access",
        "configuration": {
            "ssid": "Guest_WiFi",
            "encryption": "open",
            "password_policy": "none",
            "broadcasting": True
        },
        "security_flags": {
            "client_isolation": False if insecure_defaults else True,
            "network_segmentation": True,
            "monitoring_enabled": False if insecure_defaults else True
        },
        "known_issues": []
    }

    if insecure_defaults:
        open_wifi["known_issues"].extend([
            "Open authentication (no encryption)",
            "Client isolation disabled",
            "Wireless monitoring not enabled"
        ])

    networks.append(open_wifi)

    # -------------------------------------------------
    # WPA2 Wi-Fi Network
    # -------------------------------------------------
    wpa2_wifi = {
        "id": "wifi_internal_wpa2",
        "type": "wifi",
        "role": "internal_access",
        "configuration": {
            "ssid": "Corp_WiFi",
            "encryption": "WPA2-PSK",
            "password_policy": "weak" if insecure_defaults else "strong",
            "broadcasting": True
        },
        "security_flags": {
            "client_isolation": False,
            "network_segmentation": False if insecure_defaults else True,
            "monitoring_enabled": True
        },
        "known_issues": []
    }

    if insecure_defaults:
        wpa2_wifi["known_issues"].extend([
            "Weak pre-shared key policy",
            "Flat network (no segmentation between users)",
            "Client isolation disabled"
        ])

    networks.append(wpa2_wifi)

    # -------------------------------------------------
    # WPA3 Wi-Fi Network
    # -------------------------------------------------
    wpa3_wifi = {
        "id": "wifi_secure_wpa3",
        "type": "wifi",
        "role": "secure_access",
        "configuration": {
            "ssid": "Secure_WiFi",
            "encryption": "WPA3-SAE",
            "password_policy": "strong",
            "broadcasting": False
        },
        "security_flags": {
            "client_isolation": True,
            "network_segmentation": True,
            "monitoring_enabled": True
        },
        "known_issues": []
    }

    # WPA3 network is intentionally well-configured
    networks.append(wpa3_wifi)

    # -------------------------------------------------
    # Rogue Access Point (Simulated)
    # -------------------------------------------------
    if enable_rogue_ap:
        rogue_ap = {
            "id": "wifi_rogue_ap",
            "type": "wifi",
            "role": "unauthorized",
            "configuration": {
                "ssid": "Corp_WiFi_Free",
                "encryption": "open",
                "password_policy": "none",
                "broadcasting": True
            },
            "security_flags": {
                "client_isolation": False,
                "network_segmentation": False,
                "monitoring_enabled": False
            },
            "known_issues": [
                "Unauthorized (rogue) access point detected",
                "SSID mimics legitimate corporate network",
                "No encryption or access controls",
                "Not monitored by security systems"
            ]
        }

        networks.append(rogue_ap)

    log(f"Simulated {len(networks)} Wi-Fi networks")

    return networks
>>>>>>> f1bcb95265960daf489fa6a0a9429a6b08aeadb7
