from abc import abstractmethod
from typing import List

from domain.base.repository import RepositoryAbstract

from ..requested_order import RequestedOrder


class AllRequestedOrders(RepositoryAbstract[str, RequestedOrder]):
    @abstractmethod
    async def next_identity(self) -> str:
        pass

    @abstractmethod
    async def identity_from_order_id(self, source_id: str) -> str:
        pass

    @abstractmethod
    async def are_pending(self) -> List[RequestedOrder]:
        pass

    @abstractmethod
    async def from_id(self, id_: str) -> RequestedOrder:
        pass

    @abstractmethod
    async def save(self, entity: RequestedOrder):
        pass

    @abstractmethod
    async def add(self, entity: RequestedOrder):
        pass
