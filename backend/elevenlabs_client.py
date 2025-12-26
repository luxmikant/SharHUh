"""
NEXUS PROTOCOL - ElevenLabs Voice Client
Generates voice alerts from text using ElevenLabs API
"""
import asyncio
import aiohttp
import os
import uuid
import logging
from typing import Optional
from pathlib import Path
from config import settings

logger = logging.getLogger(__name__)

# Pre-generated voice clips (fallback)
FALLBACK_CLIPS = {
    "welcome": "Welcome, Engineer. Colony status operational.",
    "alert_latency": "Warning: High latency detected in service matrix.",
    "alert_cascading": "Critical alert: Cascading failure suspected across systems.",
    "repair_success": "Repair successful. Metrics normalizing.",
    "system_healthy": "System integrity restored to optimal levels."
}


class ElevenLabsClient:
    """Handles ElevenLabs text-to-speech generation"""
    
    def __init__(self):
        self.api_key = settings.elevenlabs_api_key
        self.voice_id = settings.elevenlabs_voice_id
        self.enabled = bool(self.api_key)
        self.api_url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}"
        
        # Audio output directory
        self.audio_dir = Path("static/audio")
        self.audio_dir.mkdir(parents=True, exist_ok=True)
        
        if self.enabled:
            logger.info(f"ElevenLabs client initialized with voice: {self.voice_id}")
        else:
            logger.warning("ElevenLabs API key not set - using fallback clips")
    
    async def generate_voice_alert(self, text: str) -> Optional[str]:
        """
        Generate voice audio from text.
        Returns: URL path to the audio file, or None if failed
        """
        if not self.enabled:
            return self._get_fallback_clip(text)
        
        try:
            # Generate unique filename
            filename = f"alert_{uuid.uuid4().hex[:8]}.mp3"
            filepath = self.audio_dir / filename
            
            # Call ElevenLabs API
            headers = {
                "xi-api-key": self.api_key,
                "Content-Type": "application/json"
            }
            
            payload = {
                "text": text,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {
                    "stability": 0.75,
                    "similarity_boost": 0.75,
                    "style": 0.5,
                    "use_speaker_boost": True
                }
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.api_url,
                    headers=headers,
                    json=payload
                ) as response:
                    if response.status == 200:
                        audio_data = await response.read()
                        
                        # Save to file
                        with open(filepath, "wb") as f:
                            f.write(audio_data)
                        
                        logger.info(f"Generated voice alert: {filename}")
                        return f"/static/audio/{filename}"
                    else:
                        error = await response.text()
                        logger.error(f"ElevenLabs API error: {response.status} - {error}")
                        return self._get_fallback_clip(text)
            
        except Exception as e:
            logger.error(f"ElevenLabs generation error: {e}")
            return self._get_fallback_clip(text)
    
    def _get_fallback_clip(self, text: str) -> str:
        """Get appropriate fallback clip based on text content"""
        text_lower = text.lower()
        
        if "cascading" in text_lower or "critical" in text_lower:
            return "/static/audio/alert_cascading.mp3"
        elif "latency" in text_lower or "warning" in text_lower:
            return "/static/audio/alert_latency.mp3"
        elif "repair" in text_lower or "success" in text_lower or "fixed" in text_lower:
            return "/static/audio/repair_success.mp3"
        elif "healthy" in text_lower or "optimal" in text_lower:
            return "/static/audio/system_healthy.mp3"
        elif "welcome" in text_lower:
            return "/static/audio/welcome.mp3"
        else:
            return "/static/audio/alert_latency.mp3"  # Default
    
    async def generate_welcome_message(self) -> str:
        """Generate the welcome message audio"""
        return await self.generate_voice_alert(FALLBACK_CLIPS["welcome"])
    
    async def generate_alert_for_service(self, service_id: str, analysis: str) -> Optional[str]:
        """Generate alert audio for a specific service incident"""
        text = f"Alert: {service_id} service. {analysis}"
        return await self.generate_voice_alert(text)


# Global ElevenLabs client instance
elevenlabs_client = ElevenLabsClient()
