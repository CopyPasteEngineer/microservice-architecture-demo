from domain.registry import Registry
from adapter.all_requested_orders.mongo import AllRequestedOrdersInMongo
from infrastructure.mongo import MongoDBConfig, create_mongo_db


def inject():
    mongo_db = create_mongo_db(MongoDBConfig())

    Registry().all_requested_orders = AllRequestedOrdersInMongo(mongo_db)
