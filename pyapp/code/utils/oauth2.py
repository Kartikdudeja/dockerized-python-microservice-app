from jose import jwt
from datetime import datetime, timedelta

from fastapi.exceptions import HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from starlette.status import HTTP_401_UNAUTHORIZED
from sqlalchemy.orm import Session

from routers.schemas import TokenData
from database.database import get_db
from database import models

import logging
logger = logging.getLogger(__name__)

SECRET_KEY = "21de31bb6d8d924056a0089f6f49680b0e9e14ee906c8a0444b0a155d74821b8"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTE=30

# login credential should be in form data not raw json
oauthSchema = OAuth2PasswordBearer(tokenUrl='/apigw/login')

def createAccessToken(data: dict):
    logger.info(f"createAccessToken function is called for user id : {data['id']} & username: {data['email']}")

    encodeData = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTE)
    # encodeData.update({"expiresIn": expire})
    encodeData.update({"exp": expire})

    encodedJWT = jwt.encode(encodeData, SECRET_KEY, algorithm=ALGORITHM)

    logger.info(f"token successfully generated for user id : {data['id']} & username: {data['email']}; token: {encodedJWT}")
    return encodedJWT

def verifyAccessToken(token: str, credentialException):

    try:
    
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    
        id: int = payload.get("id")
        email: str = payload.get("email")

        logger.info(f"verifying access token for the user id: {id} & username: {email}")
        
        if id == "" or email == "":
            logger.info(f"Invalid Token; user id: {id} & username: {email}")
            raise credentialException

        tokenData = TokenData(id=id, email=email)

    except:
        logger.error("JWT Exception")
        raise credentialException

    logger.info(f"valid access token; user id: {id} & username: {email}")
    return tokenData

def getCurrentUser(token: str = Depends(oauthSchema), db: Session = Depends(get_db)):
    
    credentialException = HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Could not validate Credentials", headers={"WWW-Authenticate": "Bearer"})

    logger.info(f"fetching user details for token: {token}")

    token = verifyAccessToken(token, credentialException)

    userQuery = db.query(models.Users).filter(models.Users.id == token.id)
    user = userQuery.first()

    return user