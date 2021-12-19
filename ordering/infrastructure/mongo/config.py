from pydantic import BaseSettings


class MongoDBConfig(BaseSettings):
    MONGO_SERVER: str = 'ordering-mongodb'
    MONGO_PORT: str = '27017'
    MONGO_USERNAME: str = 'root'
    MONGO_PASSWORD: str = 'admin'
