"""
Pydantic schemas for API request/response models.
Defines data structures for the AARTA API.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum


# Base schemas
class BaseResponse(BaseModel):
    """Base response schema."""
    success: bool = True
    message: str = "Operation completed successfully"
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ErrorResponse(BaseResponse):
    """Error response schema."""
    success: bool = False
    error: str
    details: Optional[Dict[str, Any]] = None


# Infrastructure schemas
class NetworkConfig(BaseModel):
    """Network configuration schema."""
    id: str
    type: str
    role: str
    configuration: Dict[str, Any]
    security_flags: Dict[str, Any]
    known_issues: List[str]
    vulnerabilities: List[str]


class SystemConfig(BaseModel):
    """System configuration schema."""
    id: str
    hostname: str
    os: Dict[str, str]
    network: Dict[str, Any]
    security: Dict[str, Any]


class DatabaseConfig(BaseModel):
    """Database configuration schema."""
    id: str
    name: str
    type: str
    version: str
    connection: Dict[str, Any]
    authentication: Dict[str, Any]
    roles: Dict[str, Any]
    tables: List[Dict[str, Any]]
    security: Dict[str, Any]


class InfrastructureData(BaseModel):
    """Complete infrastructure data schema."""
    networks: List[NetworkConfig]
    systems: List[SystemConfig]
    databases: List[DatabaseConfig]


# Simulation schemas
class SimulationRequest(BaseModel):
    """Request to run infrastructure simulation."""
    include_rogue_ap: bool = True
    include_vulnerabilities: bool = True
    network_count: int = Field(default=4, ge=1, le=10)
    system_count: int = Field(default=3, ge=1, le=10)
    database_count: int = Field(default=2, ge=1, le=10)


class SimulationResponse(BaseResponse):
    """Response from infrastructure simulation."""
    infrastructure: InfrastructureData
    networks_generated: int
    systems_generated: int
    databases_generated: int


# Attack schemas
class AttackType(str, Enum):
    """Enumeration of attack types."""
    PORT_SCAN = "port_scan"
    BRUTE_FORCE = "brute_force"
    SQL_INJECTION = "sql_injection"
    AUTHENTICATION_BYPASS = "authentication_bypass"
    PRIVILEGE_ESCALATION = "privilege_escalation"
    LATERAL_MOVEMENT = "lateral_movement"
    DATA_ACCESS = "data_access"


class AttackRequest(BaseModel):
    """Request to execute an attack."""
    attack_type: AttackType
    target: str
    parameters: Optional[Dict[str, Any]] = None
    simulate_reasoning: bool = True


class AttackResult(BaseModel):
    """Single attack result."""
    attack_id: str
    attack_type: str
    target: str
    timestamp: datetime
    success: bool
    reasoning: str
    evidence: List[str]
    duration_ms: int
    details: Dict[str, Any]


class AttackResponse(BaseResponse):
    """Response from attack execution."""
    attack_results: List[AttackResult]
    attacks_executed: int
    successful_attacks: int
    failed_attacks: int


class FullAttackSimulationRequest(BaseModel):
    """Request to run full attack simulation."""
    target_networks: Optional[List[str]] = None
    target_systems: Optional[List[str]] = None
    target_databases: Optional[List[str]] = None
    attack_phases: List[str] = ["reconnaissance", "exploitation", "post_exploitation"]
    max_attacks_per_phase: int = Field(default=10, ge=1, le=50)


# Analysis schemas
class VulnerabilitySeverity(str, Enum):
    """Vulnerability severity levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class Vulnerability(BaseModel):
    """Vulnerability schema."""
    id: str
    name: str
    severity: VulnerabilitySeverity
    description: str
    target: str
    attack_vector: str
    cwe_id: Optional[str] = None
    owasp_category: Optional[str] = None
    evidence: List[str]
    mitigation: str


class AnalysisRequest(BaseModel):
    """Request to analyze attack results."""
    include_cwe_mapping: bool = True
    include_owasp_mapping: bool = True
    generate_mitigations: bool = True


class AnalysisResponse(BaseResponse):
    """Response from vulnerability analysis."""
    vulnerabilities: List[Vulnerability]
    total_vulnerabilities: int
    severity_breakdown: Dict[str, int]
    cwe_mapping: Dict[str, List[str]]
    owasp_mapping: Dict[str, List[str]]


# Mitigation schemas
class MitigationType(str, Enum):
    """Mitigation strategy types."""
    IMMEDIATE = "immediate"
    SHORT_TERM = "short_term"
    LONG_TERM = "long_term"


class Mitigation(BaseModel):
    """Mitigation strategy schema."""
    id: str
    type: MitigationType
    title: str
    description: str
    target_vulnerability: str
    priority: int
    effort: str
    impact: str
    steps: List[str]


class MitigationResponse(BaseResponse):
    """Response from mitigation engine."""
    mitigations: List[Mitigation]
    immediate_actions: List[Mitigation]
    short_term_improvements: List[Mitigation]
    long_term_strategies: List[Mitigation]


# Report schemas
class ReportSection(BaseModel):
    """Report section schema."""
    title: str
    content: str
    subsections: Optional[List["ReportSection"]] = None


class ReportMetadata(BaseModel):
    """Report metadata schema."""
    generated_at: datetime
    session_id: str
    total_vulnerabilities: int
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int


class SecurityReport(BaseModel):
    """Complete security report schema."""
    metadata: ReportMetadata
    executive_summary: str
    attack_timeline: str
    technical_findings: List[ReportSection]
    vulnerability_analysis: str
    mitigation_checklist: List[Mitigation]
    recommendations: str
    appendices: Optional[Dict[str, Any]] = None


class ReportRequest(BaseModel):
    """Request to generate security report."""
    format: str = Field(default="markdown", pattern="^(markdown|html|pdf)$")
    include_executive_summary: bool = True
    include_technical_details: bool = True
    include_mitigations: bool = True
    severity_threshold: VulnerabilitySeverity = VulnerabilitySeverity.LOW


class ReportResponse(BaseResponse):
    """Response from report generator."""
    report: SecurityReport
    format: str
    file_path: Optional[str] = None


# Telemetry schemas
class TelemetryEvent(BaseModel):
    """Telemetry event schema."""
    timestamp: datetime
    session_id: str
    event_type: str
    message: str
    component: str
    severity: str
    source_ip: str
    success: bool
    details: Dict[str, Any]


class TelemetryResponse(BaseResponse):
    """Telemetry data response."""
    events: List[TelemetryEvent]
    total_events: int
    statistics: Dict[str, Any]


class TelemetryFilter(BaseModel):
    """Telemetry filter schema."""
    component: Optional[str] = None
    severity: Optional[str] = None
    event_type: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    limit: int = Field(default=100, ge=1, le=1000)


# System status schemas
class SystemStatus(BaseModel):
    """System status schema."""
    status: str
    session_id: str
    infrastructure_loaded: bool
    attack_results_available: bool
    report_generated: bool
    telemetry_events: int
    components: Dict[str, bool]


# Workflow schemas
class WorkflowStep(BaseModel):
    """Workflow step schema."""
    step_id: str
    name: str
    description: str
    status: str
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None


class WorkflowExecution(BaseModel):
    """Workflow execution schema."""
    workflow_id: str
    name: str
    status: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    steps: List[WorkflowStep]
    result: Optional[Dict[str, Any]] = None


class WorkflowRequest(BaseModel):
    """Request to execute a workflow."""
    workflow_type: str = Field(pattern="^(full_simulation|attack_only|analysis_only)$")
    parameters: Optional[Dict[str, Any]] = None


class WorkflowResponse(BaseResponse):
    """Response from workflow execution."""
    workflow: WorkflowExecution
    execution_id: str
