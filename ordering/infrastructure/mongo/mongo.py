import motor.motor_asyncio

from .config import MongoDBConfig


def create_mongo_db(config: MongoDBConfig, loop=None):
    uri = f'mongodb://{config.MONGO_USERNAME}:{config.MONGO_PASSWORD}@{config.MONGO_SERVER}:{config.MONGO_PORT}'
    if loop:
        client = motor.motor_asyncio.AsyncIOMotorClient(uri, io_loop=loop)
    else:
        client = motor.motor_asyncio.AsyncIOMotorClient(uri)
    db = client.OrderingService
    return db
