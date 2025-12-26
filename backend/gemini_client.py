"""
NEXUS PROTOCOL - Gemini AI Client (Vertex AI)
Generates sci-fi root cause analysis for incidents
"""
import asyncio
import logging
from typing import Optional
from config import settings

logger = logging.getLogger(__name__)

# System prompt for Gemini
SYSTEM_PROMPT = """You are NEXUS, a Starfleet-class observability AI. 
You analyze system failures and provide concise, technical explanations 
using sci-fi terminology. Keep responses under 20 words.

Examples:
- "Subspace interference in neural pathways causing token overflow"
- "Quantum decoherence detected in authentication matrix"
- "Cascading resonance failure across data substrates"
- "Temporal anomaly disrupting payment transaction streams"
- "Warp field instability in database connection pool"
"""

USER_PROMPT_TEMPLATE = """
Service: {service_id}
Status: {status}
Latency: {latency_ms}ms
Error Rate: {error_rate:.1%}
Recent Errors: {error_messages}

Provide a brief, sci-fi explanation of the root cause.
"""

# Pre-generated fallback responses for when API is unavailable
FALLBACK_RESPONSES = {
    "gateway": [
        "Subspace routing fluctuations detected in primary conduit",
        "Gateway harmonics destabilizing under load pressure",
        "Entry point experiencing quantum entanglement delays"
    ],
    "auth": [
        "Authentication matrix experiencing temporal drift",
        "Security handshake protocol in subspace interference",
        "Identity verification circuits overloaded"
    ],
    "payment": [
        "Transaction buffer overflow in payment substrate",
        "Financial data streams encountering wormhole turbulence",
        "Credit processing nodes experiencing phase variance"
    ],
    "ai-brain": [
        "Neural pathway congestion in cognitive subsystem",
        "Token overflow in synthetic thought processors",
        "Inference engine experiencing quantum decoherence"
    ],
    "database": [
        "Data crystal lattice showing stress fractures",
        "Storage matrix approaching critical entropy",
        "Query pathways blocked by subspace interference"
    ]
}


class GeminiClient:
    """Handles Gemini AI integration for incident analysis"""
    
    def __init__(self):
        self.enabled = bool(settings.google_project_id)
        self.model_name = "gemini-2.0-flash-exp"
        self.client = None
        
        if self.enabled:
            try:
                from google.cloud import aiplatform
                from vertexai.generative_models import GenerativeModel
                
                aiplatform.init(
                    project=settings.google_project_id,
                    location=settings.google_location
                )
                
                self.client = GenerativeModel(self.model_name)
                logger.info(f"Gemini client initialized with model: {self.model_name}")
            except Exception as e:
                logger.error(f"Failed to initialize Gemini client: {e}")
                self.enabled = False
        else:
            logger.warning("Google Project ID not set - using fallback responses")
    
    async def analyze_incident(
        self,
        service_id: str,
        status: str,
        latency_ms: int,
        error_rate: float,
        error_messages: list = None
    ) -> str:
        """Generate sci-fi analysis for an incident"""
        
        if not self.enabled or not self.client:
            return self._get_fallback_response(service_id)
        
        try:
            # Build the prompt
            prompt = USER_PROMPT_TEMPLATE.format(
                service_id=service_id,
                status=status,
                latency_ms=latency_ms,
                error_rate=error_rate,
                error_messages=", ".join(error_messages or ["Connection timeout"])
            )
            
            # Call Gemini API (run in executor to not block)
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.client.generate_content(
                    [SYSTEM_PROMPT, prompt],
                    generation_config={
                        "max_output_tokens": 50,
                        "temperature": 0.7
                    }
                )
            )
            
            analysis = response.text.strip()
            logger.info(f"Gemini analysis for {service_id}: {analysis}")
            
            return analysis
            
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            return self._get_fallback_response(service_id)
    
    def _get_fallback_response(self, service_id: str) -> str:
        """Get a pre-generated fallback response"""
        import random
        
        responses = FALLBACK_RESPONSES.get(
            service_id,
            ["System anomaly detected in unknown subsystem"]
        )
        
        return random.choice(responses)


# Global Gemini client instance
gemini_client = GeminiClient()
