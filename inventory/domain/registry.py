from typing import Optional
from domain.base.singleton import Singleton


class Registry(metaclass=Singleton):
    def __init__(self):
        from domain.model.requested_order.repository import AllRequestedOrders

        self.all_requested_orders: Optional[AllRequestedOrders] = None
