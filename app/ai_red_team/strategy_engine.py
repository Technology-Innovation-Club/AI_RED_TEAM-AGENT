import json
import logging
from enum import Enum

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AARTA_Strategy_Engine")

# --- DEFINE RED TEAM ATTACK PHASES ---
class AttackPhase(Enum):
    RECON = "Reconnaissance"
    EXPLOIT = "Exploitation"
    POST_EXPLOIT = "Post-Exploitation"

class StrategyEngine:
    """
    The 'Brain' of the AI Red Team Agent.
    Parses infrastructure data, identifies the attack surface,
    and dynamically selects simulated attacks with reasoning.
    """

    def __init__(self):
        self.attack_plan = []
        
    def generate_attack_plan(self, infrastructure_json):
        """
        Main entry point.
        1. Parses infrastructure state from JSON.
        2. Identifies attack surface per asset.
        3. Selects attacks dynamically based on phases.
        """
        self.attack_plan = []
        
        # 1. Parse Infrastructure State
        if isinstance(infrastructure_json, str):
            try:
                data = json.loads(infrastructure_json)
            except json.JSONDecodeError:
                logger.error("Invalid JSON provided to Strategy Engine.")
                return []
        else:
            data = infrastructure_json

        assets = data.get("assets", [])
        logger.info(f"Analyzing attack surface for {len(assets)} assets...")

        # 2. Analyze each asset to build the plan
        for asset in assets:
            self._analyze_asset_attack_surface(asset)

        # 3. Sort plan by Phase order (Recon -> Exploit -> Post-Exploit)
        phase_order = {
            AttackPhase.RECON.value: 1, 
            AttackPhase.EXPLOIT.value: 2, 
            AttackPhase.POST_EXPLOIT.value: 3
        }
        self.attack_plan.sort(key=lambda x: phase_order.get(x['phase'], 4))
        
        return self.attack_plan

    def _analyze_asset_attack_surface(self, asset):
        """
        Logic core: Evaluates an asset's properties (ports, tags, OS)
        and maps them to specific simulated attacks.
        """
        target_id = asset.get("id")
        target_name = asset.get("name")
        open_ports = asset.get("open_ports", [])
        vuln_tags = asset.get("vuln_tags", [])
        services = asset.get("services", {})
        
        # --- PHASE 1: RECONNAISSANCE ---
        # Logic: If we don't know services yet, we must scan.
        if not services and open_ports:
             self._add_attack(
                target_id, target_name,
                "Simulated Service Discovery",
                AttackPhase.RECON,
                f"Ports {open_ports} are detected but services are unidentified. Fingerprinting required."
            )
        
        # Logic: Enumeration is always valuable on web ports
        if 80 in open_ports or 443 in open_ports or 8080 in open_ports:
            self._add_attack(
                target_id, target_name,
                "Simulated Credential Enumeration",
                AttackPhase.RECON,
                "Web ports detected. Attempting to harvest metadata or usernames from public endpoints."
            )

        # --- PHASE 2: EXPLOITATION ---
        # Logic: SQL Injection
        if "database" in asset.get("type", "").lower() or "sql_injection" in vuln_tags:
            self._add_attack(
                target_id, target_name,
                "Simulated SQL Injection",
                AttackPhase.EXPLOIT,
                "Asset identified as a database or flagged with SQLi vulnerability. Testing for data exfiltration."
            )

        # Logic: Brute Force
        if "weak_password_policy" in vuln_tags or "default_creds" in vuln_tags:
             self._add_attack(
                target_id, target_name,
                "Simulated Brute Force",
                AttackPhase.EXPLOIT,
                f"Weak authentication indicators {vuln_tags} detected. Attempting dictionary attack."
            )

        # Logic: Auth Bypass
        if "broken_access_control" in vuln_tags or "api_auth_disabled" in vuln_tags:
            self._add_attack(
                target_id, target_name,
                "Simulated Auth Bypass",
                AttackPhase.EXPLOIT,
                "Access control flaws detected. Attempting to bypass login via forced browsing."
            )

        # --- PHASE 3: POST-EXPLOITATION ---
        # Logic: Privilege Escalation
        if "misconfigured_sudo" in vuln_tags or asset.get("kernel_version", 9.9) < 5.0:
            self._add_attack(
                target_id, target_name,
                "Simulated Privilege Escalation",
                AttackPhase.POST_EXPLOIT,
                "Kernel version or sudo config suggests root compromise is possible."
            )

        # Logic: Lateral Movement
        if asset.get("internal_trust_level", 0) > 5:
            self._add_attack(
                target_id, target_name,
                "Simulated Lateral Movement",
                AttackPhase.POST_EXPLOIT,
                "Asset has high internal trust level. Attempting to pivot to adjacent internal systems."
            )

    def _add_attack(self, t_id, t_name, attack_type, phase, reasoning):
        """Helper to structure the attack entry for the final JSON plan."""
        plan_entry = {
            "target_id": t_id,
            "target_name": t_name,
            "attack_type": attack_type,
            "phase": phase.value,
            "reasoning": reasoning,
            "status": "Pending"
        }
        self.attack_plan.append(plan_entry)

def get_strategy_engine():
    return StrategyEngine()