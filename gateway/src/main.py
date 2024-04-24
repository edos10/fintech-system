from fastapi import FastAPI, Request
import fetch
import os
from config import *
import uvicorn

app = FastAPI()


@app.get("/product")
async def get_all_products_pe():
    """
    redirects the request to the Product_engine service via the /product endpoint
    
    Returns: response from product_engine/product
    """

    products = await fetch.get_data(f'http://{PE_HOST}:{PE_PORT}/product')
    return products


@app.get("/product/{product_code}")
async def get_product_pe(product_code: str):
    """
    redirects the request to the Product_engine service via the /product/{product_code} endpoint

    Arguments:
    - product_code - system product code 

    Returns: 
    - response from product_engine/product/{product_code}
    """

    product = await fetch.get_data(f'http://{PE_HOST}:{PE_PORT}/product/{product_code}')
    return product


@app.post("/agreement")
async def post_agreement_pe(request: Request):
    """
    redirects the request to the Product_engine service via the /agreement endpoint

    Arguments:
    - json of data 

    Returns: 
    - response from product_engine/agreement
    """

    data_input = await request.json()
    res_post = await fetch.post_data(f'http://{PE_HOST}:{PE_PORT}/agreement', data_input)
    return res_post


@app.post("/application")
async def post_application_orig(request: Request):
    """
    redirects the request to the Origination service via the /application endpoint

    Arguments:
    - json of data

    Returns: 
    - response from origination/application
    """

    data_input = await request.json()
    products = await fetch.post_data(f'http://{ORIG_HOST}:{ORIG_PORT}/application', data_input)
    return products


@app.post("/application/{application_id}/close")
async def application_close_orig(application_id: int):
    """
    redirects the request to the Origination service via the /application/{application_id}/close endpoint

    Arguments:
    - application_id: id required application for close

    Returns: 
    - response from origination/application/{application_id}/close
    """
    
    res_close = await fetch.post_data(f'http://{ORIG_HOST}:{ORIG_PORT}/application/{application_id}/close', dict())
    return res_close


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT_GATEWAY")))
