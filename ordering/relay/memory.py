from pymongo.database import Collection


class MongoRelayMemory:
    def __init__(self, collection: Collection):
        self.collection: Collection = collection

    async def get_latest_token(self):
        memory = await self.collection.find_one({'name': 'main'})
        if not memory:
            return None
        return memory['latest_token']

    async def save_token(self, token):
        filter_ = {'name': 'main'}
        update = {'$set': {'latest_token': token}}
        await self.collection.update_one(filter_, update, upsert=True)
