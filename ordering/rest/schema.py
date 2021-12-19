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
    submitted: bool = False

    @classmethod
    def from_order(cls, order: OrderState) -> 'OrderDetail':
        items = [OrderItem(productId=t.product_id, amount=t.amount) for t in order.items]
        return OrderDetail(id=order.id_, items=items, customerId=order.customer_id,
                           submitted=order.submitted)


class CreateOrder(BaseModel):
    items: List[OrderItem]
    customer_id: str = Field(..., alias='customerId')


class UpdateOrderItem(BaseModel):
    amount: int


class CreationSuccess(BaseModel):
    id_: str = Field(..., alias='id')
    message: str


class OrderItemUpdateSuccess(BaseModel):
    order_id: str = Field(..., alias='orderId')
    product_id: str = Field(..., alias='productId')
    amount: int
    message: str


class OrderSubmissionSuccess(BaseModel):
    id_: str = Field(..., alias='id')
    message: str
