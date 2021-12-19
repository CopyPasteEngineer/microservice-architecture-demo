import json
from kafka import KafkaConsumer

from .config import KafkaConfig


def create_kafka_consumer(consumer_group: str, config: KafkaConfig) -> KafkaConsumer:
    producer = KafkaConsumer(bootstrap_servers=[f'{config.KAFKA_SERVER}:{config.KAFKA_PORT}'],
                             value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                             group_id=consumer_group)
    return producer
