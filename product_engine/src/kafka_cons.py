from common.config import NEW_AGREEMENT_TOPIC
import json
import httpx


def print_msg(msg: bytes):
    print(msg)


async def read_messages_from_scoring(msg):
    msg = json.loads(msg.value.decode('utf-8'))
    print("MSG IN PE", msg)
    if msg["response"] is True:
        print("ACCEPT")