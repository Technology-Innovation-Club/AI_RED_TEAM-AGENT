"""
Report Generator - Creates comprehensive security assessment reports.
Generates executive summaries, technical findings, and recommendations.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import json


class ReportGenerator:
    """
    Generates comprehensive security assessment reports.
    Creates executive summaries, technical findings, and actionable recommendations.
    """
    
    def __init__(self):
        self.report_template = {
            "metadata": {
                "generated_at": "",
                "session_id": "",
                "version": "1.0.0",
                "total_vulnerabilities": 0
            },
            "executive_summary": "",
            "attack_timeline": "",
            "technical_findings": [],
            "mitigation_strategies": [],
            "recommendations": "",
            "appendices": {}
        }
    
    def generate_report(self, 
                      infrastructure_data: Dict[str, Any],
                      attack_results: List[Dict[str, Any]],
                      vulnerabilities: List[Dict[str, Any]],
                      mitigations: List[Dict[str, Any]],
                      session_id: str) -> Dict[str, Any]:
        """
        Generate comprehensive security assessment report.
        
        Args:
            infrastructure_data: Infrastructure simulation data
            attack_results: Attack execution results
            vulnerabilities: Identified vulnerabilities
            mitigations: Mitigation strategies
            session_id: Session identifier
            
        Returns:
            Complete security report
        """
        report = self.report_template.copy()
        
        # Update metadata
        report["metadata"]["generated_at"] = datetime.utcnow().isoformat()
        report["metadata"]["session_id"] = session_id
        report["metadata"]["total_vulnerabilities"] = len(vulnerabilities)
        
        # Generate report sections
        report["executive_summary"] = self._generate_executive_summary(
            infrastructure_data, attack_results, vulnerabilities, mitigations
        )
        
        report["attack_timeline"] = self._generate_attack_timeline(attack_results)
        
        report["technical_findings"] = self._generate_technical_findings(vulnerabilities)
        
        report["mitigation_strategies"] = mitigations
        
        report["recommendations"] = self._generate_recommendations(vulnerabilities, mitigations)
        
        report["appendices"] = self._generate_appendices(
            infrastructure_data, attack_results, vulnerabilities
        )
        
        return report
    
    def _generate_executive_summary(self, 
                                 infrastructure_data: Dict[str, Any],
                                 attack_results: List[Dict[str, Any]],
                                 vulnerabilities: List[Dict[str, Any]],
                                 mitigations: List[Dict[str, Any]]) -> str:
        """Generate executive summary for management."""
        total_attacks = len(attack_results)
        successful_attacks = len([a for a in attack_results if a.get("success", False)])
        total_vulnerabilities = len(vulnerabilities)
        
        critical_vulns = len([v for v in vulnerabilities if v.get("severity") == "critical"])
        high_vulns = len([v for v in vulnerabilities if v.get("severity") == "high"])
        
        # Calculate risk level
        if critical_vulns > 0:
            risk_level = "CRITICAL"
        elif high_vulns > 2:
            risk_level = "HIGH"
        elif high_vulns > 0:
            risk_level = "MEDIUM-HIGH"
        else:
            risk_level = "MEDIUM"
        
        summary = f"""
# Executive Summary

## Overview
This security assessment was conducted using the AI Automated Red Team Agent (AARTA) to evaluate the security posture of the simulated infrastructure. The assessment identified {total_vulnerabilities} vulnerabilities across {len(infrastructure_data.get('systems', []))} systems and {len(infrastructure_data.get('databases', []))} databases.

## Key Findings
- **Risk Level**: {risk_level}
- **Total Vulnerabilities**: {total_vulnerabilities}
- **Critical Issues**: {critical_vulns}
- **High Priority Issues**: {high_vulns}
- **Attack Success Rate**: {successful_attacks}/{total_attacks} ({(successful_attacks/total_attacks*100):.1f}% if total_attacks > 0 else 0)

## Business Impact
The identified vulnerabilities pose significant risks to:
- Data confidentiality and integrity
- System availability and performance
- Regulatory compliance requirements
- Organizational reputation

## Immediate Actions Required
{critical_vulns + high_vulns} vulnerabilities require immediate attention to prevent potential security incidents.

## Recommendations
1. Immediately address all critical and high-priority vulnerabilities
2. Implement comprehensive security monitoring
3. Establish regular security assessment program
4. Invest in security awareness training
5. Consider security automation and testing tools

## Next Steps
A detailed technical analysis and mitigation plan is provided in the following sections. We recommend prioritizing actions based on the severity and business impact assessments outlined in this report.
        """.strip()
        
        return summary
    
    def _generate_attack_timeline(self, attack_results: List[Dict[str, Any]]) -> str:
        """Generate attack execution timeline."""
        if not attack_results:
            return "No attack simulations were executed."
        
        timeline = "# Attack Execution Timeline\n\n"
        
        # Group attacks by phase
        phases = {
            "Reconnaissance": [],
            "Exploitation": [],
            "Post-Exploitation": []
        }
        
        for attack in attack_results:
            attack_type = attack.get("attack_type", "")
            phase = self._get_attack_phase(attack_type)
            phases[phase].append(attack)
        
        for phase, attacks in phases.items():
            if attacks:
                timeline += f"## {phase} Phase\n\n"
                
                for attack in sorted(attacks, key=lambda x: x.get("timestamp", "")):
                    timestamp = attack.get("timestamp", "")
                    target = attack.get("target", "")
                    success = attack.get("success", False)
                    evidence = attack.get("evidence", [])
                    
                    status = "✅ SUCCESS" if success else "❌ FAILED"
                    timeline += f"- **[{timestamp}]** {status} - {self._format_attack_type(attack_type)} on {target}\n"
                    
                    if evidence and success:
                        timeline += f"  - Evidence: {', '.join(evidence[:3])}\n"
                
                timeline += "\n"
        
        return timeline
    
    def _generate_technical_findings(self, vulnerabilities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate detailed technical findings."""
        findings = []
        
        for vuln in vulnerabilities:
            finding = {
                "title": vuln.get("name", "Unknown Vulnerability"),
                "severity": vuln.get("severity", "medium"),
                "target": vuln.get("target", ""),
                "cwe_id": vuln.get("cwe_id", ""),
                "owasp_category": vuln.get("owasp_category", ""),
                "description": vuln.get("description", ""),
                "attack_vector": vuln.get("attack_vector", ""),
                "evidence": vuln.get("evidence", []),
                "mitigation": vuln.get("mitigation", ""),
                "risk_score": self._calculate_risk_score(vuln)
            }
            findings.append(finding)
        
        return sorted(findings, key=lambda x: self._severity_to_number(x.get("severity", "medium")))
    
    def _generate_recommendations(self, 
                               vulnerabilities: List[Dict[str, Any]],
                               mitigations: List[Dict[str, Any]]) -> str:
        """Generate comprehensive recommendations."""
        recommendations = "# Security Recommendations\n\n"
        
        # Categorize recommendations
        immediate = []
        short_term = []
        long_term = []
        
        for mitigation in mitigations:
            severity = mitigation.get("severity", "medium")
            if severity in ["critical", "high"]:
                immediate.extend(mitigation.get("immediate_actions", []))
                short_term.extend(mitigation.get("short_term_actions", []))
            else:
                short_term.extend(mitigation.get("short_term_actions", []))
                long_term.extend(mitigation.get("long_term_actions", []))
        
        # Remove duplicates and organize
        immediate = list(set(immediate))
        short_term = list(set(short_term))
        long_term = list(set(long_term))
        
        if immediate:
            recommendations += "## Immediate Actions (Critical/High Priority)\n\n"
            for i, action in enumerate(immediate[:5], 1):
                recommendations += f"{i}. {action}\n"
            recommendations += "\n"
        
        if short_term:
            recommendations += "## Short-term Actions (1-3 months)\n\n"
            for i, action in enumerate(short_term[:5], 1):
                recommendations += f"{i}. {action}\n"
            recommendations += "\n"
        
        if long_term:
            recommendations += "## Long-term Actions (3-12 months)\n\n"
            for i, action in enumerate(long_term[:5], 1):
                recommendations += f"{i}. {action}\n"
            recommendations += "\n"
        
        # Add strategic recommendations
        recommendations += """
## Strategic Recommendations

### Security Program Development
1. **Establish Security Governance**: Create formal security policies and procedures
2. **Implement Security Training**: Regular security awareness programs for all staff
3. **Security Testing Program**: Regular penetration testing and vulnerability assessments
4. **Incident Response Plan**: Develop and test incident response procedures

### Technology Investments
1. **Security Monitoring**: Implement comprehensive security monitoring and logging
2. **Access Management**: Deploy identity and access management solutions
3. **Security Automation**: Invest in security testing and monitoring automation
4. **Data Protection**: Implement data loss prevention and encryption solutions

### Compliance and Risk Management
1. **Risk Assessment**: Regular risk assessments and treatment planning
2. **Compliance Monitoring**: Continuous compliance monitoring and reporting
3. **Vendor Management**: Security assessment of third-party vendors and suppliers
4. **Business Continuity**: Regular testing of business continuity and disaster recovery plans
        """.strip()
        
        return recommendations
    
    def _generate_appendices(self, 
                           infrastructure_data: Dict[str, Any],
                           attack_results: List[Dict[str, Any]],
                           vulnerabilities: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate report appendices."""
        appendices = {}
        
        # Infrastructure summary
        appendices["infrastructure_summary"] = {
            "networks": len(infrastructure_data.get("networks", [])),
            "systems": len(infrastructure_data.get("systems", [])),
            "databases": len(infrastructure_data.get("databases", [])),
            "details": infrastructure_data
        }
        
        # Attack statistics
        appendices["attack_statistics"] = {
            "total_attacks": len(attack_results),
            "successful_attacks": len([a for a in attack_results if a.get("success", False)]),
            "failed_attacks": len([a for a in attack_results if not a.get("success", False)]),
            "success_rate": len([a for a in attack_results if a.get("success", False)]) / len(attack_results) * 100 if attack_results else 0,
            "attack_types": self._get_attack_type_breakdown(attack_results)
        }
        
        # Vulnerability statistics
        appendices["vulnerability_statistics"] = {
            "total_vulnerabilities": len(vulnerabilities),
            "severity_breakdown": self._get_severity_breakdown(vulnerabilities),
            "cwe_distribution": self._get_cwe_distribution(vulnerabilities),
            "owasp_distribution": self._get_owasp_distribution(vulnerabilities)
        }
        
        return appendices
    
    def _get_attack_phase(self, attack_type: str) -> str:
        """Get attack phase for attack type."""
        reconnaissance = ["port_scan", "service_discovery"]
        exploitation = ["brute_force", "sql_injection", "authentication_bypass"]
        post_exploitation = ["privilege_escalation", "lateral_movement", "data_access"]
        
        if attack_type in reconnaissance:
            return "Reconnaissance"
        elif attack_type in exploitation:
            return "Exploitation"
        elif attack_type in post_exploitation:
            return "Post-Exploitation"
        else:
            return "Unknown"
    
    def _format_attack_type(self, attack_type: str) -> str:
        """Format attack type for display."""
        return " ".join(word.capitalize() for word in attack_type.split("_"))
    
    def _calculate_risk_score(self, vulnerability: Dict[str, Any]) -> int:
        """Calculate risk score for vulnerability."""
        severity_scores = {"critical": 10, "high": 7, "medium": 4, "low": 1}
        severity = vulnerability.get("severity", "medium")
        return severity_scores.get(severity, 4)
    
    def _severity_to_number(self, severity: str) -> int:
        """Convert severity to numeric value for sorting."""
        severity_numbers = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        return severity_numbers.get(severity, 2)
    
    def _get_attack_type_breakdown(self, attack_results: List[Dict[str, Any]]) -> Dict[str, int]:
        """Get breakdown of attacks by type."""
        breakdown = {}
        for attack in attack_results:
            attack_type = attack.get("attack_type", "unknown")
            breakdown[attack_type] = breakdown.get(attack_type, 0) + 1
        return breakdown
    
    def _get_severity_breakdown(self, vulnerabilities: List[Dict[str, Any]]) -> Dict[str, int]:
        """Get breakdown of vulnerabilities by severity."""
        breakdown = {"critical": 0, "high": 0, "medium": 0, "low": 0}
        for vuln in vulnerabilities:
            severity = vuln.get("severity", "medium")
            if severity in breakdown:
                breakdown[severity] += 1
        return breakdown
    
    def _get_cwe_distribution(self, vulnerabilities: List[Dict[str, Any]]) -> Dict[str, int]:
        """Get distribution of vulnerabilities by CWE."""
        distribution = {}
        for vuln in vulnerabilities:
            cwe = vuln.get("cwe_id", "Unknown")
            distribution[cwe] = distribution.get(cwe, 0) + 1
        return distribution
    
    def _get_owasp_distribution(self, vulnerabilities: List[Dict[str, Any]]) -> Dict[str, int]:
        """Get distribution of vulnerabilities by OWASP category."""
        distribution = {}
        for vuln in vulnerabilities:
            owasp = vuln.get("owasp_category", "Unknown")
            distribution[owasp] = distribution.get(owasp, 0) + 1
        return distribution
    
    def export_to_markdown(self, report: Dict[str, Any]) -> str:
        """Export report to Markdown format."""
        markdown = f"""# Security Assessment Report

**Generated**: {report['metadata']['generated_at']}
**Session ID**: {report['metadata']['session_id']}
**Total Vulnerabilities**: {report['metadata']['total_vulnerabilities']}

---

{report['executive_summary']}

---

{report['attack_timeline']}

---

# Technical Findings

"""
        
        for i, finding in enumerate(report['technical_findings'], 1):
            markdown += f"""
## {i}. {finding['title']}

**Severity**: {finding['severity'].upper()}
**Target**: {finding['target']}
**CWE**: {finding['cwe_id']}
**OWASP**: {finding['owasp_category']}

**Description**: {finding['description']}

**Attack Vector**: {finding['attack_vector']}

**Evidence**: {', '.join(finding['evidence']) if finding['evidence'] else 'None'}

**Mitigation**: {finding['mitigation']}

---

"""
        
        markdown += f"""
{report['recommendations']}

---

# Appendices

## Infrastructure Summary
- Networks: {report['appendices']['infrastructure_summary']['networks']}
- Systems: {report['appendices']['infrastructure_summary']['systems']}
- Databases: {report['appendices']['infrastructure_summary']['databases']}

## Attack Statistics
- Total Attacks: {report['appendices']['attack_statistics']['total_attacks']}
- Successful: {report['appendices']['attack_statistics']['successful_attacks']}
- Failed: {report['appendices']['attack_statistics']['failed_attacks']}
- Success Rate: {report['appendices']['attack_statistics']['success_rate']:.1f}%

## Vulnerability Statistics
- Total Vulnerabilities: {report['appendices']['vulnerability_statistics']['total_vulnerabilities']}
- Severity Breakdown: {report['appendices']['vulnerability_statistics']['severity_breakdown']}

---

*Report generated by AI Automated Red Team Agent (AARTA)*
        """
        
        return markdown