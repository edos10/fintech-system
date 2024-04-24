import json

async def print_msg(msg):
    print(f"\n\nNEW MESSAGE IN SCORING:\n\n\n{msg}\n\n\n")


async def processing_requests_from_origination(msg):
    print(f"NEW IN SCORING: {msg.value, type(msg.value)}")
    msg = json.loads(msg.value.decode('utf-8'))
    print(msg, "DICT")