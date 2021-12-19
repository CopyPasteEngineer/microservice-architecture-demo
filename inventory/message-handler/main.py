from typing import Dict
import asyncio

from domain import usecase

import dependency


async def handle_order_submitted(event: Dict):
    source_id = event['id_']
    customer_id = event['customer_id']
    items = [(item['product_id'], item['amount']) for item in event['items']]

    await usecase.receive_requested_order(source_id=source_id, customer_id=customer_id, items=items)


event_handlers = {
    'Ordering.OrderSubmittedEvent': handle_order_submitted,
}
topics = list(event_handlers.keys())


def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    dependency.inject(loop)

    consumer = dependency.get_kafka_consumer(consumer_group='inventory-service')
    consumer.subscribe(topics)

    print('READY')
    while True:
        msg_pack = consumer.poll(timeout_ms=500, max_records=1)

        for tp, messages in msg_pack.items():
            for message in messages:
                print(message.value)
                loop.run_until_complete(event_handlers[tp.topic](message.value))

        consumer.commit()


if __name__ == '__main__':
    main()
