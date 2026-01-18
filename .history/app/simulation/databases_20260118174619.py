from typing import List, Dict

def simulate_databases() -> List[Dict]:
    """
    Simulate database environments.
    """
    return [
        {
            "name": "user_db",
            "engine": "PostgreSQL",
            "auth_method": "password",
            "network_access": "internal",
            "access_control": "role_based",
            "config_flags": [
                "weak_password_policy"
            ]
        }
    ]
