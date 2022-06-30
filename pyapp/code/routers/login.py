from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN , HTTP_409_CONFLICT

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from routers.schemas import Login, LoginResponse, SignUp, SignUpResponse
from database.database import get_db
from database import models
from utils.hash import hashPassword, verifyPassword
from utils.oauth2 import createAccessToken, ACCESS_TOKEN_EXPIRE_MINUTE

import logging
logger = logging.getLogger(__name__)

router = APIRouter (
    prefix= "/apigw/login"
)

@router.post ("/", response_model= LoginResponse)
async def login (body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    logger.info(f'login request received for username: {body.username}')
    
    # check if user exit or not
    userQuery = db.query(models.Users).filter(models.Users.email == body.username)
    user = userQuery.first()

    if not user:
        logger.error(f'no user found: {body.username}')
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail= "Invalid Credentails")

    if not verifyPassword(body.password, user.password):
        logger.error("password verification failed")
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail= "Invalid Credentails")

    accessToken = createAccessToken(data = {"id": user.id, "email": user.email})

    tokenData = {"accessToken": accessToken, "tokenType": "bearer", "expiresIn": ACCESS_TOKEN_EXPIRE_MINUTE * 60}

    return {"status": "success", "username": body.username, "token": tokenData}

@router.post ("/signup", status_code= HTTP_201_CREATED, response_model= SignUpResponse)
async def signup(body: SignUp, db: Session = Depends(get_db)):
    logger.info(f'signup request received for username: {body.email}')

    # check for blank parameter is request body (email will be checked by pydantic as well because of EmailStr)    
    if body.email == "" or body.password == "":
        logger.info('Invalid signup request: username or password is blank')
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Invalid Request")

    # hash the password before storing in database
    hashedPassword = hashPassword(body.password)
    body.password = hashedPassword

    newUser = models.Users(**body.dict())

    try:
        # add new user in db and commit the new value
        db.add(newUser)
        db.commit()
        db.refresh(newUser)
        logger.info(f'new user created with Email id: {body.email}')

    # if user already exit; duplication entry
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