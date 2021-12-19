from typing import Optional
from domain.base.singleton import Singleton


class Registry(metaclass=Singleton):
    def __init__(self):
        from domain.model.order.repository import AllOrders

        self.all_orders: Optional[AllOrders] = None
