import json
from kafka import KafkaProducer

from .config import KafkaConfig


def create_kafka_producer(config: KafkaConfig) -> KafkaProducer:
    producer = KafkaProducer(bootstrap_servers=[f'{config.KAFKA_SERVER}:{config.KAFKA_PORT}'],
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    return producer
