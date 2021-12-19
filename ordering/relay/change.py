from typing import Optional, Dict, AsyncIterator
from pymongo.database import Collection
from pymongo.change_stream import CollectionChangeStream


class MongoChangeWatcher:
    def __init__(self, db: Collection):
        self.collection: Collection = db
        self.current_stream: Optional[CollectionChangeStream] = None

    @property
    def resume_token(self) -> str:
        return self.current_stream.resume_token

    async def iter_changes(self, latest_token=None) -> AsyncIterator[Dict]:
        async with self.collection.watch(resume_after=latest_token) as stream:  # change stream
            self.current_stream = stream
            async for change in self.current_stream:
                yield change
