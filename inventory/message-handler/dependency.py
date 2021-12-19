from domain.registry import Registry
from adapter.all_requested_orders.mongo import AllRequestedOrdersInMongo
from infrastructure.mongo import MongoDBConfig, create_mongo_db
from infrastructure.kafka import KafkaConfig, create_kafka_consumer


def inject(loop):
    mongo_db = create_mongo_db(MongoDBConfig(), loop=loop)
    Registry().all_requested_orders = AllRequestedOrdersInMongo(mongo_db)


def get_kafka_consumer(consumer_group: str):
    consumer = create_kafka_consumer(consumer_group, KafkaConfig())
    return consumer
