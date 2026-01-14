"""
attack_library.py
Contains the logic for SIMULATED attacks.
No real exploit code. Returns dictionaries with simulation outcomes.
"""

def simulated_port_scan(target_details):
    open_ports = target_details.get("open_ports", [])
    if open_ports:
        return {
            "success": True,
            "evidence": f"Open ports found: {', '.join(map(str, open_ports))}",
            "log": "SYN Stealth Scan completed. 1000 ports scanned.",
            "next_stage_available": True
        }
    else:
        return {
            "success": False,
            "evidence": "No open ports found.",
            "log": "All ports filtered.",
            "next_stage_available": False
        }

def simulated_service_discovery(target_details):
    services = target_details.get("services", {})
    if services:
        evidence = [f"Port {p}: {s}" for p, s in services.items()]
        return {
            "success": True,
            "evidence": "Services identified:\n" + "\n".join(evidence),
            "log": "Version detection scripts executed successfully.",
            "next_stage_available": True
        }
    return {"success": False, "evidence": "Service fingerprinting failed.", "log": "No banners.", "next_stage_available": False}

def simulated_credential_enumeration(target_details):
    if "exposed_metadata" in target_details.get("vuln_tags", []):
        return {
            "success": True,
            "evidence": "Enumerated users: [admin, backup, dev_test]",
            "log": "Found /authors.json leaking usernames.",
            "next_stage_available": True
        }
    return {"success": False, "evidence": "No user enumeration vectors.", "log": "Clean.", "next_stage_available": False}

def simulated_sql_injection(target_details):
    is_db = "database" in target_details.get("type", "").lower()
    sanitization = target_details.get("input_sanitization", True)
    if is_db and not sanitization:
        return {
            "success": True,
            "evidence": "Dumped 'users' table (50 records).",
            "log": "Payload 'OR 1=1' accepted.",
            "next_stage_available": True
        }
    return {"success": False, "evidence": "Input sanitized. WAF blocked.", "log": "Rejected.", "next_stage_available": False}

def simulated_brute_force(target_details):
    weak_policy = "weak_password_policy" in target_details.get("vuln_tags", [])
    default_creds = "default_creds" in target_details.get("vuln_tags", [])
    if weak_policy or default_creds:
        return {
            "success": True,
            "evidence": "Cracked password: 'password123' (admin).",
            "log": "Match found at attempt #42.",
            "next_stage_available": True
        }
    return {"success": False, "evidence": "Account locked.", "log": "Failed.", "next_stage_available": False}

def simulated_auth_bypass(target_details):
    if "broken_access_control" in target_details.get("vuln_tags", []):
        return {
            "success": True,
            "evidence": "Accessed /admin/dashboard without token.",
            "log": "Forced browsing succeeded.",
            "next_stage_available": True
        }
    return {"success": False, "evidence": "401 Unauthorized.", "log": "Secured.", "next_stage_available": False}

def simulated_privilege_escalation(target_details):
    kernel = target_details.get("kernel_version", 6.0)
    sudo_bad = "misconfigured_sudo" in target_details.get("vuln_tags", [])
    if kernel < 5.0 or sudo_bad:
        return {
            "success": True,
            "evidence": "EUID changed to 0 (root).",
            "log": "Exploited sudo config.",
            "next_stage_available": True
        }
    return {"success": False, "evidence": "Permission Denied.", "log": "Failed.", "next_stage_available": False}

def simulated_lateral_movement(target_details):
    if target_details.get("internal_trust_level", 0) > 5:
        return {
            "success": True,
            "evidence": f"Established SSH tunnel to {target_details.get('name')}.",
            "log": "Key auth successful.",
            "next_stage_available": True
        }
    return {"success": False, "evidence": "Connection refused.", "log": "Failed.", "next_stage_available": False}

# REGISTRY
ATTACK_REGISTRY = {
    "Simulated Port Scan": simulated_port_scan,
    "Simulated Service Discovery": simulated_service_discovery,
    "Simulated Credential Enumeration": simulated_credential_enumeration,
    "Simulated SQL Injection": simulated_sql_injection,
    "Simulated Brute Force": simulated_brute_force,
    "Simulated Privilege Escalation": simulated_privilege_escalation,
    "Simulated Auth Bypass": simulated_auth_bypass,
    "Simulated Lateral Movement": simulated_lateral_movement
}

def get_attack_function(attack_type):
    return ATTACK_REGISTRY.get(attack_type)