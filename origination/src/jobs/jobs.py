from db.base import *
from db.dao import *
from sqlalchemy import select, update
from models.model_orm import *
import json
import os
import httpx
from common.kafka import send_producer_kafka
from common.base import get_producer
from common.config import NEW_AGREEMENT_TOPIC, SCORING_REQUEST


async def applications_to_scoring():
    async with async_session() as session:
        res = await session.execute(select(Applications).where(Applications.status == "new"))
        data_for_send = res.scalars().all()
        if not data_for_send:
            print("Non new applications for new -> scoring")
            return
        
        for i in range(len(data_for_send)):
            data_for_send[i] = data_for_send[i].__dict__
            data_for_send[i].pop('_sa_instance_state')
        
        """
        res = httpx.post(os.getenv("SCORING_SEND"), json=json.dumps(data_for_send))
        if res.status_code != 200:
            print("Unsuccess attempt for sending data to scoring")
            return
        """
        producer = await get_producer()
        try:
            await send_producer_kafka(producer, data_for_send, SCORING_REQUEST)

            for appl in data_for_send:
                await session.execute(update(Applications).where(Applications.id == appl['id']).values({'status': 'scoring'}))
            await session.commit()
        except Exception as e:
            print("------------------------------------")
            print(f"ERROR ERROR: {str(e)}")
            print("unsuccessful sending to kafka and updating in job, try to restart kafka for correct job work")
            print("------------------------------------")


async def accepted_applications_to_pe():
    async with async_session() as session:
        res = await session.execute(select(Applications).where(Applications.status == "accepted"))
        data_for_send = res.scalars().all()
        if not data_for_send:
            print("Non new accepted applications for origination -> pe")
            return
        
        for i in range(len(data_for_send)):
            data_for_send[i] = data_for_send[i].__dict__
            data_for_send[i].pop('_sa_instance_state')

        for appl in data_for_send:
            appl['product_code'] = appl['product_name']
            res = httpx.post(os.getenv("URL_SEND_APPLICATION"), json=json.dumps(appl))
            if res.status_code != 201:
                print(f"Unsuccess attempt for creating agreeement with id = {appl['id']} in product engine")