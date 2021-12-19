from typing import List, Tuple, TYPE_CHECKING
from pydantic import Field, PrivateAttr

from domain.base.aggregate import AggregateBase


_ERR_MSG_EDIT_AFTER_SUBMIT = 'Submitted Order cannot be edited'
_ERR_MSG_DOUBLE_SUBMIT = 'Submitted Order cannot be submitted again'
_ERR_MSG_ITEM_AMOUNT_NOT_INTEGER = 'Order Item amount must be an integer'
_ERR_MSG_ITEM_AMOUNT_LESS_THAN_ZERO = 'Order Item amount cannot be less than 0'


class RequestedOrder(AggregateBase):
    id_: str = Field(..., alias='id')
    source_id: str = Field(..., alias='sourceId')
    requested_items: List[Tuple[str, int]] = Field(..., alias='requestedItems')
    customer_id: str = Field(..., alias='customerId')
    status: str = 'pending'
    _version: int = PrivateAttr(default=0)

    def is_pending(self) -> bool:
        return self.status == 'pending'

    if TYPE_CHECKING:
        def __init__(self, *, id: str, sourceId: str, requestedItems: List[Tuple[str, int]], customerId: str,
                     status: str = 'pending'):
            super().__init__()
