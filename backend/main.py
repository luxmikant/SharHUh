"""
NEXUS PROTOCOL - FastAPI Backend
Main application entry point
"""
import asyncio
import logging
import sys
from datetime import datetime, timezone
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import settings
from models import (
    HealthResponse, 
    RemediationRequest, 
    RemediationResponse,
    DatadogWebhookPayload,
    ServiceStatus,
    TelemetryEvent
)
from state import state_manager
from websocket_manager import ws_manager
from datadog_client import datadog_client
from gemini_client import gemini_client
from elevenlabs_client import elevenlabs_client
from kafka_consumer import kafka_consumer

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
logger = logging.getLogger(__name__)

# Background task references
background_tasks = {}


async def process_telemetry_event(event: TelemetryEvent):
    """Process incoming telemetry event from Kafka or Chaos Engine"""
    # Update state
    await state_manager.update_from_event(event)
    
    # Emit Datadog metrics
    datadog_client.emit_service_metrics(
        event.service_id,
        event.status,
        event.latency_ms,
        event.error_rate
    )
    datadog_client.emit_throughput(event.service_id, event.traffic_volume)
    
    # Emit LLM metrics if this is the ai-brain service
    if event.service_id == "ai-brain" and "tokens_in" in event.metadata:
        datadog_client.emit_llm_metrics(
            model=event.metadata.get("model", "gemini-2.0-flash"),
            tokens_in=event.metadata.get("tokens_in", 0),
            tokens_out=event.metadata.get("tokens_out", 0),
            latency_ms=event.latency_ms,
            cost=event.metadata.get("tokens_in", 0) * 0.00001  # Rough cost estimate
        )


async def broadcast_state_loop():
    """Periodically broadcast system state to all WebSocket clients"""
    while True:
        try:
            if ws_manager.connection_count > 0:
                state = await state_manager.get_system_state()
                
                # Emit system integrity to Datadog
                datadog_client.emit_system_integrity(state.system_integrity)
                datadog_client.emit_websocket_connections(ws_manager.connection_count)
                
                # Broadcast to all clients
                await ws_manager.broadcast_state_update(state.model_dump())
            
            await asyncio.sleep(2)  # Broadcast every 2 seconds
            
        except asyncio.CancelledError:
            break
        except Exception as e:
            logger.error(f"Error in broadcast loop: {e}")
            await asyncio.sleep(1)


async def run_simulation_mode():
    """Run built-in simulation when Kafka is not available"""
    from chaos_engine.main import ChaosEngine
    
    logger.info("Starting simulation mode (Kafka not available)")
    engine = ChaosEngine()
    
    async def event_callback(event):
        # Convert chaos engine event to model
        telemetry = TelemetryEvent(
            timestamp=event.timestamp,
            service_id=event.service_id,
            status=event.status,
            latency_ms=event.latency_ms,
            error_rate=event.error_rate,
            traffic_volume=event.traffic_volume,
            message=event.message,
            metadata=event.metadata
        )
        await process_telemetry_event(telemetry)
    
    await engine.run(callback=event_callback)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    logger.info("🚀 Starting NEXUS PROTOCOL Backend...")
    
    # Start background state broadcast
    background_tasks["broadcast"] = asyncio.create_task(broadcast_state_loop())
    
    # Start Kafka consumer or simulation mode
    if kafka_consumer.enabled:
        background_tasks["kafka"] = asyncio.create_task(
            kafka_consumer.start(process_telemetry_event)
        )
    else:
        background_tasks["simulation"] = asyncio.create_task(run_simulation_mode())
    
    logger.info("✅ Backend started successfully")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down NEXUS PROTOCOL Backend...")
    
    for name, task in background_tasks.items():
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
    
    kafka_consumer.stop()
    logger.info("👋 Backend shutdown complete")


# Create FastAPI app
app = FastAPI(
    title="NEXUS PROTOCOL",
    description="3D Observability Holodeck for LLM Systems",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files for audio
static_dir = Path(__file__).parent / "static"
static_dir.mkdir(exist_ok=True)
(static_dir / "audio").mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")


# ============================================
# REST ENDPOINTS
# ============================================

@app.get("/", response_class=JSONResponse)
async def root():
    """Root endpoint"""
    return {
        "name": "NEXUS PROTOCOL",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs"
    }


@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    services = await state_manager.get_all_services()
    service_status = {s.service_id: s.status.value for s in services}
    
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        services=service_status
    )


@app.get("/api/state")
async def get_state():
    """Get current system state"""
    state = await state_manager.get_system_state()
    return state.model_dump()


@app.get("/api/metrics/recent")
async def get_recent_metrics(limit: int = 100):
    """Get recent telemetry events"""
    events = await state_manager.get_recent_events(limit)
    return [e.model_dump() for e in events]


@app.post("/api/remediate", response_model=RemediationResponse)
async def apply_remediation(request: RemediationRequest):
    """Apply remediation action to a service"""
    service = await state_manager.get_service_state(request.service_id)
    
    if not service:
        raise HTTPException(status_code=404, detail=f"Service {request.service_id} not found")
    
    previous_status = service.status
    
    # Apply remediation
    await state_manager.set_service_status(request.service_id, ServiceStatus.HEALTHY)
    
    # Emit Datadog metric
    datadog_client.emit_remediation(
        request.service_id,
        request.action.value,
        success=True
    )
    
    # Broadcast result
    await ws_manager.broadcast_remediation_result({
        "success": True,
        "service_id": request.service_id,
        "action": request.action.value,
        "message": f"Remediation applied: {request.action.value}"
    })
    
    return RemediationResponse(
        success=True,
        service_id=request.service_id,
        action=request.action,
        previous_status=previous_status,
        new_status=ServiceStatus.HEALTHY,
        message=f"Remediation applied successfully"
    )


@app.post("/api/datadog/webhook")
async def datadog_webhook(payload: DatadogWebhookPayload, background: BackgroundTasks):
    """Receive webhook from Datadog monitor"""
    logger.info(f"Received Datadog webhook: {payload.alert_title}")
    
    # Extract service ID from alert (if available)
    service_id = "unknown"
    if payload.alert_scope:
        # Parse service_id from scope like "service_id:ai-brain"
        for part in payload.alert_scope.split(","):
            if "service_id:" in part:
                service_id = part.split(":")[1].strip()
                break
    
    # Get current service state
    service = await state_manager.get_service_state(service_id)
    
    # Generate Gemini analysis
    analysis = await gemini_client.analyze_incident(
        service_id=service_id,
        status=service.status.value if service else "critical",
        latency_ms=service.latency_ms if service else 5000,
        error_rate=service.error_rate if service else 0.5,
        error_messages=[payload.text_only_msg or "Unknown error"]
    )
    
    # Generate voice alert
    audio_url = await elevenlabs_client.generate_alert_for_service(service_id, analysis)
    
    # Increment incident count
    await state_manager.increment_incidents()
    
    # Broadcast alert to all clients
    await ws_manager.broadcast_alert({
        "severity": payload.priority or "p2",
        "service_id": service_id,
        "message": payload.alert_title,
        "analysis": analysis,
        "audio_url": audio_url,
        "datadog_url": f"https://app.datadoghq.com/monitors/{payload.alert_id}" if payload.alert_id else None
    })
    
    return {"received": True, "service_id": service_id, "analysis": analysis}


@app.post("/api/chaos/mode/{mode}")
async def set_chaos_mode(mode: str):
    """Set chaos engine mode (for demo)"""
    valid_modes = ["steady_state", "latency_spike", "cascading_failure", "recovery"]
    
    if mode not in valid_modes:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid mode. Choose from: {valid_modes}"
        )
    
    # This would communicate with the chaos engine in production
    # For now, we manually update states
    if mode == "steady_state":
        for service_id in ["gateway", "auth", "payment", "ai-brain", "database"]:
            await state_manager.set_service_status(service_id, ServiceStatus.HEALTHY)
    elif mode == "latency_spike":
        await state_manager.set_service_status("ai-brain", ServiceStatus.CRITICAL)
    elif mode == "cascading_failure":
        await state_manager.set_service_status("ai-brain", ServiceStatus.CRITICAL)
        await state_manager.set_service_status("payment", ServiceStatus.WARNING)
        await state_manager.set_service_status("auth", ServiceStatus.WARNING)
    elif mode == "recovery":
        for service_id in ["gateway", "auth", "payment", "ai-brain", "database"]:
            await state_manager.set_service_status(service_id, ServiceStatus.HEALTHY)
    
    logger.info(f"Chaos mode set to: {mode}")
    return {"mode": mode, "success": True}


# ============================================
# WEBSOCKET ENDPOINT
# ============================================

@app.websocket("/ws/nexus")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time state updates"""
    client_id = await ws_manager.connect(websocket)
    
    try:
        # Send initial state
        state = await state_manager.get_system_state()
        await ws_manager.send_personal(client_id, {
            "type": "state_update",
            **state.model_dump()
        })
        
        # Keep connection alive and handle incoming messages
        while True:
            try:
                # Wait for incoming messages (ping/pong or future commands)
                data = await asyncio.wait_for(
                    websocket.receive_text(),
                    timeout=30.0  # 30 second timeout
                )
                
                # Handle ping
                if data == "ping":
                    await websocket.send_text("pong")
                    
            except asyncio.TimeoutError:
                # Send keepalive
                await websocket.send_text("ping")
                
    except WebSocketDisconnect:
        await ws_manager.disconnect(client_id)
    except Exception as e:
        logger.error(f"WebSocket error for {client_id}: {e}")
        await ws_manager.disconnect(client_id)


# ============================================
# MAIN ENTRY POINT
# ============================================

if __name__ == "__main__":
    import uvicorn
    
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║           NEXUS PROTOCOL - BACKEND SERVER                 ║
    ║                                                           ║
    ║   3D Observability Holodeck for LLM Systems              ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )
