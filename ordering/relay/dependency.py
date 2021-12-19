from infrastructure.mongo import MongoDBConfig, create_mongo_db
from infrastructure.kafka import KafkaConfig, create_kafka_producer


def get_mongo_db(loop=None):
    mongo_db = create_mongo_db(MongoDBConfig(), loop=loop)
    return mongo_db


def get_kafka_producer():
    producer = create_kafka_producer(KafkaConfig())
    return producer
