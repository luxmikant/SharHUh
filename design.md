# 🌌 NEXUS PROTOCOL - SINGLE SOURCE OF TRUTH
**Version 1.0 | Last Updated: December 26, 2025**

***

## 📖 TABLE OF CONTENTS
1. [Project Overview](#1-project-overview)
2. [System Architecture](#2-system-architecture)
3. [Component Specifications](#3-component-specifications)
4. [Feature Specifications](#4-feature-specifications)
5. [Data Schemas](#5-data-schemas)
6. [API Specifications](#6-api-specifications)
7. [Observability Strategy](#7-observability-strategy)
8. [Tech Stack](#8-tech-stack)
9. [Development Roadmap](#9-development-roadmap)
10. [Risk Mitigation](#10-risk-mitigation)
11. [Deployment](#11-deployment)
12. [Demo Script](#12-demo-script)

***

## 1. PROJECT OVERVIEW

### 1.1 Elevator Pitch
**NEXUS PROTOCOL** transforms abstract server metrics into a 3D cyberpunk holodeck where observability becomes visible, audible, and interactive. Instead of reading logs, you watch a digital core pulse with light. When systems fail, buildings glitch, voices alert you, and you can fix problems by clicking in 3D space.

### 1.2 The Problem
- LLM developers struggle to debug multi-agent systems in real-time
- Traditional dashboards are 2D, overwhelming, and disconnected from user experience
- Engineers don't know WHICH service is failing or HOW failures cascade
- Observability is reactive (alerts after problems) not experiential

### 1.3 The Solution
A 3D visualization platform where:
- **Each service = a glowing monolith** in a circular cluster
- **Datadog metrics = visual states** (color, glitch effects, particle flow)
- **Gemini AI = root cause analyst** generating sci-fi explanations
- **ElevenLabs = system voice** narrating alerts in real-time
- **Confluent = data nervous system** streaming all telemetry

### 1.4 Target Audience
- **Primary:** AI/ML engineers building LLM applications
- **Secondary:** DevOps/SRE teams seeking better incident visualization
- **Tertiary:** Tech educators teaching distributed systems

### 1.5 Success Metrics
- Judges can understand system health in < 5 seconds by looking at 3D scene
- Detection rules trigger visible/audible feedback within 2 seconds
- "Fix" action resolves visual corruption within 5 seconds
- Demo video is memorable and sharable

***

## 2. SYSTEM ARCHITECTURE

### 2.1 High-Level Architecture
```
┌─────────────────────────────────────────────────────────────────┐
│                      CHAOS ENGINE (Simulator)                    │
│  Generates fake traffic, latency spikes, cascading failures     │
└────────────────┬────────────────────────────────────────────────┘
                 │ Produces events
                 ▼
┌─────────────────────────────────────────────────────────────────┐
│              CONFLUENT KAFKA (Data Nervous System)               │
│  Topic: nexus-telemetry | Partitions: 3 | Retention: 1 hour    │
└────────────────┬────────────────────────────────────────────────┘
                 │ Consumes events
                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                   BACKEND (FastAPI + Python)                     │
│  ┌──────────────┬──────────────┬──────────────┬───────────────┐ │
│  │ Kafka        │ State        │ Datadog      │ WebSocket     │ │
│  │ Consumer     │ Manager      │ Client       │ Manager       │ │
│  └──────────────┴──────────────┴──────────────┴───────────────┘ │
│  ┌──────────────┬──────────────┐                                │
│  │ Gemini       │ ElevenLabs   │                                │
│  │ Client       │ Client       │                                │
│  └──────────────┴──────────────┘                                │
└────────────────┬────────────────────────────────────────────────┘
                 │ WebSocket stream
                 ▼
┌─────────────────────────────────────────────────────────────────┐
│              FRONTEND (React + Three.js + Vite)                  │
│  ┌──────────────┬──────────────┬──────────────┬───────────────┐ │
│  │ 3D Scene     │ Monolith     │ Particle     │ HUD           │ │
│  │ Manager      │ Components   │ System       │ Overlay       │ │
│  └──────────────┴──────────────┴──────────────┴───────────────┘ │
│  ┌──────────────┬──────────────┐                                │
│  │ Audio        │ Modal        │                                │
│  │ Player       │ Manager      │                                │
│  └──────────────┴──────────────┘                                │
└────────────────┬────────────────────────────────────────────────┘
                 │ RUM events
                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                   DATADOG CLOUD (Observability)                  │
│  APM | Metrics | Logs | RUM | Monitors | Dashboards | Incidents │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Data Flow
```
1. Chaos Engine → Kafka (telemetry events)
2. Backend consumes Kafka → Updates state
3. Backend → Datadog (metrics, traces, logs)
4. Backend → Gemini (error analysis)
5. Backend → ElevenLabs (voice generation)
6. Backend → Frontend (WebSocket state updates)
7. Frontend → Datadog (RUM performance data)
8. Datadog Monitor → Backend Webhook (incident alerts)
9. Backend → Frontend (alert notifications)
10. User clicks "Fix" → Backend → Chaos Engine (remediation)
```

### 2.3 Technology Choices
| Layer | Technology | Reasoning |
|-------|-----------|-----------|
| **Simulation** | Python Script | Simple, controllable, no dependencies |
| **Streaming** | Confluent Kafka | Required partner, handles high throughput |
| **Backend** | FastAPI (Python) | Async support, fast dev, good docs |
| **Frontend** | React + Vite | Industry standard, fast HMR |
| **3D Engine** | Three.js + R3F | Most examples, lightest bundle |
| **Styling** | Tailwind CSS | Rapid iteration, no JS overhead |
| **Observability** | Datadog APM/RUM | Required partner, best-in-class |
| **AI** | Vertex AI (Gemini) | Required partner, Gemini 2.0 Flash |
| **Voice** | ElevenLabs API | Required partner, low latency |
| **State** | In-memory (Python dict) | Fast, simple, no DB overhead |
| **Deployment** | Google Cloud Run | Serverless, auto-scaling, free tier |

***

## 3. COMPONENT SPECIFICATIONS

### 3.1 Chaos Engine (Simulator)

**Purpose:** Generates realistic traffic patterns and failure scenarios for demo

**Tech:** Python 3.10+

**Location:** `chaos_engine/main.py`

**Modes:**
1. **Steady State** (Default)
   - Frequency: 10 events/second
   - Latency: 200-800ms (normal distribution)
   - Error rate: 1-2%
   - Duration: Continuous

2. **Latency Spike** (Triggered at demo T+60s)
   - Target: `ai-brain` service
   - Latency: 4000-6000ms
   - Error rate: 5%
   - Duration: 30 seconds
   - Expected: Datadog monitor fires after 2 minutes

3. **Cascading Failure** (Triggered at demo T+120s)
   - Sequence:
     - T+0s: `database` error_rate → 80%
     - T+10s: `ai-brain` latency → 5000ms (depends on DB)
     - T+20s: `gateway` error_rate → 50% (all deps failing)
   - Duration: 60 seconds
   - Expected: 3 monitors fire, voice says "Cascading failure detected"

4. **Recovery** (Triggered by user "Apply Fix")
   - All services return to Steady State over 5 seconds (gradual)
   - Expected: Green glow returns, voice says "Metrics normalizing"

**Configuration:**
```python
SERVICES = [
    {"id": "gateway", "position": (0, 0, 0)},
    {"id": "auth", "position": (5, 0, 0)},
    {"id": "payment", "position": (2.5, 0, 4.33)},
    {"id": "ai-brain", "position": (-2.5, 0, 4.33)},
    {"id": "database", "position": (-5, 0, 0)}
]

LATENCY_RANGES = {
    "healthy": (200, 800),
    "degraded": (800, 2000),
    "critical": (3000, 6000)
}

ERROR_RATE_RANGES = {
    "healthy": (0.01, 0.03),
    "degraded": (0.03, 0.10),
    "critical": (0.15, 0.80)
}
```

**Output Schema:** See Section 5.1

***

### 3.2 Backend (FastAPI Server)

**Purpose:** Central coordinator consuming Kafka, managing state, sending to Datadog/frontend

**Tech:** FastAPI 0.108+, Python 3.10+

**Location:** `backend/`

**Folder Structure:**
```
backend/
├── main.py                 # FastAPI app entrypoint
├── kafka_consumer.py       # Consumes from Confluent
├── state.py                # In-memory state management
├── datadog_client.py       # Sends metrics/traces/logs
├── gemini_client.py        # Calls Vertex AI for analysis
├── elevenlabs_client.py    # Generates voice alerts
├── websocket_manager.py    # Manages WS connections
├── models.py               # Pydantic schemas
├── config.py               # Environment variables
├── requirements.txt
└── .env.example
```

**Key Endpoints:**

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/api/health` | Health check (all services status) |
| GET | `/api/state` | Current system state (services + integrity) |
| GET | `/api/metrics/recent` | Last 100 events from memory |
| POST | `/api/remediate` | Apply fix action to service |
| POST | `/api/datadog/webhook` | Receive Datadog monitor alerts |
| WS | `/ws/nexus` | Real-time state updates |

**Environment Variables:**
```bash
# Confluent
KAFKA_BOOTSTRAP_SERVERS=pkc-xxxxx.us-east-1.aws.confluent.cloud:9092
KAFKA_SASL_USERNAME=XXXXX
KAFKA_SASL_PASSWORD=XXXXX
KAFKA_TOPIC=nexus-telemetry

# Datadog
DD_API_KEY=xxxxx
DD_APP_KEY=xxxxx
DD_SITE=datadoghq.com
DD_SERVICE=nexus-backend
DD_ENV=production

# Google Cloud (Vertex AI)
GOOGLE_PROJECT_ID=nexus-protocol
GOOGLE_LOCATION=us-central1
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json

# ElevenLabs
ELEVENLABS_API_KEY=xxxxx
ELEVENLABS_VOICE_ID=xxxxx  # The "computer" voice

# App Config
PORT=8000
LOG_LEVEL=INFO
CORS_ORIGINS=http://localhost:5173,https://nexus-protocol.dev
```

**Dependencies:**
```txt
fastapi==0.108.0
uvicorn[standard]==0.25.0
websockets==12.0
confluent-kafka==2.3.0
datadog==0.48.0
ddtrace==2.5.0
google-cloud-aiplatform==1.38.0
requests==2.31.0
python-dotenv==1.0.0
pydantic==2.5.0
```

***

### 3.3 Frontend (React + Three.js)

**Purpose:** 3D visualization of system state with interactive controls

**Tech:** React 18, Vite 5, Three.js 0.160, React Three Fiber 8

**Location:** `frontend/`

**Folder Structure:**
```
frontend/
├── src/
│   ├── components/
│   │   ├── NexusScene.jsx       # Main 3D scene container
│   │   ├── Monolith.jsx         # Individual service monolith
│   │   ├── ParticleStream.jsx   # Data flow visualization
│   │   ├── HUD.jsx              # Heads-up display overlay
│   │   ├── IncidentModal.jsx    # Alert detail modal
│   │   └── RemediationPanel.jsx # Fix action controls
│   ├── hooks/
│   │   ├── useWebSocket.js      # WS connection manager
│   │   ├── useAudioPlayer.js    # Voice alert player
│   │   └── useDatadogRUM.js     # RUM initialization
│   ├── utils/
│   │   ├── colorMapping.js      # Status → color conversion
│   │   └── positionCalculator.js # Service positioning
│   ├── shaders/
│   │   └── glitchShader.js      # Corruption effect
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
├── public/
│   └── audio/                   # Pre-generated voice clips
│       ├── welcome.mp3
│       ├── alert_latency.mp3
│       ├── alert_cascading.mp3
│       ├── repair_success.mp3
│       └── system_healthy.mp3
├── package.json
├── vite.config.js
└── tailwind.config.js
```

**Dependencies:**
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "three": "^0.160.0",
    "@react-three/fiber": "^8.15.0",
    "@react-three/drei": "^9.92.0",
    "@react-three/postprocessing": "^2.16.0",
    "zustand": "^4.4.7"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.2.1",
    "vite": "^5.0.8",
    "tailwindcss": "^3.4.0",
    "autoprefixer": "^10.4.16",
    "postcss": "^8.4.32"
  }
}
```

**Component Specifications:**

**Monolith Component:**
```jsx
<Monolith 
  position={[x, y, z]}
  data={{
    service_id: "ai-brain",
    status: "critical",      // healthy, warning, critical
    latency_ms: 4500,
    error_rate: 0.15,
    particle_count: 85
  }}
  onClick={handleClick}
/>
```

**Visual States:**
| Status | Color | Emissive | Effect | Animation |
|--------|-------|----------|--------|-----------|
| healthy | #00ff00 | 0.5 | None | Slow pulse (2s) |
| warning | #ffaa00 | 0.8 | Slight flicker | Fast pulse (0.5s) |
| critical | #ff0000 | 1.0 | Glitch shader | Strobe (0.2s) |

***

### 3.4 Datadog Integration

**Purpose:** Store all telemetry, detect anomalies, trigger alerts

**Components:**
1. **APM (Application Performance Monitoring)**
   - Traces every request through backend
   - Spans: Kafka consume, Gemini call, ElevenLabs call, WS broadcast

2. **Metrics**
   - Custom StatsD metrics (see Section 7.1)
   - System metrics (CPU, memory, network)

3. **Logs**
   - Structured JSON logs from backend
   - Enriched with trace_id for correlation

4. **RUM (Real User Monitoring)**
   - Frontend 3D performance (FPS, frame time)
   - User interactions (clicks, remediations)

5. **Monitors**
   - Detection rules (see Section 7.2)
   - Webhook to backend on trigger

6. **Dashboards**
   - System Overview (see Section 7.3)
   - LLM Deep Dive (see Section 7.3)

***

### 3.5 Gemini Integration (Vertex AI)

**Purpose:** Generate sci-fi root cause analysis for incidents

**Model:** `gemini-2.0-flash-exp` (fast, cost-effective)

**Prompt Template:**
```python
SYSTEM_PROMPT = """You are NEXUS, a Starfleet-class observability AI. 
You analyze system failures and provide concise, technical explanations 
using sci-fi terminology. Keep responses under 20 words.

Examples:
- "Subspace interference in neural pathways causing token overflow"
- "Quantum decoherence detected in authentication matrix"
- "Cascading resonance failure across data substrates"
"""

USER_PROMPT_TEMPLATE = """
Service: {service_id}
Status: {status}
Latency: {latency_ms}ms
Error Rate: {error_rate}%
Recent Errors: {error_messages}

Provide a brief, sci-fi explanation of the root cause.
"""
```

**Integration:**
```python
from google.cloud import aiplatform

def analyze_incident(service_data: dict) -> str:
    prompt = USER_PROMPT_TEMPLATE.format(**service_data)
    
    response = aiplatform.gapic.PredictionServiceClient().predict(
        endpoint=f"projects/{PROJECT}/locations/{LOCATION}/publishers/google/models/gemini-2.0-flash-exp",
        instances=[{"content": prompt}],
        parameters={"temperature": 0.7, "maxOutputTokens": 50}
    )
    
    return response.predictions[0]["content"]
```

**Rate Limits:**
- 60 requests/minute (free tier)
- Mitigation: Cache common failures, use pre-generated responses as fallback

***

### 3.6 ElevenLabs Integration

**Purpose:** Convert Gemini analysis to voice alerts

**Voice:** Professional female AI voice (similar to Star Trek computer)

**API Endpoint:** `https://api.elevenlabs.io/v1/text-to-speech/{voice_id}`

**Implementation:**
```python
import requests

def generate_voice_alert(text: str) -> str:
    """Returns URL to audio file"""
    
    response = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}",
        headers={"xi-api-key": ELEVENLABS_API_KEY},
        json={
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75
            }
        }
    )
    
    # Save to public/audio/
    audio_path = f"audio/alert_{uuid.uuid4()}.mp3"
    with open(f"frontend/public/{audio_path}", "wb") as f:
        f.write(response.content)
    
    return f"/{audio_path}"
```

**Pre-generated Clips (Fallback):**
1. `welcome.mp3` - "Welcome, Engineer. Colony status operational."
2. `alert_latency.mp3` - "Warning: High latency detected."
3. `alert_cascading.mp3` - "Critical alert: Cascading failure suspected."
4. `repair_success.mp3` - "Repair successful. Metrics normalizing."
5. `system_healthy.mp3` - "System integrity restored to optimal levels."

***

## 4. FEATURE SPECIFICATIONS

### 4.1 Core Features (MVP - Must Have)

**F1: Real-Time 3D Visualization**
- 5 monoliths in circular formation
- Color changes based on status (green/yellow/red)
- Smooth transitions (0.5s fade)
- 60 FPS minimum on standard laptop

**F2: Live Metric Streaming**
- WebSocket connection to backend
- Updates every 2 seconds
- Graceful reconnection on disconnect
- Shows connection status in HUD

**F3: Click Interaction**
- Click monolith → open modal with details
- Modal shows: service ID, latency, error rate, recent errors
- Embed Datadog APM trace (iframe)
- "Apply Fix" button triggers remediation

**F4: Voice Alerts**
- Auto-play when critical alert fires
- Volume control in HUD
- Mute toggle
- Fallback to text if audio fails

**F5: System Integrity Display**
- HUD shows percentage (0-100%)
- Calculated from: (healthy_services / total_services) × 100
- Updates in real-time
- Color-coded (green >80%, yellow 50-80%, red <50%)

**F6: Datadog Integration**
- All metrics sent to Datadog
- APM traces for backend requests
- RUM tracking for frontend
- Monitors configured and firing
- Dashboard accessible via link

***

### 4.2 Enhanced Features (Nice to Have)

**F7: Particle Flow Visualization**
- Glowing dots flow from gateway to other services
- Speed = throughput
- Count = traffic_volume
- Color = cyan (#00ffff)

**F8: Glitch Shader Effect**
- Applied when status = critical
- Mesh distortion + chromatic aberration
- Intensity increases with error_rate

**F9: Post-Processing Effects**
- Bloom (neon glow)
- Vignette (dark edges)
- Film grain (subtle)
- Toggle for performance

**F10: LCARS-Style UI**
- Star Trek inspired header
- Orange/purple color scheme
- Rounded corners
- Okuda font (if available)

**F11: Incident Timeline**
- Scrolling list of past alerts
- Shows time, service, status, resolution
- Click to see details
- Last 10 incidents visible

**F12: Chaos Mode Controls**
- Manual trigger buttons for demo
- "Steady State" / "Latency Spike" / "Cascading Failure"
- Visible only in dev mode
- Keyboard shortcuts (Ctrl+1/2/3)

***

### 4.3 Stretch Features (Only if Ahead of Schedule)

**F13: ksqlDB Integration**
- Rolling average calculations
- Anomaly detection queries
- Stream-table joins
- Real-time aggregations

**F14: MCP Server Endpoint**
- Expose `/mcp` endpoint
- Tools: get_system_status, apply_remediation, query_metrics
- Claude integration demo

**F15: Dark/Light Mode Toggle**
- Switch between cyberpunk (dark) and clean (light)
- Persist preference in localStorage

***

## 5. DATA SCHEMAS

### 5.1 Kafka Message Schema (nexus-telemetry topic)

```json
{
  "timestamp": "2025-12-26T10:00:00.123Z",
  "service_id": "ai-brain",
  "status": "critical",
  "latency_ms": 4500,
  "error_rate": 0.15,
  "traffic_volume": 85,
  "message": "Timeout waiting for vector DB response",
  "metadata": {
    "chaos_mode": "latency_spike",
    "region": "us-central1",
    "version": "1.2.3"
  }
}
```

**Field Definitions:**
| Field | Type | Values | Purpose |
|-------|------|--------|---------|
| timestamp | ISO 8601 string | Any valid datetime | Event occurrence time |
| service_id | string | gateway, auth, payment, ai-brain, database | Service identifier |
| status | enum | healthy, warning, critical | Overall health status |
| latency_ms | integer | 0-10000 | Response time in milliseconds |
| error_rate | float | 0.0-1.0 | Percentage of failed requests |
| traffic_volume | integer | 0-100 | Relative request count |
| message | string | Any | Human-readable description |
| metadata | object | Key-value pairs | Additional context |

***

### 5.2 WebSocket Message Schema (Backend → Frontend)

**Message Type 1: State Update**
```json
{
  "type": "state_update",
  "timestamp": "2025-12-26T10:00:00.123Z",
  "system_integrity": 73,
  "services": [
    {
      "service_id": "gateway",
      "position": {"x": 0, "y": 0, "z": 0},
      "status": "healthy",
      "latency_ms": 120,
      "error_rate": 0.01,
      "particle_count": 50
    }
    // ...4 more services
  ]
}
```

**Message Type 2: Alert**
```json
{
  "type": "alert",
  "severity": "critical",
  "service_id": "ai-brain",
  "message": "Latency spike detected",
  "voice_url": "/audio/alert_12345.mp3",
  "analysis": "Subspace interference in neural pathway",
  "trace_id": "dd-trace-abc123",
  "datadog_url": "https://app.datadoghq.com/apm/trace/abc123"
}
```

**Message Type 3: Remediation Result**
```json
{
  "type": "remediation_result",
  "service_id": "ai-brain",
  "action": "reset_context",
  "success": true,
  "new_status": "healthy",
  "message": "Context reset successful. Latency reduced to 850ms."
}
```

***

### 5.3 API Request/Response Schemas

**POST /api/remediate**
```json
// Request
{
  "service_id": "ai-brain",
  "action": "reset_context"
}

// Response
{
  "success": true,
  "service_id": "ai-brain",
  "action": "reset_context",
  "previous_status": "critical",
  "new_status": "healthy",
  "message": "Remediation applied successfully"
}
```

**GET /api/state**
```json
// Response
{
  "timestamp": "2025-12-26T10:00:00.123Z",
  "system_integrity": 73,
  "services": [...],  // Same as WebSocket state_update
  "active_incidents": 2,
  "uptime_seconds": 3600
}
```

***

## 6. API SPECIFICATIONS

### 6.1 Backend REST API

**Base URL:** `http://localhost:8000` (dev) | `https://api.nexus-protocol.dev` (prod)

**Authentication:** None (hackathon demo)

**Endpoints:**

| Method | Path | Request | Response | Status Codes |
|--------|------|---------|----------|--------------|
| GET | `/api/health` | None | `{"status": "healthy", "services": {...}}` | 200, 503 |
| GET | `/api/state` | None | Current system state | 200 |
| GET | `/api/metrics/recent` | `?limit=100` | Array of events | 200 |
| POST | `/api/remediate` | `{service_id, action}` | Remediation result | 200, 400, 500 |
| POST | `/api/datadog/webhook` | Datadog payload | `{"received": true}` | 200 |
| WS | `/ws/nexus` | WebSocket upgrade | Bidirectional stream | 101 |

***

### 6.2 WebSocket Protocol

**Connection:** `ws://localhost:8000/ws/nexus`

**Client → Server Messages:** None (receive-only for MVP)

**Server → Client Messages:**
- `state_update` every 2 seconds
- `alert` when Datadog monitor fires
- `remediation_result` after fix applied

**Reconnection Logic:**
```javascript
let reconnectAttempts = 0;
const maxReconnectAttempts = 5;

ws.onclose = () => {
  if (reconnectAttempts < maxReconnectAttempts) {
    setTimeout(() => {
      reconnectAttempts++;
      connectWebSocket();
    }, 2000 * reconnectAttempts); // Exponential backoff
  }
};
```

***

## 7. OBSERVABILITY STRATEGY

### 7.1 Datadog Metrics (Custom StatsD)

**All metrics prefixed with `nexus.`**

| Metric Name | Type | Tags | Unit | Purpose |
|-------------|------|------|------|---------|
| `nexus.service.latency` | Gauge | service_id, status | ms | Response time per service |
| `nexus.service.error_rate` | Gauge | service_id | % | Failed requests percentage |
| `nexus.service.throughput` | Counter | service_id | req/s | Requests per second |
| `nexus.llm.tokens.input` | Gauge | service_id, model | count | Gemini input tokens |
| `nexus.llm.tokens.output` | Gauge | service_id, model | count | Gemini output tokens |
| `nexus.llm.latency` | Histogram | service_id, model | ms | Gemini API call duration |
| `nexus.llm.cost` | Gauge | service_id | USD | Calculated cost per request |
| `nexus.frontend.fps` | Gauge | browser, device | fps | 3D render performance |
| `nexus.kafka.lag` | Gauge | consumer_group | messages | Consumer lag |
| `nexus.websocket.connections` | Gauge | - | count | Active WS connections |
| `nexus.system.integrity` | Gauge | - | % | Overall health score |
| `nexus.remediation.count` | Counter | service_id, action | count | Fixes applied |

**Code Example:**
```python
from datadog import statsd

# Service metrics
statsd.gauge('nexus.service.latency', event['latency_ms'], 
             tags=[f"service:{event['service_id']}", f"status:{event['status']}"])

# LLM metrics
statsd.gauge('nexus.llm.tokens.input', gemini_response.usage.input_tokens,
             tags=[f"service:ai-brain", f"model:gemini-2.0-flash"])

# Frontend metrics (from RUM)
datadogRum.addAction('fps_sample', {fps: currentFps, frameTime: frameTime})
```

***

### 7.2 Datadog Detection Rules (Monitors)

**Monitor 1: Service Latency Spike**
```yaml
Name: "Nexus: High Service Latency"
Type: Metric
Query: avg(last_2m):avg:nexus.service.latency{*} by {service_id} > 2000
Alert Threshold: 2000ms
Warning Threshold: 1000ms
Message: |
  Service {{service_id.name}} latency is {{value}}ms (threshold: 2000ms)
  
  @webhook-nexus-backend
  
  Trace: {{trace_id}}
Tags: severity:p2, team:platform
```

**Monitor 2: Cascading Failure**
```yaml
Name: "Nexus: Cascading Failure Detected"
Type: Composite
Logic: (monitor_1 AND monitor_4) OR (3 service monitors in critical)
Message: |
  CRITICAL: Multiple services failing simultaneously
  
  @webhook-nexus-backend
  @pagerduty-critical
  
  Investigate immediately
Tags: severity:p1, team:platform
```

**Monitor 3: LLM Cost Spike**
```yaml
Name: "Nexus: LLM Cost Budget Exceeded"
Type: Metric
Query: sum(last_1h):sum:nexus.llm.cost{*} > 5
Alert Threshold: $5/hour
Message: |
  LLM costs exceeded $5 in the last hour
  
  Consider throttling AI analysis or caching responses
Tags: severity:p3, team:ml
```

**Monitor 4: Frontend Performance Degradation**
```yaml
Name: "Nexus: Low FPS Detected"
Type: Metric
Query: avg(last_1m):avg:nexus.frontend.fps{*} < 30
Alert Threshold: 30 fps
Warning Threshold: 45 fps
Message: |
  3D performance degraded: {{value}} FPS
  
  Consider reducing particle count or disabling post-processing
Tags: severity:p3, team:frontend
```

***

### 7.3 Datadog Dashboards

**Dashboard 1: System Overview**

**Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│ NEXUS PROTOCOL - SYSTEM OVERVIEW                            │
│                                                              │
│ System Integrity: [███████░░░] 73%   Active Incidents: 2   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│ ┌─────────────┬─────────────┬─────────────┬──────────────┐ │
│ │ Gateway     │ Auth        │ Payment     │ AI-Brain     │ │
│ │ Latency:    │ Latency:    │ Latency:    │ Latency:     │ │
│ │ [GRAPH]     │ [GRAPH]     │ [GRAPH]     │ [GRAPH]      │ │
│ └─────────────┴─────────────┴─────────────┴──────────────┘ │
│                                                              │
│ ┌────────────────────────────────────────────────────────┐  │
│ │ Error Rate Heatmap (by service)                       │  │
│ │ [HEATMAP: service_id × time]                          │  │
│ └────────────────────────────────────────────────────────┘  │
│                                                              │
│ ┌────────────────────────────────────────────────────────┐  │
│ │ Live Incident Stream                                   │  │
│ │ • 14:52 - AI-Brain - P2 - High latency (4500ms)       │  │
│ │ • 14:50 - Database - P1 - Cascading failure           │  │
│ └────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

**Widgets:**
1. **Big Number:** System Integrity % (green/yellow/red conditional formatting)
2. **Big Number:** Active Incidents count
3. **Timeseries (×5):** Latency per service (last 15 minutes)
4. **Heatmap:** Error rate by service over time
5. **Timeseries:** Kafka consumer lag
6. **Query Value:** Average FPS (frontend)
7. **Event Stream:** Monitors firing/resolving

***

**Dashboard 2: LLM Deep Dive**

**Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│ NEXUS PROTOCOL - LLM OBSERVABILITY                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│ ┌─────────────────┬─────────────────┬─────────────────────┐ │
│ │ Token Usage/Hr  │ API Calls/Min   │ Cost/Hour           │ │
│ │ 125,430         │ 45              │ $2.30               │ │
│ └─────────────────┴─────────────────┴─────────────────────┘ │
│                                                              │
│ ┌────────────────────────────────────────────────────────┐  │
│ │ Gemini API Latency (P50, P95, P99)                     │  │
│ │ [TIMESERIES GRAPH]                                     │  │
│ └────────────────────────────────────────────────────────┘  │
│                                                              │
│ ┌────────────────────────────────────────────────────────┐  │
│ │ APM Trace Waterfall (Sample)                           │  │
│ │ [EMBEDDED APM TRACE]                                   │  │
│ │ kafka.consume ─┬─ datadog.send ──┬─ gemini.analyze    │  │
│ │                └─ websocket.send │                     │  │
│ └────────────────────────────────────────────────────────┘  │
│                                                              │
│ ┌────────────────────────────────────────────────────────┐  │
│ │ Cost Attribution (by service)                          │  │
│ │ [PIE CHART: ai-brain 65%, payment 20%, auth 15%]      │  │
│ └────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

***

### 7.4 Incident Workflow

**Step-by-Step:**
```
1. Datadog Monitor evaluates every 60 seconds
   ↓
2. Condition met (e.g., latency > 2000ms for 2 minutes)
   ↓
3. Monitor state: OK → ALERT
   ↓
4. Datadog creates Incident
   ↓
5. Webhook fires: POST https://api.nexus-protocol.dev/api/datadog/webhook
   ↓
6. Backend receives webhook:
   - Extracts service_id, severity, trace_id
   - Queries recent logs/errors for context
   - Calls Gemini: "Analyze this incident: {context}"
   ↓
7. Gemini returns: "Subspace interference in neural pathways"
   ↓
8. Backend calls ElevenLabs: text → audio
   ↓
9. Backend sends to Frontend via WebSocket:
   {
     "type": "alert",
     "service_id": "ai-brain",
     "analysis": "...",
     "voice_url": "/audio/alert_xyz.mp3",
     "trace_id": "..."
   }
   ↓
10. Frontend:
    - Plays voice alert
    - Highlights affected monolith (red + glitch shader)
    - Shows modal with Datadog APM trace embedded
    - Displays "Apply Fix" button
    ↓
11. User clicks "Apply Fix"
    ↓
12. Frontend: POST /api/remediate {service_id, action: "reset_context"}
    ↓
13. Backend:
    - Tells Chaos Engine to reduce latency
    - Logs remediation action to Datadog
    ↓
14. Chaos Engine reduces latency: 4500ms → 800ms
    ↓
15. Backend sends: {type: "remediation_result", success: true}
    ↓
16. Frontend:
    - Monolith fades red → yellow → green (5 seconds)
    - Plays "Repair successful" voice clip
    ↓
17. Datadog Monitor re-evaluates: latency now < 2000ms
    ↓
18. Monitor state: ALERT → OK
    ↓
19. Incident auto-resolves
```

***

## 8. TECH STACK

### 8.1 Complete Dependency List

**Backend (Python):**
```txt
fastapi==0.108.0
uvicorn[standard]==0.25.0
websockets==12.0
confluent-kafka==2.3.0
datadog==0.48.0
ddtrace==2.5.0
google-cloud-aiplatform==1.38.0
requests==2.31.0
python-dotenv==1.0.0
pydantic==2.5.0
aiohttp==3.9.1
```

**Frontend (Node.js):**
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "three": "^0.160.0",
    "@react-three/fiber": "^8.15.0",
    "@react-three/drei": "^9.92.0",
    "@react-three/postprocessing": "^2.16.0",
    "zustand": "^4.4.7"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.2.1",
    "vite": "^5.0.8",
    "tailwindcss": "^3.4.0",
    "autoprefixer": "^10.4.16",
    "postcss": "^8.4.32",
    "eslint": "^8.56.0"
  }
}
```

**Infrastructure:**
- **Confluent Cloud:** Kafka cluster (Standard tier)
- **Datadog:** Pro tier (14-day trial)
- **Google Cloud:** Vertex AI, Cloud Run, Cloud Storage
- **ElevenLabs:** Creator tier (free 10k characters/month)

***

### 8.2 Development Tools

| Category | Tool | Purpose |
|----------|------|---------|
| Code Editor | VS Code | Primary IDE |
| VS Code Extensions | Python, ESLint, Tailwind IntelliSense | Code quality |
| API Testing | Thunder Client | Test REST endpoints |
| WebSocket Testing | wscat | Test WS connections |
| Log Viewing | Datadog Live Tail | Real-time log streaming |
| 3D Debugging | R3F DevTools | Three.js scene inspection |
| Version Control | Git + GitHub | Source control |
| Container | Docker Desktop | Local Kafka (optional) |

***

## 9. DEVELOPMENT ROADMAP

### 9.1 Phase 1: Foundation (Days 1-3)

**Goal:** Data flowing end-to-end without frontend

**Day 1 Tasks:**
- [ ] Set up Confluent Cloud cluster
- [ ] Set up Datadog account + API keys
- [ ] Create project structure (backend/, chaos_engine/)
- [ ] Install dependencies
- [ ] Write Chaos Engine (Steady State mode only)
- [ ] Test: Events appear in Confluent UI

**Day 2 Tasks:**
- [ ] Build FastAPI backend skeleton
- [ ] Implement Kafka consumer
- [ ] Implement Datadog client (send 1 test metric)
- [ ] Test: Metric appears in Datadog Metrics Explorer
- [ ] Write state manager (in-memory)

**Day 3 Tasks:**
- [ ] Send all 8 metrics to Datadog
- [ ] Create 4 Datadog monitors
- [ ] Test: Manually trigger latency spike, monitor fires
- [ ] Implement WebSocket server (echo test)
- [ ] Commit: Phase 1 complete

**Milestone:** Backend running, Datadog receiving metrics, monitors configured

***

### 9.2 Phase 2: Visuals (Days 4-7)

**Goal:** 3D scene showing real-time data

**Day 4 Tasks:**
- [ ] Initialize Vite + React project
- [ ] Install Three.js + R3F
- [ ] Create basic scene (5 cubes in circle)
- [ ] Add orbital camera controls
- [ ] Test: Can see and rotate scene

**Day 5 Tasks:**
- [ ] Build Monolith component
- [ ] Implement color mapping (status → color)
- [ ] Test: Manually change status, color updates
- [ ] Add emissive glow
- [ ] Add ground plane

**Day 6 Tasks:**
- [ ] Connect frontend to backend WebSocket
- [ ] Parse incoming messages
- [ ] Update monolith states in real-time
- [ ] Test: Run Chaos Engine, see colors change

**Day 7 Tasks:**
- [ ] Add click interaction (modal with details)
- [ ] Build HUD overlay (system integrity %)
- [ ] Add tooltip on hover
- [ ] Polish: smooth transitions, loading states
- [ ] Commit: Phase 2 complete

**Milestone:** 3D scene updating in real-time from backend

***

### 9.3 Phase 3: Intelligence (Days 8-10)

**Goal:** Voice alerts + AI analysis

**Day 8 Tasks:**
- [ ] Set up Vertex AI credentials
- [ ] Implement Gemini client
- [ ] Test: Send error log, get analysis
- [ ] Create Datadog webhook endpoint
- [ ] Test: Trigger monitor, webhook receives payload

**Day 9 Tasks:**
- [ ] Set up ElevenLabs account
- [ ] Pre-generate 5 voice clips (fallback)
- [ ] Implement live voice generation
- [ ] Test: Play audio in frontend
- [ ] Wire up: webhook → Gemini → ElevenLabs → WS → Frontend

**Day 10 Tasks:**
- [ ] Implement remediation API
- [ ] Connect "Apply Fix" button
- [ ] Test full incident loop
- [ ] Add Chaos Engine modes (Latency Spike, Cascading)
- [ ] Commit: Phase 3 complete

**Milestone:** Full incident workflow working (detect → voice → fix → resolve)

***

### 9.4 Phase 4: Polish & Demo (Days 11-14)

**Goal:** Ship-ready product

**Day 11 Tasks:**
- [ ] **FEATURE FREEZE** (no new features)
- [ ] Add glitch shader effect
- [ ] Add particle streams (optional)
- [ ] Add bloom post-processing
- [ ] Finalize Datadog dashboards

**Day 12 Tasks:**
- [ ] Write demo script (3 minutes)
- [ ] Record demo video (3-5 takes)
- [ ] Edit video (text overlays, music)
- [ ] Upload to YouTube
- [ ] Test backup pre-recorded clips

**Day 13 Tasks:**
- [ ] Write README.md (setup instructions)
- [ ] Create architecture diagram
- [ ] Document all metrics + detection rules
- [ ] Add MIT license
- [ ] Fill out Devpost form (90%)

**Day 14 Tasks:**
- [ ] Final testing (fresh browser, incognito)
- [ ] Deploy to Cloud Run (optional)
- [ ] Complete Devpost submission
- [ ] Submit before deadline
- [ ] Celebrate 🎉

**Milestone:** Submitted to hackathon

***

## 10. RISK MITIGATION

### 10.1 Risk Matrix

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| ElevenLabs API slow/down | Medium | High | Pre-generate 10 clips, use as fallback |
| Gemini rate limits | Medium | High | Cache 20 responses, cycle through |
| 3D scene lags | Medium | Medium | Quality toggle (Low Poly Mode) |
| Kafka connection fails | Low | High | Local Docker Kafka backup |
| Running out of time | High | High | Feature freeze Day 10, MVP by Day 8 |
| Demo day bugs | Medium | High | Pre-record video as backup |

***

### 10.2 Fallback Strategies

**If ElevenLabs Fails:**
```javascript
// frontend/src/hooks/useAudioPlayer.js
async function playAlert(voiceUrl) {
  try {
    await audio.load(voiceUrl);
    await audio.play();
  } catch (error) {
    // Fallback to pre-generated clip
    const fallback = '/audio/alert_latency.mp3';
    await audio.load(fallback);
    await audio.play();
  }
}
```

**If Gemini Fails:**
```python
# backend/gemini_client.py
FALLBACK_ANALYSES = [
    "Neural pathway congestion detected",
    "Quantum coherence failure in processing matrix",
    "Subspace communication lag exceeding tolerances",
    "Data substrate corruption identified",
    "Temporal synchronization error detected"
]

def analyze_incident(data):
    try:
        return call_gemini(data)
    except Exception as e:
        logger.warning(f"Gemini failed: {e}. Using fallback.")
        return random.choice(FALLBACK_ANALYSES)
```

**If 3D Performance Poor:**
```jsx
// Frontend performance monitor
useEffect(() => {
  if (avgFps < 30) {
    setQuality('low'); // Reduce particles, disable bloom
  }
}, [avgFps]);
```

***

### 10.3 Pre-Demo Checklist

**24 Hours Before Demo:**
- [ ] All environment variables backed up
- [ ] Pre-generated voice clips tested
- [ ] Demo video recorded and uploaded
- [ ] Backup laptop with project ready
- [ ] Internet connection tested (mobile hotspot ready)
- [ ] All accounts (Datadog, Confluent, etc.) login tested
- [ ] README instructions tested on fresh clone

**1 Hour Before Demo:**
- [ ] Start all services (backend, frontend, chaos engine)
- [ ] Verify Datadog dashboards loading
- [ ] Test full incident flow once
- [ ] Open demo video as backup
- [ ] Close unnecessary browser tabs
- [ ] Disable notifications
- [ ] Full battery charge

***

## 11. DEPLOYMENT

### 11.1 Local Development

**Prerequisites:**
- Python 3.10+
- Node.js 18+
- Git

**Setup:**
```bash
# Clone repo
git clone https://github.com/yourusername/nexus-protocol
cd nexus-protocol

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
python main.py

# Frontend setup (new terminal)
cd frontend
npm install
npm run dev

# Chaos Engine (new terminal)
cd chaos_engine
python main.py
```

**Accessing:**
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- Backend Docs: http://localhost:8000/docs

***

### 11.2 Cloud Deployment (Optional)

**Google Cloud Run (Backend):**
```bash
# Build container
gcloud builds submit --tag gcr.io/PROJECT_ID/nexus-backend

# Deploy
gcloud run deploy nexus-backend \
  --image gcr.io/PROJECT_ID/nexus-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars KAFKA_BOOTSTRAP_SERVERS=...,DD_API_KEY=...
```

**Vercel (Frontend):**
```bash
npm install -g vercel
cd frontend
vercel --prod
```

***

## 12. DEMO SCRIPT

### 12.1 Three-Minute Demo Script

**0:00-0:20 | THE HOOK**
```
Visual: Fade in to 3D holodeck, 5 glowing monoliths pulsing
Voiceover: "In 2385, Starfleet built an AI colony. Yesterday, it started glitching."
Action: Camera orbits around scene
NEXUS voice: "Welcome, Engineer. Colony status: 73% operational. 4 critical alerts detected."
```

**0:20-0:50 | THE PROBLEM**
```
Visual: Zoom to ai-brain monolith (red, glitching)
Voiceover: "When LLM systems fail, traditional dashboards show numbers. But what if you could SEE the corruption?"
Action: Click monolith → modal shows Datadog APM trace
Visual: Split screen - 3D scene + Datadog dashboard
NEXUS voice: "Critical alert: Latency spike detected in AI-Brain module."
```

**0:50-1:30 | THE SOLUTION**
```
Visual: Monolith glitching intensifies
Voiceover: "NEXUS Protocol uses Datadog to detect anomalies, Gemini to analyze them, and ElevenLabs to narrate them."
Action: Datadog monitor fires → webhook → backend processes
Visual: Show code snippet (webhook → Gemini → voice generation)
NEXUS voice: "Analysis complete: Subspace interference in neural pathways causing token overflow."
Visual: Voice waveform animates
```

**1:30-2:00 | THE FIX**
```
Visual: "Apply Remediation" button appears in modal
Voiceover: "And here's the magic: you can fix it from the 3D interface."
Action: Click button
Visual: Monolith color transitions red → yellow → green (5 seconds)
NEXUS voice: "Repair successful. Metrics normalizing."
Visual: Datadog dashboard shows latency dropping from 4500ms → 800ms
```

**2:00-2:30 | THE SCALE**
```
Visual: Camera pulls back, show all 5 monoliths + particle streams
Voiceover: "This is powered by Confluent Kafka, streaming 10,000 events per second."
Visual: Cascade demo - trigger 3 services to fail
NEXUS voice: "Warning: Cascading failure detected."
Visual: Multiple monoliths turn red in sequence
Action: Show detection rules in Datadog UI
```

**2:30-3:00 | THE PAYOFF**
```
Visual: All monoliths return to green, system integrity 98%
NEXUS voice: "System integrity restored to optimal levels. Well done, Engineer."
Visual: Fade to title card with:
  ✅ End-to-end LLM observability
  ✅ Real-time detection & remediation
  ✅ Multi-agent orchestration at scale
Action: Show GitHub QR code + "nexus-protocol.dev"
Voiceover: "Built with Google Cloud, Datadog, Confluent, and ElevenLabs."
```

***

### 12.2 Q&A Preparation

**Expected Judge Questions:**

**Q: "What happens to old incidents?"**
A: "They're stored in Datadog for long-term analysis. We can query up to 15 months of history via the API."

**Q: "How do you prevent false positives?"**
A: "We use rolling averages and require sustained thresholds (e.g., latency > 2s for 2 minutes, not just a single spike)."

**Q: "Can this work with real LLM applications?"**
A: "Absolutely. The instrumentation is the same whether data comes from our simulator or a production Gemini app. We'd just swap the Chaos Engine for real API calls."

**Q: "What's the cost to run this?"**
A: "With Datadog Pro trial, Confluent free tier, and Gemini Flash model, cost is ~$50/month for moderate traffic. We optimize by caching Gemini responses."

**Q: "How does this compare to Grafana/Prometheus?"**
A: "Those are excellent for traditional metrics. NEXUS adds spatial visualization, voice narration, and interactive remediation - making observability experiential, not just analytical."

***

## 13. SUCCESS CRITERIA

### 13.1 Minimum Viable Demo (Must Have)
- [ ] 5 monoliths visible, changing colors based on backend data
- [ ] WebSocket streaming working (updates every 2 seconds)
- [ ] Click interaction opens modal with service details
- [ ] At least 1 Datadog monitor firing and visible
- [ ] Voice alert plays (pre-recorded is acceptable)
- [ ] "Apply Fix" button triggers visual recovery
- [ ] 3-minute video uploaded to YouTube
- [ ] GitHub repo public with clear README

### 13.2 Winning Demo (Should Have)
- [ ] All 4 Datadog monitors configured and demonstrated
- [ ] Live Gemini integration (real-time analysis)
- [ ] Live ElevenLabs integration (generated voice)
- [ ] Glitch shader effect on critical services
- [ ] Particle streams showing traffic flow
- [ ] Full incident workflow (detect → analyze → voice → fix → resolve)
- [ ] Datadog dashboard with 8+ widgets
- [ ] Architecture diagram in README

### 13.3 Perfect Execution (Nice to Have)
- [ ] ksqlDB real-time processing demo
- [ ] Post-processing effects (bloom, vignette)
- [ ] LCARS-styled UI elements
- [ ] Deployed live demo URL
- [ ] MCP server endpoint working
- [ ] Blog post explaining technical approach

***

## 14. DOCUMENT CONTROL

**Version:** 1.0  
**Last Updated:** December 26, 2025, 4:28 PM IST  
**Author:** Nexus Protocol Team  
**Status:** Active  

**Change Log:**
- v1.0 (Dec 26, 2025): Initial comprehensive design document

**Next Review:** After Phase 1 completion (Day 3)

***

## 15. QUICK REFERENCE

### 15.1 Critical URLs
- **GitHub Repo:** https://github.com/yourusername/nexus-protocol
- **Devpost:** https://devpost.com/software/nexus-protocol
- **Demo Video:** https://youtu.be/YOUR_VIDEO_ID
- **Live Demo:** https://nexus-protocol.dev (optional)
- **Datadog Dashboard:** [Bookmark after creation]

### 15.2 Emergency Contacts
- **Datadog Support:** support@datadoghq.com
- **Confluent Support:** support@confluent.io
- **Google Cloud Support:** Via Console Chat
- **ElevenLabs Support:** support@elevenlabs.io

### 15.3 Keyboard Shortcuts (Dev Mode)
- `Ctrl+1` - Trigger Steady State
- `Ctrl+2` - Trigger Latency Spike
- `Ctrl+3` - Trigger Cascading Failure
- `Ctrl+M` - Toggle Mute
- `Ctrl+D` - Toggle Debug Overlay
- `Ctrl+Q` - Toggle Quality (Low/High)

***

**END OF DOCUMENT**

***

This is your **SINGLE SOURCE OF TRUTH**. Bookmark this file. Reference it daily. Update it as you build.

**Next Steps:**
1. Save this as `DESIGN.md` in your project root
2. Start with Phase 1, Day 1
3. Check off items as you complete them
4. Share checkpoints with me for review

**Ready to start building?** 🚀