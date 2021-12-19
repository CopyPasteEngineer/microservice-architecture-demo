from typing import Dict
from bson.objectid import ObjectId

from domain.port import AllOrders

from domain.model.order import Order
from domain.model.order.repository.exception import OrderNotFoundException


class AllOrdersInMemory(AllOrders):
    def __init__(self, data: Dict[str, Order] = None):
        self.data: Dict[str, Order] = data or {}

    async def next_identity(self) -> str:
        return 'OR-'+str(ObjectId())

    async def from_id(self, id_: str) -> Order:
        order = self.data.get(id_, None)
        if order is None:
            raise OrderNotFoundException(f'Order id {id_} not found')
        return order

    async def save(self, entity: Order):
        self.data[entity.id_] = entity
