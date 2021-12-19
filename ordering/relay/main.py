from typing import Dict, List
import asyncio
from pymongo.database import Database
from kafka import KafkaProducer

from change import MongoChangeWatcher
from memory import MongoRelayMemory
import dependency


def extract_events(change: Dict) -> List[Dict]:
    operation_type = change.get('operationType', '')
    if operation_type == 'update':
        fields: Dict = change['updateDescription']['updatedFields']
        pairs = [(key, event) for key, event in fields.items() if key.startswith('events.')]
        return [event for _, event in pairs]

    elif operation_type == 'insert':
        return change['fullDocument']['events']

    return []


async def relay(watcher: MongoChangeWatcher, memory: MongoRelayMemory, producer: KafkaProducer):
    latest_token = await memory.get_latest_token()
    print('READY')
    async for change in watcher.iter_changes(latest_token=latest_token):
        events = extract_events(change)
        for event in events:
            print(event)
            try:
                event_type = event['_event_type']
            except KeyError as e:
                raise e  # or do something

            producer.send(f'Ordering.{event_type}', event)

        resume_token = watcher.resume_token
        await memory.save_token(resume_token)


def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    db: Database = dependency.get_mongo_db(loop)
    producer = dependency.get_kafka_producer()

    watcher = MongoChangeWatcher(db['order'])
    memory = MongoRelayMemory(db['relayProgress'])

    loop.run_until_complete(relay(watcher, memory, producer))


if __name__ == '__main__':
    main()
