from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import asyncio
import json
from .config import KAFKA_INSTANCE


async def print_msg(msg):
    print(f"New msg from topic:\n\n{msg}\n")


async def receive_consumer_message(wrap_func, topic: str):
    consumer = AIOKafkaConsumer(
        topic,
        client_id='all',
        bootstrap_servers=KAFKA_INSTANCE,
        enable_auto_commit=False,
    )

    await consumer.start()
    print("CONSUMER START")
    try:
        async for msg in consumer:
            print(f"NEW MSG IN TOPIC {topic}: {msg.value}")
            await wrap_func(msg)
    except Exception as e:
        print(f"error in consumer: {str(e)}")
    finally:
        await consumer.stop()

async def send_producer_kafka(producer: AIOKafkaProducer, data_for_kafka: dict, topic: str) -> None:
    await producer.start()
    try:
        await asyncio.wait_for(producer.send(topic, json.dumps(data_for_kafka).encode("ascii")), timeout=3)
    finally:
        await producer.stop()
