from typing import Dict, TypeVar, Type
from pydantic import BaseModel


EventType = TypeVar('EventType')


class EventBase(BaseModel):
    def serialize(self) -> Dict:
        d = self.dict()
        d['_event_type'] = self.__class__.__name__
        return d

    @classmethod
    def deserialize(cls: Type[EventType], data: Dict) -> EventType:
        del data['_event_type']
        return cls(**data)
