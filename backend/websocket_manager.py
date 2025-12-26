"""
NEXUS PROTOCOL - WebSocket Manager
Handles real-time connections to frontend clients
"""
import asyncio
import json
from typing import Dict, Set
from fastapi import WebSocket
from datetime import datetime, timezone
import logging
import uuid

logger = logging.getLogger(__name__)


class WebSocketManager:
    """Manages WebSocket connections to frontend clients"""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self._lock = asyncio.Lock()
    
    async def connect(self, websocket: WebSocket) -> str:
        """Accept new WebSocket connection and return client ID"""
        await websocket.accept()
        client_id = str(uuid.uuid4())[:8]
        
        async with self._lock:
            self.active_connections[client_id] = websocket
        
        logger.info(f"Client {client_id} connected. Total: {len(self.active_connections)}")
        
        # Send connection acknowledgment
        await self.send_personal(client_id, {
            "type": "connection_ack",
            "message": "Connected to NEXUS PROTOCOL",
            "client_id": client_id,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
        
        return client_id
    
    async def disconnect(self, client_id: str):
        """Remove WebSocket connection"""
        async with self._lock:
            if client_id in self.active_connections:
                del self.active_connections[client_id]
        
        logger.info(f"Client {client_id} disconnected. Total: {len(self.active_connections)}")
    
    async def send_personal(self, client_id: str, message: dict):
        """Send message to specific client"""
        async with self._lock:
            if client_id in self.active_connections:
                try:
                    await self.active_connections[client_id].send_json(message)
                except Exception as e:
                    logger.error(f"Error sending to {client_id}: {e}")
    
    async def broadcast(self, message: dict):
        """Send message to all connected clients"""
        async with self._lock:
            if not self.active_connections:
                return
            
            disconnected = []
            
            for client_id, websocket in self.active_connections.items():
                try:
                    await websocket.send_json(message)
                except Exception as e:
                    logger.error(f"Error broadcasting to {client_id}: {e}")
                    disconnected.append(client_id)
            
            # Clean up disconnected clients
            for client_id in disconnected:
                del self.active_connections[client_id]
    
    async def broadcast_state_update(self, state: dict):
        """Broadcast system state update to all clients"""
        message = {
            "type": "state_update",
            **state
        }
        await self.broadcast(message)
    
    async def broadcast_alert(self, alert: dict):
        """Broadcast alert to all clients"""
        message = {
            "type": "alert",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            **alert
        }
        await self.broadcast(message)
    
    async def broadcast_remediation_result(self, result: dict):
        """Broadcast remediation result to all clients"""
        message = {
            "type": "remediation_result",
            **result
        }
        await self.broadcast(message)
    
    @property
    def connection_count(self) -> int:
        """Get number of active connections"""
        return len(self.active_connections)


# Global WebSocket manager instance
ws_manager = WebSocketManager()
