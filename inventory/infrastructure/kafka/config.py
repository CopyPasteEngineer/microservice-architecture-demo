from pydantic import BaseSettings


class KafkaConfig(BaseSettings):
    KAFKA_SERVER: str = 'kafka'
    KAFKA_PORT: str = '9092'
