from typing import List, TYPE_CHECKING
from pydantic import BaseModel, Field

from domain.base.event import EventBase


class OrderItemRepresentation(BaseModel):
    product_id: str
    amount: int

    if TYPE_CHECKING:
        def __init__(self, *, product_id: str, amount: int):
            super().__init__()


class OrderCreatedEvent(EventBase):
    id_: str = Field(..., alias='id')
    items: List[OrderItemRepresentation]
    customer_id: str

    if TYPE_CHECKING:
        def __init__(self, *, id: str, items: List[OrderItemRepresentation], customer_id: str):
            super().__init__()


class OrderItemAmountUpdatedEvent(EventBase):
    order_id: str
    product_id: str
    amount: int

    if TYPE_CHECKING:
        def __init__(self, *, order_id: str, product_id: str, amount: int):
            super().__init__()


class OrderSubmittedEvent(EventBase):
    id_: str = Field(..., alias='id')
    items: List[OrderItemRepresentation]
    customer_id: str

    if TYPE_CHECKING:
        def __init__(self, *, id: str, items: List[OrderItemRepresentation], customer_id: str):
            super().__init__()
