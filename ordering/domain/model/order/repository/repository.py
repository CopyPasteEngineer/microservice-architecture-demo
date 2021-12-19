from abc import abstractmethod

from domain.base.repository import RepositoryAbstract

from ..order import Order


class AllOrders(RepositoryAbstract[str, Order]):
    @abstractmethod
    async def next_identity(self) -> str:
        pass

    @abstractmethod
    async def from_id(self, id_: str) -> Order:
        pass

    @abstractmethod
    async def save(self, entity: Order):
        pass
