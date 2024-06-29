from fastapi import FastAPI, Response
from fastapi import Depends, HTTPException
from fastapi.responses import JSONResponse
from jobs.jobs import applications_to_scoring, accepted_applications_to_pe, ping_scoring
from db.base import get_session
from service.application import ApplicationRepository
from models.model_orm import *
from sqlalchemy.ext.asyncio import AsyncSession
import uvicorn
from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import os
from common.config import SCORING_RESPONSE, SCORING_REQUEST
from common.kafka import *
from common.base import get_session
import asyncio
from common.base import get_producer
from common.kafka import send_producer_kafka
from kafka_cons import read_messages_from_scoring


@asynccontextmanager
async def lifespan_wrapper(app):
    scheduler.add_job(applications_to_scoring, 'interval', seconds=45)
    scheduler.add_job(accepted_applications_to_pe, 'interval', seconds=40)
    scheduler.start()
    asyncio.create_task(receive_consumer_message_to_origination())
    asyncio.create_task(receive_consumer_message(read_messages_from_scoring, SCORING_RESPONSE, "origination"))
    yield

app = FastAPI(lifespan=lifespan_wrapper)
scheduler = AsyncIOScheduler()

@app.post("/application")
async def new_application(application: ApplicationCreate, session: AsyncSession = Depends(get_session), 
                          producer: AsyncSession = Depends(get_producer)):
    """
        Preprocessing and send new application to Scoring service

        Parameters:
        - application: Input application in JSON

        Returns:
        - Status code: 200 - successfully created, 409 - double application, it will close
    """
    repo = ApplicationRepository(session)
    try:
        id_new = await repo.create(application)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
    output = {"application_id": id_new}

    for_scoring = application.dict()
    for_scoring["application_id"] = id_new
    await send_producer_kafka(producer, for_scoring, SCORING_REQUEST)

    return JSONResponse(status_code=200, content=output)


@app.post("/application/{application_id}/close")
async def close_application_id(application_id: str, session: AsyncSession = Depends(get_session)):
    """
        Close application with definite id

        Parameters:
        - application_id: id of required application

        Returns:
        - Status code: 200 - successfully closed, 404 - such application doesn't exist
    """

    repo = ApplicationRepository(session)
    try:
        application_id = int(application_id)
        _ = await repo.update_status(application_id, "closed")
    except ValueError as _:
        raise HTTPException(status_code=404, detail="such application doesn't exist")

    return Response(status_code=200)


@app.post("/application/{application_id}/accept")
async def close_application_id(application_id: str, session: AsyncSession = Depends(get_session)):
    """
        Accept application with definite id

        Parameters:
        - application_id: id of required application

        Returns:
        - Status code: 200 - successfully accepted, 404 - such application doesn't exist
    """

    repo = ApplicationRepository(session)
    try:
        application_id = int(application_id)
        _ = await repo.update_status(application_id, "accepted")
    except ValueError as e:
        raise HTTPException(status_code=404, detail="such application doesn't exist")

    return Response(status_code=200)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT_ORIG")))
