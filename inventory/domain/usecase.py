from typing import TYPE_CHECKING, List, Tuple
from pydantic import BaseModel, Field
from domain.base.repository import transaction
from .registry import Registry
from domain.model.requested_order.requested_order import RequestedOrder
from domain.model.requested_order.repository.exception import DuplicateKeyError


class OrderItem(BaseModel):
    product_id: str = Field(..., alias='productId')
    amount: int


class OrderState(BaseModel):
    id_: str = Field(..., alias='id')
    items: List[OrderItem]
    customer_id: str = Field(..., alias='customerId')
    status: str = 'pending'

    @classmethod
    def from_order(cls, order: RequestedOrder) -> 'OrderState':
        items = [OrderItem(productId=product_id, amount=amount) for product_id, amount in order.requested_items]
        return cls(id=order.id_, items=items, customerId=order.customer_id, status=order.status)


@transaction
async def get_pending_orders() -> List[OrderState]:
    all_requested_orders = Registry().all_requested_orders
    pending_orders = await all_requested_orders.are_pending()
    return [OrderState.from_order(pending_order) for pending_order in pending_orders]


@transaction
async def receive_requested_order(source_id: str, customer_id: str, items: List[Tuple[str, int]]) -> str:
    all_requested_orders = Registry().all_requested_orders

    id_: str = await all_requested_orders.identity_from_order_id(source_id)

    requested_order = RequestedOrder(id=id_, sourceId=source_id, requestedItems=items, customerId=customer_id)
    try:
        await all_requested_orders.add(requested_order)
    except DuplicateKeyError:  # duplicate message, do nothing
        print('key duplicated; just ignore')

    return id_


if TYPE_CHECKING:
    async def get_pending_orders() -> List[OrderState]: ...

    async def receive_requested_order(source_id: str, customer_id: str, items: List[Tuple[str, int]]) -> str: ...
