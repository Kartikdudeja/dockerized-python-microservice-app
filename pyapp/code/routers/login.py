from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from routers.schemas import Login, LoginResponse, SignUp, SignUpResponse
from database.database import get_db
from database import models
from utils.hash import hashPassword

import logging
logger = logging.getLogger(__name__)

router = APIRouter (
    prefix= "/apigw/login"
)

@router.post ("/", response_model= LoginResponse)
async def login (body: Login):
    logger.info(f'login request received for username: {body.username}')
    res_status = "success"
    res_token = "somerandomstring"
    return {"status": res_status, "username": body.username, "token": res_token}

@router.post ("/signup", status_code= HTTP_201_CREATED, response_model= SignUpResponse)
async def signup(body: SignUp, db: Session = Depends(get_db)):
    logger.info(f'signup request received for username: {body.email}')
    
    if body.email == "" or body.password == "":
        logger.info('Invalid signup request: username or password is blank')
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Invalid Request")

    hashedPassword = hashPassword(body.password)
    body.password = hashedPassword

    newUser = models.Users(**body.dict())

    try:
        # add new user in db and commit the new value
        db.add(newUser)
        db.commit()
        db.refresh(newUser)
        logger.info(f'new user created with Email id: {body.email}')

    except IntegrityError:
        # rollback in case of exception
        db.rollback()
        logger.error(f'{body.email} already exist')
        
        raise HTTPException(status_code=HTTP_409_CONFLICT, detail=f"User: {body.email} already exist")

    return {
        "status": "Success",
        "username": newUser.email,
        "message": "user created successfully"
        }