"""
NEXUS PROTOCOL - Chaos Engine
Generates realistic traffic patterns and failure scenarios for demo
"""
import asyncio
import json
import random
import time
from datetime import datetime, timezone
from typing import Literal
from dataclasses import dataclass, asdict
import os

# Configuration
SERVICES = [
    {"id": "gateway", "position": (0, 0, 5)},
    {"id": "auth", "position": (4.76, 0, 1.55)},
    {"id": "payment", "position": (2.94, 0, -4.05)},
    {"id": "ai-brain", "position": (-2.94, 0, -4.05)},
    {"id": "database", "position": (-4.76, 0, 1.55)}
]

LATENCY_RANGES = {
    "healthy": (200, 800),
    "warning": (1000, 2000),
    "critical": (3000, 6000)
}

ERROR_RATE_RANGES = {
    "healthy": (0.01, 0.03),
    "warning": (0.05, 0.10),
    "critical": (0.15, 0.80)
}

TRAFFIC_VOLUME_RANGES = {
    "healthy": (60, 100),
    "warning": (30, 60),
    "critical": (5, 30)
}

@dataclass
class TelemetryEvent:
    timestamp: str
    service_id: str
    status: Literal["healthy", "warning", "critical"]
    latency_ms: int
    error_rate: float
    traffic_volume: int
    message: str
    metadata: dict

    def to_json(self) -> str:
        return json.dumps(asdict(self))

    def to_dict(self) -> dict:
        return asdict(self)


class ChaosEngine:
    """Generates simulated telemetry events for NEXUS PROTOCOL"""
    
    def __init__(self):
        self.mode = "steady_state"
        self.service_states = {s["id"]: "healthy" for s in SERVICES}
        self.running = False
        self.events_per_second = 10
        self.kafka_producer = None
        
    def set_mode(self, mode: str):
        """Change the chaos mode"""
        valid_modes = ["steady_state", "latency_spike", "cascading_failure", "recovery"]
        if mode not in valid_modes:
            raise ValueError(f"Invalid mode. Choose from: {valid_modes}")
        
        print(f"🔄 Switching mode: {self.mode} → {mode}")
        self.mode = mode
        
        if mode == "steady_state":
            self.service_states = {s["id"]: "healthy" for s in SERVICES}
        elif mode == "latency_spike":
            self.service_states["ai-brain"] = "critical"
        elif mode == "cascading_failure":
            self._trigger_cascade()
        elif mode == "recovery":
            self._begin_recovery()
    
    def _trigger_cascade(self):
        """Simulate cascading failure: ai-brain → payment → auth"""
        self.service_states["ai-brain"] = "critical"
        self.service_states["payment"] = "warning"
        # After 2 seconds, escalate
        asyncio.get_event_loop().call_later(2, self._escalate_cascade)
    
    def _escalate_cascade(self):
        """Escalate cascade to more services"""
        if self.mode == "cascading_failure":
            self.service_states["payment"] = "critical"
            self.service_states["auth"] = "warning"
            asyncio.get_event_loop().call_later(2, self._final_cascade)
    
    def _final_cascade(self):
        """Final stage of cascade"""
        if self.mode == "cascading_failure":
            self.service_states["auth"] = "critical"
            self.service_states["database"] = "warning"
    
    def _begin_recovery(self):
        """Gradually recover all services"""
        for service_id in self.service_states:
            if self.service_states[service_id] == "critical":
                self.service_states[service_id] = "warning"
        asyncio.get_event_loop().call_later(2, self._complete_recovery)
    
    def _complete_recovery(self):
        """Complete recovery to healthy state"""
        if self.mode == "recovery":
            self.service_states = {s["id"]: "healthy" for s in SERVICES}
            self.mode = "steady_state"
            print("✅ Recovery complete - all services healthy")
    
    def generate_event(self, service_id: str) -> TelemetryEvent:
        """Generate a single telemetry event for a service"""
        status = self.service_states.get(service_id, "healthy")
        
        # Add some randomness - occasional blips
        if status == "healthy" and random.random() < 0.05:
            status = "warning"
        
        latency_range = LATENCY_RANGES[status]
        error_range = ERROR_RATE_RANGES[status]
        traffic_range = TRAFFIC_VOLUME_RANGES[status]
        
        latency_ms = random.randint(*latency_range)
        error_rate = round(random.uniform(*error_range), 4)
        traffic_volume = random.randint(*traffic_range)
        
        # Generate contextual message
        messages = {
            "healthy": [
                "Operating within normal parameters",
                "All systems nominal",
                "Request processed successfully",
                "Connection stable"
            ],
            "warning": [
                "Elevated latency detected",
                "Increased error rate observed",
                "Resource utilization above threshold",
                "Retry attempts increasing"
            ],
            "critical": [
                "Service degradation severe",
                "Multiple timeouts detected",
                "Circuit breaker triggered",
                "Failover initiated"
            ]
        }
        
        message = random.choice(messages[status])
        
        # Add metadata based on service
        metadata = {
            "node_id": f"{service_id}-node-{random.randint(1, 3)}",
            "region": random.choice(["us-east-1", "us-west-2", "eu-west-1"]),
            "version": "v2.1.0"
        }
        
        if service_id == "ai-brain":
            metadata["model"] = "gemini-2.0-flash"
            metadata["tokens_in"] = random.randint(100, 500)
            metadata["tokens_out"] = random.randint(50, 200)
        
        return TelemetryEvent(
            timestamp=datetime.now(timezone.utc).isoformat(),
            service_id=service_id,
            status=status,
            latency_ms=latency_ms,
            error_rate=error_rate,
            traffic_volume=traffic_volume,
            message=message,
            metadata=metadata
        )
    
    async def generate_events(self):
        """Generate events for all services"""
        events = []
        for service in SERVICES:
            event = self.generate_event(service["id"])
            events.append(event)
        return events
    
    async def run(self, callback=None):
        """Main loop - generates events at configured rate"""
        self.running = True
        interval = 1.0 / self.events_per_second
        
        print(f"🚀 Chaos Engine started - Mode: {self.mode}")
        print(f"   Generating {self.events_per_second} events/second")
        
        while self.running:
            try:
                # Generate events for all services
                events = await self.generate_events()
                
                for event in events:
                    if callback:
                        await callback(event)
                    else:
                        # Default: print to console
                        status_emoji = {"healthy": "🟢", "warning": "🟡", "critical": "🔴"}
                        print(f"{status_emoji[event.status]} [{event.service_id}] "
                              f"Latency: {event.latency_ms}ms | Error: {event.error_rate:.2%} | "
                              f"{event.message}")
                
                await asyncio.sleep(interval)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"❌ Error generating events: {e}")
                await asyncio.sleep(1)
        
        print("⏹️ Chaos Engine stopped")
    
    def stop(self):
        """Stop the chaos engine"""
        self.running = False


# Kafka Producer Integration
async def create_kafka_callback(producer, topic: str):
    """Create a callback that sends events to Kafka"""
    async def send_to_kafka(event: TelemetryEvent):
        try:
            producer.produce(
                topic,
                key=event.service_id.encode('utf-8'),
                value=event.to_json().encode('utf-8')
            )
            producer.poll(0)  # Trigger callbacks
        except Exception as e:
            print(f"❌ Kafka send error: {e}")
    
    return send_to_kafka


async def main():
    """Demo mode - run chaos engine with console output"""
    engine = ChaosEngine()
    
    # Demo sequence
    async def demo_sequence():
        await asyncio.sleep(5)
        print("\n" + "="*50)
        print("🎬 DEMO: Triggering latency spike on ai-brain...")
        print("="*50 + "\n")
        engine.set_mode("latency_spike")
        
        await asyncio.sleep(10)
        print("\n" + "="*50)
        print("🎬 DEMO: Triggering cascading failure...")
        print("="*50 + "\n")
        engine.set_mode("cascading_failure")
        
        await asyncio.sleep(15)
        print("\n" + "="*50)
        print("🎬 DEMO: Initiating recovery...")
        print("="*50 + "\n")
        engine.set_mode("recovery")
    
    # Run both concurrently
    await asyncio.gather(
        engine.run(),
        demo_sequence()
    )


if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║           NEXUS PROTOCOL - CHAOS ENGINE                   ║
    ║                                                           ║
    ║   Generating simulated telemetry for observability demo  ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Chaos Engine shutdown requested")
