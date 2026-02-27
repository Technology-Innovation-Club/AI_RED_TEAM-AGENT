"""
API routes for the AI Automated Red Team Agent (AARTA).
Defines all REST endpoints for the web interface.
"""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import List, Dict, Any, Optional
import uuid
from datetime import datetime

from app.api.schemas import (
    BaseResponse, ErrorResponse, SimulationRequest, SimulationResponse,
    AttackRequest, AttackResponse, FullAttackSimulationRequest,
    AnalysisRequest, AnalysisResponse, ReportRequest, ReportResponse,
    TelemetryFilter, TelemetryResponse, WorkflowRequest, WorkflowResponse,
    InfrastructureData, SystemStatus
)
from app.core.orchestrator import Orchestrator
from app.core.state_manager import StateManager
from app.core.telemetry import Telemetry

# Create router
router = APIRouter()

# Dependency injection for components
def get_orchestrator() -> Orchestrator:
    """Get orchestrator instance."""
    # This will be injected from main.py
    from app.main import orchestrator
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator not initialized")
    return orchestrator

def get_state_manager() -> StateManager:
    """Get state manager instance."""
    from app.main import state_manager
    if not state_manager:
        raise HTTPException(status_code=503, detail="State manager not initialized")
    return state_manager

def get_telemetry() -> Telemetry:
    """Get telemetry instance."""
    from app.main import telemetry
    if not telemetry:
        raise HTTPException(status_code=503, detail="Telemetry not initialized")
    return telemetry


# Infrastructure endpoints
@router.get("/infrastructure", response_model=InfrastructureData)
async def get_infrastructure(
    state_manager: StateManager = Depends(get_state_manager)
):
    """Get current infrastructure configuration."""
    try:
        infrastructure = state_manager.get_infrastructure()
        if not infrastructure:
            raise HTTPException(status_code=404, detail="No infrastructure data available")
        return infrastructure
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get infrastructure: {str(e)}")


@router.post("/infrastructure/simulate", response_model=SimulationResponse)
async def simulate_infrastructure(
    request: SimulationRequest,
    orchestrator: Orchestrator = Depends(get_orchestrator),
    telemetry: Telemetry = Depends(get_telemetry)
):
    """Run infrastructure simulation."""
    try:
        telemetry.log_system_event("Infrastructure Simulation", "Starting infrastructure simulation")
        
        result = orchestrator.run_infrastructure_simulation(
            include_rogue_ap=request.include_rogue_ap,
            include_vulnerabilities=request.include_vulnerabilities,
            network_count=request.network_count,
            system_count=request.system_count,
            database_count=request.database_count
        )
        
        telemetry.log_system_event("Infrastructure Simulation", f"Completed simulation: {result['networks_generated']} networks, {result['systems_generated']} systems, {result['databases_generated']} databases")
        
        return SimulationResponse(
            infrastructure=result["infrastructure"],
            networks_generated=result["networks_generated"],
            systems_generated=result["systems_generated"],
            databases_generated=result["databases_generated"]
        )
    except Exception as e:
        telemetry.log_system_event("Infrastructure Simulation Error", str(e), "error")
        raise HTTPException(status_code=500, detail=f"Simulation failed: {str(e)}")


# Attack endpoints
@router.post("/attack/execute", response_model=AttackResponse)
async def execute_attack(
    request: AttackRequest,
    orchestrator: Orchestrator = Depends(get_orchestrator),
    telemetry: Telemetry = Depends(get_telemetry)
):
    """Execute a single attack."""
    try:
        telemetry.log_attack_execution(request.attack_type.value, request.target, False)
        
        result = orchestrator.execute_attack(
            attack_type=request.attack_type.value,
            target=request.target,
            parameters=request.parameters or {},
            simulate_reasoning=request.simulate_reasoning
        )
        
        telemetry.log_attack_execution(request.attack_type.value, request.target, result["success"])
        
        return AttackResponse(
            attack_results=result["attack_results"],
            attacks_executed=result["attacks_executed"],
            successful_attacks=result["successful_attacks"],
            failed_attacks=result["failed_attacks"]
        )
    except Exception as e:
        telemetry.log_system_event("Attack Execution Error", str(e), "error")
        raise HTTPException(status_code=500, detail=f"Attack execution failed: {str(e)}")


@router.post("/attack/simulate", response_model=AttackResponse)
async def simulate_full_attack(
    request: FullAttackSimulationRequest,
    orchestrator: Orchestrator = Depends(get_orchestrator),
    telemetry: Telemetry = Depends(get_telemetry)
):
    """Run full attack simulation."""
    try:
        telemetry.log_system_event("Full Attack Simulation", "Starting comprehensive attack simulation")
        
        result = orchestrator.run_full_attack_simulation(
            target_networks=request.target_networks,
            target_systems=request.target_systems,
            target_databases=request.target_databases,
            attack_phases=request.attack_phases,
            max_attacks_per_phase=request.max_attacks_per_phase
        )
        
        telemetry.log_system_event("Full Attack Simulation", f"Completed simulation: {result['attacks_executed']} attacks executed")
        
        return AttackResponse(
            attack_results=result["attack_results"],
            attacks_executed=result["attacks_executed"],
            successful_attacks=result["successful_attacks"],
            failed_attacks=result["failed_attacks"]
        )
    except Exception as e:
        telemetry.log_system_event("Full Attack Simulation Error", str(e), "error")
        raise HTTPException(status_code=500, detail=f"Attack simulation failed: {str(e)}")


@router.get("/attack/results", response_model=List[Dict[str, Any]])
async def get_attack_results(
    state_manager: StateManager = Depends(get_state_manager)
):
    """Get all attack results."""
    try:
        results = state_manager.get_attack_results()
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get attack results: {str(e)}")


# Analysis endpoints
@router.post("/analysis/vulnerabilities", response_model=AnalysisResponse)
async def analyze_vulnerabilities(
    request: AnalysisRequest,
    orchestrator: Orchestrator = Depends(get_orchestrator),
    telemetry: Telemetry = Depends(get_telemetry)
):
    """Analyze attack results for vulnerabilities."""
    try:
        telemetry.log_system_event("Vulnerability Analysis", "Starting vulnerability analysis")
        
        result = orchestrator.analyze_vulnerabilities(
            include_cwe_mapping=request.include_cwe_mapping,
            include_owasp_mapping=request.include_owasp_mapping,
            generate_mitigations=request.generate_mitigations
        )
        
        telemetry.log_system_event("Vulnerability Analysis", f"Analysis complete: {result['total_vulnerabilities']} vulnerabilities found")
        
        return AnalysisResponse(
            vulnerabilities=result["vulnerabilities"],
            total_vulnerabilities=result["total_vulnerabilities"],
            severity_breakdown=result["severity_breakdown"],
            cwe_mapping=result["cwe_mapping"],
            owasp_mapping=result["owasp_mapping"]
        )
    except Exception as e:
        telemetry.log_system_event("Vulnerability Analysis Error", str(e), "error")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.get("/analysis/vulnerabilities", response_model=List[Dict[str, Any]])
async def get_vulnerabilities(
    state_manager: StateManager = Depends(get_state_manager)
):
    """Get analyzed vulnerabilities."""
    try:
        vulnerabilities = state_manager.get_vulnerabilities()
        return vulnerabilities
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get vulnerabilities: {str(e)}")


# Report endpoints
@router.post("/report/generate", response_model=ReportResponse)
async def generate_report(
    request: ReportRequest,
    orchestrator: Orchestrator = Depends(get_orchestrator),
    telemetry: Telemetry = Depends(get_telemetry)
):
    """Generate security report."""
    try:
        telemetry.log_system_event("Report Generation", "Starting security report generation")
        
        result = orchestrator.generate_report(
            format=request.format,
            include_executive_summary=request.include_executive_summary,
            include_technical_details=request.include_technical_details,
            include_mitigations=request.include_mitigations,
            severity_threshold=request.severity_threshold.value
        )
        
        telemetry.log_system_event("Report Generation", f"Report generated: {result['format']} format")
        
        return ReportResponse(
            report=result["report"],
            format=result["format"],
            file_path=result.get("file_path")
        )
    except Exception as e:
        telemetry.log_system_event("Report Generation Error", str(e), "error")
        raise HTTPException(status_code=500, detail=f"Report generation failed: {str(e)}")


@router.get("/report/download")
async def download_report(
    state_manager: StateManager = Depends(get_state_manager)
):
    """Download generated report."""
    try:
        report_content = state_manager.get_report_content()
        if not report_content:
            raise HTTPException(status_code=404, detail="No report available")
        
        return JSONResponse(
            content=report_content,
            headers={
                "Content-Disposition": "attachment; filename=security_report.md"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to download report: {str(e)}")


# Telemetry endpoints
@router.get("/telemetry/events", response_model=TelemetryResponse)
async def get_telemetry_events(
    component: Optional[str] = None,
    severity: Optional[str] = None,
    limit: int = 100,
    telemetry: Telemetry = Depends(get_telemetry)
):
    """Get telemetry events."""
    try:
        # Apply filters
        events = telemetry.export()
        
        if component:
            events = [e for e in events if e["component"] == component]
        
        if severity:
            events = [e for e in events if e["severity"] == severity]
        
        # Limit results
        events = events[-limit:]
        
        return TelemetryResponse(
            events=events,
            total_events=len(events),
            statistics=telemetry.get_statistics()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get telemetry: {str(e)}")


@router.get("/telemetry/statistics")
async def get_telemetry_statistics(
    telemetry: Telemetry = Depends(get_telemetry)
):
    """Get telemetry statistics."""
    try:
        return telemetry.get_statistics()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get statistics: {str(e)}")


# Workflow endpoints
@router.post("/workflow/execute", response_model=WorkflowResponse)
async def execute_workflow(
    request: WorkflowRequest,
    orchestrator: Orchestrator = Depends(get_orchestrator),
    telemetry: Telemetry = Depends(get_telemetry)
):
    """Execute a complete workflow."""
    try:
        telemetry.log_system_event("Workflow Execution", f"Starting {request.workflow_type} workflow")
        
        result = orchestrator.execute_workflow(
            workflow_type=request.workflow_type,
            parameters=request.parameters or {}
        )
        
        telemetry.log_system_event("Workflow Execution", f"Completed {request.workflow_type} workflow")
        
        return WorkflowResponse(
            workflow=result["workflow"],
            execution_id=result["execution_id"]
        )
    except Exception as e:
        telemetry.log_system_event("Workflow Execution Error", str(e), "error")
        raise HTTPException(status_code=500, detail=f"Workflow execution failed: {str(e)}")


# Utility endpoints
@router.delete("/data/reset")
async def reset_all_data(
    orchestrator: Orchestrator = Depends(get_orchestrator),
    state_manager: StateManager = Depends(get_state_manager),
    telemetry: Telemetry = Depends(get_telemetry)
):
    """Reset all application data."""
    try:
        telemetry.log_system_event("Data Reset", "Resetting all application data")
        
        state_manager.reset_all_data()
        telemetry.clear_logs()
        
        return BaseResponse(
            success=True,
            message="All data has been reset successfully"
        )
    except Exception as e:
        telemetry.log_system_event("Data Reset Error", str(e), "error")
        raise HTTPException(status_code=500, detail=f"Data reset failed: {str(e)}")


@router.get("/system/status", response_model=SystemStatus)
async def get_system_status(
    orchestrator: Orchestrator = Depends(get_orchestrator),
    state_manager: StateManager = Depends(get_state_manager),
    telemetry: Telemetry = Depends(get_telemetry)
):
    """Get comprehensive system status."""
    try:
        return SystemStatus(
            status="ready",
            session_id=telemetry.session_id,
            infrastructure_loaded=state_manager.infrastructure_loaded(),
            attack_results_available=state_manager.attack_results_available(),
            report_generated=state_manager.report_generated(),
            telemetry_events=len(telemetry.events),
            components={
                "orchestrator": orchestrator is not None,
                "state_manager": state_manager is not None,
                "telemetry": telemetry is not None
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get system status: {str(e)}")