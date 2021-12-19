from domain.registry import Registry
from adapter.all_orders.mongo import AllOrdersInMongo
from infrastructure.mongo import MongoDBConfig, create_mongo_db


def inject():
    mongo_db = create_mongo_db(MongoDBConfig())
    Registry().all_orders = AllOrdersInMongo(mongo_db)
