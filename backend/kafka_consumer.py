"""
NEXUS PROTOCOL - Kafka Consumer
Consumes telemetry events from Confluent Kafka
"""
import asyncio
import json
import logging
from typing import Callable, Optional
from confluent_kafka import Consumer, KafkaError, KafkaException
from config import settings
from models import TelemetryEvent

logger = logging.getLogger(__name__)


class KafkaConsumer:
    """Consumes events from Confluent Kafka"""
    
    def __init__(self):
        self.enabled = bool(settings.kafka_bootstrap_servers)
        self.consumer: Optional[Consumer] = None
        self.running = False
        self.topic = settings.kafka_topic
        
        if self.enabled and settings.kafka_sasl_username:
            try:
                self.consumer = Consumer(settings.kafka_config)
                logger.info(f"Kafka consumer initialized for topic: {self.topic}")
            except Exception as e:
                logger.error(f"Failed to initialize Kafka consumer: {e}")
                self.enabled = False
        else:
            logger.warning("Kafka not configured - running in simulation mode")
    
    async def start(self, callback: Callable[[TelemetryEvent], None]):
        """Start consuming messages"""
        if not self.enabled or not self.consumer:
            logger.info("Kafka disabled - skipping consumer start")
            return
        
        try:
            self.consumer.subscribe([self.topic])
            self.running = True
            logger.info(f"Subscribed to topic: {self.topic}")
            
            while self.running:
                # Poll for messages
                msg = self.consumer.poll(timeout=0.1)
                
                if msg is None:
                    await asyncio.sleep(0.01)
                    continue
                
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        logger.error(f"Kafka error: {msg.error()}")
                        continue
                
                try:
                    # Parse message
                    value = json.loads(msg.value().decode("utf-8"))
                    event = TelemetryEvent(**value)
                    
                    # Call callback
                    if asyncio.iscoroutinefunction(callback):
                        await callback(event)
                    else:
                        callback(event)
                        
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse Kafka message: {e}")
                except Exception as e:
                    logger.error(f"Error processing Kafka message: {e}")
                
                await asyncio.sleep(0)  # Yield control
                
        except Exception as e:
            logger.error(f"Kafka consumer error: {e}")
        finally:
            self.stop()
    
    def stop(self):
        """Stop consuming messages"""
        self.running = False
        if self.consumer:
            self.consumer.close()
            logger.info("Kafka consumer stopped")


class KafkaProducer:
    """Produces events to Confluent Kafka (for Chaos Engine)"""
    
    def __init__(self):
        self.enabled = bool(settings.kafka_bootstrap_servers)
        self.producer = None
        self.topic = settings.kafka_topic
        
        if self.enabled and settings.kafka_sasl_username:
            try:
                from confluent_kafka import Producer
                
                config = {
                    "bootstrap.servers": settings.kafka_bootstrap_servers,
                    "security.protocol": "SASL_SSL",
                    "sasl.mechanism": "PLAIN",
                    "sasl.username": settings.kafka_sasl_username,
                    "sasl.password": settings.kafka_sasl_password
                }
                
                self.producer = Producer(config)
                logger.info(f"Kafka producer initialized for topic: {self.topic}")
            except Exception as e:
                logger.error(f"Failed to initialize Kafka producer: {e}")
                self.enabled = False
    
    def send(self, event: TelemetryEvent):
        """Send event to Kafka"""
        if not self.enabled or not self.producer:
            return
        
        try:
            self.producer.produce(
                self.topic,
                key=event.service_id.encode("utf-8"),
                value=event.model_dump_json().encode("utf-8")
            )
            self.producer.poll(0)
        except Exception as e:
            logger.error(f"Failed to send to Kafka: {e}")
    
    def flush(self):
        """Flush pending messages"""
        if self.producer:
            self.producer.flush()


# Global instances
kafka_consumer = KafkaConsumer()
kafka_producer = KafkaProducer()
