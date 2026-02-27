"""
State Manager - Handles JSON-based state persistence for AARTA.
Manages reading/writing of infrastructure, attack results, and reports.
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime


class StateManager:
    """
    Manages application state through JSON file persistence.
    Handles infrastructure data, attack results, vulnerabilities, and reports.
    """
    
    def __init__(self, data_dir: str = "app/data"):
        self.data_dir = Path(data_dir)
        self.infrastructure_file = self.data_dir / "infrastructure.json"
        self.attack_results_file = self.data_dir / "attack_results.json"
        self.vulnerabilities_file = self.data_dir / "vulnerabilities.json"
        self.report_file = self.data_dir / "report.json"
        self.report_md_file = self.data_dir / "report.md"
        
        # Ensure data directory exists
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize empty state files if they don't exist
        self._initialize_state_files()
    
    def _initialize_state_files(self):
        """Initialize empty state files if they don't exist."""
        empty_infrastructure = {
            "networks": [],
            "systems": [],
            "databases": [],
            "metadata": {
                "created_at": datetime.utcnow().isoformat(),
                "version": "1.0.0"
            }
        }
        
        empty_attack_results = {
            "attacks": [],
            "metadata": {
                "created_at": datetime.utcnow().isoformat(),
                "total_attacks": 0,
                "successful_attacks": 0,
                "failed_attacks": 0
            }
        }
        
        empty_vulnerabilities = {
            "vulnerabilities": [],
            "metadata": {
                "created_at": datetime.utcnow().isoformat(),
                "total_vulnerabilities": 0,
                "severity_breakdown": {
                    "critical": 0,
                    "high": 0,
                    "medium": 0,
                    "low": 0,
                    "info": 0
                }
            }
        }
        
        empty_report = {
            "metadata": {
                "generated_at": None,
                "session_id": None,
                "total_vulnerabilities": 0
            },
            "content": None
        }
        
        # Create files with empty structure if they don't exist
        if not self.infrastructure_file.exists():
            self._write_json(self.infrastructure_file, empty_infrastructure)
        
        if not self.attack_results_file.exists():
            self._write_json(self.attack_results_file, empty_attack_results)
        
        if not self.vulnerabilities_file.exists():
            self._write_json(self.vulnerabilities_file, empty_vulnerabilities)
        
        if not self.report_file.exists():
            self._write_json(self.report_file, empty_report)
    
    def _read_json(self, file_path: Path) -> Dict[str, Any]:
        """Read JSON file safely."""
        try:
            if file_path.exists():
                return json.loads(file_path.read_text(encoding='utf-8'))
            else:
                return {}
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error reading {file_path}: {e}")
            return {}
    
    def _write_json(self, file_path: Path, data: Dict[str, Any]):
        """Write JSON file safely."""
        try:
            # Ensure parent directory exists
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write with proper formatting
            file_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        except IOError as e:
            print(f"Error writing {file_path}: {e}")
            raise
    
    # Infrastructure management
    def save_infrastructure(self, infrastructure: Dict[str, Any]):
        """
        Save infrastructure data to JSON file.
        
        Args:
            infrastructure: Infrastructure data dictionary
        """
        try:
            data = {
                "networks": infrastructure.get("networks", []),
                "systems": infrastructure.get("systems", []),
                "databases": infrastructure.get("databases", []),
                "metadata": {
                    "created_at": datetime.utcnow().isoformat(),
                    "updated_at": datetime.utcnow().isoformat(),
                    "version": "1.0.0",
                    "network_count": len(infrastructure.get("networks", [])),
                    "system_count": len(infrastructure.get("systems", [])),
                    "database_count": len(infrastructure.get("databases", []))
                }
            }
            
            self._write_json(self.infrastructure_file, data)
            
        except Exception as e:
            raise RuntimeError(f"Failed to save infrastructure: {e}")
    
    def get_infrastructure(self) -> Optional[Dict[str, Any]]:
        """
        Get infrastructure data from JSON file.
        
        Returns:
            Infrastructure data dictionary or None if not found
        """
        try:
            data = self._read_json(self.infrastructure_file)
            
            if not data:
                return None
            
            return {
                "networks": data.get("networks", []),
                "systems": data.get("systems", []),
                "databases": data.get("databases", [])
            }
            
        except Exception as e:
            raise RuntimeError(f"Failed to get infrastructure: {e}")
    
    def infrastructure_loaded(self) -> bool:
        """Check if infrastructure data is loaded."""
        data = self._read_json(self.infrastructure_file)
        return bool(data.get("networks") or data.get("systems") or data.get("databases"))
    
    # Attack results management
    def save_attack_result(self, attack_result: Dict[str, Any]):
        """
        Save a single attack result to JSON file.
        
        Args:
            attack_result: Attack result dictionary
        """
        try:
            data = self._read_json(self.attack_results_file)
            
            # Add attack to list
            attacks = data.get("attacks", [])
            attacks.append(attack_result)
            
            # Update metadata
            successful_attacks = len([a for a in attacks if a.get("success", False)])
            failed_attacks = len(attacks) - successful_attacks
            
            data.update({
                "attacks": attacks,
                "metadata": {
                    "created_at": data.get("metadata", {}).get("created_at", datetime.utcnow().isoformat()),
                    "updated_at": datetime.utcnow().isoformat(),
                    "total_attacks": len(attacks),
                    "successful_attacks": successful_attacks,
                    "failed_attacks": failed_attacks,
                    "last_attack": attack_result.get("timestamp")
                }
            })
            
            self._write_json(self.attack_results_file, data)
            
        except Exception as e:
            raise RuntimeError(f"Failed to save attack result: {e}")
    
    def save_attack_results(self, attack_results: List[Dict[str, Any]]):
        """
        Save multiple attack results to JSON file.
        
        Args:
            attack_results: List of attack result dictionaries
        """
        try:
            data = self._read_json(self.attack_results_file)
            
            # Add attacks to list
            attacks = data.get("attacks", [])
            attacks.extend(attack_results)
            
            # Update metadata
            successful_attacks = len([a for a in attacks if a.get("success", False)])
            failed_attacks = len(attacks) - successful_attacks
            
            data.update({
                "attacks": attacks,
                "metadata": {
                    "created_at": data.get("metadata", {}).get("created_at", datetime.utcnow().isoformat()),
                    "updated_at": datetime.utcnow().isoformat(),
                    "total_attacks": len(attacks),
                    "successful_attacks": successful_attacks,
                    "failed_attacks": failed_attacks
                }
            })
            
            self._write_json(self.attack_results_file, data)
            
        except Exception as e:
            raise RuntimeError(f"Failed to save attack results: {e}")
    
    def get_attack_results(self) -> List[Dict[str, Any]]:
        """
        Get all attack results from JSON file.
        
        Returns:
            List of attack result dictionaries
        """
        try:
            data = self._read_json(self.attack_results_file)
            return data.get("attacks", [])
        except Exception as e:
            raise RuntimeError(f"Failed to get attack results: {e}")
    
    def attack_results_available(self) -> bool:
        """Check if attack results are available."""
        data = self._read_json(self.attack_results_file)
        return len(data.get("attacks", [])) > 0
    
    def clear_attack_results(self):
        """Clear all attack results."""
        try:
            empty_data = {
                "attacks": [],
                "metadata": {
                    "created_at": datetime.utcnow().isoformat(),
                    "total_attacks": 0,
                    "successful_attacks": 0,
                    "failed_attacks": 0
                }
            }
            self._write_json(self.attack_results_file, empty_data)
        except Exception as e:
            raise RuntimeError(f"Failed to clear attack results: {e}")
    
    # Vulnerability management
    def save_vulnerabilities(self, vulnerabilities: List[Dict[str, Any]]):
        """
        Save vulnerabilities to JSON file.
        
        Args:
            vulnerabilities: List of vulnerability dictionaries
        """
        try:
            # Calculate severity breakdown
            severity_breakdown = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
            for vuln in vulnerabilities:
                severity = vuln.get("severity", "info")
                severity_breakdown[severity] = severity_breakdown.get(severity, 0) + 1
            
            data = {
                "vulnerabilities": vulnerabilities,
                "metadata": {
                    "created_at": datetime.utcnow().isoformat(),
                    "updated_at": datetime.utcnow().isoformat(),
                    "total_vulnerabilities": len(vulnerabilities),
                    "severity_breakdown": severity_breakdown
                }
            }
            
            self._write_json(self.vulnerabilities_file, data)
            
        except Exception as e:
            raise RuntimeError(f"Failed to save vulnerabilities: {e}")
    
    def get_vulnerabilities(self) -> List[Dict[str, Any]]:
        """
        Get all vulnerabilities from JSON file.
        
        Returns:
            List of vulnerability dictionaries
        """
        try:
            data = self._read_json(self.vulnerabilities_file)
            return data.get("vulnerabilities", [])
        except Exception as e:
            raise RuntimeError(f"Failed to get vulnerabilities: {e}")
    
    def vulnerabilities_available(self) -> bool:
        """Check if vulnerabilities are available."""
        data = self._read_json(self.vulnerabilities_file)
        return len(data.get("vulnerabilities", [])) > 0
    
    def clear_vulnerabilities(self):
        """Clear all vulnerabilities."""
        try:
            empty_data = {
                "vulnerabilities": [],
                "metadata": {
                    "created_at": datetime.utcnow().isoformat(),
                    "total_vulnerabilities": 0,
                    "severity_breakdown": {
                        "critical": 0,
                        "high": 0,
                        "medium": 0,
                        "low": 0,
                        "info": 0
                    }
                }
            }
            self._write_json(self.vulnerabilities_file, empty_data)
        except Exception as e:
            raise RuntimeError(f"Failed to clear vulnerabilities: {e}")
    
    # Report management
    def save_report(self, report: Dict[str, Any]):
        """
        Save report to JSON file.
        
        Args:
            report: Report data dictionary
        """
        try:
            data = {
                "metadata": report.get("metadata", {}),
                "content": report,
                "saved_at": datetime.utcnow().isoformat()
            }
            
            self._write_json(self.report_file, data)
            
            # Also save as markdown if report content is available
            if report:
                self._save_report_as_markdown(report)
            
        except Exception as e:
            raise RuntimeError(f"Failed to save report: {e}")
    
    def get_report(self) -> Optional[Dict[str, Any]]:
        """
        Get report from JSON file.
        
        Returns:
            Report data dictionary or None if not found
        """
        try:
            data = self._read_json(self.report_file)
            return data.get("content")
        except Exception as e:
            raise RuntimeError(f"Failed to get report: {e}")
    
    def get_report_content(self) -> Optional[Dict[str, Any]]:
        """
        Get report content for API responses.
        
        Returns:
            Report content dictionary or None if not found
        """
        try:
            report = self.get_report()
            if not report:
                return None
            
            return {
                "metadata": report.get("metadata", {}),
                "executive_summary": report.get("executive_summary", ""),
                "attack_timeline": report.get("attack_timeline", ""),
                "technical_findings": report.get("technical_findings", []),
                "vulnerability_analysis": report.get("vulnerability_analysis", ""),
                "mitigation_checklist": report.get("mitigation_checklist", []),
                "recommendations": report.get("recommendations", "")
            }
        except Exception as e:
            raise RuntimeError(f"Failed to get report content: {e}")
    
    def report_generated(self) -> bool:
        """Check if report is generated."""
        data = self._read_json(self.report_file)
        return data.get("content") is not None
    
    def clear_report(self):
        """Clear report."""
        try:
            empty_data = {
                "metadata": {
                    "generated_at": None,
                    "session_id": None,
                    "total_vulnerabilities": 0
                },
                "content": None,
                "saved_at": datetime.utcnow().isoformat()
            }
            self._write_json(self.report_file, empty_data)
            
            # Also remove markdown file if it exists
            if self.report_md_file.exists():
                self.report_md_file.unlink()
                
        except Exception as e:
            raise RuntimeError(f"Failed to clear report: {e}")
    
    def _save_report_as_markdown(self, report: Dict[str, Any]):
        """Save report as markdown file."""
        try:
            markdown_content = self._generate_markdown_report(report)
            self.report_md_file.write_text(markdown_content, encoding='utf-8')
        except Exception as e:
            print(f"Warning: Failed to save markdown report: {e}")
    
    def _generate_markdown_report(self, report: Dict[str, Any]) -> str:
        """Generate markdown format report."""
        metadata = report.get("metadata", {})
        
        markdown = f"""# Security Assessment Report

**Generated:** {metadata.get('generated_at', 'Unknown')}  
**Session ID:** {metadata.get('session_id', 'Unknown')}  
**Total Vulnerabilities:** {metadata.get('total_vulnerabilities', 0)}

---

## Executive Summary

{report.get('executive_summary', 'No executive summary available.')}

---

## Attack Timeline

{report.get('attack_timeline', 'No attack timeline available.')}

---

## Technical Findings

"""
        
        findings = report.get('technical_findings', [])
        for finding in findings:
            markdown += f"### {finding.get('title', 'Untitled')}\n\n"
            markdown += f"{finding.get('content', 'No content available.')}\n\n"
        
        markdown += f"""---

## Vulnerability Analysis

{report.get('vulnerability_analysis', 'No vulnerability analysis available.')}

---

## Mitigation Checklist

"""
        
        mitigations = report.get('mitigation_checklist', [])
        for i, mitigation in enumerate(mitigations, 1):
            markdown += f"### {i}. {mitigation.get('title', 'Untitled')}\n\n"
            markdown += f"**Priority:** {mitigation.get('priority', 'Unknown')}\n\n"
            markdown += f"**Effort:** {mitigation.get('effort', 'Unknown')}\n\n"
            markdown += f"**Impact:** {mitigation.get('impact', 'Unknown')}\n\n"
            markdown += f"**Description:** {mitigation.get('description', 'No description available.')}\n\n"
            
            steps = mitigation.get('steps', [])
            if steps:
                markdown += "**Steps:**\n"
                for step in steps:
                    markdown += f"- {step}\n"
                markdown += "\n"
        
        markdown += f"""---

## Recommendations

{report.get('recommendations', 'No recommendations available.')}

---

*This report was generated by the AI Automated Red Team Agent (AARTA).*
"""
        
        return markdown
    
    # General state management
    def reset_all_data(self):
        """Reset all application data."""
        try:
            self.clear_attack_results()
            self.clear_vulnerabilities()
            self.clear_report()
            
            # Reset infrastructure to empty state
            empty_infrastructure = {
                "networks": [],
                "systems": [],
                "databases": [],
                "metadata": {
                    "created_at": datetime.utcnow().isoformat(),
                    "updated_at": datetime.utcnow().isoformat(),
                    "version": "1.0.0",
                    "network_count": 0,
                    "system_count": 0,
                    "database_count": 0
                }
            }
            self._write_json(self.infrastructure_file, empty_infrastructure)
            
        except Exception as e:
            raise RuntimeError(f"Failed to reset all data: {e}")
    
    def get_state_summary(self) -> Dict[str, Any]:
        """
        Get a summary of all current state.
        
        Returns:
            Dictionary containing state summary
        """
        try:
            infra_data = self._read_json(self.infrastructure_file)
            attack_data = self._read_json(self.attack_results_file)
            vuln_data = self._read_json(self.vulnerabilities_file)
            report_data = self._read_json(self.report_file)
            
            return {
                "infrastructure": {
                    "loaded": self.infrastructure_loaded(),
                    "network_count": len(infra_data.get("networks", [])),
                    "system_count": len(infra_data.get("systems", [])),
                    "database_count": len(infra_data.get("databases", [])),
                    "last_updated": infra_data.get("metadata", {}).get("updated_at")
                },
                "attacks": {
                    "available": self.attack_results_available(),
                    "total_attacks": attack_data.get("metadata", {}).get("total_attacks", 0),
                    "successful_attacks": attack_data.get("metadata", {}).get("successful_attacks", 0),
                    "failed_attacks": attack_data.get("metadata", {}).get("failed_attacks", 0),
                    "last_updated": attack_data.get("metadata", {}).get("updated_at")
                },
                "vulnerabilities": {
                    "available": self.vulnerabilities_available(),
                    "total_vulnerabilities": vuln_data.get("metadata", {}).get("total_vulnerabilities", 0),
                    "severity_breakdown": vuln_data.get("metadata", {}).get("severity_breakdown", {}),
                    "last_updated": vuln_data.get("metadata", {}).get("updated_at")
                },
                "report": {
                    "generated": self.report_generated(),
                    "generated_at": report_data.get("metadata", {}).get("generated_at"),
                    "session_id": report_data.get("metadata", {}).get("session_id"),
                    "saved_at": report_data.get("saved_at")
                }
            }
            
        except Exception as e:
            raise RuntimeError(f"Failed to get state summary: {e}")
    
    def export_all_data(self) -> Dict[str, Any]:
        """
        Export all application data.
        
        Returns:
            Dictionary containing all application data
        """
        try:
            return {
                "infrastructure": self.get_infrastructure(),
                "attack_results": self.get_attack_results(),
                "vulnerabilities": self.get_vulnerabilities(),
                "report": self.get_report(),
                "state_summary": self.get_state_summary(),
                "export_timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            raise RuntimeError(f"Failed to export all data: {e}")
    
    def import_data(self, data: Dict[str, Any]):
        """
        Import application data from dictionary.
        
        Args:
            data: Dictionary containing application data
        """
        try:
            if "infrastructure" in data:
                self.save_infrastructure(data["infrastructure"])
            
            if "attack_results" in data:
                self.save_attack_results(data["attack_results"])
            
            if "vulnerabilities" in data:
                self.save_vulnerabilities(data["vulnerabilities"])
            
            if "report" in data:
                self.save_report(data["report"])
                
        except Exception as e:
            raise RuntimeError(f"Failed to import data: {e}")