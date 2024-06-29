from fastapi import FastAPI
from fastapi import Request
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from jobs.jobs import send_accepted_to_origination
from kafka_read import processing_requests_from_origination
import uvicorn
import os
import asyncio
from contextlib import asynccontextmanager
from common.kafka import receive_consumer_message
from common.config import SCORING_REQUEST
from kafka_read import print_msg


@asynccontextmanager
async def lifespan_wrapper(app):
    scheduler.add_job(send_accepted_to_origination, 'interval',
                      seconds=int(os.getenv("SECONDS_FOR_JOB_TO_ORIGINATION")))
    asyncio.create_task(receive_consumer_message(processing_requests_from_origination, SCORING_REQUEST, "orig"))
    scheduler.start()
    print("COMPLETE")
    yield

app = FastAPI(lifespan=lifespan_wrapper)
scheduler = AsyncIOScheduler()


@app.post("/check_application")
async def check_application(request: Request):
    input_data = await request.body()
    print(input_data)
    return 200


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT_SCORING")))
