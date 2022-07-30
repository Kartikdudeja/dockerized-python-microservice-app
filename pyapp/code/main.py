from fastapi import FastAPI, Depends

from fastapi_utils.tasks import repeat_every

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from datetime import datetime

from routers import login, data
from database import models
from database.database import engine, SQLALCHEMY_DATABASE_URL, get_db
from utils.producer import initializeQueue, Publisher

import os
from dotenv import load_dotenv

load_dotenv()

WAIT_FOR_QUEUE_SECONDS = int(os.getenv('WAIT_FOR_QUEUE_SECONDS'))
SCHEDULER_INTERVAL_SECONDS = int(os.getenv('SCHEDULER_INTERVAL_SECONDS'))

# fastapi instance
app = FastAPI()

# logging instance
import logging
logger = logging.getLogger(__name__)

# logging configuration
# logging.basicConfig(level=logging.INFO, filename='app.log', format="%(asctime)s: %(levelname)s: [%(process)d:%(processName)s] (%(filename)s-%(module)s.%(funcName)s): %(message)s")
logging.basicConfig(level=logging.INFO, filename='app.log', format="%(asctime)s: %(levelname)s: [%(filename)s-%(module)s.%(funcName)s]: %(message)s")

# ORM Engine to create DB Tables using models.py file
models.Base.metadata.create_all(bind=engine)

# Endpoint Request Router
app.include_router(login.router)
app.include_router(data.router)

def get_connection():
    return create_engine(
        url=SQLALCHEMY_DATABASE_URL
    )

# check database connection on application startup
@app.on_event("startup")
async def startup_event(db: Session = Depends(get_db)):
    
    TIMESTAMP = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # logger.info('Declaring Messaging Queue.')
    # initializeQueue()

    try:
        engine = get_connection()
        with open("setup.log", mode="a") as log:
            log.write(f"{TIMESTAMP}: Successfully Connected to the RDMS, Starting the Application.\n")
        logger.info('Successfully Connected to the RDMS, Starting the Application.')
    except Exception as ex:
        with open("setup.log", mode="a") as log:
           log.write(f"{TIMESTAMP}: Database Connection Failed, shutting down the application.\nReason: {ex}\n")
        logger.exception(f'Database Connection Failed, shutting down the application.\nReason: {ex}\n')
        exit()

# default endpoint
@app.get ("/")
async def root():
    logger.info('Request Received for default Path')
    return {"message": "Application is Running."}

@app.on_event("startup")
@repeat_every(seconds=SCHEDULER_INTERVAL_SECONDS, wait_first= True)
def Scheduler():
    logger.info('calling queue scheduler')
    output = Publisher()
    logger.info(f"Data Retreived via scheduler: {output}")

@app.on_event("startup")
@repeat_every(seconds=WAIT_FOR_QUEUE_SECONDS, wait_first= True, max_repetitions=1)
def StartMQ():
    logger.info('Starting Message Queue')
    initializeQueue()