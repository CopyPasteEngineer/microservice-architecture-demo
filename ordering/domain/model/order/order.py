from typing import Dict, List, Tuple, TYPE_CHECKING
from pydantic import Field, PrivateAttr

from domain.base.aggregate import AggregateBase
from .event import (
    OrderItemRepresentation, OrderCreatedEvent, OrderItemAmountUpdatedEvent, OrderSubmittedEvent,
)
from .exception import OrderSubmittedException, InvalidOrderItemAmountException


_ERR_MSG_EDIT_AFTER_SUBMIT = 'Submitted Order cannot be edited'
_ERR_MSG_DOUBLE_SUBMIT = 'Submitted Order cannot be submitted again'
_ERR_MSG_ITEM_AMOUNT_NOT_INTEGER = 'Order Item amount must be an integer'
_ERR_MSG_ITEM_AMOUNT_LESS_THAN_ZERO = 'Order Item amount cannot be less than 0'


class Order(AggregateBase):
    id_: str = Field(..., alias='id')
    items: Dict[str, int]
    customer_id: str = Field(..., alias='customerId')
    submitted: bool = False
    _version: int = PrivateAttr(default=0)

    @classmethod
    def create_new_order_with_items(cls, *, id: str, items: List[Tuple[str, int]], customer_id: str) -> 'Order':
        items_dict: Dict[str, int] = {product_id: amount for product_id, amount in items}
        order = cls(id=id, items=items_dict, customerId=customer_id)

        event = OrderCreatedEvent(id=id, items=order._get_items_represent(), customer_id=customer_id)
        order._append_event(event)
        return order

    def update_item_amount(self, product_id: str, amount: int):
        if self.submitted:
            raise OrderSubmittedException(_ERR_MSG_EDIT_AFTER_SUBMIT)

        if int(amount) != amount:
            raise InvalidOrderItemAmountException(_ERR_MSG_ITEM_AMOUNT_NOT_INTEGER)

        if amount < 0:
            raise InvalidOrderItemAmountException(_ERR_MSG_ITEM_AMOUNT_LESS_THAN_ZERO)

        if amount == 0:
            if product_id in self.items:
                del self.items[product_id]
        else:
            self.items[product_id] = amount

        event = OrderItemAmountUpdatedEvent(order_id=self.id_, product_id=product_id, amount=amount)
        self._append_event(event)

    def submit(self):
        if self.submitted:
            raise OrderSubmittedException(_ERR_MSG_DOUBLE_SUBMIT)

        self.submitted = True

        event = OrderSubmittedEvent(id=self.id_, items=self._get_items_represent(), customer_id=self.customer_id)
        self._append_event(event)

    def _get_items_represent(self) -> List[OrderItemRepresentation]:
        return [OrderItemRepresentation(product_id=pid, amount=amount)
                for pid, amount in sorted(self.items.items())]

    if TYPE_CHECKING:
        def __init__(self, *, id: str, items: Dict[str, int], customerId: str, submitted: bool = False):
            super().__init__()
