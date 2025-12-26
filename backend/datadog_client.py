"""
NEXUS PROTOCOL - Datadog Client
Sends metrics, traces, and logs to Datadog
"""
import os
import logging
from typing import Dict, Any, Optional
from datadog import initialize, statsd
from config import settings

logger = logging.getLogger(__name__)


class DatadogClient:
    """Handles all Datadog metric emissions"""
    
    def __init__(self):
        self.enabled = bool(settings.dd_api_key)
        self.prefix = "nexus"
        
        if self.enabled:
            initialize(
                api_key=settings.dd_api_key,
                app_key=settings.dd_app_key,
                statsd_host="localhost",
                statsd_port=8125
            )
            logger.info("Datadog client initialized")
        else:
            logger.warning("Datadog API key not set - metrics will be logged only")
    
    def _format_tags(self, tags: Dict[str, str]) -> list:
        """Format tags dict to Datadog format"""
        return [f"{k}:{v}" for k, v in tags.items()]
    
    def gauge(self, metric: str, value: float, tags: Optional[Dict[str, str]] = None):
        """Send gauge metric"""
        full_metric = f"{self.prefix}.{metric}"
        tag_list = self._format_tags(tags or {})
        
        if self.enabled:
            statsd.gauge(full_metric, value, tags=tag_list)
        
        logger.debug(f"METRIC [gauge] {full_metric}={value} tags={tag_list}")
    
    def counter(self, metric: str, value: int = 1, tags: Optional[Dict[str, str]] = None):
        """Send counter metric"""
        full_metric = f"{self.prefix}.{metric}"
        tag_list = self._format_tags(tags or {})
        
        if self.enabled:
            statsd.increment(full_metric, value, tags=tag_list)
        
        logger.debug(f"METRIC [counter] {full_metric}+={value} tags={tag_list}")
    
    def histogram(self, metric: str, value: float, tags: Optional[Dict[str, str]] = None):
        """Send histogram metric"""
        full_metric = f"{self.prefix}.{metric}"
        tag_list = self._format_tags(tags or {})
        
        if self.enabled:
            statsd.histogram(full_metric, value, tags=tag_list)
        
        logger.debug(f"METRIC [histogram] {full_metric}={value} tags={tag_list}")
    
    # ============================================
    # NEXUS-SPECIFIC METRICS
    # ============================================
    
    def emit_service_metrics(self, service_id: str, status: str, latency_ms: int, error_rate: float):
        """Emit all metrics for a service"""
        tags = {"service_id": service_id, "status": status}
        
        self.gauge("service.latency", latency_ms, tags)
        self.gauge("service.error_rate", error_rate * 100, tags)  # Convert to percentage
    
    def emit_throughput(self, service_id: str, traffic_volume: int):
        """Emit throughput metric"""
        self.gauge("service.throughput", traffic_volume, {"service_id": service_id})
    
    def emit_llm_metrics(self, model: str, tokens_in: int, tokens_out: int, latency_ms: int, cost: float):
        """Emit LLM-specific metrics"""
        tags = {"model": model, "service_id": "ai-brain"}
        
        self.gauge("llm.tokens.input", tokens_in, tags)
        self.gauge("llm.tokens.output", tokens_out, tags)
        self.histogram("llm.latency", latency_ms, tags)
        self.gauge("llm.cost", cost, tags)
    
    def emit_system_integrity(self, integrity: float):
        """Emit system integrity percentage"""
        self.gauge("system.integrity", integrity)
    
    def emit_websocket_connections(self, count: int):
        """Emit WebSocket connection count"""
        self.gauge("websocket.connections", count)
    
    def emit_kafka_lag(self, lag: int, consumer_group: str = "nexus-backend"):
        """Emit Kafka consumer lag"""
        self.gauge("kafka.lag", lag, {"consumer_group": consumer_group})
    
    def emit_remediation(self, service_id: str, action: str, success: bool):
        """Emit remediation counter"""
        tags = {
            "service_id": service_id,
            "action": action,
            "success": str(success).lower()
        }
        self.counter("remediation.count", 1, tags)
    
    def emit_frontend_fps(self, fps: float, browser: str = "unknown"):
        """Emit frontend FPS metric"""
        self.gauge("frontend.fps", fps, {"browser": browser})


# Global Datadog client instance
datadog_client = DatadogClient()
