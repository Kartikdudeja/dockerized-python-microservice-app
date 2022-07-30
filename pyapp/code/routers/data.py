from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from starlette.responses import Response
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_202_ACCEPTED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT, HTTP_422_UNPROCESSABLE_ENTITY

from datetime import timedelta
from typing import List, Optional

import logging
logger = logging.getLogger(__name__)

from routers.schemas import Data, DataResponse, UpdateData, DataAll
from database.database import get_db, redisClient
from database import models
from utils.oauth2 import getCurrentUser
from utils.producer import producer

import os
from dotenv import load_dotenv

load_dotenv()

REDIS_KEY_EXPIRE_MINUTE = int(os.getenv('REDIS_KEY_EXPIRE_MINUTE'))

LIMIT=10
OFFSET=0

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
        newData = models.Data(**body.dict(), owner_id=loggedIn.id)

        db.add(newData)
        db.commit()
        db.refresh(newData)

    except IntegrityError:
        # rollback in case of exception
        db.rollback()
        logger.error(f"key : '{body.key}' already exist")

        raise HTTPException(status_code=HTTP_409_CONFLICT, detail=f"key : '{body.key}' already exist")

    logger.info(f"new data added; key: {body.key}, value: {body.value}")
    logger.info(f"putting value in redis cache; key: '{newData.key}' & value: '{newData.value}'")
    redisClient.set(newData.key, newData.value, timedelta(minutes=REDIS_KEY_EXPIRE_MINUTE))

    # Publish Message to the Queue.
    # MESSAGE=f'{{"key": "{body.key}", "value": "{body.value}"}}'
    # logger.info(f"Calling Producer Function to Publish Message to the Queue: {MESSAGE}")
    # producer(MESSAGE)

    
    resData = {"status": "Success", "message": "key-value pair added"}

    return resData

@router.get ("/{key}", status_code=HTTP_200_OK, response_model= Data)
async def readData (key: str, db: Session = Depends(get_db), loggedIn: str = Depends(getCurrentUser)):
    
    logger.info(f"Get Data Request; querying database for key: '{key}' from user id: '{loggedIn.id}'")


    cacheData = redisClient.get(key)
    
    if not cacheData:
        logger.info(f"cache miss for key: '{key}'; Querying RDBMS")

        dataQuery = db.query(models.Data).filter(models.Data.owner_id == loggedIn.id).filter(models.Data.key == key)
        data = dataQuery.first()
        
        if not data:
            logger.info(f"No Result found for the key: '{key}'")
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f"No Result found for the key: '{key}'")
        
        logger.info(f"result found for key: '{key}'")
        resData = {"key": data.key, "value": data.value}

        logger.info(f"putting value in redis cache; key: '{data.key}' & value: '{data.value}'")
        redisClient.set(data.key, data.value, timedelta(minutes=REDIS_KEY_EXPIRE_MINUTE))

        return resData

    else:
        logger.info(f"cache hit for the key: '{key}'")
        resData = {"key": key, "value": cacheData}
        return resData

@router.get ("/", status_code=HTTP_200_OK, response_model=List[DataAll])
# @router.get ("/", status_code=HTTP_200_OK)
def readAllData(search: Optional[str] = "", limit: int = LIMIT, offset: int = OFFSET, db: Session = Depends(get_db), loggedIn: str = Depends(getCurrentUser)):
    
    logger.info(f'Get All Account Details Request from User ID: {loggedIn.id}')

    if limit > LIMIT:
        logger.error(f'Limit Error: Parameter Value ({limit}) is greater than defined Threshold')
        raise HTTPException(status_code=HTTP_422_UNPROCESSABLE_ENTITY, detail="You cannot request more than 10 items")

    allDataQuery = db.query(models.Data).filter(models.Data.owner_id == loggedIn.id).filter(models.Data.key.contains(search)).limit(limit).offset(offset)
    allData = allDataQuery.all()

    if allData is None:
        logger.error(f"No Result found for used id: {loggedIn.id}")
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f"No Result found")

    return allData

@router.put ("/{key}", status_code=HTTP_202_ACCEPTED, response_model= DataResponse)
async def updateData (key: str, value: UpdateData, db: Session = Depends(get_db), loggedIn: str = Depends(getCurrentUser)):
    
    logger.info(f"Update Data Request; querying database for key: '{key}' from user id: '{loggedIn.id}'")

    updateQuery = db.query(models.Data).filter(models.Data.owner_id == loggedIn.id).filter(models.Data.key == key)
    update = updateQuery.first()

    if not update:
        logger.error(f"No Result found for the key: '{key}'")
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f"No Result found for the key: '{key}'")
    
    logger.info(f"result found for key: '{key}'")

    if update.owner_id != loggedIn.id:

        logger.error(f'User ID: {loggedIn.id} is not authorized to perform requested action')
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not Authorized to perform requested action")

    updateQuery.update(value.dict(), synchronize_session=False)
    db.commit()

    logger.info(f"data updated; key: {key}, value: {update.value}")
    
    resData = {"status": "Success", "message": f"value for the key: '{key}' Updated"}

    return resData

@router.delete ("/{key}", status_code=HTTP_204_NO_CONTENT)
async def deleteData (key: str, db: Session = Depends(get_db), loggedIn: str = Depends(getCurrentUser)):

    logger.info(f"delete Data Request; querying database for key: '{key}' from user id: '{loggedIn.id}'")

    deleteQuery = db.query(models.Data).filter(models.Data.owner_id == loggedIn.id).filter(models.Data.key == key)
    delete = deleteQuery.first()

    if not delete:
        logger.error(f"No Result found for the key: '{key}'")
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f"No Result found for the key: '{key}'")
    
    logger.info(f"result found for key: '{key}'")

    if delete.owner_id != loggedIn.id:

        logger.error(f'User ID: {loggedIn.id} is not authorized to perform requested action')
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not Authorized to perform requested action")

    deleteQuery.delete(synchronize_session=False)
    db.commit()

    logger.info(f"data deleted; key: '{key}'")
    
    return Response(status_code=HTTP_204_NO_CONTENT)