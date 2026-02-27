"""
Mitigation Engine - Generates mitigation strategies for identified vulnerabilities.
Provides actionable recommendations for security improvements.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime


class MitigationEngine:
    """
    Generates comprehensive mitigation strategies for vulnerabilities.
    Provides prioritized recommendations with implementation guidance.
    """
    
    def __init__(self):
        self.mitigation_strategies = {
            "sql_injection": {
                "immediate": [
                    "Implement parameterized queries and prepared statements",
                    "Apply input validation and sanitization",
                    "Use stored procedures where possible"
                ],
                "short_term": [
                    "Deploy Web Application Firewall (WAF)",
                    "Implement database access controls",
                    "Conduct code review for injection vulnerabilities"
                ],
                "long_term": [
                    "Adopt secure coding practices",
                    "Implement regular security testing",
                    "Educate development team on secure coding"
                ],
                "priority": "critical"
            },
            "authentication_bypass": {
                "immediate": [
                    "Implement multi-factor authentication",
                    "Review and fix authentication logic",
                    "Update authentication mechanisms"
                ],
                "short_term": [
                    "Implement session management best practices",
                    "Deploy account lockout mechanisms",
                    "Conduct authentication testing"
                ],
                "long_term": [
                    "Adopt zero-trust architecture",
                    "Implement continuous authentication monitoring",
                    "Regular security assessments"
                ],
                "priority": "critical"
            },
            "privilege_escalation": {
                "immediate": [
                    "Review user permissions and access rights",
                    "Implement principle of least privilege",
                    "Audit administrative accounts"
                ],
                "short_term": [
                    "Implement role-based access control (RBAC)",
                    "Deploy privilege access management (PAM)",
                    "Regular permission audits"
                ],
                "long_term": [
                    "Implement zero-trust security model",
                    "Continuous monitoring of privilege usage",
                    "Security awareness training"
                ],
                "priority": "high"
            },
            "data_access": {
                "immediate": [
                    "Implement data encryption at rest and in transit",
                    "Review data access permissions",
                    "Audit data access logs"
                ],
                "short_term": [
                    "Implement data loss prevention (DLP)",
                    "Deploy database activity monitoring",
                    "Regular data access reviews"
                ],
                "long_term": [
                    "Implement data classification policies",
                    "Adopt privacy-by-design principles",
                    "Regular privacy impact assessments"
                ],
                "priority": "high"
            },
            "brute_force": {
                "immediate": [
                    "Implement account lockout policies",
                    "Deploy rate limiting mechanisms",
                    "Strengthen password policies"
                ],
                "short_term": [
                    "Implement multi-factor authentication",
                    "Deploy account monitoring tools",
                    "Conduct password security audit"
                ],
                "long_term": [
                    "Adopt passwordless authentication",
                    "Implement continuous authentication",
                    "Regular security awareness training"
                ],
                "priority": "medium"
            },
            "lateral_movement": {
                "immediate": [
                    "Implement network segmentation",
                    "Review internal network access controls",
                    "Audit inter-system communications"
                ],
                "short_term": [
                    "Deploy network monitoring tools",
                    "Implement micro-segmentation",
                    "Regular network architecture reviews"
                ],
                "long_term": [
                    "Adopt zero-trust network architecture",
                    "Implement software-defined networking",
                    "Continuous network monitoring"
                ],
                "priority": "medium"
            },
            "port_scan": {
                "immediate": [
                    "Close unnecessary open ports",
                    "Implement firewall rules",
                    "Review service configurations"
                ],
                "short_term": [
                    "Deploy port knocking mechanisms",
                    "Implement network segmentation",
                    "Regular port scanning audits"
                ],
                "long_term": [
                    "Adopt minimal service footprint",
                    "Implement service hardening",
                    "Continuous vulnerability scanning"
                ],
                "priority": "low"
            },
            "service_discovery": {
                "immediate": [
                    "Disable unnecessary services",
                    "Implement service hardening",
                    "Review service configurations"
                ],
                "short_term": [
                    "Deploy service monitoring tools",
                    "Implement service discovery controls",
                    "Regular service audits"
                ],
                "long_term": [
                    "Adopt microservices architecture",
                    "Implement service mesh security",
                    "Continuous service monitoring"
                ],
                "priority": "low"
            }
        }
    
    def generate_mitigations(self, vulnerabilities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Generate mitigation strategies for vulnerabilities.
        
        Args:
            vulnerabilities: List of vulnerability objects
            
        Returns:
            List of mitigation strategies
        """
        mitigations = []
        
        for vuln in vulnerabilities:
            attack_vector = vuln.get("attack_vector", "")
            target = vuln.get("target", "")
            severity = vuln.get("severity", "medium")
            
            mitigation = self._create_mitigation_strategy(vuln, attack_vector, target, severity)
            mitigations.append(mitigation)
        
        return self._prioritize_mitigations(mitigations)
    
    def _create_mitigation_strategy(self, vulnerability: Dict[str, Any], 
                                 attack_vector: str, target: str, severity: str) -> Dict[str, Any]:
        """Create mitigation strategy for a specific vulnerability."""
        strategy = self.mitigation_strategies.get(attack_vector, self._get_default_strategy())
        
        return {
            "vulnerability_id": vulnerability.get("id", ""),
            "vulnerability_name": vulnerability.get("name", ""),
            "target": target,
            "attack_vector": attack_vector,
            "severity": severity,
            "priority": strategy["priority"],
            "immediate_actions": strategy["immediate"],
            "short_term_actions": strategy["short_term"],
            "long_term_actions": strategy["long_term"],
            "estimated_effort": self._estimate_effort(severity),
            "business_impact": self._assess_business_impact(severity, attack_vector),
            "compliance_impact": self._assess_compliance_impact(attack_vector),
            "generated_at": datetime.utcnow().isoformat()
        }
    
    def _get_default_strategy(self) -> Dict[str, Any]:
        """Get default mitigation strategy for unknown vulnerabilities."""
        return {
            "immediate": [
                "Assess vulnerability scope and impact",
                "Implement temporary controls",
                "Document vulnerability details"
            ],
            "short_term": [
                "Develop comprehensive fix",
                "Test security patches",
                "Implement monitoring"
            ],
            "long_term": [
                "Security architecture review",
                "Implement security best practices",
                "Regular security assessments"
            ],
            "priority": "medium"
        }
    
    def _estimate_effort(self, severity: str) -> str:
        """Estimate implementation effort based on severity."""
        effort_mapping = {
            "critical": "High (1-2 weeks)",
            "high": "Medium (1-2 weeks)",
            "medium": "Medium (2-4 weeks)",
            "low": "Low (1-2 weeks)"
        }
        return effort_mapping.get(severity, "Medium (2-4 weeks)")
    
    def _assess_business_impact(self, severity: str, attack_vector: str) -> str:
        """Assess business impact of vulnerability."""
        if severity == "critical":
            return "Severe - Potential data breach, system compromise, regulatory violations"
        elif severity == "high":
            return "High - Significant data exposure, service disruption, reputation damage"
        elif severity == "medium":
            return "Moderate - Limited data exposure, partial service impact"
        else:
            return "Low - Minimal impact, information disclosure only"
    
    def _assess_compliance_impact(self, attack_vector: str) -> str:
        """Assess compliance impact of vulnerability."""
        high_impact_vectors = ["sql_injection", "authentication_bypass", "data_access"]
        medium_impact_vectors = ["privilege_escalation", "brute_force"]
        
        if attack_vector in high_impact_vectors:
            return "High - Potential GDPR, HIPAA, PCI-DSS violations"
        elif attack_vector in medium_impact_vectors:
            return "Medium - Potential compliance framework violations"
        else:
            return "Low - Minimal compliance impact"
    
    def _prioritize_mitigations(self, mitigations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Prioritize mitigations based on severity and business impact."""
        priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        
        return sorted(mitigations, key=lambda x: (
            priority_order.get(x.get("severity", "medium"), 2),
            x.get("business_impact", "")
        ))
    
    def get_executive_summary(self, mitigations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate executive summary of mitigation strategies."""
        total_mitigations = len(mitigations)
        critical_count = sum(1 for m in mitigations if m.get("severity") == "critical")
        high_count = sum(1 for m in mitigations if m.get("severity") == "high")
        
        return {
            "total_vulnerabilities": total_mitigations,
            "critical_issues": critical_count,
            "high_priority_issues": high_count,
            "immediate_actions_required": critical_count + high_count,
            "estimated_total_effort": self._calculate_total_effort(mitigations),
            "business_risk_level": self._assess_overall_risk(mitigations),
            "compliance_concerns": sum(1 for m in mitigations if "High" in m.get("compliance_impact", "")),
            "recommendations": self._get_executive_recommendations(mitigations)
        }
    
    def _calculate_total_effort(self, mitigations: List[Dict[str, Any]]) -> str:
        """Calculate total effort for all mitigations."""
        effort_days = 0
        for mitigation in mitigations:
            effort_str = mitigation.get("estimated_effort", "Medium (2-4 weeks)")
            if "1-2 weeks" in effort_str:
                effort_days += 10  # Average 10 days
            elif "2-4 weeks" in effort_str:
                effort_days += 21  # Average 21 days
        
        if effort_days < 30:
            return f"{effort_days} days"
        else:
            return f"{effort_days // 7} weeks"
    
    def _assess_overall_risk(self, mitigations: List[Dict[str, Any]]) -> str:
        """Assess overall business risk."""
        critical_count = sum(1 for m in mitigations if m.get("severity") == "critical")
        high_count = sum(1 for m in mitigations if m.get("severity") == "high")
        
        if critical_count > 0:
            return "Critical - Immediate action required"
        elif high_count > 2:
            return "High - Urgent action recommended"
        elif high_count > 0:
            return "Medium-High - Prompt action needed"
        else:
            return "Low - Routine security improvements"
    
    def _get_executive_recommendations(self, mitigations: List[Dict[str, Any]]) -> List[str]:
        """Get high-level executive recommendations."""
        recommendations = []
        
        critical_count = sum(1 for m in mitigations if m.get("severity") == "critical")
        if critical_count > 0:
            recommendations.append(f"Immediately address {critical_count} critical security vulnerabilities")
        
        high_count = sum(1 for m in mitigations if m.get("severity") == "high")
        if high_count > 0:
            recommendations.append(f"Prioritize {high_count} high-priority security improvements")
        
        compliance_issues = sum(1 for m in mitigations if "High" in m.get("compliance_impact", ""))
        if compliance_issues > 0:
            recommendations.append("Address compliance-related security concerns")
        
        recommendations.extend([
            "Implement regular security assessment program",
            "Invest in security awareness training",
            "Consider security testing automation"
        ])
        
        return recommendations[:5]  # Return top 5 recommendations