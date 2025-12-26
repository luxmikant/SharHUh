"""
NEXUS PROTOCOL - In-Memory State Manager
Maintains current system state and service metrics
"""
import asyncio
from datetime import datetime, timezone
from typing import Dict, List, Optional
from models import ServiceState, SystemState, ServiceStatus, TelemetryEvent
import logging

logger = logging.getLogger(__name__)

# Service positions in 3D space (circular formation)
SERVICE_POSITIONS = {
    "gateway": (0, 0, 5),
    "auth": (4.76, 0, 1.55),
    "payment": (2.94, 0, -4.05),
    "ai-brain": (-2.94, 0, -4.05),
    "database": (-4.76, 0, 1.55)
}


class StateManager:
    """Manages in-memory state for all services"""
    
    def __init__(self):
        self.services: Dict[str, ServiceState] = {}
        self.recent_events: List[TelemetryEvent] = []
        self.max_events = 100
        self.active_incidents: int = 0
        self.start_time = datetime.now(timezone.utc)
        self._lock = asyncio.Lock()
        
        # Initialize all services as healthy
        self._initialize_services()
    
    def _initialize_services(self):
        """Initialize all services with default healthy state"""
        now = datetime.now(timezone.utc).isoformat()
        
        for service_id, position in SERVICE_POSITIONS.items():
            self.services[service_id] = ServiceState(
                service_id=service_id,
                status=ServiceStatus.HEALTHY,
                latency_ms=500,
                error_rate=0.02,
                traffic_volume=75,
                last_updated=now,
                position=position
            )
        
        logger.info(f"Initialized {len(self.services)} services")
    
    async def update_from_event(self, event: TelemetryEvent):
        """Update service state from telemetry event"""
        async with self._lock:
            service_id = event.service_id
            
            if service_id in self.services:
                self.services[service_id] = ServiceState(
                    service_id=service_id,
                    status=ServiceStatus(event.status),
                    latency_ms=event.latency_ms,
                    error_rate=event.error_rate,
                    traffic_volume=event.traffic_volume,
                    last_updated=event.timestamp,
                    position=SERVICE_POSITIONS.get(service_id, (0, 0, 0))
                )
            
            # Add to recent events
            self.recent_events.append(event)
            if len(self.recent_events) > self.max_events:
                self.recent_events.pop(0)
    
    async def get_service_state(self, service_id: str) -> Optional[ServiceState]:
        """Get current state for a specific service"""
        async with self._lock:
            return self.services.get(service_id)
    
    async def get_all_services(self) -> List[ServiceState]:
        """Get current state for all services"""
        async with self._lock:
            return list(self.services.values())
    
    async def get_system_state(self) -> SystemState:
        """Get complete system state for frontend"""
        async with self._lock:
            services = list(self.services.values())
            
            # Calculate system integrity
            healthy_count = sum(1 for s in services if s.status == ServiceStatus.HEALTHY)
            total_count = len(services)
            integrity = (healthy_count / total_count * 100) if total_count > 0 else 0
            
            # Calculate uptime
            uptime = (datetime.now(timezone.utc) - self.start_time).total_seconds()
            
            return SystemState(
                timestamp=datetime.now(timezone.utc).isoformat(),
                system_integrity=round(integrity, 1),
                services=services,
                active_incidents=self.active_incidents,
                uptime_seconds=int(uptime)
            )
    
    async def get_recent_events(self, limit: int = 100) -> List[TelemetryEvent]:
        """Get recent telemetry events"""
        async with self._lock:
            return self.recent_events[-limit:]
    
    async def set_service_status(self, service_id: str, status: ServiceStatus):
        """Manually set service status (for remediation)"""
        async with self._lock:
            if service_id in self.services:
                current = self.services[service_id]
                self.services[service_id] = ServiceState(
                    service_id=service_id,
                    status=status,
                    latency_ms=500 if status == ServiceStatus.HEALTHY else current.latency_ms,
                    error_rate=0.02 if status == ServiceStatus.HEALTHY else current.error_rate,
                    traffic_volume=75 if status == ServiceStatus.HEALTHY else current.traffic_volume,
                    last_updated=datetime.now(timezone.utc).isoformat(),
                    position=current.position
                )
                logger.info(f"Service {service_id} status set to {status}")
    
    async def increment_incidents(self):
        """Increment active incident count"""
        async with self._lock:
            self.active_incidents += 1
    
    async def decrement_incidents(self):
        """Decrement active incident count"""
        async with self._lock:
            if self.active_incidents > 0:
                self.active_incidents -= 1


# Global state manager instance
state_manager = StateManager()
