"""
Simulated Wi-Fi network infrastructure.

This module is responsible ONLY for modeling wireless network
topology and configuration in a safe, offline, and ethical manner.

No attack logic is implemented here.
"""

from typing import List, Dict, Any
import uuid


class NetworkSimulation:
    """
    Simulates Wi-Fi network infrastructure for red team exercises.
    All networks are virtual and contain no real connectivity.
    """
    
    def __init__(self):
        self.networks: List[Dict[str, Any]] = []
        self.telemetry = None
    
    def add_open_network(self, ssid: str, signal_strength: int = 75) -> str:
        """
        Add an open (unencrypted) Wi-Fi network.
        
        Args:
            ssid: Network name
            signal_strength: Signal strength percentage
            
        Returns:
            Network ID
        """
        network_id = f"wifi_open_{uuid.uuid4().hex[:8]}"
        
        network = {
            "id": network_id,
            "type": "wifi",
            "role": "guest_access",
            "configuration": {
                "ssid": ssid,
                "encryption": "open",
                "password_policy": "none",
                "broadcasting": True,
                "signal_strength": signal_strength
            },
            "security_flags": {
                "client_isolation": False,
                "network_segmentation": True,
                "monitoring_enabled": False
            },
            "known_issues": [
                "Open authentication (no encryption)",
                "Client isolation disabled",
                "Wireless monitoring not enabled"
            ],
            "vulnerabilities": [
                "unauthorized_access",
                "traffic_interception",
                "man_in_the_middle"
            ]
        }
        
        self.networks.append(network)
        return network_id
    
    def add_wpa2_network(self, ssid: str, misconfigured: bool = False, signal_strength: int = 80) -> str:
        """
        Add a WPA2-PSK encrypted Wi-Fi network.
        
        Args:
            ssid: Network name
            misconfigured: Whether to introduce security misconfigurations
            signal_strength: Signal strength percentage
            
        Returns:
            Network ID
        """
        network_id = f"wifi_wpa2_{uuid.uuid4().hex[:8]}"
        
        network = {
            "id": network_id,
            "type": "wifi",
            "role": "internal_access",
            "configuration": {
                "ssid": ssid,
                "encryption": "WPA2-PSK",
                "password_policy": "weak" if misconfigured else "strong",
                "broadcasting": True,
                "signal_strength": signal_strength
            },
            "security_flags": {
                "client_isolation": False,
                "network_segmentation": False if misconfigured else True,
                "monitoring_enabled": True
            },
            "known_issues": [],
            "vulnerabilities": []
        }
        
        if misconfigured:
            network["known_issues"].extend([
                "Weak pre-shared key policy",
                "Flat network (no segmentation between users)",
                "Client isolation disabled"
            ])
            network["vulnerabilities"].extend([
                "weak_encryption",
                "lateral_movement",
                "credential_theft"
            ])
        
        self.networks.append(network)
        return network_id
    
    def add_wpa3_network(self, ssid: str, signal_strength: int = 85) -> str:
        """
        Add a WPA3-SAE encrypted Wi-Fi network (secure configuration).
        
        Args:
            ssid: Network name
            signal_strength: Signal strength percentage
            
        Returns:
            Network ID
        """
        network_id = f"wifi_wpa3_{uuid.uuid4().hex[:8]}"
        
        network = {
            "id": network_id,
            "type": "wifi",
            "role": "secure_access",
            "configuration": {
                "ssid": ssid,
                "encryption": "WPA3-SAE",
                "password_policy": "strong",
                "broadcasting": False,
                "signal_strength": signal_strength
            },
            "security_flags": {
                "client_isolation": True,
                "network_segmentation": True,
                "monitoring_enabled": True
            },
            "known_issues": [],
            "vulnerabilities": []
        }
        
        self.networks.append(network)
        return network_id
    
    def add_rogue_ap(self, ssid: str, target_ssid: str = None) -> str:
        """
        Add a rogue access point (evil twin).
        
        Args:
            ssid: Rogue AP SSID
            target_ssid: Legitimate network being mimicked
            
        Returns:
            Network ID
        """
        network_id = f"wifi_rogue_{uuid.uuid4().hex[:8]}"
        
        network = {
            "id": network_id,
            "type": "wifi",
            "role": "unauthorized",
            "configuration": {
                "ssid": ssid,
                "encryption": "open",
                "password_policy": "none",
                "broadcasting": True,
                "signal_strength": 90,
                "target_ssid": target_ssid
            },
            "security_flags": {
                "client_isolation": False,
                "network_segmentation": False,
                "monitoring_enabled": False
            },
            "known_issues": [
                "Unauthorized (rogue) access point detected",
                "SSID mimics legitimate corporate network" if target_ssid else "Suspicious network name",
                "No encryption or access controls",
                "Not monitored by security systems"
            ],
            "vulnerabilities": [
                "credential_harvesting",
                "man_in_the_middle",
                "malware_distribution"
            ]
        }
        
        self.networks.append(network)
        return network_id
    
    def export(self) -> List[Dict[str, Any]]:
        """
        Export all networks as structured data.
        
        Returns:
            List of network configurations
        """
        return self.networks
    
    def get_network_by_id(self, network_id: str) -> Dict[str, Any]:
        """
        Get a specific network by ID.
        
        Args:
            network_id: Network identifier
            
        Returns:
            Network configuration or empty dict if not found
        """
        for network in self.networks:
            if network["id"] == network_id:
                return network
        return {}
    
    def get_networks_by_type(self, encryption_type: str) -> List[Dict[str, Any]]:
        """
        Get all networks with specific encryption type.
        
        Args:
            encryption_type: Encryption type (open, WPA2-PSK, WPA3-SAE)
            
        Returns:
            List of matching networks
        """
        return [n for n in self.networks if n["configuration"]["encryption"] == encryption_type]
    
    def get_vulnerable_networks(self) -> List[Dict[str, Any]]:
        """
        Get all networks with known vulnerabilities.
        
        Returns:
            List of vulnerable networks
        """
        return [n for n in self.networks if n["vulnerabilities"]]
