from typing import Dict, List, TypeVar, Type
from pydantic import BaseModel, PrivateAttr

from .event import EventBase


AggregateType = TypeVar('AggregateType')


class AggregateBase(BaseModel):
    _pending_events: List = PrivateAttr(default_factory=list)

    def _append_event(self, event: EventBase):
        self._pending_events.append(event)

    def get_pending_events(self) -> List[EventBase]:
        return self._pending_events

    def serialize(self) -> Dict:
        return self.dict(by_alias=True)

    @classmethod
    def deserialize(cls: Type[AggregateType], data: Dict) -> AggregateType:
        return cls(**data)
