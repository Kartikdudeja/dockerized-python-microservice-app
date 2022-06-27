import logging

from fastapi import APIRouter

from .schemas import Data

logger = logging.getLogger(__name__)

router = APIRouter (
    prefix= "/apigw/data"
)

@router.post ("/", response_model= Data)
async def createData (body: Data):
    logger.info (f'create data request received for {body.recipient}, {body.message}')
    res_status = "success"
    res_id = 0
    return {"status": res_status, "id": res_id}

@router.get ("/")
async def readData ():
    res_status = "success"
    return {"status": res_status}

@router.get ("/{id}")
async def readDataById (id: int):
    res_status = "success"
    res_id = id
    return {"status": res_status, "id": res_id}

@router.put ("/{id}")
async def readDataById (id: int):
    res_status = "success"
    res_id = id
    return {"status": res_status, "id": res_id}

@router.delete ("/{id}")
async def readDataById (id: int):
    res_status = "success"
    res_id = id
    return {"status": res_status, "id": res_id}