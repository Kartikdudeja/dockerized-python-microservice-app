# All details related to database connection
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import redis
import logging
logger = logging.getLogger(__name__)

import os
from dotenv import load_dotenv

load_dotenv()

TEST_DATABASE_HOSTNAME = os.getenv('TEST_DATABASE_HOSTNAME')
DOCKER_DATABASE_HOSTNAME = os.getenv('DOCKER_DATABASE_HOSTNAME')
DATABASE_PORT = os.getenv('DATABASE_PORT')
DATABASE_NAME = os.getenv('DATABASE_NAME')
DATABASE_USERNAME = os.getenv('DATABASE_USERNAME')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')

TEST_REDIS_HOSTNAME = os.getenv('TEST_REDIS_HOSTNAME')
DOCKER_REDIS_HOSTNAME = os.getenv('DOCKER_REDIS_HOSTNAME')
REDIS_DATABASE = os.getenv('REDIS_DATABASE')
REDIS_PORT = os.getenv('REDIS_PORT')

# SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@<ip-address/hostname>/<database-name>"

# local database connection string
SQLALCHEMY_DATABASE_URL = f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{TEST_DATABASE_HOSTNAME}/{DATABASE_NAME}"
redisClient = redis.Redis(host=f"{TEST_REDIS_HOSTNAME}", port=f"{REDIS_PORT}", db=f"{REDIS_DATABASE}")

# docker database
# SQLALCHEMY_DATABASE_URL = f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DOCKER_DATABASE_HOSTNAME}/{DATABASE_NAME}"
# redisClient = redis.Redis(host=f"{DOCKER_REDIS_HOSTNAME}", port=f"{REDIS_PORT}", db=f"{REDIS_DATABASE}")

# database engine to create db tables
engine = create_engine(SQLALCHEMY_DATABASE_URL)

#session for db call
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# create a session for every db call
def get_db():
    db = SessionLocal()
    try:   
        yield db
    finally:
        db.close()

# Redis Connection
# redis_client = redis.Redis(host=environment_variable.REDIS_HOSTNAME, port=environment_variable.REDIS_PORT, db=environment_variable.REDIS_DATABASE)

# Retry mechanism for connecting with Redis DB
# To-Do: Try to implement a Exponential Back-Off Algorithm
# while True:

#     try:

#         redis_client = redis.Redis(host=environment_variable.REDIS_HOSTNAME, port=environment_variable.REDIS_PORT, db=environment_variable.REDIS_DATABASE)
#         logger.info("Successfully Connected to Redis")
#         break

#     except:
#         logger.error("Failed to connect to Redis. Retrying in 3 seconds...")
#         time.sleep(3)
#         continue


# database connected logic

# @app.on_event("startup")
# async def startup():
#     if not database.is_connected:
#         await database.connect()
#     # create a dummy entry
#     await User.objects.get_or_create(email="test@test.com")


# @app.on_event("shutdown")
# async def shutdown():
#     if database.is_connected:
#         await database.disconnect()
