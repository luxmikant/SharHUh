"""
NEXUS PROTOCOL - Configuration Management
Loads environment variables with Pydantic Settings
"""
from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Kafka / Confluent
    kafka_bootstrap_servers: str = "localhost:9092"
    kafka_sasl_username: str = ""
    kafka_sasl_password: str = ""
    kafka_topic: str = "nexus-telemetry"
    
    # Datadog
    dd_api_key: str = ""
    dd_app_key: str = ""
    dd_site: str = "datadoghq.com"
    dd_service: str = "nexus-backend"
    dd_env: str = "development"
    
    # Google Cloud / Vertex AI
    google_project_id: str = ""
    google_location: str = "us-central1"
    google_application_credentials: str = ""
    
    # ElevenLabs
    elevenlabs_api_key: str = ""
    elevenlabs_voice_id: str = "21m00Tcm4TlvDq8ikWAM"  # Rachel voice
    
    # Application
    port: int = 8000
    log_level: str = "INFO"
    cors_origins: str = "http://localhost:5173,http://localhost:3000"
    debug: bool = True
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from comma-separated string"""
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    @property
    def kafka_config(self) -> dict:
        """Get Kafka configuration dict"""
        config = {
            "bootstrap.servers": self.kafka_bootstrap_servers,
            "group.id": "nexus-backend",
            "auto.offset.reset": "latest"
        }
        
        # Add SASL auth if credentials provided
        if self.kafka_sasl_username and self.kafka_sasl_password:
            config.update({
                "security.protocol": "SASL_SSL",
                "sasl.mechanism": "PLAIN",
                "sasl.username": self.kafka_sasl_username,
                "sasl.password": self.kafka_sasl_password
            })
        
        return config
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()
