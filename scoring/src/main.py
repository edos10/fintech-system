from fastapi import FastAPI
from fastapi import Request
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from jobs.jobs import send_accepted_to_origination
from kafka_read import print_msg, processing_requests_from_origination
import uvicorn
import os
import asyncio 
from common.kafka import receive_consumer_message
from common.config import SCORING_REQUEST

app = FastAPI()
scheduler = AsyncIOScheduler()


@app.post("/check_application")
async def check_application(request: Request):
    input_data = await request.body()
    print(input_data)
    return 200


@app.on_event('startup')
async def init_data():
    scheduler.add_job(send_accepted_to_origination, 'interval', 
                      seconds=int(os.getenv("SECONDS_FOR_JOB_TO_ORIGINATION")))
    scheduler.start()
    asyncio.create_task(receive_consumer_message(processing_requests_from_origination, SCORING_REQUEST))
    print("COMPLETE")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT_SCORING")))
