from passlib.context import CryptContext

import logging
logger = logging.getLogger(__name__)

passwordContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

# hash user's password
def hashPassword(password):
    logger.info("hashing function called")
    return passwordContext.hash(password)

# validates hash for user login
def verifyPassword(plainPassword, hashedPassword):
    logger.info("verify hash function called")
    return passwordContext.verify(plainPassword, hashedPassword)
