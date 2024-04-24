import aiohttp
import json
from fastapi.responses import JSONResponse


async def get_data(url: str) -> JSONResponse:
    """
    This function sends a GET request to another service with address = url and 
    returns a response in the form of a json

    Parameters:
    - url: str - input address of service
    Returns:
    - JSONREsponse object - status code, headers, json response
    """

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            res = await response.json()
            return JSONResponse(res, status_code=response.status)


async def post_data(url: str, data: dict) -> JSONResponse:
    """
    This function sends a POST request to another service with address = url and data type of dict and 
    returns a response in the form of a json

    Parameters:
    - url: str - input address of service
    Returns:
    - JSONREsponse object - status code, headers, json response
    """

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=json.dumps(data), 
                                headers={"Content-Type": "application/json"}) as response:
            res = await response.json()
            return JSONResponse(res, status_code=response.status)
