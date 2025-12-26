"""
NEXUS PROTOCOL - Pydantic Models
Data schemas for API requests/responses and internal state
"""
from pydantic import BaseModel, Field
from typing import Literal, Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


# ============================================
# ENUMS
# ============================================

class ServiceStatus(str, Enum):
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"


class RemediationAction(str, Enum):
    RESET_CONTEXT = "reset_context"
    SCALE_UP = "scale_up"
    FAILOVER = "failover"
    RATE_LIMIT = "rate_limit"


class AlertSeverity(str, Enum):
    P1 = "p1"
    P2 = "p2"
    P3 = "p3"


# ============================================
# TELEMETRY MODELS
# ============================================

class TelemetryEvent(BaseModel):
    """Single telemetry event from Chaos Engine"""
    timestamp: str
    service_id: str
    status: ServiceStatus
    latency_ms: int = Field(ge=0, le=10000)
    error_rate: float = Field(ge=0.0, le=1.0)
    traffic_volume: int = Field(ge=0, le=100)
    message: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ServiceState(BaseModel):
    """Current state of a single service"""
    service_id: str
    status: ServiceStatus
    latency_ms: int
    error_rate: float
    traffic_volume: int
    last_updated: str
    position: tuple = Field(default=(0, 0, 0))


class SystemState(BaseModel):
    """Complete system state for frontend"""
    timestamp: str
    system_integrity: float = Field(ge=0.0, le=100.0)
    services: List[ServiceState]
    active_incidents: int = 0
    uptime_seconds: int = 0


# ============================================
# API REQUEST/RESPONSE MODELS
# ============================================

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str = "1.0.0"
    services: Dict[str, str]


class RemediationRequest(BaseModel):
    """Request to apply a fix"""
    service_id: str
    action: RemediationAction


class RemediationResponse(BaseModel):
    """Response after remediation attempt"""
    success: bool
    service_id: str
    action: RemediationAction
    previous_status: ServiceStatus
    new_status: ServiceStatus
    message: str


class DatadogWebhookPayload(BaseModel):
    """Incoming webhook from Datadog monitor"""
    alert_id: Optional[str] = None
    alert_title: str
    alert_type: str
    event_type: str
    hostname: Optional[str] = None
    org_name: Optional[str] = None
    priority: Optional[str] = None
    tags: Optional[str] = None
    text_only_msg: Optional[str] = None
    alert_query: Optional[str] = None
    alert_scope: Optional[str] = None
    alert_status: Optional[str] = None


# ============================================
# WEBSOCKET MESSAGES
# ============================================

class WSMessageType(str, Enum):
    STATE_UPDATE = "state_update"
    ALERT = "alert"
    REMEDIATION_RESULT = "remediation_result"
    CONNECTION_ACK = "connection_ack"


class WSStateUpdate(BaseModel):
    """WebSocket message: state update"""
    type: Literal["state_update"] = "state_update"
    timestamp: str
    system_integrity: float
    services: List[ServiceState]


class WSAlert(BaseModel):
    """WebSocket message: alert notification"""
    type: Literal["alert"] = "alert"
    timestamp: str
    severity: AlertSeverity
    service_id: str
    message: str
    analysis: str  # Gemini analysis
    audio_url: Optional[str] = None  # ElevenLabs audio
    datadog_url: Optional[str] = None


class WSRemediationResult(BaseModel):
    """WebSocket message: remediation result"""
    type: Literal["remediation_result"] = "remediation_result"
    success: bool
    service_id: str
    action: str
    message: str


class WSConnectionAck(BaseModel):
    """WebSocket message: connection acknowledged"""
    type: Literal["connection_ack"] = "connection_ack"
    message: str = "Connected to NEXUS PROTOCOL"
    client_id: str


# ============================================
# GEMINI / AI MODELS
# ============================================

class IncidentAnalysisRequest(BaseModel):
    """Request for Gemini to analyze incident"""
    service_id: str
    status: ServiceStatus
    latency_ms: int
    error_rate: float
    recent_errors: List[str] = Field(default_factory=list)


class IncidentAnalysisResponse(BaseModel):
    """Gemini analysis result"""
    analysis: str
    confidence: float = Field(ge=0.0, le=1.0)
    suggested_action: Optional[RemediationAction] = None
