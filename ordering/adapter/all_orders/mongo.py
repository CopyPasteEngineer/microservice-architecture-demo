from bson.objectid import ObjectId
import bson.errors
from pymongo.database import Database
from pymongo.errors import DuplicateKeyError

from domain.port import AllOrders

from domain.model.order import Order
from domain.model.order.repository.exception import (
    OrderNotFoundException, InvalidOrderIdException, EntityOutdated,
)


class AllOrdersInMongo(AllOrders):
    def __init__(self, mongo_db: Database, collection_name: str = 'order'):
        self.mongo_db = mongo_db
        self.collection_name = collection_name

    async def next_identity(self) -> str:
        return 'OR-'+str(ObjectId())

    @staticmethod
    def _entity_id_to_mongo_id(id_: str) -> ObjectId:
        try:
            return ObjectId(id_.split('-', maxsplit=1)[1])
        except (IndexError, bson.errors.InvalidId):
            raise InvalidOrderIdException('Invalid Order id')

    async def from_id(self, id_: str) -> Order:
        mongo_id = self._entity_id_to_mongo_id(id_)
        filter_ = {'_id': ObjectId(mongo_id)}
        projection = {'_id': False, 'events': False}

        raw = await self.mongo_db[self.collection_name].find_one(filter_, projection)
        if raw is None:
            raise OrderNotFoundException(f'Order id {id_} not found')
        order = Order.deserialize(raw['state'])
        order._version = raw['version']
        return order

    async def save(self, entity: Order):
        data = entity.serialize()
        id_ = self._entity_id_to_mongo_id(entity.id_)

        current_version = entity._version
        spec = {'_id': id_, 'version': current_version}
        pending_events = [dict(**event.serialize(), version=current_version+1+i)
                          for i, event in enumerate(entity.get_pending_events())]
        update = {
            '$set': {'state': data},
            '$push': {'events': {'$each': pending_events}},
            '$inc': {'version': len(pending_events)},
        }

        try:
            await self.mongo_db[self.collection_name].update_one(spec, update, upsert=True)
        except DuplicateKeyError:
            raise EntityOutdated()
