"""
Orchestrator - Central execution controller for AARTA.
Coordinates all components and manages the overall workflow.
"""

from typing import Dict, List, Any, Optional
import uuid
from datetime import datetime

from app.core.telemetry import Telemetry
from app.core.state_manager import StateManager
from app.simulation.network import NetworkSimulation
from app.simulation.systems import linux_server, web_server, api_server
from app.simulation.databases import sql_database, nosql_database
from app.analysis.vulnerability_analyzer import VulnerabilityAnalyzer
from app.analysis.mitigation_engine import MitigationEngine
from app.analysis.report_generator import ReportGenerator


class Orchestrator:
    """
    Central orchestrator that coordinates all AARTA components.
    Manages the execution flow from simulation to reporting.
    """
    
    def __init__(self, telemetry: Telemetry, state_manager: StateManager):
        self.telemetry = telemetry
        self.state_manager = state_manager
        self.session_id = uuid.uuid4().hex[:8]
        
        # Initialize component references
        self._strategy_engine = None
        self._attack_library = None
        self._attack_executor = None
        self._vulnerability_analyzer = VulnerabilityAnalyzer()
        self._mitigation_engine = MitigationEngine()
        self._report_generator = ReportGenerator()
        
        self.telemetry.log_system_event("Orchestrator Initialized", f"Session ID: {self.session_id}")
    
    def run_infrastructure_simulation(self, include_rogue_ap: bool = True, 
                                    include_vulnerabilities: bool = True,
                                    network_count: int = 4,
                                    system_count: int = 3,
                                    database_count: int = 2) -> Dict[str, Any]:
        """
        Run complete infrastructure simulation.
        
        Args:
            include_rogue_ap: Whether to include rogue access points
            include_vulnerabilities: Whether to include vulnerabilities
            network_count: Number of networks to simulate
            system_count: Number of systems to simulate
            database_count: Number of databases to simulate
            
        Returns:
            Dictionary containing simulation results
        """
        try:
            self.telemetry.log_system_event("Infrastructure Simulation", "Starting infrastructure simulation")
            
            # Simulate networks
            network_sim = NetworkSimulation()
            network_sim.add_open_network("Guest_WiFi")
            network_sim.add_wpa2_network("Office_WiFi", misconfigured=include_vulnerabilities)
            network_sim.add_wpa3_network("Secure_WiFi")
            if include_rogue_ap:
                network_sim.add_rogue_ap("EvilTwin", "Office_WiFi")
            
            # Simulate systems
            systems = []
            server1 = linux_server("auth-server")
            if include_vulnerabilities:
                server1.enable_weak_credentials()
            systems.append(server1.to_dict())
            
            server2 = web_server("web-prod")
            if include_vulnerabilities:
                server2.enable_weak_ssl()
                server2.enable_directory_listing()
            systems.append(server2.to_dict())
            
            server3 = api_server("api-prod")
            if include_vulnerabilities:
                server3.enable_no_authentication()
                server3.enable_rate_limiting_disabled()
            systems.append(server3.to_dict())
            
            # Simulate databases
            databases = []
            db1 = sql_database("users_db")
            if include_vulnerabilities:
                db1.enable_sql_injection()
                db1.enable_weak_credentials()
            databases.append(db1.to_dict())
            
            db2 = nosql_database("logs_db")
            if include_vulnerabilities:
                db2.enable_no_auth()
                db2.enable_excessive_privileges()
            databases.append(db2.to_dict())
            
            # Build infrastructure data
            infrastructure = {
                "networks": network_sim.export(),
                "systems": systems,
                "databases": databases
            }
            
            # Save to state manager
            self.state_manager.save_infrastructure(infrastructure)
            
            result = {
                "infrastructure": infrastructure,
                "networks_generated": len(infrastructure["networks"]),
                "systems_generated": len(infrastructure["systems"]),
                "databases_generated": len(infrastructure["databases"])
            }
            
            self.telemetry.log_system_event("Infrastructure Simulation", f"Completed: {result['networks_generated']} networks, {result['systems_generated']} systems, {result['databases_generated']} databases")
            
            return result
            
        except Exception as e:
            self.telemetry.log_system_event("Infrastructure Simulation Error", str(e), "error")
            raise
    
    def execute_attack(self, attack_type: str, target: str, 
                      parameters: Dict[str, Any] = None,
                      simulate_reasoning: bool = True) -> Dict[str, Any]:
        """
        Execute a single attack against a target.
        
        Args:
            attack_type: Type of attack to execute
            target: Target identifier
            parameters: Attack parameters
            simulate_reasoning: Whether to simulate attack reasoning
            
        Returns:
            Dictionary containing attack results
        """
        try:
            self.telemetry.log_attack_execution(attack_type, target, False)
            
            # Simulate attack execution
            attack_id = f"attack_{uuid.uuid4().hex[:8]}"
            start_time = datetime.utcnow()
            
            # Simulate attack logic based on type
            success = self._simulate_attack_success(attack_type, target)
            reasoning = self._generate_attack_reasoning(attack_type, target, success)
            evidence = self._generate_attack_evidence(attack_type, target, success)
            
            duration = int((datetime.utcnow() - start_time).total_seconds() * 1000)
            
            attack_result = {
                "attack_id": attack_id,
                "attack_type": attack_type,
                "target": target,
                "timestamp": start_time.isoformat(),
                "success": success,
                "reasoning": reasoning,
                "evidence": evidence,
                "duration_ms": duration,
                "details": parameters or {}
            }
            
            # Save attack result
            self.state_manager.save_attack_result(attack_result)
            
            self.telemetry.log_attack_execution(attack_type, target, success)
            
            return {
                "attack_results": [attack_result],
                "attacks_executed": 1,
                "successful_attacks": 1 if success else 0,
                "failed_attacks": 0 if success else 1
            }
            
        except Exception as e:
            self.telemetry.log_system_event("Attack Execution Error", str(e), "error")
            raise
    
    def run_full_attack_simulation(self, target_networks: List[str] = None,
                                target_systems: List[str] = None,
                                target_databases: List[str] = None,
                                attack_phases: List[str] = None,
                                max_attacks_per_phase: int = 10) -> Dict[str, Any]:
        """
        Run comprehensive attack simulation across all targets.
        
        Args:
            target_networks: Specific network targets
            target_systems: Specific system targets
            target_databases: Specific database targets
            attack_phases: Attack phases to execute
            max_attacks_per_phase: Maximum attacks per phase
            
        Returns:
            Dictionary containing all attack results
        """
        try:
            self.telemetry.log_system_event("Full Attack Simulation", "Starting comprehensive attack simulation")
            
            # Get infrastructure
            infrastructure = self.state_manager.get_infrastructure()
            if not infrastructure:
                raise ValueError("No infrastructure data available")
            
            attack_results = []
            attacks_executed = 0
            successful_attacks = 0
            failed_attacks = 0
            
            # Default phases
            if not attack_phases:
                attack_phases = ["reconnaissance", "exploitation", "post_exploitation"]
            
            # Attack types by phase
            attack_types = {
                "reconnaissance": ["port_scan", "service_discovery"],
                "exploitation": ["brute_force", "sql_injection", "authentication_bypass"],
                "post_exploitation": ["privilege_escalation", "lateral_movement", "data_access"]
            }
            
            for phase in attack_phases:
                if phase not in attack_types:
                    continue
                
                self.telemetry.log_system_event("Attack Phase", f"Starting {phase} phase")
                
                for attack_type in attack_types[phase]:
                    # Get targets for this attack type
                    targets = self._get_targets_for_attack_type(attack_type, infrastructure)
                    
                    for target in targets[:max_attacks_per_phase]:
                        result = self.execute_attack(attack_type, target)
                        attack_results.extend(result["attack_results"])
                        attacks_executed += result["attacks_executed"]
                        successful_attacks += result["successful_attacks"]
                        failed_attacks += result["failed_attacks"]
            
            result = {
                "attack_results": attack_results,
                "attacks_executed": attacks_executed,
                "successful_attacks": successful_attacks,
                "failed_attacks": failed_attacks
            }
            
            self.telemetry.log_system_event("Full Attack Simulation", f"Completed: {attacks_executed} attacks executed")
            
            return result
            
        except Exception as e:
            self.telemetry.log_system_event("Full Attack Simulation Error", str(e), "error")
            raise
    
    def analyze_vulnerabilities(self, include_cwe_mapping: bool = True,
                              include_owasp_mapping: bool = True,
                              generate_mitigations: bool = True) -> Dict[str, Any]:
        """
        Analyze attack results to identify vulnerabilities.
        
        Args:
            include_cwe_mapping: Whether to include CWE mapping
            include_owasp_mapping: Whether to include OWASP mapping
            generate_mitigations: Whether to generate mitigations
            
        Returns:
            Dictionary containing vulnerability analysis
        """
        try:
            self.telemetry.log_system_event("Vulnerability Analysis", "Starting vulnerability analysis")
            
            # Get attack results
            attack_results = self.state_manager.get_attack_results()
            if not attack_results:
                return {
                    "vulnerabilities": [],
                    "total_vulnerabilities": 0,
                    "severity_breakdown": {},
                    "cwe_mapping": {},
                    "owasp_mapping": {}
                }
            
            # Use the VulnerabilityAnalyzer to analyze attacks
            vulnerabilities = self._vulnerability_analyzer.analyze_attack_results(attack_results)
            
            # Generate mitigations if requested
            mitigations = []
            if generate_mitigations:
                mitigations = self._mitigation_engine.generate_mitigations(vulnerabilities)
            
            # Get severity breakdown
            severity_breakdown = self._vulnerability_analyzer.get_severity_breakdown(vulnerabilities)
            
            # Save vulnerabilities
            self.state_manager.save_vulnerabilities(vulnerabilities)
            
            result = {
                "vulnerabilities": vulnerabilities,
                "total_vulnerabilities": len(vulnerabilities),
                "severity_breakdown": severity_breakdown,
                "cwe_mapping": {},
                "owasp_mapping": {},
                "mitigations": mitigations
            }
            
            self.telemetry.log_system_event("Vulnerability Analysis", f"Completed: {len(vulnerabilities)} vulnerabilities found")
            
            return result
            
        except Exception as e:
            self.telemetry.log_system_event("Vulnerability Analysis Error", str(e), "error")
            raise
    
    def generate_report(self, format: str = "markdown",
                      include_executive_summary: bool = True,
                      include_technical_details: bool = True,
                      include_mitigations: bool = True,
                      severity_threshold: str = "low") -> Dict[str, Any]:
        """
        Generate security report.
        
        Args:
            format: Report format (markdown, html, pdf)
            include_executive_summary: Whether to include executive summary
            include_technical_details: Whether to include technical details
            include_mitigations: Whether to include mitigations
            severity_threshold: Minimum severity to include
            
        Returns:
            Dictionary containing report data
        """
        try:
            self.telemetry.log_system_event("Report Generation", "Starting security report generation")
            
            # Get data
            infrastructure = self.state_manager.get_infrastructure()
            attack_results = self.state_manager.get_attack_results()
            vulnerabilities = self.state_manager.get_vulnerabilities()
            
            # Generate mitigations if needed
            mitigations = []
            if include_mitigations:
                mitigations = self._mitigation_engine.generate_mitigations(vulnerabilities)
            
            # Use ReportGenerator to create report
            report = self._report_generator.generate_report(
                infrastructure_data=infrastructure,
                attack_results=attack_results,
                vulnerabilities=vulnerabilities,
                mitigations=mitigations,
                session_id=self.session_id
            )
            
            # Save report
            self.state_manager.save_report(report)
            
            result = {
                "report": report,
                "format": format
            }
            
            self.telemetry.log_system_event("Report Generation", f"Completed: {format} format")
            
            return result
            
        except Exception as e:
            self.telemetry.log_system_event("Report Generation Error", str(e), "error")
            raise
    
    def execute_workflow(self, workflow_type: str, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Execute a complete workflow.
        
        Args:
            workflow_type: Type of workflow to execute
            parameters: Workflow parameters
            
        Returns:
            Dictionary containing workflow results
        """
        try:
            workflow_id = f"workflow_{uuid.uuid4().hex[:8]}"
            start_time = datetime.utcnow()
            
            self.telemetry.log_system_event("Workflow Execution", f"Starting {workflow_type} workflow")
            
            steps = []
            result = None
            
            if workflow_type == "full_simulation":
                # Step 1: Infrastructure simulation
                step1_start = datetime.utcnow()
                infra_result = self.run_infrastructure_simulation(
                    include_rogue_ap=parameters.get("include_rogue_ap", True),
                    include_vulnerabilities=parameters.get("include_vulnerabilities", True)
                )
                steps.append({
                    "step_id": "infrastructure_simulation",
                    "name": "Infrastructure Simulation",
                    "description": "Simulate network, systems, and databases",
                    "status": "completed",
                    "started_at": step1_start.isoformat(),
                    "completed_at": datetime.utcnow().isoformat(),
                    "result": infra_result
                })
                
                # Step 2: Attack simulation
                step2_start = datetime.utcnow()
                attack_result = self.run_full_attack_simulation(
                    max_attacks_per_phase=parameters.get("max_attacks_per_phase", 10)
                )
                steps.append({
                    "step_id": "attack_simulation",
                    "name": "Attack Simulation",
                    "description": "Execute simulated attacks",
                    "status": "completed",
                    "started_at": step2_start.isoformat(),
                    "completed_at": datetime.utcnow().isoformat(),
                    "result": attack_result
                })
                
                # Step 3: Vulnerability analysis
                step3_start = datetime.utcnow()
                analysis_result = self.analyze_vulnerabilities()
                steps.append({
                    "step_id": "vulnerability_analysis",
                    "name": "Vulnerability Analysis",
                    "description": "Analyze attack results for vulnerabilities",
                    "status": "completed",
                    "started_at": step3_start.isoformat(),
                    "completed_at": datetime.utcnow().isoformat(),
                    "result": analysis_result
                })
                
                # Step 4: Report generation
                step4_start = datetime.utcnow()
                report_result = self.generate_report(
                    format=parameters.get("report_format", "markdown")
                )
                steps.append({
                    "step_id": "report_generation",
                    "name": "Report Generation",
                    "description": "Generate security report",
                    "status": "completed",
                    "started_at": step4_start.isoformat(),
                    "completed_at": datetime.utcnow().isoformat(),
                    "result": report_result
                })
                
                result = {
                    "infrastructure": infra_result,
                    "attacks": attack_result,
                    "analysis": analysis_result,
                    "report": report_result
                }
            
            workflow = {
                "workflow_id": workflow_id,
                "name": f"{workflow_type.replace('_', ' ').title()} Workflow",
                "status": "completed",
                "started_at": start_time.isoformat(),
                "completed_at": datetime.utcnow().isoformat(),
                "steps": steps,
                "result": result
            }
            
            self.telemetry.log_system_event("Workflow Execution", f"Completed {workflow_type} workflow")
            
            return {
                "workflow": workflow,
                "execution_id": workflow_id
            }
            
        except Exception as e:
            self.telemetry.log_system_event("Workflow Execution Error", str(e), "error")
            raise
    
    # Helper methods
    def _simulate_attack_success(self, attack_type: str, target: str) -> bool:
        """Simulate attack success based on type and target."""
        # Simple simulation logic - in real implementation this would be more sophisticated
        success_rates = {
            "port_scan": 0.95,
            "service_discovery": 0.90,
            "brute_force": 0.40,
            "sql_injection": 0.60,
            "authentication_bypass": 0.30,
            "privilege_escalation": 0.35,
            "lateral_movement": 0.45,
            "data_access": 0.70
        }
        
        import random
        return random.random() < success_rates.get(attack_type, 0.5)
    
    def _generate_attack_reasoning(self, attack_type: str, target: str, success: bool) -> str:
        """Generate attack reasoning."""
        if success:
            return f"Successfully executed {attack_type} against {target}. The attack leveraged known vulnerabilities and misconfigurations in the target system."
        else:
            return f"Failed to execute {attack_type} against {target}. The target had appropriate security controls in place to prevent this attack vector."
    
    def _generate_attack_evidence(self, attack_type: str, target: str, success: bool) -> List[str]:
        """Generate attack evidence."""
        if success:
            return [
                f"Port {self._get_default_port(attack_type)} found open on {target}",
                f"Service vulnerable to {attack_type} detected",
                f"Successfully bypassed authentication on {target}",
                f"Gained unauthorized access to {target}"
            ]
        else:
            return [
                f"Port {self._get_default_port(attack_type)} filtered on {target}",
                f"Service patched against {attack_type}",
                f"Authentication controls blocked access attempt",
                f"No vulnerabilities found for {attack_type} on {target}"
            ]
    
    def _get_default_port(self, attack_type: str) -> int:
        """Get default port for attack type."""
        port_map = {
            "port_scan": 80,
            "service_discovery": 22,
            "brute_force": 22,
            "sql_injection": 3306,
            "authentication_bypass": 80,
            "privilege_escalation": 22,
            "lateral_movement": 445,
            "data_access": 5432
        }
        return port_map.get(attack_type, 80)
    
    def _get_targets_for_attack_type(self, attack_type: str, infrastructure: Dict[str, Any]) -> List[str]:
        """Get appropriate targets for attack type."""
        targets = []
        
        if attack_type in ["port_scan", "service_discovery"]:
            # All systems are targets
            for system in infrastructure.get("systems", []):
                targets.append(system["hostname"])
        
        elif attack_type in ["brute_force", "authentication_bypass", "privilege_escalation"]:
            # Systems with SSH/HTTP services
            for system in infrastructure.get("systems", []):
                if any(port in system["network"]["open_ports"] for port in [22, 80, 443]):
                    targets.append(system["hostname"])
        
        elif attack_type == "sql_injection":
            # Database systems
            for database in infrastructure.get("databases", []):
                targets.append(database["name"])
        
        elif attack_type in ["lateral_movement", "data_access"]:
            # All systems and databases
            for system in infrastructure.get("systems", []):
                targets.append(system["hostname"])
            for database in infrastructure.get("databases", []):
                targets.append(database["name"])
        
        return targets
    
    def _create_vulnerability_from_attack(self, attack: Dict[str, Any]) -> Dict[str, Any]:
        """Create vulnerability from successful attack."""
        vulnerability_map = {
            "brute_force": {
                "name": "Weak Authentication",
                "severity": "high",
                "cwe_id": "CWE-521",
                "owasp_category": "A02:2021 - Cryptographic Failures"
            },
            "sql_injection": {
                "name": "SQL Injection",
                "severity": "critical",
                "cwe_id": "CWE-89",
                "owasp_category": "A03:2021 - Injection"
            },
            "authentication_bypass": {
                "name": "Authentication Bypass",
                "severity": "critical",
                "cwe_id": "CWE-287",
                "owasp_category": "A07:2021 - Identification and Authentication Failures"
            },
            "privilege_escalation": {
                "name": "Privilege Escalation",
                "severity": "high",
                "cwe_id": "CWE-269",
                "owasp_category": "A01:2021 - Broken Access Control"
            }
        }
        
        vuln_info = vulnerability_map.get(attack["attack_type"], {
            "name": f"Security Vulnerability from {attack['attack_type']}",
            "severity": "medium",
            "cwe_id": None,
            "owasp_category": None
        })
        
        return {
            "id": f"vuln_{uuid.uuid4().hex[:8]}",
            "name": vuln_info["name"],
            "severity": vuln_info["severity"],
            "description": f"Vulnerability discovered via {attack['attack_type']} attack on {attack['target']}",
            "target": attack["target"],
            "attack_vector": attack["attack_type"],
            "cwe_id": vuln_info["cwe_id"],
            "owasp_category": vuln_info["owasp_category"],
            "evidence": attack["evidence"],
            "mitigation": f"Implement proper security controls to prevent {attack['attack_type']} attacks"
        }
    
    def _generate_executive_summary(self, vulnerabilities: List[Dict[str, Any]]) -> str:
        """Generate executive summary."""
        if not vulnerabilities:
            return "No security vulnerabilities were discovered during the assessment."
        
        critical_count = len([v for v in vulnerabilities if v["severity"] == "critical"])
        high_count = len([v for v in vulnerabilities if v["severity"] == "high"])
        
        summary = f"The security assessment identified {len(vulnerabilities)} vulnerabilities across the simulated infrastructure."
        if critical_count > 0:
            summary += f" {critical_count} critical vulnerabilities require immediate attention."
        if high_count > 0:
            summary += f" {high_count} high-severity vulnerabilities should be addressed promptly."
        
        return summary
    
    def _generate_attack_timeline(self, attack_results: List[Dict[str, Any]]) -> str:
        """Generate attack timeline."""
        if not attack_results:
            return "No attacks were executed during this assessment."
        
        timeline = "Attack Execution Timeline:\n"
        for attack in sorted(attack_results, key=lambda x: x["timestamp"]):
            status = "✓" if attack["success"] else "✗"
            timeline += f"{status} {attack['timestamp']} - {attack['attack_type']} against {attack['target']}\n"
        
        return timeline
    
    def _generate_technical_findings(self, vulnerabilities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate technical findings sections."""
        if not vulnerabilities:
            return [{"title": "No Findings", "content": "No security vulnerabilities were discovered."}]
        
        findings = []
        for severity in ["critical", "high", "medium", "low"]:
            sev_vulns = [v for v in vulnerabilities if v["severity"] == severity]
            if sev_vulns:
                content = f"Found {len(sev_vulns)} {severity} vulnerabilities:\n"
                for vuln in sev_vulns:
                    content += f"- {vuln['name']} on {vuln['target']}\n"
                    content += f"  {vuln['description']}\n"
                
                findings.append({
                    "title": f"{severity.title()} Severity Vulnerabilities",
                    "content": content
                })
        
        return findings
    
    def _generate_vulnerability_analysis(self, vulnerabilities: List[Dict[str, Any]]) -> str:
        """Generate vulnerability analysis."""
        if not vulnerabilities:
            return "No vulnerabilities to analyze."
        
        analysis = f"Analysis of {len(vulnerabilities)} discovered vulnerabilities:\n\n"
        
        # Severity breakdown
        severity_counts = {}
        for vuln in vulnerabilities:
            severity_counts[vuln["severity"]] = severity_counts.get(vuln["severity"], 0) + 1
        
        analysis += "Severity Breakdown:\n"
        for severity, count in severity_counts.items():
            analysis += f"- {severity.title()}: {count}\n"
        
        # Attack vector analysis
        vector_counts = {}
        for vuln in vulnerabilities:
            vector = vuln["attack_vector"]
            vector_counts[vector] = vector_counts.get(vector, 0) + 1
        
        analysis += "\nAttack Vector Analysis:\n"
        for vector, count in vector_counts.items():
            analysis += f"- {vector}: {count}\n"
        
        return analysis
    
    def _generate_mitigation_checklist(self, vulnerabilities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate mitigation checklist."""
        mitigations = []
        
        # Group by severity
        for severity in ["critical", "high", "medium", "low"]:
            sev_vulns = [v for v in vulnerabilities if v["severity"] == severity]
            if sev_vulns:
                for i, vuln in enumerate(sev_vulns):
                    mitigations.append({
                        "id": f"mit_{uuid.uuid4().hex[:8]}",
                        "type": "immediate" if severity in ["critical", "high"] else "short_term",
                        "title": f"Address {vuln['name']} on {vuln['target']}",
                        "description": vuln["mitigation"],
                        "target_vulnerability": vuln["id"],
                        "priority": 4 - ["critical", "high", "medium", "low"].index(severity),
                        "effort": "Medium",
                        "impact": "High",
                        "steps": [
                            "Review vulnerability details",
                            "Apply security patches",
                            "Configure security controls",
                            "Validate fix effectiveness"
                        ]
                    })
        
        return mitigations
    
    def _generate_recommendations(self, vulnerabilities: List[Dict[str, Any]]) -> str:
        """Generate security recommendations."""
        if not vulnerabilities:
            return "Continue following security best practices."
        
        recommendations = "Security Recommendations:\n\n"
        
        # General recommendations based on findings
        has_auth_issues = any(v["attack_vector"] in ["brute_force", "authentication_bypass"] for v in vulnerabilities)
        has_sql_issues = any(v["attack_vector"] == "sql_injection" for v in vulnerabilities)
        has_privilege_issues = any(v["attack_vector"] == "privilege_escalation" for v in vulnerabilities)
        
        if has_auth_issues:
            recommendations += "1. Implement strong authentication mechanisms including MFA\n"
            recommendations += "2. Enforce complex password policies\n"
            recommendations += "3. Implement account lockout policies\n\n"
        
        if has_sql_issues:
            recommendations += "1. Implement input validation and parameterized queries\n"
            recommendations += "2. Use web application firewalls\n"
            recommendations += "3. Regularly patch database systems\n\n"
        
        if has_privilege_issues:
            recommendations += "1. Implement principle of least privilege\n"
            recommendations += "2. Regularly review user permissions\n"
            recommendations += "3. Monitor for privilege escalation attempts\n\n"
        
        recommendations += "4. Conduct regular security assessments\n"
        recommendations += "5. Implement continuous monitoring\n"
        recommendations += "6. Maintain security awareness training"
        
        return recommendations