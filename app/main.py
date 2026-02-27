# """
# AI Automated Red Team Agent (AARTA) - FastAPI Application
# Main entry point for the web interface.
# """

# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import JSONResponse, FileResponse
# from fastapi.staticfiles import StaticFiles
# import uvicorn
# from pathlib import Path
# import sys
# import os

# # Add the project root directory to Python path for imports
# project_root = Path(__file__).parent.parent
# sys.path.insert(0, str(project_root))
# sys.path.insert(0, str(project_root / "app"))

# from app.api.routes import router
# from app.core.orchestrator import Orchestrator
# from app.core.state_manager import StateManager
# from app.core.telemetry import Telemetry

# # Create FastAPI application
# app = FastAPI(
#     title="AI Automated Red Team Agent (AARTA)",
#     description="Ethical AI-powered red team simulation for cybersecurity training",
#     version="1.0.0",
#     docs_url="/docs",
#     redoc_url="/redoc"
# )

# # Add CORS middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Global components
# orchestrator = None
# state_manager = None
# telemetry = None


# @app.on_event("startup")
# async def startup_event():
#     """Initialize application components on startup."""
#     global orchestrator, state_manager, telemetry
    
#     # Initialize core components
#     telemetry = Telemetry()
#     state_manager = StateManager()
#     orchestrator = Orchestrator(telemetry, state_manager)
    
#     telemetry.log_system_event("Application Startup", "AARTA web interface started")
    
#     # Ensure data directory exists
#     data_dir = Path("app/data")
#     data_dir.mkdir(parents=True, exist_ok=True)


# @app.on_event("shutdown")
# async def shutdown_event():
#     """Clean up on application shutdown."""
#     if telemetry:
#         telemetry.log_system_event("Application Shutdown", "AARTA web interface shutting down")
#         telemetry.save_to_file()


# @app.get("/")
# async def root():
#     """Serve the frontend index page."""
#     frontend_path = Path(__file__).parent.parent / "frontend" / "index.html"
#     if frontend_path.exists():
#         return FileResponse(frontend_path)
#     else:
#         return {
#             "message": "AI Automated Red Team Agent (AARTA)",
#             "version": "1.0.0",
#             "description": "Ethical AI-powered red team simulation for cybersecurity training",
#             "frontend": "Frontend not found. Please check the frontend directory.",
#             "endpoints": {
#                 "infrastructure": "/api/infrastructure",
#                 "simulation": "/api/simulation",
#                 "attack": "/api/attack",
#                 "analysis": "/api/analysis",
#                 "report": "/api/report",
#                 "docs": "/docs"
#             }
#         }


# @app.get("/health")
# async def health_check():
#     """Health check endpoint."""
#     return {
#         "status": "healthy",
#         "components": {
#             "orchestrator": orchestrator is not None,
#             "state_manager": state_manager is not None,
#             "telemetry": telemetry is not None
#         }
#     }


# @app.get("/api/status")
# async def get_status():
#     """Get current system status."""
#     if not orchestrator:
#         raise HTTPException(status_code=503, detail="System not initialized")
    
#     # Get state summary from state manager
#     state_summary = state_manager.get_state_summary() if state_manager else {}
    
#     return {
#         "status": "ready",
#         "session_id": telemetry.session_id if telemetry else None,
#         "data": {
#             "infrastructure": {
#                 "loaded": state_manager.infrastructure_loaded() if state_manager else False,
#                 "network_count": state_summary.get("infrastructure", {}).get("network_count", 0),
#                 "system_count": state_summary.get("infrastructure", {}).get("system_count", 0),
#                 "database_count": state_summary.get("infrastructure", {}).get("database_count", 0),
#                 "last_updated": state_summary.get("infrastructure", {}).get("last_updated")
#             },
#             "attacks": {
#                 "available": state_manager.attack_results_available() if state_manager else False,
#                 "total_attacks": state_summary.get("attacks", {}).get("total_attacks", 0),
#                 "successful_attacks": state_summary.get("attacks", {}).get("successful_attacks", 0),
#                 "failed_attacks": state_summary.get("attacks", {}).get("failed_attacks", 0),
#                 "last_updated": state_summary.get("attacks", {}).get("last_updated")
#             },
#             "vulnerabilities": {
#                 "available": state_manager.vulnerabilities_available() if state_manager else False,
#                 "total_vulnerabilities": state_summary.get("vulnerabilities", {}).get("total_vulnerabilities", 0),
#                 "severity_breakdown": state_summary.get("vulnerabilities", {}).get("severity_breakdown", {}),
#                 "last_updated": state_summary.get("vulnerabilities", {}).get("last_updated")
#             },
#             "report": {
#                 "generated": state_manager.report_generated() if state_manager else False,
#                 "generated_at": state_summary.get("report", {}).get("generated_at"),
#                 "session_id": state_summary.get("report", {}).get("session_id"),
#                 "saved_at": state_summary.get("report", {}).get("saved_at")
#             }
#         },
#         "telemetry_events": len(telemetry.events) if telemetry else 0
#     }


# # Include API routes
# app.include_router(router, prefix="/api", tags=["API"])

# # Mount static files for frontend
# frontend_dir = Path(__file__).parent.parent / "frontend"
# if frontend_dir.exists():
#     app.mount("/static", StaticFiles(directory=str(frontend_dir)), name="static")


# # Error handlers
# @app.exception_handler(Exception)
# async def global_exception_handler(request, exc):
#     """Global exception handler."""
#     if telemetry:
#         telemetry.log_system_event("Error", f"Unhandled exception: {str(exc)}", "error")
    
#     return JSONResponse(
#         status_code=500,
#         content={
#             "error": "Internal server error",
#             "message": "An unexpected error occurred. Please check the logs."
#         }
#     )


# @app.exception_handler(HTTPException)
# async def http_exception_handler(request, exc):
#     """HTTP exception handler."""
#     return JSONResponse(
#         status_code=exc.status_code,
#         content={"error": exc.detail}
#     )


# if __name__ == "__main__":
#     """
#     Development server entry point.
#     Use this for local development only.
#     For production, use uvicorn directly.
#     """
#     print("Starting AARTA Development Server...")
#     print("API Documentation: http://localhost:8000/docs")
#     print("Health Check: http://localhost:8000/health")
    
#     uvicorn.run(
#         "app.main:app",
#         host="0.0.0.0",
#         port=8000,
#         reload=True,
#         log_level="info"
#     )

"""
AI Automated Red Team Agent (AARTA) - FastAPI Application
Main entry point for the web interface.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from pathlib import Path
import sys

# ---------------------------------------------------------
# PATH CONFIGURATION (Stabilized)
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
APP_DIR = PROJECT_ROOT / "app"
FRONTEND_DIR = PROJECT_ROOT / "frontend"

sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(APP_DIR))

from app.api.routes import router
from app.core.orchestrator import Orchestrator
from app.core.state_manager import StateManager
from app.core.telemetry import Telemetry

# ---------------------------------------------------------
# FASTAPI APPLICATION
# ---------------------------------------------------------

app = FastAPI(
    title="AI Automated Red Team Agent (AARTA)",
    description="Ethical AI-powered red team simulation for cybersecurity training",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# ---------------------------------------------------------
# CORS CONFIGURATION
# (Safe for dev — restrict in production)
# ---------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------
# GLOBAL COMPONENTS
# ---------------------------------------------------------

orchestrator = None
state_manager = None
telemetry = None

# ---------------------------------------------------------
# STARTUP EVENT
# ---------------------------------------------------------

@app.on_event("startup")
async def startup_event():
    """Initialize application components on startup."""
    global orchestrator, state_manager, telemetry

    telemetry = Telemetry()
    state_manager = StateManager()
    orchestrator = Orchestrator(telemetry, state_manager)

    telemetry.log_system_event(
        "Application Startup",
        "AARTA web interface started"
    )

    # Ensure data directory exists
    data_dir = PROJECT_ROOT / "app" / "data"
    data_dir.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------
# SHUTDOWN EVENT
# ---------------------------------------------------------

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up on application shutdown."""
    if telemetry:
        telemetry.log_system_event(
            "Application Shutdown",
            "AARTA web interface shutting down"
        )
        telemetry.save_to_file()


# ---------------------------------------------------------
# ROOT ROUTE - SERVE FRONTEND
# ---------------------------------------------------------

@app.get("/", include_in_schema=False)
async def root():
    """Serve the frontend index page."""
    index_path = FRONTEND_DIR / "index.html"

    if index_path.exists():
        return FileResponse(index_path)
    else:
        return {
            "message": "AI Automated Red Team Agent (AARTA)",
            "version": "1.0.0",
            "description": "Frontend not found. Check /frontend directory.",
            "docs": "/docs",
            "health": "/health"
        }


# ---------------------------------------------------------
# HEALTH CHECK
# ---------------------------------------------------------

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "components": {
            "orchestrator": orchestrator is not None,
            "state_manager": state_manager is not None,
            "telemetry": telemetry is not None
        }
    }


# ---------------------------------------------------------
# STATUS ENDPOINT
# ---------------------------------------------------------

@app.get("/api/status")
async def get_status():
    """Get current system status."""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="System not initialized")

    state_summary = state_manager.get_state_summary() if state_manager else {}

    return {
        "status": "ready",
        "session_id": telemetry.session_id if telemetry else None,
        "data": {
            "infrastructure": {
                "loaded": state_manager.infrastructure_loaded() if state_manager else False,
                "network_count": state_summary.get("infrastructure", {}).get("network_count", 0),
                "system_count": state_summary.get("infrastructure", {}).get("system_count", 0),
                "database_count": state_summary.get("infrastructure", {}).get("database_count", 0),
                "last_updated": state_summary.get("infrastructure", {}).get("last_updated")
            },
            "attacks": {
                "available": state_manager.attack_results_available() if state_manager else False,
                "total_attacks": state_summary.get("attacks", {}).get("total_attacks", 0),
                "successful_attacks": state_summary.get("attacks", {}).get("successful_attacks", 0),
                "failed_attacks": state_summary.get("attacks", {}).get("failed_attacks", 0),
                "last_updated": state_summary.get("attacks", {}).get("last_updated")
            },
            "vulnerabilities": {
                "available": state_manager.vulnerabilities_available() if state_manager else False,
                "total_vulnerabilities": state_summary.get("vulnerabilities", {}).get("total_vulnerabilities", 0),
                "severity_breakdown": state_summary.get("vulnerabilities", {}).get("severity_breakdown", {}),
                "last_updated": state_summary.get("vulnerabilities", {}).get("last_updated")
            },
            "report": {
                "generated": state_manager.report_generated() if state_manager else False,
                "generated_at": state_summary.get("report", {}).get("generated_at"),
                "session_id": state_summary.get("report", {}).get("session_id"),
                "saved_at": state_summary.get("report", {}).get("saved_at")
            }
        },
        "telemetry_events": len(telemetry.events) if telemetry else 0
    }


# ---------------------------------------------------------
# INCLUDE API ROUTES
# ---------------------------------------------------------

app.include_router(router, prefix="/api", tags=["API"])


# ---------------------------------------------------------
# STATIC FILE MOUNT (CRITICAL FIX)
# ---------------------------------------------------------

if FRONTEND_DIR.exists():
    app.mount(
        "/static",
        StaticFiles(directory=str(FRONTEND_DIR)),
        name="static"
    )


# ---------------------------------------------------------
# GLOBAL ERROR HANDLERS
# ---------------------------------------------------------

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    if telemetry:
        telemetry.log_system_event(
            "Error",
            f"Unhandled exception: {str(exc)}",
            "error"
        )

    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred. Please check the logs."
        }
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """HTTP exception handler."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )


# ---------------------------------------------------------
# DEVELOPMENT ENTRY POINT
# ---------------------------------------------------------

if __name__ == "__main__":
    print("Starting AARTA Development Server...")
    print("Frontend: http://localhost:8000")
    print("API Docs: http://localhost:8000/docs")
    print("Health: http://localhost:8000/health")

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
