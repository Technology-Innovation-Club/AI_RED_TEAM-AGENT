import json
import os
from datetime import datetime, timezone
from app.ai_red_team.attack_library import get_attack_function

# Configuration
DATA_DIR = "app/data"
RESULTS_FILE = os.path.join(DATA_DIR, "attack_results.json")

def save_result_to_json(result_data):
    """Helper to append results to the JSON log."""
    os.makedirs(DATA_DIR, exist_ok=True)
    current_data = []
    if os.path.exists(RESULTS_FILE):
        try:
            with open(RESULTS_FILE, 'r') as f:
                content = f.read()
                if content:
                    current_data = json.loads(content)
                    if isinstance(current_data, dict): current_data = [current_data]
        except json.JSONDecodeError:
            pass # File exists but is corrupt/empty, start fresh
            
    current_data.append(result_data)
    with open(RESULTS_FILE, 'w') as f:
        json.dump(current_data, f, indent=4)

def execute_attack_plan(planned_attacks_list, infrastructure_context):
    """
    Executes a list of planned attacks step-by-step.
    Handles success/failure logic dynamically.
    """
    execution_log = []
    campaign_active = True  # Flag to stop chain if critical failure occurs

    print(f"[*] Starting execution of {len(planned_attacks_list)} planned attacks...")

    for attack_plan in planned_attacks_list:
        
        # 1. Check if we should continue based on previous failure
        if not campaign_active:
            result_entry = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "target_name": attack_plan['target_name'],
                "attack_type": attack_plan['attack_type'],
                "status": "Skipped",
                "reasoning": "Dependency failed in previous step.",
                "evidence_artifact": "N/A"
            }
            save_result_to_json(result_entry)
            execution_log.append(result_entry)
            continue

        # 2. Resolve target details (Simulated lookup)
        # In a real scenario, we would search infrastructure_context by ID
        target_id = attack_plan.get("target_id")
        # Creating a combined context for the function to read
        target_details = next((item for item in infrastructure_context.get("assets", []) if item["id"] == target_id), {})
        
        if not target_details:
             target_details = {"name": attack_plan['target_name']} # Fallback

        # 3. Get the simulation logic
        attack_func = get_attack_function(attack_plan['attack_type'])
        
        if not attack_func:
            print(f"[!] Unknown attack type: {attack_plan['attack_type']}")
            continue

        # 4. Execute Step
        print(f"[*] Executing {attack_plan['attack_type']} on {attack_plan['target_name']}...")
        simulation_result = attack_func(target_details)

        # 5. Handle Success/Failure Logic
        status = "Success" if simulation_result['success'] else "Failed"
        
        # Logic: If a lateral movement fails, stop the chain
        if not simulation_result['success'] and "Lateral" in attack_plan['attack_type']:
            campaign_active = False
            print("[!] Critical step failed. Aborting downstream attacks.")

        # 6. Capture Evidence & Timestamp
        result_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "target_id": target_id,
            "target_name": attack_plan['target_name'],
            "attack_type": attack_plan['attack_type'],
            "phase": attack_plan.get('phase', 'Unknown'),
            "status": status,
            "reasoning": attack_plan.get("reasoning", "No reasoning provided"),
            "evidence_artifact": simulation_result['evidence'],
            "simulation_log": simulation_result['log']
        }

        # 7. Export to JSON
        save_result_to_json(result_entry)
        execution_log.append(result_entry)

    return execution_log