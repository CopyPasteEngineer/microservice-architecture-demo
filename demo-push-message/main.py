import json
from kafka import KafkaProducer


def get_kafka_producer() -> KafkaProducer:
    producer = KafkaProducer(bootstrap_servers=['kafka:9092'],
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    return producer


def main():
    producer = get_kafka_producer()
    topic = 'Ordering.OrderSubmittedEvent'
    data = {
        "id_": "OR-619be7adda6893a6c84c5809",
        "items": [
            {
                "product_id": "string",
                "amount": 7777
            }
        ],
        "customer_id": "string",
        "_event_type": "OrderSubmittedEvent",
        "version": 2
    }
    producer.send(topic, data)


if __name__ == '__main__':
    main()
