from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT

import logging
logger = logging.getLogger(__name__)

from routers.schemas import Data, DataResponse
from database.database import get_db
from database import models
from utils.oauth2 import getCurrentUser

router = APIRouter (
    prefix= "/apigw/data"
)

@router.post ("/", status_code=HTTP_201_CREATED, response_model= DataResponse)
async def createData (body: Data, db: Session = Depends(get_db), loggedIn: str = Depends(getCurrentUser)):

    if body.key == "" or body.value == "":
        logger.info('Invalid request: key or value is blank')
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Invalid Request")

    logger.info(f"create data request received from user: '{loggedIn.id}'; data: {body}")

    try:
        newData = models.Data(**body.dict(), ownerId=loggedIn.id)

        db.add(newData)
        db.commit()
        db.refresh(newData)

    except IntegrityError:
        # rollback in case of exception
        db.rollback()
        logger.error(f"key : '{body.key}' already exist")

        raise HTTPException(status_code=HTTP_409_CONFLICT, detail=f"key : '{body.key}' already exist")

    logger.info(f"new data added; key: {body.key}, value: {body.value}")
    
    resData = {"status": "Success", "message": "key-value pair added"}

    return resData

@router.get ("/")
async def readData ():
    pass

@router.get ("/{id}", response_model= Data)
async def readDataById (id: int):
    pass

@router.put ("/{id}")
async def updateDataById (id: int):
    pass

@router.delete ("/{id}")
async def deleteDataById (id: int):
    pass