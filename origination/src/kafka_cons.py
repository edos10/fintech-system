from common.config import NEW_AGREEMENT_TOPIC
import json
import httpx


def print_msg(msg: bytes):
    print(msg)


async def read_messages_from_scoring(msg):
    msg = json.loads(msg.value.decode('utf-8'))
    if msg["response"] is True:
        res = httpx.post(f"http://origination:5002/{msg['application_id']}/accept")
        if res.status_code != httpx.codes.OK:
            print(f"ERROR IN UPDATING STATUS OF THIS APPLICATION WITH ID = {msg['application_id']}")