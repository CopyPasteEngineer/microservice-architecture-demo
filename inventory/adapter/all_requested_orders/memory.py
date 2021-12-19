from typing import List, Dict
from bson.objectid import ObjectId

from domain.port import AllRequestedOrders

from domain.model.requested_order import RequestedOrder
from domain.model.requested_order.repository.exception import (
    OrderNotFoundException, InvalidOrderIdException, DuplicateKeyError
)


class AllRequestedOrdersInMemory(AllRequestedOrders):
    def __init__(self, data: Dict[str, RequestedOrder] = None):
        self.data: Dict[str, RequestedOrder] = data or {}

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
        return [order for order in self.data.values() if order.is_pending()]

    async def from_id(self, id_: str) -> RequestedOrder:
        order = self.data.get(id_, None)
        if order is None:
            raise OrderNotFoundException(f'Order id {id_} not found')
        return order

    async def save(self, entity: RequestedOrder):
        self.data[entity.id_] = entity

    async def add(self, entity: RequestedOrder):
        if entity.id_ in self.data:
            raise DuplicateKeyError(f'Order with ID {str(entity.id_)} already exists')
        self.data[entity.id_] = entity
