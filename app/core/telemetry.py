"""
Centralized telemetry and logging system for the AI Red Team Agent.
Provides structured logging for all components.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional


class Telemetry:
    """
    Centralized logging and telemetry system.
    Tracks all system events, access attempts, and security events.
    """
    
    def __init__(self, log_file: Optional[str] = None):
        self.log_file = Path(log_file or "app/data/system_logs.json")
        self.events: List[Dict[str, Any]] = []
        self.session_id = f"session_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Ensure log directory exists
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Load existing logs if file exists
        self._load_existing_logs()
    
    def _load_existing_logs(self):
        """Load existing logs from file."""
        try:
            if self.log_file.exists():
                data = json.loads(self.log_file.read_text())
                self.events = data.get("events", [])
        except (json.JSONDecodeError, FileNotFoundError):
            self.events = []
    
    def log(self, event_type: str, message: str, component: str = "system", 
            severity: str = "info", source_ip: str = "127.0.0.1", 
            success: bool = True, details: Dict[str, Any] = None):
        """
        Log a telemetry event.
        
        Args:
            event_type: Type of event (e.g., "WiFi Scan", "SSH Login")
            message: Event description
            component: Component generating the event
            severity: Event severity (info, warning, error, critical)
            source_ip: Source IP address
            success: Whether the event was successful
            details: Additional event details
        """
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "session_id": self.session_id,
            "event_type": event_type,
            "message": message,
            "component": component,
            "severity": severity,
            "source_ip": source_ip,
            "success": success,
            "details": details or {}
        }
        
        self.events.append(event)
        
        # Keep only last 1000 events in memory
        if len(self.events) > 1000:
            self.events = self.events[-1000:]
    
    def log_access_attempt(self, service: str, username: str, source_ip: str, 
                          success: bool, reason: str = None):
        """Log access attempt to a service."""
        self.log(
            event_type="Access Attempt",
            message=f"{service} login attempt for user '{username}'",
            component=service,
            severity="info" if success else "warning",
            source_ip=source_ip,
            success=success,
            details={
                "username": username,
                "reason": reason
            }
        )
    
    def log_network_discovery(self, network_type: str, target: str, 
                            findings: List[str], source_ip: str = "127.0.0.1"):
        """Log network discovery activity."""
        self.log(
            event_type="Network Discovery",
            message=f"{network_type} discovery of {target}",
            component="network_scanner",
            severity="info",
            source_ip=source_ip,
            success=True,
            details={
                "target": target,
                "findings": findings
            }
        )
    
    def log_vulnerability_found(self, vulnerability: str, target: str, 
                              severity: str, source_ip: str = "127.0.0.1"):
        """Log vulnerability discovery."""
        self.log(
            event_type="Vulnerability Found",
            message=f"{vulnerability} discovered on {target}",
            component="vulnerability_scanner",
            severity=severity,
            source_ip=source_ip,
            success=True,
            details={
                "vulnerability": vulnerability,
                "target": target
            }
        )
    
    def log_attack_execution(self, attack_type: str, target: str, 
                            success: bool, details: Dict[str, Any] = None):
        """Log attack execution."""
        self.log(
            event_type="Attack Execution",
            message=f"{attack_type} against {target}",
            component="attack_executor",
            severity="warning" if success else "info",
            source_ip="127.0.0.1",
            success=success,
            details=details or {"attack_type": attack_type, "target": target}
        )
    
    def log_system_event(self, event: str, message: str, severity: str = "info"):
        """Log general system event."""
        self.log(
            event_type="System Event",
            message=message,
            component="system",
            severity=severity,
            source_ip="127.0.0.1",
            success=True,
            details={"event": event}
        )
    
    def get_events_by_component(self, component: str) -> List[Dict[str, Any]]:
        """Get all events from a specific component."""
        return [event for event in self.events if event["component"] == component]
    
    def get_events_by_severity(self, severity: str) -> List[Dict[str, Any]]:
        """Get all events with specific severity."""
        return [event for event in self.events if event["severity"] == severity]
    
    def get_recent_events(self, count: int = 50) -> List[Dict[str, Any]]:
        """Get the most recent events."""
        return self.events[-count:]
    
    def get_failed_attempts(self) -> List[Dict[str, Any]]:
        """Get all failed access attempts."""
        return [event for event in self.events if not event["success"]]
    
    def export(self) -> List[Dict[str, Any]]:
        """Export all events as structured data."""
        return self.events
    
    def save_to_file(self, file_path: Optional[str] = None):
        """Save logs to file."""
        target_file = Path(file_path) if file_path else self.log_file
        
        log_data = {
            "metadata": {
                "session_id": self.session_id,
                "total_events": len(self.events),
                "last_updated": datetime.utcnow().isoformat()
            },
            "events": self.events
        }
        
        target_file.parent.mkdir(parents=True, exist_ok=True)
        target_file.write_text(json.dumps(log_data, indent=2))
    
    def clear_logs(self):
        """Clear all logs from memory."""
        self.events = []
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get telemetry statistics."""
        if not self.events:
            return {"total_events": 0}
        
        stats = {
            "total_events": len(self.events),
            "successful_events": len([e for e in self.events if e["success"]]),
            "failed_events": len([e for e in self.events if not e["success"]]),
            "severity_breakdown": {},
            "component_breakdown": {},
            "event_types": {}
        }
        
        for event in self.events:
            # Severity breakdown
            severity = event["severity"]
            stats["severity_breakdown"][severity] = stats["severity_breakdown"].get(severity, 0) + 1
            
            # Component breakdown
            component = event["component"]
            stats["component_breakdown"][component] = stats["component_breakdown"].get(component, 0) + 1
            
            # Event types
            event_type = event["event_type"]
            stats["event_types"][event_type] = stats["event_types"].get(event_type, 0) + 1
        
        return stats


# Global telemetry instance for backward compatibility
_telemetry_instance = None


def get_telemetry() -> Telemetry:
    """Get or create the global telemetry instance."""
    global _telemetry_instance
    if _telemetry_instance is None:
        _telemetry_instance = Telemetry()
    return _telemetry_instance


# Backward compatibility functions
def log_event(component: str, message: str):
    """Legacy function for backward compatibility."""
    telemetry = get_telemetry()
    telemetry.log("Legacy Event", message, component)


def log(event_type: str, message: str):
    """Simple logging function for quick use."""
    telemetry = get_telemetry()
    telemetry.log(event_type, message)