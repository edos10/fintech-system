import json
from config.config import ALL_AGREEMENTS_PE_URL, SCORING_RESPONSE
import httpx
from common.kafka import send_producer_kafka
from common.config import KAFKA_INSTANCE
from aiokafka import AIOKafkaProducer


async def print_msg(msg):
    print(f"\n\nNEW MESSAGE IN SCORING:\n\n\n{msg}\n\n\n")


async def processing_requests_from_origination(msg):
    print(f"NEW IN SCORING: {msg.value, type(msg.value)}")
    msg = json.loads(msg.value.decode('utf-8'))
    try:
        response = await httpx.post(ALL_AGREEMENTS_PE_URL, json=msg)
        msg["response"] = False
        if response.status_code == httpx.codes.OK:
            msg["response"] = True
        producer = AIOKafkaProducer(bootstrap_servers=KAFKA_INSTANCE)
        await send_producer_kafka(producer, msg, SCORING_RESPONSE)

    except Exception as e:
        print("ERROR IN API PE", str(e))