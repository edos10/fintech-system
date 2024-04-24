from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from fastapi import FastAPI, Response, Request
from fastapi import Depends, HTTPException
from fastapi.responses import JSONResponse
from common.base import get_session, get_producer
from common.kafka import send_producer_kafka
from common.config import NEW_AGREEMENT_TOPIC
from db.dao import *
from service.agreement import AgreementRepository
from service.product import ProductRepository
from models.model_orm import *
from sqlalchemy.ext.asyncio import AsyncSession
import os
import uvicorn


app = FastAPI()


@app.get("/product")
async def get_all_products(session: AsyncSession = Depends(get_session)):
    """
        Give all products

        Parameters:
        - None

        Returns:
        - Products: all products in bank.
    """

    repo = ProductRepository(session)
    products = await repo.get_all()
    return products


@app.get("/product/{product_code}")
async def get_product(response: Response, product_code: str, session: AsyncSession = Depends(get_session)):
    """
        Give the particular product on id

        Parameters:
        - product_code: id of product, string

        Returns:
        - product: the product with id = product_code.
    """

    repo = ProductRepository(session)
    product = await repo.get_by_id(product_code)
    return product


@app.post("/product")
async def add_product(response: Response, product: ProductCreate, session: AsyncSession = Depends(get_session)):
    """
    Create a new product.

    Parameters:
        - product_data: ProductCreate - create Product to DB

    Returns:
        - status code: 200 - successfully created, 400 - wrong input data, 409 - product already exists
    """
    repo = ProductRepository(session)
    res = await repo.create(product)
    if not res:
        raise HTTPException(status_code=409, detail="Product with this code already exists")
    return Response(status_code=200)


@app.delete("/product/{product_code}")
async def delete_product_endpoint(product_code: str, session: AsyncSession = Depends(get_session)):
    """
        Delete a particular product.

        Parameters:
        - product_code: to be deleted.

        Returns:
        - Code status: 204.
    """
    repo = ProductRepository(session)
    try:
        await repo.delete_by_id(product_code)
    except ValueError as e:
        raise HTTPException(status_code=204, detail=str(e))
    return Response(status_code=204)


@app.post("/agreement")
async def add_agreement(request: CreditRequest, session: AsyncSession = Depends(get_session),
                        producer=Depends(get_producer)):
    """
    Create a new agreement.

    Parameters:
    - agreement_data: AgreementCreate.

    Returns:
    - Agreement: The created agreement.
    """
    repo = AgreementRepository(session)
    try:
        agr_id, client_id, amount = await repo.create(request)
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
    output = {"agreement_id": agr_id}

    data_for_kafka = {
        "agreement_id": agr_id,
        "client_id": client_id, 
        "disbursment_amount": amount,
    }

    await send_producer_kafka(producer, data_for_kafka, NEW_AGREEMENT_TOPIC)

    return JSONResponse(status_code=201, content=output)

@app.post("/get_all_agreements")
async def add_agreement(request: Request, client_id: int, session: AsyncSession = Depends(get_session)):
    """
    pass
    """
    input_data = await request.body()
    repo = AgreementRepository(session)
    id_client = await repo.return_id_client(input_data)
    values = await repo.get_all_on_client_id(id_client)

    return JSONResponse(status_code=201, content=values)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT_PE")))