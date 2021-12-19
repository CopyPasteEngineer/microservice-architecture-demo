from typing import List
from pydantic import BaseModel, Field

from domain.usecase import OrderState


class OrderItem(BaseModel):
    product_id: str = Field(..., alias='productId')
    amount: int


class OrderDetail(BaseModel):
    id_: str = Field(..., alias='id')
    items: List[OrderItem]
    customer_id: str = Field(..., alias='customerId')
    status: str = 'pending'

    @classmethod
    def from_order(cls, order: OrderState) -> 'OrderDetail':
        items = [OrderItem(productId=t.product_id, amount=t.amount) for t in order.items]
        return OrderDetail(id=order.id_, items=items, customerId=order.customer_id,
                           status=order.status)
