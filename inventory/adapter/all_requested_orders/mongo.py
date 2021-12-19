from typing import List
from bson.objectid import ObjectId
import bson.errors
from pymongo.database import Database

from domain.port import AllRequestedOrders

from domain.model.requested_order import RequestedOrder
from domain.model.requested_order.repository.exception import (
    OrderNotFoundException, InvalidOrderIdException, DuplicateKeyError, EntityOutdated
)


class AllRequestedOrdersInMongo(AllRequestedOrders):
    def __init__(self, mongo_db: Database, collection_name: str = 'order'):
        self.mongo_db = mongo_db
        self.collection_name = collection_name

    async def next_identity(self) -> str:
        return 'IN-'+str(ObjectId())

    async def identity_from_order_id(self, source_id: str) -> str:
        try:
            source_id_random = source_id.split('-', maxsplit=1)[1]
        except IndexError:
            raise InvalidOrderIdException('Invalid Order id')
        id_ = f'IN-{source_id_random}'
        return id_

    async def are_pending(self) -> List[RequestedOrder]:
        filter_ = {'state.status': 'pending'}
        projection = {'_id': False, 'events': False}

        raw_orders = self.mongo_db[self.collection_name].find(filter_, projection)
        pending_orders = [(RequestedOrder.deserialize(raw_order['state']), raw_order['version'])
                          async for raw_order in raw_orders]
        for pending_order, version in pending_orders:
            pending_order._version = version
        return [pending_order for pending_order, _ in pending_orders]

    async def from_id(self, id_: str) -> RequestedOrder:
        mongo_id = self._entity_id_to_mongo_id(id_)
        filter_ = {'_id': ObjectId(mongo_id)}
        projection = {'_id': False, 'events': False}

        raw = await self.mongo_db[self.collection_name].find_one(filter_, projection)
        if raw is None:
            raise OrderNotFoundException(f'Order id {id_} not found')
        order = RequestedOrder.deserialize(raw['state'])
        order._version = raw['version']
        return order

    async def save(self, entity: RequestedOrder):
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

    async def add(self, entity: RequestedOrder):
        data = entity.serialize()
        id_ = self._entity_id_to_mongo_id(entity.id_)

        current_version = entity._version
        pending_events = [dict(**event.serialize(), version=current_version+1+i)
                          for i, event in enumerate(entity.get_pending_events())]
        document = {
            '_id': id_,
            'state': data,
            'events': pending_events,
            'version': current_version + len(pending_events),
        }

        try:
            await self.mongo_db[self.collection_name].insert_one(document)
        except DuplicateKeyError as e:
            raise e

    @staticmethod
    def _entity_id_to_mongo_id(id_: str) -> ObjectId:
        try:
            return ObjectId(id_.split('-', maxsplit=1)[1])
        except (IndexError, bson.errors.InvalidId):
            raise InvalidOrderIdException('Invalid Order id')
