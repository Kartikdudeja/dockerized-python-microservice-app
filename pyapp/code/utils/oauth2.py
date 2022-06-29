from jose import jwt
from datetime import datetime, timedelta


import logging
logger = logging.getLogger(__name__)

SECRET_KEY = "21de31bb6d8d924056a0089f6f49680b0e9e14ee906c8a0444b0a155d74821b8"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTE=5

def createAccessToken(data: dict):
    logger.info(f"createAccessToken function is called for user id : {data['id']} & username: {data['email']}")

    encodeData = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTE)
    # encodeData.update({"expiresIn": expire})
    encodeData.update({"exp": expire})

    encodedJWT = jwt.encode(encodeData, SECRET_KEY, algorithm=ALGORITHM)

    logger.info(f"token successfully generated for user id : {data['id']} & username: {data['email']}; token: {encodedJWT}")
    return encodedJWT