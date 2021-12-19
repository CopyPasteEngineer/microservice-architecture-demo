from typing import TYPE_CHECKING, List, Tuple
from pydantic import BaseModel, Field
from domain.base.repository import transaction
from .registry import Registry
from domain.model.order.order import Order


class OrderItem(BaseModel):
    product_id: str = Field(..., alias='productId')
    amount: int


class OrderState(BaseModel):
    id_: str = Field(..., alias='id')
    items: List[OrderItem]
    customer_id: str = Field(..., alias='customerId')
    submitted: bool

    @classmethod
    def from_order(cls, order: Order) -> 'OrderState':
        items = [OrderItem(productId=product_id, amount=amount) for product_id, amount in order.items.items()]
        return cls(id=order.id_, items=items, customerId=order.customer_id, submitted=order.submitted)


class OrderItemUpdate(BaseModel):
    order_id: str = Field(..., alias='orderId')
    product_id: str = Field(..., alias='productId')
    amount: int


@transaction
async def get_order(order_id: str) -> OrderState:
    repo = Registry().all_orders
    order: Order = await repo.from_id(order_id)
    return OrderState.from_order(order)


@transaction
async def create_new_order(customer_id: str, items: List[Tuple[str, int]]) -> str:
    repo = Registry().all_orders
    id_: str = await repo.next_identity()
    order = Order.create_new_order_with_items(id=id_, items=items, customer_id=customer_id)
    await repo.save(order)
    return id_


@transaction
async def update_order_item_amount(order_id: str, product_id: str, amount: int) -> OrderItemUpdate:
    repo = Registry().all_orders
    order: Order = await repo.from_id(order_id)
    order.update_item_amount(product_id=product_id, amount=amount)
    await repo.save(order)
    return OrderItemUpdate(orderId=order.id_, productId=product_id, amount=order.items.get(product_id, 0))


@transaction
async def submit_order(order_id: str):
    repo = Registry().all_orders
    order: Order = await repo.from_id(order_id)
    order.submit()
    await repo.save(order)


if TYPE_CHECKING:
    async def get_order(order_id: str) -> OrderState: ...

    async def create_new_order(customer_id: str, items: List[str, int]) -> str: ...

    async def update_order_item_amount(order_id: str, product_id: str, amount: int) -> OrderItemUpdate: ...

    async def submit_order(order_id: str): ...
